import click

from crm.view.requests import FullRequest, Request


@click.group(name="contract")
def cli_contract():
    """Commands to manage contracts."""


@cli_contract.command(help="Add a new contract")
@click.option("--customer-id", prompt=True, prompt_required=True, type=int, help="Define the related customer")
@click.option("--total-amount", prompt=True, prompt_required=True, type=float, help="Define the total amount")
def add(**kwargs) -> FullRequest:
    """Command to add a new contract."""
    return FullRequest(Request.NEW_CONTRACT, **kwargs)


@cli_contract.command(help="Sign contract")
@click.option("--contract-uuid", prompt=True, prompt_required=True, type=click.UUID, help="Specify the contract")
def sign(**kwargs) -> FullRequest:
    """Command to sign a contract."""
    return FullRequest(Request.SIGN_CONTRACT, **kwargs)


@cli_contract.command(help="Add a new payment")
@click.option("--contract-uuid", prompt=True, prompt_required=True, type=click.UUID, help="Specify the contract")
@click.option("--payment", prompt=True, prompt_required=True, default=0, type=float, help="Specify the amount paid")
def add_payment(**kwargs) -> FullRequest:
    """Command to add a new payment to a contract."""
    return FullRequest(Request.ADD_CONTRACT_PAYMENT, **kwargs)


@cli_contract.command(help="Update contract amount")
@click.argument("contract-uuid", type=click.UUID)
@click.option(
    "--total-amount", default=None, prompt=True, prompt_required=False, type=float, help="Define the new total amount"
)
@click.option(
    "--customer-id", default=None, prompt=True, prompt_required=False, type=int, help="Define the new customer"
)
def update(**kwargs) -> FullRequest:
    """Command to update a contract data (customer and amount fields)."""
    if kwargs["customer_id"] is None and kwargs["total_amount"] is None:
        raise click.BadParameter("You must specify at least one field to update.")
    return FullRequest(Request.UPDATE_CONTRACT, **kwargs)


@cli_contract.command(help="Show contract details")
@click.option("--contract-uuid", prompt=True, prompt_required=True, type=click.UUID, help="Specify the contract")
def detail(**kwargs) -> FullRequest:
    """Command to show a contract details."""
    return FullRequest(Request.DETAIL_CONTRACT, **kwargs)


@cli_contract.command(help="List existing contracts", name="list")
@click.option("--not-signed-filter", is_flag=True, default=False, help="Display not signed contracts only")
@click.option("--not-paid-filter", is_flag=True, default=False, help="Display not paid contracts only")
def listing(**kwargs) -> FullRequest:
    """Command to list existing contracts."""
    return FullRequest(Request.LIST_CONTRACTS, **kwargs)
