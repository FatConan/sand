from sand.config import Site

import pytest

# set up some global useful constants and test data
def pytest_configure(config):
    pytest.test_data = {
        "site":  Site(".", {}),
        "source": "./source.file",
        "target": "./target.file",
    }
