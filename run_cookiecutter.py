#!/usr/bin/env python

from cookiecutter import config
from cookiecutter.main import cookiecutter
from slugify import slugify
import pandas as pd
import copy

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
from typing import Any, NewType
import itertools
import copy

from dataclasses import dataclass
from itertools import product, starmap
from collections import namedtuple
from pprint import pprint
import hiyapyco
from hiyapyco.odyldo import ODYD
import yaml.loader
import yaml.dumper
import yaml.representer
import jinja2

import six

import datetime
import types

import logging

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

tiamet_logger = logging.getLogger("tiamet")

TEMPLATE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATE = os.path.join(TEMPLATE_DIR, "templates")

MATRIX_COLUMNS = [
    "name",
    "rstudio_version",
    "pangeo_version",
    "python_version",
    "docker_tag",
    "base_docker_tag",
    "docker_buildargs",
    "docker_context_dir",
    "build_name",
]

README_COLUMNS =[
    "name",
    "version",
    "docker_image",
    "pangeo_version",
    "python_version",
    "snakemake_version",
    "nextflow_version",
    "prefect_version",
    "airflow_version",
]


class ODYD(yaml.SafeDumper):
    """Ordered Dict Yaml Dumper"""

    def __init__(self, *args, **kwargs):
        yaml.SafeDumper.__init__(self, *args, **kwargs)
        yaml.representer.SafeRepresenter.add_representer(str, type(self).repr_str)
        yaml.representer.SafeRepresenter.add_representer(
            OrderedDict, type(self)._odyrepr
        )

    def rstrip_multilines(self, data):
        out = []
        for line in data.splitlines():
            out.append(line.rstrip())

        return "\n".join(out)

    def _odyrepr(self, data):
        """see: yaml.representer.represent_mapping"""
        return self.represent_mapping("tag:yaml.org,2002:map", data.items())

    def repr_str(self, data):
        if "\n" in data:
            return self.represent_scalar(
                "tag:yaml.org,2002:str", self.rstrip_multilines(data), style="|"
            )
        elif len(data) > 80:
            return self.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        else:
            return self.represent_scalar("tag:yaml.org,2002:str", data, style=None)


def safe_dump(data, stream=None, **kwds):
    """implementation of safe dumper using Ordered Dict Yaml Dumper"""
    return yaml.dump(data, stream=stream, Dumper=ODYD, **kwds)


def append_latest_tag(tags):
    tags_list = tags.split(",")
    tags_list = [x.strip(" ") for x in tags_list]
    tags_list.append("latest")
    return ",".join(tags_list)


def generate_base_image_products(config_data):
    BaseImage = namedtuple("BaseImage", config_data["base_image_versions"].keys())

    data = config_data["base_image_versions"]

    # Make sure we're always sorting by versions
    for key in config_data["base_image_versions"].keys():
        versions = config_data["base_image_versions"][key]
        versions.sort(key=LooseVersion, reverse=True)
        config_data["base_image_versions"][key] = versions

    return starmap(BaseImage, product(*data.values()))


# TODO refactor this to build on other images
def generate_image_products(pangeo_versions):
    Image = namedtuple("Image", pangeo_versions.keys())

    for key in pangeo_versions.keys():
        versions = pangeo_versions[key]
        versions.sort(key=LooseVersion, reverse=True)
        pangeo_versions[key] = versions

    products = starmap(Image, product(*pangeo_versions.values()))
    return products


#TODO Docker tags can only be 128 characters
# Can't just throw everything in there
# will have to come up iwth a naming schema for tags
def generate_image_tag(image, image_product):
    tags = []

    t_image_product = copy.deepcopy(image_product)
    pangeo_version = t_image_product["pangeo"]
    del t_image_product["pangeo"]

    airflow_version = t_image_product['airflow']
    prefect_version = t_image_product['prefect']
    nextflow_version = t_image_product['nextflow']
    snakemake_version = t_image_product['snakemake']
    del t_image_product['airflow']
    del t_image_product['prefect']
    del t_image_product['nextflow']
    del t_image_product['snakemake']

    tags.append(f"pangeo-{pangeo_version}")

    for key in t_image_product.keys():
        value = t_image_product[key]
        tags.append(f"{key}-{value}")

    # tags.append(f'wms--a-{airflow_version}')
    # tags.append(f'p-{prefect_version}')
    # tags.append(f's-{snakemake_version}')
    # tags.append(f'n-{nextflow_version}')
    tags.pop()

    tags = "--".join(tags)
    assert len(tags) <= 128
    return tags


