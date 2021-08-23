#!/usr/bin/env python

from cookiecutter import config
from cookiecutter.main import cookiecutter

from collections import OrderedDict
from distutils.version import StrictVersion, LooseVersion
import json
import os
import json
import tempfile
import shutil
import yaml
import ruamel.yaml
import typing
from typing import Any
import itertools
import copy

from itertools import product, starmap
from collections import namedtuple

import logging
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

tiamet_logger = logging.getLogger('tiamet')


TEMPLATE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE = os.path.join(TEMPLATE_DIR, 'templates')


def append_latest_tag(tags):
    tags_list = tags.split(',')
    tags_list = [x.strip(' ') for x in tags_list]
    tags_list.append('latest')
    return ','.join(tags_list)


def generate_base_image_products(config_data):
    BaseImage = namedtuple(
        'BaseImage', config_data['base_image_versions'].keys())

    data = config_data['base_image_versions']

    for key in config_data['base_image_versions'].keys():
        versions = config_data['base_image_versions'][key]
        versions.sort(key=LooseVersion, reverse=True)
        config_data['base_image_versions'][key] = versions

    return starmap(BaseImage, product(*data.values()))


def generate_image_products(pangeo_versions):
    Image = namedtuple(
        'Image', pangeo_versions.keys())

    for key in pangeo_versions.keys():
        versions = pangeo_versions[key]
        versions.sort(key=LooseVersion, reverse=True)
        pangeo_versions[key] = versions

    products = starmap(Image, product(*pangeo_versions.values()))
    return products


def generate_image_tag(image_product):
    tags = []

    t_image_product = copy.deepcopy(image_product)
    pangeo_version = t_image_product['pangeo']
    del t_image_product['pangeo']
    tags.append(f'pangeo-{pangeo_version}')

    for key in t_image_product.keys():
        value = t_image_product[key]
        tags.append(f'{key}-{value}')

    tags.pop()

    return '--'.join(tags)


def hardcode_cookiecutter_data(config_data, cookiecutter_data, pangeo_version, python_version):
    cookiecutter_data['python_version'] = python_version
    cookiecutter_data['pangeo_version'] = pangeo_version
    if pangeo_version == "2021.04.05":
        cookiecutter_data['jupyterlab_version'] = "3"
    elif pangeo_version == "2021.08.17":
        cookiecutter_data['jupyterlab_version'] = "3"
    
    return cookiecutter_data


def generate_package_image_cookiecutter_data(config_data, base_image, docker_tag, package_image, latest):
    json_payload = generate_base_image_cookiecutter_data(
        config_data=config_data, base_image=base_image, docker_tag=docker_tag, latest=latest)

    keys = list(package_image.keys())
    keys.sort()
    for key in keys:
        value = package_image[key]
        json_payload.update([f'{key}_version', value])
    return json_payload


