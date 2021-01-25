import nox


@nox.session(reuse_venv=True)
def lint(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-test.txt")
    session.install("pylint", "pylint_django")
    session.run("pylint", "common", "backend", "ev_charging_api")


@nox.session()
def tests(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-test.txt")
    session.run("pytest")
