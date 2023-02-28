from .base import metadata

from sqlalchemy import Table, Column, BigInteger,\
    String, Boolean, DateTime

t_users = Table(
    "users",
    metadata,
    Column('u_id',           BigInteger),  # telegram id
    Column('name',           String),  # фамилия c инициалами
    Column('name_tg',        String),  # имя пользователя в телеге если есть
    Column('admin',          Boolean),  # является ли администратором
    Column('org_name',       String),
    Column('org_code',       String),
    Column('date_update',    DateTime),
        )
