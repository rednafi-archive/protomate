#!/bin/bash

function create()
GITHUB_NAME = "rednafi"
{
    cd
    python create.py $1 
    cd ./$1
    git init
    git remote add origin git@github.com:"$GITHUB_NAME"/$1.git
    touch README.md
    git add .
    git commit -m "initial commit"
    git push -u origin master
    code .
}