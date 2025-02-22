# NDN 101

An introductory website on Named Data Networking (NDN).

Link: [101.named-data.net](https://101.named-data.net/)

## General Information

This documentation website is made using "MkDocs" which uses markdown files for static project documentation generation. Website structure can be found in "mkdocs.yml" which is in root directory.

Dependency management is made using "poetry". So you don't need to install a "requirements.txt" file.

## Local build

First you should install poetry for dependency management, its is strongly recommended to install poetry in a dedicated virtual environment. It should in no case be installed in the environment of the project that is to be managed by Poetry.
To achieve this, you can use pipx; a tool that installs and runs Python applications in isolated environments. Further information can be found in this [website](python-poetry.org/docs/#installing-with-pipx). If pipx is not already installed, you can install it using your system's package manager or via pip with this command:

```shell
pip install pipx
```

Once pipx is installed, you can install Poetry by running:

```shell
pipx install poetry
```




After navigating to the project directory (i.e. NDN-101), run the command below to install project dependencies:

```shell
poetry install
```



For starting live preview on your machine you should execute this:

```shell
poetry run mkdocs serve
```
After executing this command, MkDocs development server should start in your local machine (default port number is 8000).

For building static web pages, use this command:

```shell
poetry run mkdocs build
```

## Contributions

You can contribute to NDN101 website documentation by creating a github pull request. Each pull request will be inspected before merging to the main branch.
You can see the code of conduct for further information. 
