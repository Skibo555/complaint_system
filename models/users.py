import sqlalchemy

from db import metadata
from models.enums import RoleType

user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("last_name", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(100), nullable=False, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("phone", sqlalchemy.String),
    sqlalchemy.Column("role", sqlalchemy.Enum(RoleType), server_default=RoleType.complainer.name, nullable=False),
    sqlalchemy.Column("iban", sqlalchemy.String(200), nullable=False)
)
