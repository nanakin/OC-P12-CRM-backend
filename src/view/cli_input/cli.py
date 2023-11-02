"""The main file of the command line interface module."""

import sys

import click

from .subcommands import cli_authentication, cli_contract, cli_customer, cli_employee, cli_event
from view.requests import FullRequest


@click.group()
def cli() -> None:
    """CRM application allows employees, customers, contracts and events management."""
    pass


def cli_main() -> FullRequest | None:
    """Deal with CLI.

    Returns understandable requests to the controller."""
    cli.add_command(cli_employee)
    cli.add_command(cli_customer)
    cli.add_command(cli_authentication)
    cli.add_command(cli_contract)
    cli.add_command(cli_event)
    try:
        # deal with command line using click module
        returned = cli(standalone_mode=False)

        # if returned == 0:  # when user asks --help
        #     return None
        # else:
        #     return returned
        if type(returned) is tuple:
            request, *param = returned
        else:
            # if the request has no parameter, give empty list as parameters
            request, param = returned, list()
        # transmit user request to the controller
        return request, param
    except click.ClickException as exc:
        exc.show()
        sys.exit(click.ClickException.exit_code)
    except click.exceptions.Abort:  # ctrl-c
        sys.exit(0)
