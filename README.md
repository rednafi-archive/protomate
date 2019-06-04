# protomate
Automating project initialisation: create a new project folder >> navigate into the folder >> initialize a git repo >> create a remote repo >> add remote to the local repo >> add a readme file >> add a license file >>  initial stage, commit, push >> open vscode

Open ````bashrc``` via the following command:

```
sudo nano ~/.bashrc
```
Put your password add the following lines to the end of the ```bashrc``` file:

```
export GITHUB_USERNAME="your-github-username"
export GITHUB_PASSWORD="your-github-password"
```

Save the edit by ```ctrl+O``` and exit via pressing ```ctrl+x```.