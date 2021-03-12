import functools
import inspect
import os

import click
import click_spinner
import requests
from click_didyoumean import DYMGroup
from click_option_group import AllOptionGroup, optgroup

options = {
    "format": click.option(
        "--format", required=True, type=click.Choice(["json", "csv"])
    ),
    "apikey": click.option("--apikey", required=True),
    "username": click.option("--username", required=True),
    "passw": click.option("--passw", required=True),
    "point": click.option("--point", required=True, type=click.UUID),
    "station": click.option("--station", required=True, type=click.UUID),
    "provider": click.option("--provider", required=True, type=click.UUID),
    "source": click.option("--source", required=True, type=click.File("r")),
    "ev": click.option("--ev", required=True, type=click.UUID),
    "datefrom": click.option(
        "--datefrom", required=True, type=click.DateTime(["%Y%m%d"])
    ),
    "dateto": click.option("--dateto", required=True, type=click.DateTime(["%Y%m%d"])),
    "users": click.option("--users"),
    "usermod": click.option("--usermod", is_flag=True),
    "sessionsupd": click.option("--sessionsupd", is_flag=True),
    "healthcheck": click.option("--healthcheck", is_flag=True),
    "resetsessions": click.option("--resetsessions", is_flag=True),
}

BASE_URL = "http://localhost:8765/evcharge/api"
AUTHENTICATION_HEADER = "X-OBSERVATORY-AUTH"
# AUTHENTICATION_HEADER = "Authorization"


def convert_to_request(f):
    @functools.wraps(f)
    def function(**kw):
        method, url, parameters, hook = f(**kw)
        if "apikey" in kw:
            headers = {AUTHENTICATION_HEADER: "Token %s" % kw["apikey"]}
        else:
            headers = {}

        with click_spinner.spinner():
            response = method(
                f"{BASE_URL}/{url}",
                hooks=dict(response=hook),
                timeout=2,
                headers=headers,
                **parameters,
            )
        return response

    return function


def apply_options(f):
    for k in reversed(inspect.signature(f).parameters.keys()):
        f = options[k](f)
    return f


def convert_to_command(target, name=None):
    def inner(f):
        f = convert_to_request(f)
        f = apply_options(f)
        return target.command(name or f.__name__)(f)

    return inner


def load_to_admin(*args, target):
    def f(ctx, **kwargs):
        sub = [x for x in args if kwargs.get(x.name)]
        if len(sub) != 1:
            click.echo(ctx.get_help())

            ctx.abort()
        ctx.invoke(sub[0], **{k: v for k, v in kwargs.items() if v})

    x = click.pass_context(f)
    x = options["apikey"](x)
    for arg in args:
        for p in arg.params:
            if p.human_readable_name == "apikey":
                continue
            o = optgroup.option(
                "--" + p.human_readable_name, type=p.type, is_flag=p.is_flag
            )
            x = o(x)

        x = optgroup.group(f"{arg}", cls=AllOptionGroup)(x)

    return target.command("Admin")(x)


@click.group(cls=DYMGroup)
def interface():
    pass


# Data endpoints


def show_data(response: requests.Response, *arg, **kwargs):
    if response.status_code == 200:
        click.echo(response.text)
    else:
        response.raise_for_status()


@convert_to_command(interface)
def SessionsPerEv(ev, datefrom, dateto, format, apikey):
    return (
        requests.get,
        f"SessionsPerEv/{ev}/{datefrom:%Y%m%d}/{dateto:%Y%m%d}",
        {"params": dict(format=format)},
        show_data,
    )


@convert_to_command(interface)
def SessionsPerStation(station, datefrom, dateto, format, apikey):
    return (
        requests.get,
        f"SessionsPerStation/{station}/{datefrom:%Y%m%d}/{dateto:%Y%m%d}",
        {"params": dict(format=format)},
        show_data,
    )


@convert_to_command(interface)
def SessionsPerPoint(point, datefrom, dateto, format, apikey):
    return (
        requests.get,
        f"SessionsPerPoint/{point}/{datefrom:%Y%m%d}/{dateto:%Y%m%d}",
        {"params": dict(format=format)},
        show_data,
    )


@convert_to_command(interface)
def SessionsPerProvider(provider, datefrom, dateto, format, apikey):
    return (
        requests.get,
        f"SessionsPerProvider/{provider}/{datefrom:%Y%m%d}/{dateto:%Y%m%d}",
        {"params": dict(format=format)},
        show_data,
    )


# authentication point


def store_token(response: requests.Response, *arg, **kwargs):
    if response.status_code == 200:
        with open("softeng20API.token", "w") as f:
            f.write(response.json()["token"])
    else:
        response.raise_for_status()


@convert_to_command(interface)
def login(username, passw):
    return (
        requests.post,
        "login/",
        dict(data=dict(username=username, password=passw)),
        store_token,
    )


def remove_token(response: requests.Response, *arg, **kwargs):
    if response.status_code == 200:
        if os.path.exists("softeng20API.token"):
            os.remove("softeng20API.token")
        else:
            click.echo("Token file not found")
    else:
        response.raise_for_status()


@convert_to_command(interface)
def logout(username, passw):
    return requests.post, "logout", {}, remove_token


# administrative endpoints


@convert_to_command(click)
def usermod(usermod, username, passw, apikey):
    return requests.post, f"admin/usermod/{username}/{passw}", {}, show_data


@convert_to_command(click)
def users(users, apikey):
    return requests.post, f"admin/users/{users}", {}, show_data


@convert_to_command(click)
def sessionsupd(sessionsupd, source, apikey):
    return requests.post, "admin/system/sessionsupd", {}, show_data


@convert_to_command(click)
def healthcheck(healthcheck, apikey):
    return requests.get, "admin/healthcheck", {}, show_data


@convert_to_command(click)
def resetsessions(resetsessions, apikey):
    return requests.post, "admin/resetsessions/", {}, show_data


admin = load_to_admin(
    users, sessionsupd, resetsessions, healthcheck, usermod, target=interface
)


if __name__ == "__main__":
    interface()
