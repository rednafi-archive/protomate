# protomate

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/rednafi/protomate/blob/master/LICENSE) ![stability-experimental](https://img.shields.io/badge/stability-experimental-orange.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

![Alt Text](https://github.com/rednafi/protomate/blob/master/demo/protomate.gif)

This will perform the following tasks:

- Create a new project folder in your **current** folder
- Initialize a git repository
- Create a remote repository
- Add remote to the local repository
- Add a `readme.md` file
- Add a `.gitignore` file specific for your language of choice
- Perform initial stage, commit, push
- Open the project folder in vscode

## Installation

```
Install `protomate` via:
```
pip3 install protomate==0.4.8
```
## Run the App

To create a new project in your designated project folder, first `cd` to your desired location:

```
cd project-location
```

To initialize the CLI, type:

```
protomate
```

This should:

- Prompt you to put your

  - Github credentials
  - Repository name
  - Repository type (public/private)
  - Language of `.gitignore` (python, javascript etc). See a list of all the supported [languages](https://github.com/rednafi/protomate/blob/master/languages.py).

- Create a new local and remote git repository

- Connect them and open vs code for you to start coding immediately

## Contributor
* Redowan Delowar (Author & primary maintainer) [@rednafi](https://github.com/rednafi)
* Manash Kumar Mandal [@manashmndl](https://github.com/manashmndl)
