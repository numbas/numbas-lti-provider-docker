# Docker Compose Recipe for Numbas LTI Tool

This repository contains a recipe to run the [Numbas LTI tool provider](https://docs.numbas.org.uk/lti) in Docker.

It contains everything needed to run the Numbas LTI tool in Docker containers.

## Documentation

There's documentation for administrators, instructors and students at [docs.numbas.org.uk/lti](https://docs.numbas.org.uk/lti).

## Installation

### Prerequisites

Install [Docker](https://docs.docker.com/engine/install/).
We have tested with Docker version 24.

### Setup

Build the docker image:

```
docker build . -t numbas/numbas-lti-provider
```

Copy the file `settings.env.dist` to `settings.env` and write your own values each of the variables inside.

Run the `get_secret_key` script to generate a value for the `SECRET_KEY` environment variable, and put that in `settings.env`:

```
docker compose run --rm numbas-setup python ./get_secret_key
```

Obtain an SSL certificate and key for the domain you will access the Numbas LTI provider from. Copy the key to `files/ssl/numbas-lti.key` and the certificate to `files/ssl/numbas-lti.pem`.

Run the installation script, to set up the database and create the superuser account:

```
docker compose run --rm numbas-setup python ./install
```

The LTI provider is ready to start.

### Starting

Run the following command:

```
docker compose up --scale daphne=4 --scale huey=2
```

You can customise the number of each of the kinds of process by changing the numbers in the `--scale` arguments.
The `daphne` process handles web requests; you will need more if you have lots of simultaneous connections.
The `huey` process runs asynchronous tasks; you will need more if you find that tasks such as reporting scores or generating report files take a very long time.

### Stopping

Stop the numbas-lti containers with `docker compose down`.

## Running in the cloud

Docker Compose files can also be used to deploy to the cloud. See the following documents for more information about deploying Docker to the cloud:
 - [Compose for Amazon ECS](https://docs.docker.com/engine/context/ecs-integration/)
 - [Compose for Microsoft ACI](https://docs.docker.com/engine/context/aci-integration/)

## Upgrading

When there is a new version of the Numbas LTI provider, you must rebuild the Docker image and apply any database migrations.

If any other changes are required when moving to a particular version, they will be listed here.

### Standard upgrade instructions

To upgrade to a new version, follow these steps after fetching the latest version of this repository.

Remake the container image:

```
docker build . --no-cache -t numbas/numbas-lti-provider
```

Then run the installation script again:

```
docker compose run --rm numbas-setup python ./install
```

### v2.x to v3.0

There are several new settings which must be set in `settings.env`.
Look at `settings.env.dist` to see what they are, copy them across to your `settings.env` file, and make changes if needed.

### v3.x to v4.0

There are no new settings.
