from .base import metadata

from sqlalchemy import Table, Column, BigInteger,\
    String, DateTime, Integer

t_journal = Table(
    "journal",
    metadata,
    Column('j_id', Integer, primary_key=True),
    Column('u_id',   BigInteger),  # telegram id
    Column('date',   DateTime),
    Column('task',   String),
        )
