from sand.config import Site

import pytest
import warnings


# set up some global useful constants and test data
def pytest_configure(config):
    #Hide warnings here, we'll be testing for outcomes
    warnings.filterwarnings("ignore")

    pytest.test_data = {
        "site":  Site(".", {}),
        "source": "./source.file",
        "target": "./target.file",
    }
