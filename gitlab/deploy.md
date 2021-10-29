# Gitlab deploy instruction

1. Add environment variables - DEPLOY_IP, DEPLOY_USER, ENV_FILE(file), ID_RSA(file), NPMRC(file), SSH_PRIVATE_KEY  
2.1 If you're using docker-compose.yml, copy this [.gitlab-ci.yml](pipelines/docker-compose.gitlab-ci.yml) to your repository  
2.2 if you're using Dockerfile, copy this [.gitlab-ci.yml](pipelines/docker.gitlab-ci.yml) to your repository  
