import subprocess
import os
import re

def git(*args):
    return subprocess.check_output(["git"] + list(args))

def npm(*args):
    return subprocess.check_output(["npm"] + list(args), shell=False if os.name == 'posix' else True)

def bump_patch(version):
    splitted = version.split('.')
    splitted[2] = str(int(splitted[2])+1)
    new_version = '.'.join(splitted)
    return new_version

def bump_minor(version):
    splitted = version.split('.')
    splitted[1] = str(int(splitted[1])+1)
    new_version = '.'.join(splitted)
    return new_version

def bump_major(version):
    splitted = version.split('.')
    splitted[0] = str(int(splitted[0])+1)
    new_version = '.'.join(splitted)
    return new_version

def get_upcoming_commit():
    commit_file = open(".git/COMMIT_EDITMSG", 'r')
    return str(commit_file.read())

def get_last_commit():
    return git("show-branch", "--no-name", "HEAD").decode()

def bump(latest, hook_commit=False):
    last_commit = get_upcoming_commit() if hook_commit == True else get_last_commit()

    is_patch = "#patch" in last_commit
    is_minor = "#minor" in last_commit
    is_major = "#major" in last_commit
    is_skip_version = "#skip-version" in last_commit

    if is_skip_version:
        return latest
    elif is_patch and not is_minor and not is_major:
        return bump_patch(latest)
    elif not is_patch and is_minor and not is_major:
        return bump_minor(latest)
    elif not is_patch and not is_minor and is_major:
        return bump_major(latest)
    else:
        return bump_patch(latest)

def get_latest_version():
    try:
        return git("describe", "--abbrev=0", "--tags").decode().strip()
    except subprocess.CalledProcessError:
        return "1.0.0"

def get_new_version(hook_commit=False):
    latest = get_latest_version()
    return bump(latest, hook_commit)
