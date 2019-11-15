import os
import sys
import urllib
import shutil
import threading
from multiprocessing import Process, Event, Queue
from git import Repo
from git import RemoteProgress
from util import AgentJobDir, createDir, getVar, fetchCredential

# inputs of plugin
GitUrl = getVar('FLOWCI_GIT_URL')
GitBranch = getVar('FLOWCI_GIT_BRANCH')
GitRepoName = getVar('FLOWCI_GIT_REPO')
GitTimeOut = int(getVar('FLOWCI_GITCLONE_TIMEOUT'))

CredentialName = getVar('FLOWCI_CREDENTIAL_NAME', False)
KeyDir = createDir(os.path.join(AgentJobDir, '.keys'))
KeyPath = None

ExitEvent = Event()
StateQueue = Queue()

class MyProgressPrinter(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        percentage = "{00:.2f}%".format(cur_count / (max_count) * 100)
        print(op_code, cur_count, max_count, percentage, message or "")


def isHttpUrl(val):
    return val.startswith('http://') or val.startswith('https://')

def put(code, msg):
    StateQueue.put({
        'code': code,
        'msg': msg
    })

def setupCredential(c):
    global GitUrl
    global KeyPath

    name = c['name']
    category = c['category']

    if isHttpUrl(GitUrl):
        if category != 'AUTH':
            put(1, '[ERROR] Credential type is miss match')
            ExitEvent.set()
            sys.exit()
        

        index = GitUrl.index('://')
        index += 3

        username = urllib.parse.quote(c['pair']['username'])
        password = urllib.parse.quote(c['pair']['password'])
        GitUrl = "{}{}:{}@{}".format(
            GitUrl[:index], username, password, GitUrl[index:])

    else:
        if category != 'SSH_RSA':
            put(1, '[ERROR] Credential type is miss match')
            ExitEvent.set()
            sys.exit()

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
            print("[ERROR]: %s - %s." % (e.filename, e.strerror))

        # repo = Repo(dest)
        # repo.remote().pull(progress = MyProgressPrinter())

    # git clone
    env = {}
    if KeyPath is not None:
        env["GIT_SSH_COMMAND"] = 'ssh -o {} -o {} -i {}'.format(
            'UserKnownHostsFile=/dev/null', 'StrictHostKeyChecking=no', KeyPath)

    try:
        repo = Repo.clone_from(
            url=GitUrl,
            to_path=dest,
            progress=MyProgressPrinter(),
            branch=GitBranch,
            env=env
        )

        put(0, '')
        ExitEvent.set()
    except Exception as e:
        put(1, e.strerror)
        ExitEvent.set()
        sys.exit()

print("[INFO] -------- start git-clone plugin --------")

print("[INFO] url:        {}".format(GitUrl))
print("[INFO] branch:     {}".format(GitBranch))
print("[INFO] name:       {}".format(GitRepoName))
print("[INFO] timeout:    {}".format(GitTimeOut))
print("[INFO] credential: {}".format(CredentialName))

# start git clone process
p = Process(target=gitPullOrClone)
p.start()

# kill if not finished within 60 seconds
val = ExitEvent.wait(timeout=GitTimeOut)
if val is False:
    p.terminate()
    sys.exit('[ERROR] git clone timeout')

state = StateQueue.get()
if state['code'] is not 0:
    print(state['msg'])
    sys.exit("[INFO] -------- exit with error --------")

cleanUp()

print("[INFO] -------- done --------")
