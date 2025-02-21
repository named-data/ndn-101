# NDN 101

An introductory website on Named Data Networking (NDN).

Link: [101.named-data.net](https://101.named-data.net/)

## General Information

This documentation website is made using [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). The website structure can be found in [`mkdocs.yml`](mkdocs.yml). Build dependencies are managed with [Poetry](https://python-poetry.org/).

## Local Build

First you should install Poetry for dependency management. We recommend using [pipx](https://pipx.pypa.io/) or [uv](https://docs.astral.sh/uv/) to install Poetry in a dedicated virtual environment. For example, you can install Poetry by running:

```shell
# Option 1: install via pipx
pipx install poetry

# Option 2: install via uv
uv tool install poetry
```

After Poetry is installed, navigate to the project directory (i.e., ndn-101) and run the command below to install the required build dependencies:

```shell
poetry install
```

To start a live preview on your machine, you can run:

```shell
poetry run mkdocs serve
```

After running this command, the MkDocs development server should start on your local machine (default port number is 8000).

To build static web pages, use this command:

```shell
poetry run mkdocs build
```

## Contributing

You can contribute to the NDN 101 website by submitting a pull request on GitHub.
