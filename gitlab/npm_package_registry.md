# Gitlab: npm package registry + auto versioning

## In workspace

1. (once for workspace) Settings > General > Visibility, project features, permissions. Enable the packages feature

## In repository

1. Generate ssh with **no passphrase** for repository: `ssh-keygen -t rsa -b 4096`  
2. Add the public part as a new Deploy Key in the Settings -> Repository. Check “Write access allowed”
3. Add the private part as a new Variable SSH_PRIVATE_KEY in the CI/CD section
4. Settings > Repository > Deploy Tokens. Enter the required details and provide the read_package_registry and write_package_registry
5. Update package.json
```
"name": "@my-org/my-package-name"
...
"publishConfig":{
  "@my-org:registry": "https://gitlab.com/api/v4/projects/<your-project-id>/packages/npm/"
}
```
6. Add gitlab-ci.yml from [here](pipelines/versioning_and_publish.gitlab-ci.yml)
7. Create scripts directory and copy scripts [update-git-tags.py](scripts/update-git-tags.py), [versioning-hook.py](scripts/versioning-hook.py), [versioning.py](scripts/versioning.py)
8. add command `python3 -m scripts.versioning-hook && git add .` to pre-commit hook(in case of husky its .husky/pre_commit)

## In repositories using source repository

1. Update .npmrc for **all projects using your published package**
```
# for instance level
@org:registry=https://gitlab.com/api/v4/packages/npm/
# for project level
@org:registry=https://gitlab.com/api/v4/projects/project_id/packages/npm/
# for any case
//gitlab.com/api/v4/projects/project_id/packages/npm/:_authToken=<<<access token>>>
```

## TODO

- add tag for disabling version - #no-version