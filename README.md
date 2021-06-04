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

The apps are run via the built-in Flask web server (each app listens on a different port) while nginx, redis and postgres are run as services on the container (no Docker-in-docker).

## How to run this project

* Clone this repo

* Clone the apps' Github repos into mount-for-container/apps-github-repos (if you are using dm-runner you could just copy the "code" directory over)

* Build the container: `docker build -t dmp-contained .`

* Run the container: `docker run -it -p 80:80 --mount type=bind,source="$(pwd)"/mount-for-container,target=/dmp-contained/mount dmp-contained /bin/bash`. This is going to open up a shell on the container

* In the container, run `/usr/local/bin/python3.6 setup.py`
  * actually, you could run this as part of the previous step, but let's keep simple for now)
  * the `--dry-run` flag is supported. Use `--help` for more info

When this script ends you should be able to hit `http://localhost` from your browser (host environment) and see a DMp webpage (or most likely a Flask error page from the container).

## Next steps
For now, only the buyer-frontend is available (via nginx) but erroring because there is no api.

Next few steps
- stand up api app (as a way to also discover how to run two apps in parallel - probably the container will need more resources, and processes may need to be launched in a detatched way so if they fail, they don't block the rest of the setup, or would we rather want the whole setup to fail?)
- stand up postgres
- import clean data
- stand up redis
- stand up all other apps

After those points are completed, look at the TODO section below and please search for "TODO" text scattered in the files.

## TODO

* Must have's
  * Clean up and refactor the code to make it very maintainable and easy-to-follow
  * Review how we can make the container more observable and easier to troubleshoot any problem during setup
  * Add implementation for Elasticsearch
  * Add implementation for S3
  * Ensure we can run automated tests against the environment
* Nice to have's
  * big
    * Add automated regression tests
    * Make the step of running the `setup.py` automatic.
      * I really wanted to add this as last step of the Dockerfile (`CMD /usr/local/python3 setup.py`) however the problem was that the setup script needs the `mount-for-container` folder to be mounted but that can't be done in the Dockerfile. There must be a proper solution/pattern for this. Maybe worth asking a Docker expert.
    * Change the versions of the dependencies to match more closely production
    * Change setup behaviour so that if the apps Github repos are not found in the mounted volume, they will be cloned by the container - this should make it easier to standup the full environment for prototyping
  * small
    * add Python typing
    * settings.yml is a direct copy of the one in `dmp-runner` - remove anything that is not needed
