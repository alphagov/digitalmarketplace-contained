from invoke import task

from dmdevtools.invoke_tasks import (
    requirements_dev,
    virtualenv,
    freeze_requirements,
    test_flake8,
    test_mypy,
)
