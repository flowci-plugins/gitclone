# flowci-plugin-gitclone

## Description

The plugin will clone the git repo based on inputs

## Inputs

- `FLOWCI_GIT_URL` (required): git http/ssh url, ex: git@github.com:FlowCI/spring-petclinic-sample.git
- `FLOWCI_GIT_BRANCH` (required): git branch name, ex: master
- `FLOWCI_GIT_REPO` (required): git repo name
- `FLOWCI_CREDENTIAL_NAME`: credential name created from flow.ci, it's required if git url is based on ssh

## How to use it

```yml
envs:
  FLOWCI_GIT_URL: "https://github.com/FlowCI/spring-petclinic-sample.git"
  FLOWCI_GIT_BRANCH: "master"
  FLOWCI_GIT_REPO: "spring-petclinic"

steps:
- name: clone
  plugin: 'gitclone'

- name: list
  script: |
    cd ${FLOWCI_GIT_REPO}
    ls

```
