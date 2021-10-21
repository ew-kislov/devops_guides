import os
import sys
import re
from datetime import datetime

from . import versioning

def get_last_commit():
    commit_file = open(".git/COMMIT_EDITMSG", 'r')
    return str(commit_file.read())

def write_changelog(version):
    last_commit = get_last_commit()
    last_commit_cleared = re.sub(r'#[^\s]*\s', '', last_commit)

    changelog = open("CHANGELOG.md", "a+")
    changelog_empty = os.stat("CHANGELOG.md").st_size == 0

    if changelog_empty:
        changelog.write("# Changelog\n\n")

    changelog.write(f"## [{version}] - {datetime.today().strftime('%Y-%m-%d')}\n")

    sys.stdin = open('/dev/tty')
    notes = str(input("Enter version description(optional): "))

    if len(notes) > 1:
        changelog.write(f"{notes}\n")
    else:
        changelog.write(f"{last_commit_cleared}\n")


def write_npm(version):
    versioning.npm("config", "set", "git-tag-version=false")
    versioning.npm("version", version)

def main():
    # get latest tags before updating changelog and npm files
    print('Getting last versions of your project.')
    versioning.git("pull", "--tags")

    new_version = versioning.get_new_version(hook_commit=True)
    latest_version = versioning.get_latest_version()

    if new_version != latest_version:
        write_changelog(new_version)
        write_npm(new_version)

    return 0


if __name__ == "__main__":
    sys.exit(main())
