import sqlalchemy

from db import metadata
from models.enums import State

complaint = sqlalchemy.Table(
    "complaints",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(50), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("photo_url", sqlalchemy.String(250), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=sqlalchemy.text("timezone('UTC', now())"), nullable=True),
    sqlalchemy.Column("status", sqlalchemy.Enum(State), server_default=State.pending.name, nullable=False),
    sqlalchemy.Column("complainer_id", sqlalchemy.ForeignKey("users.id"), nullable=False)
)
