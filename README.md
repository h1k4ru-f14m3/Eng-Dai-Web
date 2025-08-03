# English to Dai Dictionary (Web)
This project is a dictionary app to check words from English in Dai. It is currently a web app and there is no official site yet. It can be run locally to use it, though I am planning to package this into an application later.

## Installation
There are mainly 2 ways to install this on your local machine.

### Installation via Docker (Recommended)
Docker is the preferred method for running this web app locally, as it ensures a consistent environment between development and deployment.

- Install [Docker](https://docs.docker.com/get-started/get-docker/)
- Open your terminal and run the following to download the image/package:
```bash
docker pull h1k4ruf14m3/eng-dai-dictionary
```
- Then, run the following to run the program and go to the given website to use this web app:
```bash
docker run h1k4ruf14m3/eng-dai-dictionary
```

*Note: Changes to the database in the Docker container may not be saved after it stops.*

### Installation via source code
