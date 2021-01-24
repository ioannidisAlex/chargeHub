import nox


@nox.session(reuse_venv=True)
def pylint(session):
    session.install("-r", "requirements.txt")
    session.install("pylint")
    session.run("pylint", "evcharge87.py")

@nox.session(reuse_venv=True)
def flake8(session):
    session.install("flake8")
    session.run("flake8","evcharge87.py","--ignore","E501")
    
    
@nox.session(reuse_venv=True)
def style(session):
    session.install("isort","black","flake8")
    session.run("isort","--check","--diff","--profile","black", "evcharge87.py")
    session.run("black","--check","--diff","evcharge87.py")
    