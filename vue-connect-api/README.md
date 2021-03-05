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

```bash
pipenv run python wsgi.py
```

### Run the scheduler (APScheduler)

```bash
pipenv run python scheduler.py
```
