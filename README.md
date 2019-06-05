# protomate
This will perform the following tasks:

* create a new project folder in your designated directory 
* navigate into the folder  
* initialize a git repository
* create a remote repository
* add remote to the local repository 
* add a readme file
* add a license file 
* perform initial stage, commit, push 
* open the project folder in vscode


## Installation

1. Clone the repository in your project folder

```
git clone https://github.com/rednafi/protomate.git
```

2. Install PyGithub

```
pip install --user PyGithub
```

3. Open ```bashrc``` via the following command:

```
sudo nano ~/.bashrc
```
Put your password add the following lines to the end of the ```bashrc``` file:

```
export GITHUB_USERNAME="your-github-username"
export GITHUB_PASSWORD="your-gihub-password"
export PROJECT_PATH="your-project-path"

function create() {
  python "${PROJECT_PATH}protomate/src/create.py" $1
}

```

Save the edit by ```ctrl+O``` and exit via pressing ```ctrl+x```.

4. Source the ```bashrc``` file 

```
source ~/.bashrc

```

### Run the App

To create a new project in your designated project folder, simply write -

```
create your-new-project-name

```

This should create a new local and remote git repository, connect them and open vs code for you code immediately!!!