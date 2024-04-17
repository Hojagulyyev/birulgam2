# PCA: Python Clean Architecture.

## Prerequisites
- python3.12
- postgres
- fastapi
- sqlalchemy
- alembic
- redis
- poetry
- strawberry

## Installation

Note: Use the dev branch for installation and contributing.

```
git clone https://github.com/Hojagulyyev/python-clean-architecture.git
cd python-clean-architecture
cp .env.example .env
vim .env
```
and setup the .env

## Run Server

To run cli server:
```
python infrastructure/cli/main.py
```

To run http server:
```
python infrastructure/cli/main.py
```
then you can see the below http server api docs:
 - [REST API DOCS](http://localhost:8000/api/v0/docs) on OpenAPI
 - [GRAPHQL API DOCS](http://localhost:8000/api/graphql) on Strawberry

 api docs credentials:
 - username: username
 - password: password

Note: Use headers `{"access-token": "Bearer xxx"}` to use GQL queries.
