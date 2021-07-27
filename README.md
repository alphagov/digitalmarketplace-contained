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

The apps are run via the built-in Flask web server (each app listens on a different port) while nginx, redis, 
postgres and elasticsearch are run as services on the container (no Docker-in-docker).

[Localstack](https://github.com/localstack/localstack) (which "emulates" the AWS S3 service so to run the environment
without the need of AWS credentials) is running as a separate container. 
The dmp-contained and localstack containers are  attached to a Docker network so that they can communicate.

## Pain points

1. As the backend services run directly on this container it is more difficult (albeit not impossible) to control
their version compared to running them as separate containers - that is because we install the version available
for the container operating system (see Dockerfile) which may be different from the one we use on production.

2. It is slow to stand up an environment - everything needs to be provisioned basically from scratch.
At the time of writing, on a Macbook Pro, 2.2 GHz Quad-Core Intel Core i7, 16 GB 1600 MHz DDR3 RAM:
   * it takes around 35 mins for the environment to be ready if the code is already on your computer, roughly distributed as
   1 min to provision the backend services, 20 mins to start the apps, 5 mins for importing test data in Postgres
   and 10 minutes to build the Elasticsearch indexes.
   * it takes around 75 mins for the environment to be ready if the code is not already on your computer


3. Having at least 6GB of RAM for Docker is needed, mostly because the ElasticSearch indexing is very intensive.



## Requirements

Docker, with a reservation of at least 6GB of RAM (that is because Elasticsearch indexing is very intensive)


## How to run this project

1. Clone this repo

2. In the `/resources-for-container/mount` folder, add a file `test_data.sql` containing the SQL statements 
  to initialise the database (you can use the one from dm-runner).
   
3. Create network to attach both the Localstack and dmp-contained containers to (only the first time):
   `docker network create dmp-contained`

4. Run the Localstack container in a separate terminal (or terminal tab):
  ```
  docker run \
  --rm -it \
  --net=dmp-contained \
  --net-alias=s3.localhost.localstack.cloud \
  --net-alias=digitalmarketplace-dev-uploads.s3.localhost.localstack.cloud \
  --name=localstack \
  -p 4566:4566 \
  --env SERVICES=s3 \
  --env DATA_DIR=/tmp/localstack \
  --env DEFAULT_REGION=eu-west-1 \
  --mount 'type=volume,source=s3-data,target=/tmp/localstack' \
  --volume /var/run/docker.sock:/var/run/docker.sock \
  localstack/localstack:0.12.9.1@sha256:bf1685501c6b3f75a871b5319857b2cc88158eb80a225afe8abef9a935d5148a
  ``` 

5. Build the dmp-contained container: `docker build -t dmp-contained .`

6. Run the container:
  ```
  docker run \
  --init --rm -it \
  --memory 6G \
  --name dmp-contained \
  --net=dmp-contained \
  -p 80:80 \
  -p 55000:55000 \
  -p 55009:55009 \
  --mount type=bind,source="$(pwd)"/resources-for-container/mount,target=/dmp-contained/mount \
  dmp-contained /bin/bash
  ``` 
  This is going to open up a shell on the container

7. In the container, run `/usr/local/bin/python3.6 start.py` (use the `--help` option for seeing all the options
   available when running the script) 

__This step will checkout the code into `/resources-for-container/mount/local-repos`. If the code was already
checked out, it will perform a `git pull --rebase` on all the checkout folders.__

When this script ends you should be able to hit `http://localhost` from your browser (host environment) and see a
DMp webpage (or most likely a Flask error page from the container at this stage of development).

## Running the functional tests

To run the [functional tests](https://github.com/alphagov/digitalmarketplace-functional-tests) against the environment,
set `55000` and `55009` as api and search-api ports respectively (that is the original ports with an extra `5` at
the start).

Those two ports will be proxied to the api apps by nginx. It would have been nice if
we didn't need this extra step and we could have used the apps ports directly from the host. That may be possible with some
nginx and/or Docker network configuration change. One other solution may be to have the flask api apps run on
`localhost` rather than `127.0.0.1`.

## Managing the environment

Utilities to manage the environment can be found in the `resources-for-container/files/utils` folder, which is copied
onto the container - typically, those utilities need to be run on the container.

Ideally, we will have time to provide a more integrated and convenient management "consolle" at some point.

## TODO
* Smaller refactoring / improvements that should be done next:
  * finish the work in the branch `ci` to introduce tests and checks on Github
  * fix design flow: backend should be initialised independently to whether they were provisioned internally or 
    externally
  * test backends services are accepting incoming requests before provisioning apps
  * --dry-run will fail miserably if the repos are not already checked out - not something to fix probably but just to 
    manage better
  * remove type hints from within methods (suggested in a code review)
  * try to have localStack run within the container
    
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