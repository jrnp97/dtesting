## Dependencies

* [pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv)

## Installation

1. `pipenv install`
2. `pipenv shell`
3. `cd dtesting`
4. `cp .env.local_example .env`
5. `python manage.py migrate`
6. `python manage.py test`