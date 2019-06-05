# protomate
This will perform the following tasks:

* Create a new project folder in your designated directory 
* Navigate into the folder  
* Initialize a git repository
* Create a remote repository
* Add remote to the local repository 
* Add a readme file 
* Perform initial stage, commit, push 
* Open the project folder in vscode


## Installation

* Clone the repository in your main project folder (where all of your project folders will reside)

```
git clone https://github.com/rednafi/protomate.git
```

* Install ```PyGithub```

```
pip install --user PyGithub
```

* Open ```bashrc``` via the following command:

```
sudo nano ~/.bashrc
```
Add the following lines to the end of the ```bashrc``` file. Change replace the three variables: ```GITHUB_USERNAME```, ```GITHUB_PASSWORD``` and ```PROJECT_PATH``` with relevant values.

```
export GITHUB_USERNAME="your-github-username"       #e.g. flunkypuppy
export GITHUB_PASSWORD="your-gihub-password"        #e.g. 1234
export PROJECT_PATH="your-project-path"             #e.g. /home/redowan/code/

function create() {
  python "${PROJECT_PATH}/protomate/src/create.py" $1
}
```

Save the edit by ```ctrl+O``` and exit via pressing ```ctrl+x```.

* Source the ```bashrc``` file 

```
source ~/.bashrc
```

## Run the App

To create a new project in your designated project folder, simply write -

```
create your-new-project-name
```

This should create a new local and remote git repository, connect them and open vs code for you to start coding immediately.

