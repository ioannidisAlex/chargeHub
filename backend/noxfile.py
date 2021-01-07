import nox

@nox.session(reuse_venv=True)
def lint(session):
	session.install("-r","requirements.txt")
	session.install("pylint","pylint_django")
	session.run("pylint","common")
