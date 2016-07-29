# Authentication

## Authentication methods and scopes

Authentication in Stolos needs to give access to the user to:

1. Managing user related resources through the API, like projects, stacks, etc
2. The Docker daemon for running containers
3. The filesystem

### Managing resources through the API

For managing resources through the API, the user should always supply a [JWT](https://jwt.io/) authentication token as header, in the following form: `Authorization: Bearer <token>`, except the login request where she should supply her username and password to get her token.

### Docker daemon

Docker daemon authentication is currently handled using TLS certificates. This means that the user should be supplied with the following files when logging in:

* ca.pem
* cert.pem
* key.pem

Using these files, the user can communicate with the Docker API on the Stolos server IP at port 2736.

### Filesystem

For syncing the filesystem using Unison, the user needs SSH access to the Stolos server. The user should be able to authenticate as user `stolos`, using a server-provided private key. The files needed for this are:

* id_rsa
* id_rsa.pub

## Authentication api

The authentication API features the following endpoints from the [ones provided by the djoser library](https://github.com/sunscrapers/djoser#endpoints):

* `/me/`
* `/login/`
* `/logout/`
* `/password/`
* `/password/reset/`
* `/password/reset/confirm/`
