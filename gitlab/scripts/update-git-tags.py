import os
import re
import sys

from . import versioning


def tag_repo(tag):
    url = os.environ["CI_REPOSITORY_URL"]

    # Transforms the repository URL to the SSH URL
    # Example input: https://gitlab-ci-token:xxxxxxxxxxxxxxxxxxxx@gitlab.com/project/repository.git
    # Example output: git@gitlab.com:project/repository.git
    push_url = re.sub(r'.+@([^/]+)/', r'git@\1:', url)

    versioning.git("remote", "set-url", "--push", "origin", push_url)
    versioning.git("tag", tag, os.environ["CI_COMMIT_SHA"])
    versioning.git("push", "origin", tag)


def main():
    new_version = versioning.get_new_version()
    latest_version = versioning.get_latest_version()

    if new_version != latest_version:
        tag_repo(new_version)

    return 0


if __name__ == "__main__":
    sys.exit(main())
