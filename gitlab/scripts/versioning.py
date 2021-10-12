import semver
import subprocess


def git(*args):
    return subprocess.check_output(["git"] + list(args))

def npm(*args):
    return subprocess.check_output(["npm"] + list(args))

def bump(latest):
    last_commit = git("show-branch", "--no-name", "HEAD").decode()

    is_patch = "#patch" in last_commit
    is_minor = "#minor" in last_commit
    is_major = "#major" in last_commit

    if is_patch and not is_minor and not is_major:
        return semver.bump_patch(latest)
    elif not is_patch and is_minor and not is_major:
        return semver.bump_minor(latest)
    elif not is_patch and not is_minor and is_major:
        return semver.bump_major(latest)
    else:
        return semver.bump_patch(latest)

def get_new_version():
    try:
        latest = git("describe", "--abbrev=0", "--tags").decode().strip()
    except subprocess.CalledProcessError:
        return "1.0.0"

    return bump(latest)
