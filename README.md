# DMp Contained

** EXPERIMENTAL / UNDER DEVELOPMENT **

## Goal

To be able to run the Digitalmarketplace web service on a single Docker container for 
exploration, prototyping, development and testing purposes, in a way that is easy also for non-developers.

## Caveats

This is not for production use. If this was run on the public Internet (e.g. on GOV.UK PaaS),
it should be password protected at the very least, to also avoid search engines indexing its content


## Architecture

The architecture priorities simplicity and economy of setup above other factors.

The single Docker container runs all the apps and backend services. The apps code is mounted onto the container so that 
when the code is changed on the host, those changes are reflected in the container.

The apps are run via the built-in Flask web server (each app listens on a different port) while nginx, redis and 
postgres are run as services on the container (no Docker-in-docker).

## Pain points

1. As the backend services run directly on this container it is more difficult (albeit not impossible) to control
their version compared to running them as separate containers - that is because we install the version available
for the container operating system (see Dockerfile) which may be different from the one we use on production.

2. It is slow to stand up an environment - everything needs to be provisioned basically from scratch.
At the time of writing, it takes around 35 mins* for the environment to be ready, roughly distributed as
   1 min to provision the backend services, 20 mins to start the apps, 5 mins for importing test data in Postgres
   and 10 minutes to build the Elasticsearch indexes.
   (*) on a Macbook Pro, 2.2 GHz Quad-Core Intel Core i7, 16 GB 1600 MHz DDR3 RAM)

3. Having at least 6GB of RAM for Docker is needed, mostly because the ElasticSearch indexing is very intensive.



## Requirements

Docker, with a reservation of at least 6GB of RAM (that is because Elasticsearch indexing is very intensive)


## How to run this project

1. Clone this repo

2. Clone the apps' Github repos into `/resources-for-container/mount/apps-github-repos` (if you are using dm-runner you
   could just copy the content of the `code` directory over there) [TODO: create a script to do this]

3. In the `/resources-for-container/mount` folder, add a file `test_data.sql` containing the SQL statements 
  to initialise the database (you can use the one from dm-runner).

4. Build the container: `docker build -t dmp-contained .`

5. Run the container:
  ```
  docker run \
  --init --rm -it \
  --memory 6G \
  --name dmp-contained \
  -p 80:80 \
  --mount type=bind,source="$(pwd)"/resources-for-container/mount,target=/dmp-contained/mount \
  dmp-contained /bin/bash
  ``` 
  This is going to open up a shell on the container

6. In the container, run `/usr/local/bin/python3.6 start.py` (use the `--help` option for seeing all the options
   available when running the script) 

When this script ends you should be able to hit `http://localhost` from your browser (host environment) and see a
DMp webpage (or most likely a Flask error page from the container at this stage of development).

## TODO
* Look at `TODO` comments in the files
* Must haves
  * Protect the Github main branch and require review for integration
  * Clean up and refactor the code to make it very maintainable and easy-to-follow
  * Review how we can make the container more observable and easier to troubleshoot problems
  * Add implementation for S3
  * Ensure we can run automated tests against the environment
* Nice to haves
  * Add automated regression tests
  * Improve speed of the setup (e.g. caching, parallelisation)
  * Make the step of running the `start.py` automatic.
    * I really wanted to add this as last step of the Dockerfile (`CMD /usr/local/python3 start.py`)
      however the problem was that the start script needs the `mount` folder to be mounted
      but that can't be done in the Dockerfile.
      There must be a proper solution/pattern for this. Maybe worth asking a Docker expert.