# Data models

## Servers

Servers contain the needed information for connecting and syncing files with a Stolos server. For the authentication model see [the authentication docs](authentication.md).

### Fields

* `docker_ca_pem`: `ca.pem` (certificate authority certificate) to use for connecting to Docker
* `host`: the server IP or hostname to use when connecting
* `created`: the date this stack was created
* `last_update`: the date this stack was last updated

## Stacks

Stacks are the basic building blocks of Stolos projects. Stacks contain the needed Docker Compose file that should stay the same for all projects created by this Stack. Also, by updating the Docker Compose file of a Stack, all the projects created by it should be updated automatically.

### Fields

* `docker_compose_file`: Docker compose file
* `owner`: the company owning this stack
* `created`: the date this stack was created
* `last_update`: the date this stack was last updated

## Project routing configs

Project routing configs are the corner-stone of [`stolos-watchd`](https://github.com/sourcelair/stolos#sister-watchd) - currently incorporated into `stolosd`. Routing configs are identified by a combination of a domain name and a project id.


### Fields

* `project`: the related project, unique
* `domain`: the domain name to use as a base when creating the semantic URLs for the project's services
* `config`: arbitrary key-value configuration options, currently supporting only the `subdomains` option
* `created`: the date this routing config was created
* `last_update`: the date this routing config was last updated

## Projects

Projects are created from stacks and represent the unit that developers work on. They have an one-to-one relationship with routing configs - every project needs to have exactly one routing config associated with it.

Projects are the models that developers have

### Fields

* `stack`: the stack that this project relates to
* `server`: the stolos server this project was assigned
* `owner`: the user owning this project
* `created`: the date this project was created
* `last_update`: the date this project was last updated
