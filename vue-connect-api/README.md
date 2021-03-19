# vue-connect-api

## Project setup

Install pipenv

```bash
$ pip install --user pipenv
```

Install all the required packages

```bash
$ pipenv install --dev
```

### Run the Tests

```bash
pipenv run pytest
```

### Run the backend (flask)

First start redis.

```bash
 docker run -p 6379:6379 redis
```

After that you can start the backend.

```bash
pipenv run python wsgi.py
```
