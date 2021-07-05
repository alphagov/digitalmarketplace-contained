# DMp Contained

** EXPERIMENTAL / UNDER DEVELOPMENT **


## Motivations and vision

Anybody in a multidisciplinary team should be able to explore the service without depending on others.
This is not the exact case in our team: developers are required when colleagues would like to check out the service 
having a procurement framework in a state different from the one available to our users.

The vision for this project is to have a very simple setup of the service so that anybody in the team, at any time, 
could spin up an ephemeral instance of the service (loaded with test data) and explore what the service looks like at different states of the frameworks life-cycle.

That being the main intent, this project could also be useful to developers, architects and others for doing development
and testing in a simplified environment that is easy to stand up.

Finally, having a (relatively) easy and inexpensive way of setting up an environment could open up new possibilities.

## Goal

The goal of this project is to be able to run the Digitalmarketplace web service on a single Docker container for 
exploration, prototyping, development and testing purposes.


## Caveats

This is not for production use. If this was run on the public Internet (e.g. on GOV.UK PaaS),
it should be password protected at the very least, to also avoid search engines indexing its content

Running the backend services directly on this container makes it more difficult (albeit not impossible) to control
their version compared to running them as separate containers - that is because we install the version available
for the container operating system (see Dockerfile) which may be different from the one we use on production.

## Architecture

The architecture priorities simplicity and economy of setup above other factors.

The single Docker container runs all the apps and backend services. The apps code is mounted onto the container so that 
when the code is changed on the host, those changes are reflected in the container.

The apps are run via the built-in Flask web server (each app listens on a different port) while nginx, redis and 
postgres are run as services on the container (no Docker-in-docker).
The drawback of running the backend services not as individual containers is that it will be more difficult to pin their
versions to the ones used on production (as here we rely on the packages available for the single Docker image).


## Requirements

Docker


## How to run this project

* Clone this repo

* Clone the apps' Github repos into `mount-for-container/apps-github-repos` (if you are using dm-runner you could just 
  copy the content of the `code` directory over there)

* In the `mount-for-container` folder, add a file `test_data.sql` containing the SQL statements 
  to initialise the database.

* Build the container: `docker build -t dmp-contained .`

* Run the container:
  ```
  docker run \
  --init --rm -it \
  --name dmp-contained \
  -p 80:80 \
  --mount type=bind,source="$(pwd)"/mount-for-container,target=/dmp-contained/mount \
  dmp-contained /bin/bash
  ``` 
  This is going to open up a shell on the container

* In the container, run `/usr/local/bin/python3.6 start.py`
  * use the `--help` option for finding out all the options available when running the script
  * (actually, you could run this as part of the previous step, but let's keep simple for now)

When this script ends you should be able to hit `http://localhost` from your browser (host environment) and see a
DMp webpage (or most likely a Flask error page from the container at this stage of development).

## TODO
* Look at `TODO` comments in the files
* Must haves
  * Protect the Github main branch and require review for integration
  * Clean up and refactor the code to make it very maintainable and easy-to-follow
  * Review how we can make the container more observable and easier to troubleshoot problems
  * Add implementation for Elasticsearch
  * Add implementation for S3
  * Ensure we can run automated tests against the environment
* Nice to haves
  * Add automated regression tests
  * Improve speed of the setup (e.g. caching, parallelisation)
  * Make the step of running the `start.py` automatic.
    * I really wanted to add this as last step of the Dockerfile (`CMD /usr/local/python3 start.py`)
      however the problem was that the start script needs the `mount-for-container` folder to be mounted
      but that can't be done in the Dockerfile.
      There must be a proper solution/pattern for this. Maybe worth asking a Docker expert.