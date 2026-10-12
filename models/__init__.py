"""Capa MODELO: definición de las entidades y acceso a datos."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .vendedor import Vendedor  # noqa: E402
from .venta import Venta  # noqa: E402
from .regla import Regla  # noqa: E402

__all__ = ["db", "Vendedor", "Venta", "Regla"]
