import functools
import click
import inspect
import requests


options = {
    "format": click.option("--format", required=True, type=click.Choice(["json", "csv"])),
    "apikey": click.option("--apikey", required=True),
    "username": click.option("--username", required=True),
    "passw": click.option("--passw", required=True),
    "point": click.option("--point", required=True,type= click.UUID),
    "station": click.option("--station", required=True,type= click.UUID),
    "provider": click.option("--provider", required=True,type= click.UUID),
    "source": click.option("--source", required=True, type=click.File("r")),
    "ev": click.option("--ev", required=True,type= click.UUID),
    "datefrom": click.option("--datefrom", required=True,type= click.DateTime(["%Y%m%d"])),
    "dateto": click.option("--dateto", required=True,type= click.DateTime(["%Y%m%d"])),
    "users": click.option("--users", is_flag=True),
    "usermod": click.option("--usermod", is_flag=True),
    "sessionupd": click.option("--sessionupd", is_flag=True),
    "healthcheck": click.option("--healthcheck", is_flag=True),
    "resetsessions": click.option("--resetsessions", is_flag=True),
}

BASE_URL = "http://localhost:8765/evcharge/api"


def apply_options(f):
    for k in reversed(inspect.signature(f).parameters.keys()):
        f = options[k](f)
    return f


def show_data(response: requests.Response, *arg, **kwargs):
    if response.status_code == 200:
        click.echo(response.text)
    else:
        response.raise_for_status()


def store_token(response: requests.Response, *arg, **kwargs):
    if response.status_code == 200:
        with open("softeng20API.token", "w") as f:
            f.write(response.json()["token"])
    else:
        response.raise_for_status()


def convert_to_request(f):
    @functools.wraps(f)
    def function(**kw):
        method, url, parameters, hook = f(**kw)
        return method(f"{BASE_URL}/{url}", hooks=dict(response=hook), timeout=2, **parameters)
    return function


def convert_to_command(target):
    def inner(f):
        f = convert_to_request(f)
        f = apply_options(f)
        return target.command(f.__name__)(f)  
    return inner


interface = click.Group()


@convert_to_command(interface)
def healthcheck():
    return requests.get, "healthcheck", {}, show_data


# Data endpoints

@convert_to_command(interface)
def SessionsPerEv(ev, datefrom, dateto, format,apikey):
    return (
        requests.get, f"SessionsPerEv/{ev}/{datefrom:%Y%m%d}/{dateto:%Y%m%d}", 
        {"params": dict(format=format)}, show_data
    )

@convert_to_command(interface)
def SessionsPerStation(station, datefrom, dateto, format,apikey):
    return (
        requests.get, f"SessionsPerStation/{station}/{datefrom:%Y%m%d}/{dateto:%Y%m%d}", 
        {"params": dict(format=format)}, show_data
    )

@convert_to_command(interface)
def SessionsPerPoint(point, datefrom, dateto, format,apikey):
    return (
        requests.get, f"SessionsPerPoint/{point}/{datefrom:%Y%m%d}/{dateto:%Y%m%d}", 
        {"params": dict(format=format)}, show_data
    )

@convert_to_command(interface)
def SessionsPerProvider(provider, datefrom, dateto, format,apikey):
    print(provider,datefrom,dateto,format,apikey)
    return (
        requests.get, f"SessionsPerProvider/{provider}/{datefrom:%Y%m%d}/{dateto:%Y%m%d}", 
        {"params": dict(format=format)}, show_data
    )



if __name__ == "__main__":
    interface()
