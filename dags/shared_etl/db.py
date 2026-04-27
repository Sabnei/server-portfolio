"""
dags/shared_etl/db.py

Módulo central de conexión a la base de datos.
Todos los proyectos importan get_engine() desde aquí.

Uso en cualquier proyecto:
    from shared_etl.db import get_engine, ensure_schema
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def get_engine():
    """
    Crea un SQLAlchemy engine con las variables del .env.

    Variables requeridas (inyectadas por Docker via env_file):
        DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

    Returns:
        sqlalchemy.engine.Engine

    Raises:
        RuntimeError si falta alguna variable o falla la conexión
    """
    try:
        host     = os.environ["DB_HOST"]
        port     = os.environ.get("DB_PORT", "5432")
        user     = os.environ["DB_USER"]
        password = os.environ["DB_PASSWORD"]
        dbname   = os.environ["DB_NAME"]
    except KeyError as e:
        raise RuntimeError(f"Variable de entorno faltante: {e}")

    conn_str = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

    try:
        return create_engine(conn_str, pool_pre_ping=True)
    except SQLAlchemyError as e:
        raise RuntimeError(f"Error creando engine: {e}")


def ensure_schema(engine, schema: str) -> None:
    """
    Crea el schema si no existe. Seguro de llamar en cada run.

    Args:
        engine: SQLAlchemy engine
        schema: nombre del schema (ej: "crypto")
    """
    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
