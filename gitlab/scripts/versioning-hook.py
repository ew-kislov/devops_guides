import os
import re
import sys
from datetime import datetime

from . import versioning

def write_changelog(version):
    changelog = open("CHANGELOG.md", "a+")
    changelog_empty = os.stat("CHANGELOG.md").st_size == 0

    last_commit = versioning.git("show-branch", "--no-name", "HEAD").decode()
    last_commit_cleared = re.sub(r'#[^\s]*\s', '', last_commit)

    if changelog_empty:
        changelog.write("# Changelog\n\n")

    changelog.write(f"## [{version}] - {datetime.today().strftime('%Y-%m-%d')}\n")
    changelog.write(f"{last_commit_cleared}\n")

def write_npm(version):
    versioning.npm("config", "set", "git-tag-version=false")
    versioning.npm("version", version)

def main():
    # get latest tags before updating changelog and npm files
    print('Getting last versions of your project.')
    versioning.git("pull", "--tags")

    version = versioning.get_new_version()
    write_changelog(version)
    write_npm(version)

    return 0


if __name__ == "__main__":
    sys.exit(main())
