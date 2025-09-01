from sand.config import Site

import pytest

# set up some global useful constants and test data
def pytest_configure(config):
    pytest.test_data = {
        "SITE":  Site(".", {}),
        "SOURCE": "./source.file",
        "TARGET": "./target.file",
    }
