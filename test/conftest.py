from pytest import fixture


def pytest_addoption(parser):
    parser.addoption(
        "--configfile",
        action="store"
    )


@fixture()
def configfile(request):
    return request.config.getoption("--configfile")
