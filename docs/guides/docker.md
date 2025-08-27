# Docker

Docker is a platform that packages your application and its dependencies into a standardized unit called a container. We use Docker to distribute the app as a single docker compose file and it's also used to deploy the project locally during development. This guide will help you set up a minimal Docker environment to ensure our project runs consistently across any machine.

## Installation

This part of the guide is a condensed version of what was found at the official documentation during August 2025. For always up to date check: https://docs.docker.com/get-started/

### Linux

To install docker and its packages on linux (debian based) you'll first need to set up the apt repository:

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

Then simply install Docker along its utilities:

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

To test everything works you can:

```bash
sudo docker run hello-world
```

### Windows

Download the installer from https://docs.docker.com/desktop/setup/install/windows-install/

## Usage

For the most part we write docker compose files to follow an Infrastructure as Code approach to deployment of the app. This avoids having to remember the full syntax for all the settings you need for the image and to simply run the command:

```bash
docker compose up -f path/to/config.yml
```

To quickly deploy the app during development you can use the dev-compose.yml file. To avoid messing with project directory and having to copy around configuration files, you can use a `dockerdev` directory in the root of the project as the home for your docker images, for example like:

```bash
mkdir dockerdev
cd dockerdev
docker compose up ../docker/dev-compose.yml
```
