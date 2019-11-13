import os
import sys
import urllib
import shutil
from git import Repo
from git import RemoteProgress
from util import AgentJobDir, createDir, getVar, fetchCredential

# inputs of plugin
GitUrl = getVar('FLOWCI_GIT_URL')
GitBranch = getVar('FLOWCI_GIT_BRANCH')
GitRepoName = getVar('FLOWCI_GIT_REPO')

CredentialName = getVar('FLOWCI_CREDENTIAL_NAME', False)
KeyDir = createDir(os.path.join(AgentJobDir, '.keys'))
KeyPath = None

class MyProgressPrinter(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        percentage = "{00:.2f}%".format(cur_count / (max_count) * 100)
        print(op_code, cur_count, max_count, percentage, message or "")

def isHttpUrl(val):
    return val.startswith('http://') or val.startswith('https://')

def setupCredential(c):
    global GitUrl
    global KeyPath

    name = c['name']
    category = c['category']

    if isHttpUrl(GitUrl):
        if category != 'AUTH':
            sys.exit('[ERROR] Credential type is miss match')

        index = GitUrl.index('://')
        index += 3

        username = urllib.parse.quote(c['pair']['username'])
        password = urllib.parse.quote(c['pair']['password'])
        GitUrl = "{}{}:{}@{}".format(GitUrl[:index], username, password, GitUrl[index:]) 

    else:
        if category != 'SSH_RSA':
            sys.exit('[ERROR] Credential type is miss match')

        privateKey = c['pair']['privateKey']
        KeyPath = os.path.join(KeyDir, name)
        print(privateKey, file=open(KeyPath, 'w'))
        os.chmod(KeyPath, 0o600)

def cleanUp():
    if KeyPath is not None:
        os.remove(KeyPath)

def gitPullOrClone():
    dest = os.path.join(AgentJobDir, GitRepoName)

    # load credential
    if CredentialName is not None:
        c = fetchCredential(CredentialName)
        setupCredential(c)
                
    # clean up
    if os.path.exists(dest):
        try:
            shutil.rmtree(dest)
        except OSError as e:
            print ("[ERROR]: %s - %s." % (e.filename, e.strerror))

        # repo = Repo(dest)
        # repo.remote().pull(progress = MyProgressPrinter())

    # git clone
    env = {}
    if KeyPath is not None:
        env["GIT_SSH_COMMAND"] = 'ssh -o {} -o {} -i {}'.format('UserKnownHostsFile=/dev/null', 'StrictHostKeyChecking=no', KeyPath)

    try:
        repo = Repo.clone_from(
            url = GitUrl, 
            to_path = dest,
            progress = MyProgressPrinter(),
            branch = GitBranch,
            env = env
        )
    except Exception as e:
        sys.exit(e)
        print(e)

print("[INFO] -------- start git-clone plugin --------")

print("[INFO] url:        {}".format(GitUrl))
print("[INFO] branch:     {}".format(GitBranch))
print("[INFO] name:       {}".format(GitRepoName))
print("[INFO] credential: {}".format(CredentialName))

gitPullOrClone()
cleanUp()

print("[INFO] -------- done --------")
