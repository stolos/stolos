# stolos

stolod contains the API and the watcher logic for Stolos.

## API

The API contains the Authentication mechanism of Stolos, as well as the needed API endpoints for managing projects.

### Prerequisites

Before creating Users and Stacks for Stolos, the following things need to happen in the Admin:

1. A Company account should be created in the form of a Group
2. The Group should be given rights to:
  - view, add and delete Projects
  - view Stacks
  - view, add and delete public keys
3. Every user created should be added to it's company's group

### Documentation

* [Authentication docs](docs/authentication.md)
* [Models docs](docs/models.md)

## stolos-watchd
Watch Docker daemon for events and update [ceryx](https://github.com/sourcelair/ceryx) accordingly

### Data structure

`stolos-watchd` understands projects and services in the same way that Docker Compose understands them. On top of that, it also understands domain names and configuration options for domain name/project mappings. A typical mapping can be found below:

```json
{
  "project-name": {
    "domain": "domain.name",
    "config": {
      "use-subdomains": true
    }
  }
}
```

### Logic

`stolos-watchd` watches the given Docker engine for events and reacts to the following ones:
* `start` - when a container starts, its service is exposed
* `die` - when a container dies, its service route is removed

#### Exposing services

Services are exposed in the following way:
* domain name is `domain.name` and has the `use-subdomains` flag `true`
  * web service is exposed at `domain.name`
  * all services (including the web service) are exposed to `<service-name>.domain.name`
* domain name is `sub.domain.name` and has the `use-subdomains` flag `false`
  * web service is exposed at `sub.domain.name`
  * all services (including the web service) are exposed to `sub-<service-name>.domain.name`

##### Examples

If domain is `project.apps.lair.io` and has `web` and `api` services with the `use-subdomains` flag `true`, then the following domains will be exposed:
* `project.apps.lair.io` will point to `web`
* `web.project.apps.lair.io` will point to `web`
* `api.project.apps.lair.io` will point to `api`

If domain is `project.apps.lair.io` and has `web` and `api` services with the `use-subdomains` flag `false`, then the following domains will be exposed:
* `project.apps.lair.io` will point to `web`
* `project-web.apps.lair.io` will point to `web`
* `project-api.apps.lair.io` will point to `api`