def generate_package_image_cookiecutter(config_data, base_image, base_docker_tag, base_latest_tag, tmp_dirpath):
    t_pangeo_versions = config_data['pangeo_versions']

    for image in config_data['image_versions'].keys():

        pangeo_versions = copy.deepcopy(t_pangeo_versions)
        pangeo_versions[image] = config_data['image_versions'][image]

        image_products = generate_image_products(pangeo_versions)

        image_latest = None
        for image_product in image_products:

            image_product = image_product._asdict()
            image_tag = generate_image_tag(image_product)
            image_tag = f'{image}-{image_product[image]}--{image_tag}'
            image_tag = image_tag.replace('*', '')

            if not image_latest:
                image_latest = image_tag

            image_dir = image.replace('_', '-')
            notebook_dir = None

            if os.path.exists(os.path.join('templates', 'images', f'{image_dir}-{image_product[image]}-notebook')):

                notebook_dir = os.path.join(
                    'templates', 'images', f'{image_dir}-{image_product[image]}-notebook')

            elif os.path.exists(os.path.join('templates', 'images', f'{image_dir}-notebook')):
                notebook_dir = os.path.join(
                    'templates', 'images', f'{image_dir}-notebook')
            else:

                tiamet_logger.info('Noteboks dirs do not exist')
                tiamet_logger.info(notebook_dir)
                notebook_dir = os.path.join(
                    'templates', 'images', f'{image_dir}-notebook')
                tiamet_logger.info(notebook_dir)

                raise Exception(
                    f'Template directory not found for {notebook_dir}')

            dst_dir = os.path.join(tmp_dirpath, "{{cookiecutter.project_slug}}",
                                   image_dir, f'{image_dir}-{image_product[image]}-notebook--{base_docker_tag}--{image_tag}')

            # Up next is workflow managers
            #   "nextflow={{cookiecutter.nextflow_version}}",
            #   "snakemake={{cookiecutter.snakemake_version}}",
            #   "prefect={{cookiecutter.prefect_version}}",

            dst_dir = dst_dir.replace('*', '')
            notebook_dir = notebook_dir.replace('*', '')

            # os.makedirs(dst_dir)
            shutil.copytree(notebook_dir, dst_dir, dirs_exist_ok=False)

            cookiecutter_dst_dir = os.path.join(
                TEMPLATE_DIR)
            cookiecutter_data = read_json(os.path.join(
                TEMPLATE_DIR, 'templates', 'cookiecutter.json'))

            cookiecutter_data = hardcode_cookiecutter_data(config_data=config_data, cookiecutter_data=cookiecutter_data,
                                                           python_version=image_product['python'],
                                                           pangeo_version=image_product['pangeo'])

            docker_context_dir = os.path.join(
                'tiamet-docker-images', image_dir, f'{image_dir}-{image_product[image]}-notebook--{base_docker_tag}--{image_tag}')
            docker_context_dir = docker_context_dir.replace('*', '')
            build_name = f'{image_dir}-{image_product[image]}-notebook--{base_docker_tag}--{image_tag}'.replace(
                '*', '')

            cookiecutter_data['docker_tag'] = f'{base_docker_tag}--{image_tag}'
            cookiecutter_data['base_docker_tag'] = base_docker_tag
            cookiecutter_data['docker_context_dir'] = docker_context_dir
            cookiecutter_data['build_name'] = build_name

            write_json(file=os.path.join(
                tmp_dirpath, 'cookiecutter.json'), json_payload=cookiecutter_data)

            cookiecutter(
                tmp_dirpath,  # path/url to cookiecutter template
                overwrite_if_exists=True,
                extra_context=cookiecutter_data,
                output_dir=cookiecutter_dst_dir,
                no_input=True
            )

            shutil.rmtree(tmp_dirpath)

            # Github Actions Build.yml
            gh_workflow = read_yaml(os.path.join(
                TEMPLATE_DIR, 'templates', 'images', 'Build.yml'))
            gh_workflow['name'] = f'Build-{build_name}'
            gh_workflow['on']['push']['paths'][0] = docker_context_dir
            gh_workflow['jobs']['bio-image']['steps'][2]['with']['workdir'] = docker_context_dir
            gh_workflow['jobs'][
                'bio-image']['steps'][2]['with']['buildargs'] = f'DODO_TAG={base_docker_tag}'
            gh_workflow['env']['BASE_DOCKER_TAG'] = base_docker_tag
            gh_workflow['env']['BIO_DOCKER_TAG'] = f'{image_tag}--{base_docker_tag}'
            gh_workflow['env']['IMAGE'] = f'{image}-notebook'
            # if force rebuild
            del gh_workflow['on']['push']['paths']

            if image_latest == image_tag and base_latest_tag == base_docker_tag:
                tags = gh_workflow['jobs']['bio-image']['steps'][2]['with']['tags']
                tags = append_latest_tag(tags)
                gh_workflow['jobs']['bio-image']['steps'][2]['with']['tags'] = tags

            write_yaml(file=os.path.join('.github', 'workflows',
                       f'Build-{build_name}.yml'), yaml_payload=gh_workflow)


def generate_base_image_cookiecutter_data(config_data, base_image, docker_tag, latest):
    json_payload = OrderedDict(
        [
            ('project_slug', 'tiamet-docker-images'),
            ('docker_tag', docker_tag),
            # TODO This should not be hardcoded
            ('conda_version', base_image.conda),
            ('r_version', base_image.r),
            ('rstudio_version', base_image.rstudio),
            ('label', config_data['label_text']),
        ]
    )
    if latest == docker_tag:
        json_payload['latest'] = True
    else:
        json_payload['latest'] = False
    return json_payload


