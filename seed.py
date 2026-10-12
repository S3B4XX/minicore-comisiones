"""Datos de prueba del ejercicio MiniCore (se cargan solo si la BD está vacía)."""
from datetime import date

from models import db, Vendedor, Venta, Regla

VENDEDORES = ["Perico P", "Zoila B", "Aquiles C", "Johny M"]

# (fecha, índice de vendedor, monto)
VENTAS = [
    (date(2026, 7, 21), 0, 400.00),
    (date(2026, 7, 29), 1, 600.00),
    (date(2026, 8, 3), 1, 200.00),
    (date(2026, 8, 9), 0, 300.00),
    (date(2026, 8, 11), 2, 900.00),
    (date(2026, 8, 15), 3, 1000.00),
    (date(2026, 8, 20), 0, 1200.00),
    (date(2026, 8, 25), 1, 800.00),
    (date(2026, 9, 1), 2, 500.00),
    (date(2026, 9, 5), 3, 700.00),
    (date(2026, 9, 14), 0, 250.00),
    (date(2026, 9, 22), 1, 150.00),
    (date(2026, 10, 2), 2, 350.00),
    (date(2026, 10, 6), 3, 450.00),
]

# (nombre, monto mínimo, porcentaje)
REGLAS = [
    ("Regla 1", 500, 0.06),
    ("Regla 2", 600, 0.08),
    ("Regla 3", 800, 0.10),
    ("Regla 4", 1000, 0.15),
]


def cargar_datos():
    if Vendedor.query.first():
        return  # ya hay datos
    vendedores = [Vendedor(nombre=n) for n in VENDEDORES]
    db.session.add_all(vendedores)
    db.session.flush()
    db.session.add_all(
        Venta(fecha=f, vendedor_id=vendedores[i].id, monto=m) for f, i, m in VENTAS
    )
    db.session.add_all(
        Regla(nombre=n, monto_minimo=mm, porcentaje=p) for n, mm, p in REGLAS
    )
    db.session.commit()
