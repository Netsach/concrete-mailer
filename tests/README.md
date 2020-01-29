# Code Quality

## Running the test suite

### Configure the environment

```shell
python3 -m venv env
source env/bin/activate
pip install .
pip install -r tests/requirements.txt
```

### Run the tests

Invoke Pytest with the following args:

```shell
pytest -s concrete_mailer --pyargs -q tests --cov --cov-report html --cov-report term --cov-config tests/.coveragerc
```

You can decide to deactivate coverage

```shell
pytest -s concrete_mailer --pyargs -q tests
```

You can also decide of which test file(s) you want to run by adding the filename(s) in the command:

```shell
pytest -s concrete_mailer --pyargs -q tests -k 'test_imports or test_prepare_email'
```