def generate_base_image_cookiecutter(config_data):
    tiamet_logger.info('')
    base_image_products = generate_base_image_products(config_data)
    t_base_image_products = []

    tmp_dirpath = tempfile.mkdtemp(prefix='tiamet_tmp')

    # cookiecutter dir
    # tmp_dirpath = os.path.join(TEMPLATE_DIR, 'tiamet-docker-images')
    # os.makedirs(tmp_dirpath, exist_ok=True)

    latest = None
    for base_image in base_image_products:
        t_base_image_products.append(base_image)
        docker_tag = f'r-{base_image.r}--rstudio-{base_image.rstudio}--conda-{base_image.conda}'
        if not latest:
            latest = docker_tag
        cookiecutter_data = generate_base_image_cookiecutter_data(config_data=config_data,
                                                                  docker_tag=docker_tag, base_image=base_image, latest=latest)

        cookiecutter_data['label_text'] = config_data['label_text']
        write_json(os.path.join('templates', 'base_image',
                   'cookiecutter.json'), cookiecutter_data)
        write_json(os.path.join('templates', 'base_image',
                   f'cookiecutter--base_image-{docker_tag}.json'), cookiecutter_data)

        cookiecutter_data['project_slug'] = f'base_image-{docker_tag}'

        tmp_base_dirpath = tempfile.mkdtemp(prefix='tiamet_base_tmp')

        cookiecutter_dst_dir = os.path.join(
            tmp_base_dirpath)

        docker_context_dir = os.path.join(
            'tiamet-docker-images', 'base_image', f'base_image-{docker_tag}')

        cookiecutter(
            # path/url to cookiecutter template
            os.path.join('templates', 'base_image'),
            overwrite_if_exists=True,
            extra_context=cookiecutter_data,
            output_dir=cookiecutter_dst_dir,
            no_input=True
        )

        shutil.copytree(os.path.join(cookiecutter_dst_dir, cookiecutter_data['project_slug']),
                        docker_context_dir, dirs_exist_ok=True
                        )
        shutil.rmtree(cookiecutter_dst_dir)
        # generate base_image gh build script
        gh_workflow = read_yaml(
            os.path.join("templates", "base_image", "Base-Image.yml"))

        if latest == docker_tag:
            tags = gh_workflow['jobs']['base-image']['steps'][2]['with']['tags']
            tags = append_latest_tag(tags)
            gh_workflow['jobs']['base-image']['steps'][2]['with']['tags'] = tags

        gh_workflow['name'] = f'Base-Image-{docker_tag}'
        gh_workflow['env']['DOCKER_TAG'] = docker_tag
        gh_workflow['env']['CONDA_VERSION'] = base_image.conda
        gh_workflow['env']['RSTUDIO_VERSION'] = base_image.rstudio
        gh_workflow['env']['R_VERSION'] = base_image.r
        gh_workflow['on']['push']['paths'][0] = docker_context_dir
        gh_workflow['jobs']['base-image']['steps'][2]['with']['workdir'] = docker_context_dir
        gh_workflow['jobs']['base-image']['steps'][2]['with'][
            'buildargs'] = f'CONDA_VERSION={base_image.conda},RSTUDIO_VERSION={base_image.rstudio},R_VERSION={base_image.r}'

        # # if force rebuild
        # del gh_workflow['on']['push']['paths']
        write_yaml(os.path.join('.github', 'workflows',
                   f'Base-Image-{docker_tag}.yml'), gh_workflow)

        generate_package_image_cookiecutter(
            config_data=config_data, base_image=base_image, base_docker_tag=docker_tag, base_latest_tag=latest, tmp_dirpath=tmp_dirpath)

    return t_base_image_products, latest


def write_yaml(file, yaml_payload):
    with open(file, 'w') as outfile:
        yaml.dump(yaml_payload, outfile,
                  sort_keys=False,
                  )


def write_json(file, json_payload):
    with open(file, 'w') as f:
        json.dump(json_payload, f, indent=4, default=str, sort_keys=False)


def read_json(file) -> Any:
    with open(file, 'r') as reader:
        data = json.load(reader)
    return data


def read_yaml(file) -> Any:
    with open(file, 'r') as stream:
        data = ruamel.yaml.safe_load(stream)
    return data


def read_config() -> Any:
    return read_yaml("config.yml")


# with open('templates/cookiecutter.json', 'r') as reader:
#     data = json.load(reader)

# for pangeo_version in data['pangeo_versions']:

#     data['pangeo_notebook_version'] = pangeo_version

#     if pangeo_version == "2021.04.05":
#         data['jupyterlab_version'] = "3"

#     cookiecutter(
#         TEMPLATE,  # path/url to cookiecutter template
#         overwrite_if_exists=True,
#         extra_context=data,
#         output_dir='.',
#         no_input=True
#     )
