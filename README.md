# flowci-plugin-gitclone

## Description

The plugin will clone the git repo, and submodules based on inputs

## Inputs

- `FLOWCI_GIT_URL` (required): git http/ssh url, ex: git@github.com:FlowCI/spring-petclinic-sample.git
- `FLOWCI_GIT_BRANCH`: git branch name, default value is master
- `FLOWCI_GIT_COMMIT_ID`: clone from commit id if this variable specified
- `FLOWCI_GIT_CREDENTIAL`: credential name created from flow.ci, it's required if git url is based on ssh
- `FLOWCI_GITCLONE_TIMEOUT`: timeout for gitclone in seconds, default is 60 seconds
- `FLOWCI_PIP_SOURCE`: since `gitpython` will be installed from `pip`, you can define the pip source if needed

## Exports

- `FLOWCI_GIT_AUTHOR`: commit author email
- `FLOWCI_GIT_COMMIT_ID`: commit id
- `FLOWCI_GIT_COMMIT_MESSAGE`: commit message
- `FLOWCI_GIT_COMMIT_TIME`: commit time

## How to use it

```yml
envs:
  FLOWCI_GIT_URL: "https://github.com/FlowCI/spring-petclinic-sample.git"
  FLOWCI_GIT_BRANCH: "master"

  # FLOWCI_GIT_CREDENTIAL: "created from ci admin page"
  # FLOWCI_GITCLONE_TIEMOUT: 60

steps:
- name: clone
  plugin: 'gitclone'

  # customize pip source from FLOWCI_PIP_SOURCE, please add --trusted-host if source is not https
  # envs:
  #   FLOWCI_PIP_SOURCE: "http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com"

- name: list
  script: |
    cd ${FLOWCI_GIT_REPO}
    ls

```
