import os
import shutil
import sys

from invoke import task

WINDOWS = os.name == "nt"
openssl = '"C:\\Program Files\\Git\\usr\\bin\\openssl"' if WINDOWS else "openssl"


def inside_virtual(e, *commands):
    if WINDOWS:
        return " & ".join(
            [
                f"cd {e}",
                "call .venv\\Scripts\\activate",
                *commands,
                "call deactivate",
                "cd ..",
            ]
        )
    else:
        return " && ".join(
            [
                f"cd {e}/",
                "source ./.venv/bin/activate",
                *commands,
                "deactivate",
                "cd ..",
            ]
        )


@task
def certificate(c):
    s = f"{openssl} req -x509 -out localhost.crt -keyout localhost.key -newkey rsa:2048 -nodes -sha256  -subj '/CN=localhost' -extensions EXT -config config.txt"
    print(s)
    c.run(s)


@task
def clean(c, front=False, back=False, cli=False):
    everything = not (front or back or cli)
    for flag, folder in [(front, "front-end"), (back, "backend"), (cli, "cli-client")]:
        if flag or everything:
            try:
                shutil.rmtree(os.path.join(folder, ".venv"))
            except:
                pass


@task
def build(c, front=False, back=False, cli=False):
    everything = not (front or back or cli)
    for flag, folder in [(front, "front-end"), (back, "backend"), (cli, "cli-client")]:
        if flag or everything:
            try:
                c.run(f"{sys.executable} -m virtualenv {os.path.join(folder,'.venv')}")
                c.run(
                    inside_virtual(folder, "python -m pip install -r requirements.txt ")
                )
            except:
                pass


@task
def run(c, front=False, back=False):
    assert front or back
    d, port = (front and ("front-end", 8000)) or (back and ("backend", 8765))
    c.run(
        inside_virtual(
            d,
            f"python manage.py runsslserver {port} "
            + f"--certificate {os.path.join('..','localhost.crt')} "
            + f"--key {os.path.join('..','localhost.key')}",
        )
    )