def hardcode_cookiecutter_data(
    config_data, cookiecutter_data, pangeo_version, python_version, snakemake_version, nextflow_version, prefect_version, airflow_version
):
    # For now only supporting jupyterlab versions >3
    cookiecutter_data["jupyterlab_version"] = "3"
    cookiecutter_data["python_version"] = python_version
    cookiecutter_data["pangeo_version"] = pangeo_version
    cookiecutter_data['snakemake_version'] = snakemake_version
    cookiecutter_data['nextflow_version'] = nextflow_version
    cookiecutter_data['prefect_version'] = prefect_version
    cookiecutter_data['airflow_version'] = airflow_version

    return cookiecutter_data


def generate_package_image_cookiecutter_data(
    config_data, base_image, docker_tag, package_image, latest
):
    json_payload = generate_base_image_cookiecutter_data(
        config_data=config_data,
        base_image=base_image,
        docker_tag=docker_tag,
        latest=latest,
    )

    keys = list(package_image.keys())
    keys.sort()
    for key in keys:
        value = package_image[key]
        json_payload.update([f"{key}_version", value])
    return json_payload


def generate_package_image_cookiecutter(
    config_data,
    base_image,
    base_docker_tag,
    base_latest_tag,
    tmp_dirpath,
    base_gh_workflow,
):
    tiamet_logger.info(f"Package Cookiecutter: {base_docker_tag}")
    t_pangeo_versions = config_data["pangeo_versions"]

    data = []

    for image in config_data["image_versions"].keys():

        tiamet_logger.info(f"Image: {image}")
        pangeo_versions = copy.deepcopy(t_pangeo_versions)
        pangeo_versions[image] = config_data["image_versions"][image]

        image_products = generate_image_products(pangeo_versions)

        image_latest = None
        for image_product in image_products:

            image_product = image_product._asdict()
            image_tag = generate_image_tag(image, image_product)
            image_tag = f"{image}-{image_product[image]}--{image_tag}"
            image_tag = image_tag.replace("*", "")

            if not image_latest:
                image_latest = image_tag

            image_dir = image.replace("_", "-")
            notebook_dir = None

            if os.path.exists(
                os.path.join(
                    "templates",
                    "images",
                    f"{image_dir}-{image_product[image]}-notebook",
                )
            ):

                notebook_dir = os.path.join(
                    "templates",
                    "images",
                    f"{image_dir}-{image_product[image]}-notebook",
                )

            elif os.path.exists(
                os.path.join("templates", "images", f"{image_dir}-notebook")
            ):
                notebook_dir = os.path.join(
                    "templates", "images", f"{image_dir}-notebook"
                )
            else:

                tiamet_logger.info("Noteboks dirs do not exist")
                tiamet_logger.info(notebook_dir)
                notebook_dir = os.path.join(
                    "templates", "images", f"{image_dir}-notebook"
                )
                tiamet_logger.info(notebook_dir)

                raise Exception(f"Template directory not found for {notebook_dir}")

            dst_dir = os.path.join(
                tmp_dirpath,
                "{{cookiecutter.project_slug}}",
                image_dir,
                f"{image_dir}-{image_product[image]}-notebook--{base_docker_tag}--{image_tag}",
            )

            dst_dir = dst_dir.replace("*", "")
            notebook_dir = notebook_dir.replace("*", "")

            # os.makedirs(dst_dir)
            shutil.copytree(notebook_dir, dst_dir, dirs_exist_ok=False)

            cookiecutter_dst_dir = os.path.join(TEMPLATE_DIR)
            cookiecutter_data = read_json(
                os.path.join(TEMPLATE_DIR, "templates", "cookiecutter.json")
            )

            cookiecutter_data = hardcode_cookiecutter_data(
                config_data=config_data,
                cookiecutter_data=cookiecutter_data,
                python_version=image_product["python"],
                pangeo_version=image_product["pangeo"],
                nextflow_version=image_product['nextflow'],
                snakemake_version=image_product['snakemake'],
                prefect_version=image_product['prefect'],
                airflow_version=image_product['airflow'],
            )

            docker_context_dir = os.path.join(
                "tiamet-docker-images",
                image_dir,
                f"{image_dir}-{image_product[image]}-notebook--{base_docker_tag}--{image_tag}",
            )
            docker_context_dir = docker_context_dir.replace("*", "")
            build_name = f"{image_dir}-{image_product[image]}-notebook--{base_docker_tag}--{image_tag}".replace(
                "*", ""
            )

            cookiecutter_data["name"] = image
            cookiecutter_data["version"] = image_product[image]
            cookiecutter_data["docker_tag"] = f"{base_docker_tag}--{image_tag}"
            cookiecutter_data["base_docker_tag"] = base_docker_tag
            cookiecutter_data["docker_context_dir"] = docker_context_dir
            cookiecutter_data["build_name"] = build_name
            cookiecutter_data["build_name_slug"] = slugify(build_name)
            cookiecutter_data["docker_buildargs"] = f"DODO_TAG={base_docker_tag}"
            cookiecutter_data['docker_image'] = f'dabbleofdevops/{image}:{image_tag}'

            write_json(
                file=os.path.join(tmp_dirpath, "cookiecutter.json"),
                json_payload=cookiecutter_data,
            )

            data.append(cookiecutter_data)

            cookiecutter(
                tmp_dirpath,  # path/url to cookiecutter template
                overwrite_if_exists=True,
                extra_context=cookiecutter_data,
                output_dir=cookiecutter_dst_dir,
                no_input=True,
            )

            shutil.rmtree(tmp_dirpath)

    # Add the build matrix to the gh_workflows
    df = pd.DataFrame.from_records(data)
    matrix = []
    for index, row in df[MATRIX_COLUMNS].iterrows():
        matrix.append(dict(row))

    base_gh_workflow["jobs"]["image"]["strategy"]["matrix"]["include"] = matrix
    write_yaml(
        file=f".github/workflows/base-{base_docker_tag}.yml",
        yaml_payload=base_gh_workflow,
    )

    return data


