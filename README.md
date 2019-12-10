# flowci-plugin-gitclone

## Description

The plugin will clone the git repo based on inputs

## Inputs

- `FLOWCI_GIT_URL` (required): git http/ssh url, ex: git@github.com:FlowCI/spring-petclinic-sample.git
- `FLOWCI_GIT_BRANCH` (required): git branch name, ex: master
- `FLOWCI_GIT_REPO` (required): git repo name
- `FLOWCI_GIT_CREDENTIAL`: credential name created from flow.ci, it's required if git url is based on ssh
- `FLOWCI_GITCLONE_TIMEOUT`: timeout for gitclone in seconds, default is 60 seconds

## How to use it

```yml
envs:
  FLOWCI_GIT_URL: "https://github.com/FlowCI/spring-petclinic-sample.git"
  FLOWCI_GIT_BRANCH: "master"
  FLOWCI_GIT_REPO: "spring-petclinic"

  # FLOWCI_GIT_CREDENTIAL: "created from ci admin page"
  # FLOWCI_GITCLONE_TIEMOUT: 60

steps:
- name: clone
  plugin: 'gitclone'

- name: list
  script: |
    cd ${FLOWCI_GIT_REPO}
    ls

```
