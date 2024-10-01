import asyncclick as click
from db import database
from managers.user import UserManager
from models import RoleType


@click.command()
@click.option("-f", "--first_name", type=str, required=True)
@click.option("-l", "--last_name", type=str, required=True)
@click.option("-p", "--password", type=str, required=True)
@click.option("-i", "--iban", type=str, required=True)
@click.option("-ph", "--phone", type=str, required=True)
@click.option("-e", "--email", type=str, required=True)
async def create_admin(first_name, last_name, password, iban, phone, email):
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "iban": iban,
        "phone": phone,
        "email": email,
        "role": RoleType.admin
    }

    await database.connect()
    await UserManager.register_user(payload)
    await database.disconnect()


if __name__ == "__main__":
    create_admin(_anyio_backend="asyncio")