def generate_base_image_cookiecutter_data(config_data, base_image, docker_tag, latest):
    json_payload = OrderedDict(
        [
            ("project_slug", "tiamet-docker-images"),
            ("docker_tag", docker_tag),
            ("docker_tag_slug", slugify(docker_tag)),
            ("conda_version", base_image.conda),
            ("r_version", base_image.r),
            ("rstudio_version", base_image.rstudio),
            ("label_text", config_data["label_text"]),
        ]
    )
    if latest == docker_tag:
        json_payload["latest"] = True
    else:
        json_payload["latest"] = False
    return json_payload

def generate_readme(config_data, package_data_t):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))
    t = env.get_template("README.md.j2")

    package_data = copy.deepcopy(package_data_t)
    for p in package_data:
        df = p['images'][README_COLUMNS]
        p['images'] = {}
        names = df['name'].unique().tolist()
        for name in names:
            p['images'][name] = df[df['name']==name]
    rendered = t.render(package_data=package_data, config_data=config_data)
    f = open("README.md", "w")
    f.write(rendered)
    f.close()

def generate_base_image_cookiecutter(config_data):
    base_image_products = generate_base_image_products(config_data)
    t_base_image_products = []

    tmp_dirpath = tempfile.mkdtemp(prefix="tiamet_tmp")

    # cookiecutter dir
    # tmp_dirpath = os.path.join(TEMPLATE_DIR, 'tiamet-docker-images')
    # os.makedirs(tmp_dirpath, exist_ok=True)
    package_image_data_all = []

    latest = None
    for base_image in base_image_products:
        t_base_image_products.append(base_image)
        docker_tag = (
            f"r-{base_image.r}--rstudio-{base_image.rstudio}--conda-{base_image.conda}"
        )
        if not latest:
            latest = docker_tag

        cookiecutter_data = generate_base_image_cookiecutter_data(
            config_data=config_data,
            docker_tag=docker_tag,
            base_image=base_image,
            latest=latest,
        )

        cookiecutter_data["label_text"] = config_data["label_text"]
        cookiecutter_data["project"] = f"base_image-{docker_tag}"
        cookiecutter_data["project_slug"] = slugify(f"base_image-{docker_tag}")
        cookiecutter_data[
            "build_args"
        ] = f"CONDA_VERSION={base_image.conda},RSTUDIO_VERSION={base_image.rstudio},R_VERSION={base_image.r}"

        write_json(
            os.path.join("templates", "base_image", "cookiecutter.json"),
            cookiecutter_data,
        )
        write_json(
            os.path.join(
                "templates", "base_image", f"cookiecutter--base_image-{docker_tag}.json"
            ),
            cookiecutter_data,
        )

        tmp_base_dirpath = tempfile.mkdtemp(prefix="tiamet_base_tmp")

        cookiecutter_dst_dir = os.path.join(tmp_base_dirpath)

        docker_context_dir = os.path.join(
            "tiamet-docker-images", "base_image", f"base_image-{docker_tag}"
        )

        cookiecutter(
            # path/url to cookiecutter template
            os.path.join("templates", "base_image"),
            overwrite_if_exists=True,
            extra_context=cookiecutter_data,
            output_dir=cookiecutter_dst_dir,
            no_input=True,
        )

        shutil.copytree(
            os.path.join(cookiecutter_dst_dir, cookiecutter_data["project_slug"]),
            docker_context_dir,
            dirs_exist_ok=True,
        )
        shutil.rmtree(cookiecutter_dst_dir)

        # Build out the GH Workflow for the first step - build base image
        base_gh_workflow = read_yaml(os.path.join("templates", "workflow.yml"))

        if latest == docker_tag:
            tags = base_gh_workflow["jobs"]["base-image"]["steps"][2]["with"]["tags"]
            tags = append_latest_tag(tags)
            base_gh_workflow["jobs"]["base-image"]["steps"][2]["with"]["tags"] = tags

        base_gh_workflow["name"] = f"Base-Image-{docker_tag}"
        base_gh_workflow["env"]["DOCKER_TAG"] = docker_tag
        base_gh_workflow["env"]["CONDA_VERSION"] = base_image.conda
        base_gh_workflow["env"]["RSTUDIO_VERSION"] = base_image.rstudio
        base_gh_workflow["env"]["R_VERSION"] = base_image.r
        base_gh_workflow["jobs"]["base-image"]["steps"][2]["with"][
            "workdir"
        ] = docker_context_dir
        base_gh_workflow["jobs"]["base-image"]["steps"][2]["with"][
            "buildargs"
        ] = f"CONDA_VERSION={base_image.conda},RSTUDIO_VERSION={base_image.rstudio},R_VERSION={base_image.r}"

        package_image_data = generate_package_image_cookiecutter(
            config_data=config_data,
            base_image=base_image,
            base_docker_tag=docker_tag,
            base_latest_tag=latest,
            tmp_dirpath=tmp_dirpath,
            base_gh_workflow=base_gh_workflow,
        )
        package_image_data_all.append(
            {
                "display_name": f"Base Image: R: {base_image.r} RStudio: {base_image.rstudio} Conda: {base_image.conda}",
                "project": cookiecutter_data["project"],
                "cookiecutter": cookiecutter_data,
                "images": pd.DataFrame.from_records(package_image_data),
            }
        )

    generate_readme(config_data, package_image_data_all)
    return t_base_image_products, latest, package_image_data_all


def write_yaml(file, yaml_payload):
    with open(file, "w") as outfile:
        safe_dump(
            yaml_payload, outfile, sort_keys=False,
        )


def write_json(file, json_payload):
    with open(file, "w") as f:
        json.dump(json_payload, f, indent=4, default=str, sort_keys=False)


def read_json(file) -> Any:
    with open(file, "r") as reader:
        data = json.load(reader)
    return data


def read_ordered_yaml(file) -> Any:
    """Read github actions and other orered yamls"""
    with open(file, "r") as stream:
        return hiyapyco.odyldo.safe_load(stream)


def read_yaml(file) -> Any:
    with open(file, "r") as stream:
        data = ruamel.yaml.safe_load(stream)
    return data


def read_config() -> Any:
    return read_yaml("config.yml")


def main():
    config_data = read_config()
    (
        base_image_products,
        latest,
        package_image_data_all,
    ) = generate_base_image_cookiecutter(config_data)


if __name__ == "__main__":
    main()
