import nox


@nox.session(reuse_venv=True)
def lint(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-test.txt")
    session.install("pylint", "pylint_django")
    session.run("pylint", "common", "backend", "ev_charging_api")


@nox.session(reuse_venv=True)
def style(session):
    session.install("isort==5.7.0", "black==20.8b1")
    session.run("isort", "--check", "--diff", "--profile", "black", ".")
    session.run("black", "--check", "--diff", ".")


@nox.session()
def tests(session):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements-test.txt")
    session.run("pytest")
