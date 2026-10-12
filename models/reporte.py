"""Lógica de negocio del MiniCore: cálculo de comisiones por rango de fechas."""
from dataclasses import dataclass, field

from .vendedor import Vendedor
from .regla import Regla


@dataclass
class FilaComision:
    vendedor: str
    ventas: list = field(default_factory=list)
    total_ventas: float = 0.0
    regla: str = "Sin comisión"
    porcentaje: float = 0.0
    comision: float = 0.0


def calcular_comisiones(fecha_inicio, fecha_fin):
    """Para cada vendedor:
    1. Suma sus ventas dentro del rango de fechas.
    2. Busca la regla que corresponde a ese total.
    3. Comisión = total * porcentaje de la regla.
    """
    filas = []
    for vendedor in Vendedor.query.order_by(Vendedor.nombre).all():
        ventas = vendedor.ventas_entre(fecha_inicio, fecha_fin)
        total = round(sum(v.monto for v in ventas), 2)
        regla = Regla.para_monto(total) if total > 0 else None

        fila = FilaComision(vendedor=vendedor.nombre, ventas=ventas, total_ventas=total)
        if regla:
            fila.regla = regla.nombre
            fila.porcentaje = regla.porcentaje
            fila.comision = round(total * regla.porcentaje, 2)
        filas.append(fila)
    return filas
