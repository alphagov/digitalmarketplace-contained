# DMp Contained

** EXPERIMENTAL / UNDER DEVELOPMENT **

## Requirements

Docker

## Goal

The goal of this project is to be able to run the Digitalmarketplace web service on a single Docker container for development, testing and prototyping purposes.

## Caveats

This is not for production use.

If this is run on the public Internet (e.g. on GOV.UK PaaS), it should be password protected at the very least, also to avoid search engines indexing its content

## Architecture

The Docker container will run all the apps and backend services. The apps code will be mounted in the container so that the code can be changed on the host, and changes should be reflected in the container.

## How to run this project

* Clone this repo

* Clone the apps' Github repos into mount-for-container/apps-github-repos (if you are using dm-runner you could just copy the "code" directory over)

* Build the container: `docker build -t dmp-contained .`

* Run the container: `docker run -it -p 80:80 --mount type=bind,source="$(pwd)"/mount-for-container,target=/dmp-contained/mount dmp-contained /bin/bash`. This is going to open up a shell on the container

* In the container, run `/usr/local/bin/python3.6 setup.py`

## TODO

* Must have's
  * Clean up and refactor the code to make it very maintainable and easy-to-follow
  * Have this running w/o Elasticsearch and S3
  * Add implementation for Elasticsearch
  * Add implementation for S3
* Nice to have's
  * big
    * Make the step of running the `setup.py` automatic.
      * I really wanted to add this as last step of the Dockerfile (`CMD /usr/local/python3 setup.py`) however the problem was that the setup script needs the `mount-for-container` folder to be mounted but that can't be done in the Dockerfile. There must be a proper solution/pattern for this. Maybe worth asking a Docker expert.
    * Change the versions of the dependencies to match more closely production
    * Change setup behaviour so that if the apps Github repos are not found in the mounted volume, they will be cloned by the container - this should make it easier to standup the full environment for prototyping
  * small
    * settings.yml is a direct copy of the one in `dmp-runner` - remove anything that is not needed
