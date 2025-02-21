# NDN 101

An introductory website on Named Data Networking (NDN).

Link: [101.named-data.net](https://101.named-data.net/)

## General Information

This documentation website is made using "MkDocs" which is a fast, simple and downright gorgeus static site generator that is geared towards building project documentation. It uses markdown files for static project documentation generation. Website structure can be found in "mkdocs.yml" which is in root directory

Dependency management is made using "poetry". So you don't need to install a "requirements.txt" file.

## Local build

First you should install poetry for dependency management:

```shell
pip install poetry
```

<br>

After navigating to the project directory (i.e. NDN-101), run the command below to install project dependencies:

```shell
poetry install
```

<br>
<br>

For starting live preview on your machine you should execute this:

```shell
poetry run mkdocs serve
```

<br>
<br>

For building static web pages, use this command:

```shell
poetry run mkdocs build
```

## Contributions

You can contribute to NDN101 website documentation by creating a github pull request. Each pull request will be inspected before merging to the main branch.
You can see the code of conducts for further information. 
