# About the Rijks ICT-dashboard

The Rijks ICT Dashboard provides insight into central government’s large-scale ICT projects. It is developed with a focus on transparency and accessibility. The development team uses an open development approach and open source software, allowing anyone to follow along and contribute.
You can view the project’s progress and source code on GitHub. The dashboard is continuously evolving—new projects are added, and existing information is updated regularly.
The Rijks ICT Dashboard is being developed using open source software. The source code is openly available on GitHub. It can be viewed, downloaded, and reused. GitHub offers transparent version control, making it easy to collaborate and track changes during development.

## Motivation

The government carries out many large and complex ICT projects that are essential to public services and society. To ensure transparency, accountability, and public trust, it is important that everyone can see how these projects are progressing.
The Rijks ICT Dashboard makes information about these government ICT projects accessible to all: citizens, journalists, researchers, policymakers, and other stakeholders. It supports open government by providing insight into timelines, budgets, and project goals—so everyone can stay informed and involved.

### Open source software

Will you join us and add your thoughts? To contribute, create an account on GitHub (https://github.com/signup ) and read this readme and the code of conduct to get started.
Once signed-up, you can provide feedback on the code of this website, on the algorithm 'standard', on the published description or on the user-friendliness of the website, etc.
Get started: join us and add your thoughts!

# Technical information

In order to run the application locally, the following tooling is required:

- Docker ([installation instructions](https://docs.docker.com/get-docker/))
- Node.js. The version is specified in `frontend/.nvmrc`. It is recommended to use use [Node version manager](https://github.com/nvm-sh/nvm), the correct Node version can then be activated with with `nvm use`.
- Python. The version is specified in `backend/.python-version`. It is recommended to use [pyenv](https://github.com/pyenv/pyenv) to switch between Python versions, but this is not mandatory.
- Poetry. See the [docs](https://python-poetry.org/docs/#installation) for installation instructions.
- Make. This is a build automation tool. It is typically pre-installed on Linux and macOS. For Windows, you can install it via [Chocolatey](https://chocolatey.org/) or [Git for Windows](https://gitforwindows.org/).

The documentation below is tested on Ubuntu, but it should work on Windows as well.

### Environment variables

Environment variables are stored in `.env` in the `backend` folder, but because they can contain secrets (passwords), they are not included in the repository. Therefore, copy and paste `.env.dummy` to `.env` in the folder.

### Database

1. Start database. Run from `/backend` folder: `make init_db`.

Validate the database is running by navigating to the GUI (DBgate) on `http://localhost:8091/`. There you should be able to open the database `rid-data`.

### Running the app locally

### Backend

First, let's set up the dashboard backend. All commands below should be run from the `/backend` directory.

1. Specify Python version to use for virtual environment: `poetry env use <python_version>`. (The required Python version is specified in `backend/.python-version`.)
2. Install packages: `poetry install`.
3. Activate virtual environment: `poetry shell`.
4. Start backend: `make server`
   Validate the backend is running by navigating to the documentation on `http://localhost:8000/api-docs`.

### Frontend

1.  Install dependencies. Run from '`/frontend`: `npm install`.
2.  Start local server. Run from '`/frontend`: `npm run dev -- --port 5473`.

Validate the frontend is running by navigating to `http://localhost:5473`.

### Running the app in Docker

You can also run the complete project using Docker from the root directory. This is the easiest way to get everything up and running without installing all dependencies manually.

From the root of the project, run the following command to start all services: `make init_app`

Validate that the dashboard application is running by navigating to:
Backend: `http://localhost:8000/api-docs`
Frontend: `http://localhost:5473`
