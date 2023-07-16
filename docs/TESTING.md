# Get Job Testing

## Table of Contents
...

## Unit Testing
The unit tests were written using Django's built-in testing framework based on Python's unittest module. The tests can be found in the `tests' directory of each app. To run the tests, use the following command: `python manage.py test`. To run the tests automatically I used CI/CD processes with GitHub Actions. The more detailed information about the CI/CD processes can be found in the **Deployment** section of the [README.md](https://github.com/FlashDrag/get-job/blob/master/README.md) file.

*Django Unit Tests GitHub Actions Workflow*
![Unit Tests](images/testing/unit-testing.png)

### Coverage
<!-- TODO Add screenshots of the coverage report -->


## Jigsaw CSS Validation
...

## JSHint
...

## Flake8 Validation
The Flake8 validation is used to check the Python code for PEP8 requirements. The validation is configured in the `production.yml` and `development.yml` files in the `.github/workflows` directory. The validation is run automatically with the CI/CD processes.

*Flake8 Validation GitHub Actions Workflow*
![Flake8 Validation](images/testing/flake8.png)

## Manual Testing
<!-- TODO -->

## User Stories Testing
<!-- TODO -->

## Bugs
<!-- TODO -->