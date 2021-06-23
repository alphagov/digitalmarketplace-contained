# DMp Contained

** EXPERIMENTAL / UNDER DEVELOPMENT **


## Motivations and vision

Anybody in a multidisciplinary team should be able to explore the service without depending on others.
This is not the exact case in our team: developers are required when colleagues would like to check out the service having a procurement framework in a state different from the one available to our users.

The vision for this project is to have a very simple setup of the service so that anybody in the team, at any time, could spin up an ephemeral instance of the service (loaded with test data) and explore what the service looks like at different states of the frameworks life-cycle.

That being the main intent, this project could also be useful to developers, architects and others for doing development and testing in a simplified environment that is easy to stand up.

Finally, having a (relatively) easy and inexpensive way of setting up an environment could open up new possibilities.

## Goal

The goal of this project is to be able to run the Digitalmarketplace web service on a single Docker container for exploration, prototyping, development and testing purposes.


## Caveats

This is not for production use.

If this is run on the public Internet (e.g. on GOV.UK PaaS), it should be password protected at the very least, also to avoid search engines indexing its content


## Architecture

The architecture priorities simplicity and economy of setup above other factors.

The single Docker container runs all the apps and backend services. The apps code is mounted onto the container so that when the code is changed on the host, those changes are reflected in the container.

The apps are run via the built-in Flask web server (each app listens on a different port) while nginx, redis and postgres are run as services on the container (no Docker-in-docker).
The drawback of running the backend services not as individual containers is that it will be more difficult to pin their versions to the ones used on production (as here we rely on the packages available for the single Docker image).


## Requirements

Docker


## How to run this project

* Clone this repo

* Clone the apps' Github repos into mount-for-container/apps-github-repos (if you are using dm-runner you could just copy the `code` directory over)

* Build the container: `docker build -t dmp-contained .`

* Run the container: `docker run --rm --name dmp-contained -it -p 80:80 --mount type=bind,source="$(pwd)"/mount-for-container,target=/dmp-contained/mount dmp-contained /bin/bash`. This is going to open up a shell on the container

* In the container, run `/usr/local/bin/python3.6 setup.py`
  * the `--dry-run` flag is supported. Use `--help` for more info
  * actually, you could run this as part of the previous step, but let's keep simple for now

When this script ends you should be able to hit `http://localhost` from your browser (host environment) and see a DMp webpage (or most likely a Flask error page from the container at this stage of development).


## Next steps
For now, only the buyer-frontend is available (via nginx) but erroring because there is no api.

Next few steps
- stand up postgres
- import test data
- stand up the api app - validate this chain of communications is working well: buyer-frontend -> api -> postgres
- stand up redis
- stand up all other apps - at this point the service should run without major issues (apart from when file management and search are involved)
- deploy the container onto GOV.UK PaaS using Github Actions

After those points are completed, look at the TODO section below and please search for "TODO" text scattered in the files.

## TODO
* Quick refactoring / tidying up
  * `settings.yml` is a direct copy of the one in `dmp-runner` - remove anything that is not needed, such as the `run-order` attribute as we don't rely on it anymore (do we need to make it clearer we launch apps in the order that are written down in settings.yml?)
* Must have's
  * Clean up and refactor the code to make it very maintainable and easy-to-follow
  * Review how we can make the container more observable and easier to troubleshoot any problem during setup
  * Add implementation for Elasticsearch
  * Add implementation for S3
  * Ensure we can run automated tests against the environment
* Nice to have's
  * big
    * Add automated regression tests
    * Improve speed of the setup (e.g. caching, parallelisation)
    * Make the step of running the `setup.py` automatic.
      * I really wanted to add this as last step of the Dockerfile (`CMD /usr/local/python3 setup.py`) however the problem was that the setup script needs the `mount-for-container` folder to be mounted but that can't be done in the Dockerfile. There must be a proper solution/pattern for this. Maybe worth asking a Docker expert.
    * Change the versions of the dependencies to match more closely production
    * Change setup behaviour so that if the apps Github repos are not found in the mounted volume, they will be cloned by the container - this should make it easier to standup the full environment for prototyping
