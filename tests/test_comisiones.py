import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
os.environ["DATABASE_URL"] = "sqlite://"  # BD en memoria para pruebas

from app import create_app  # noqa: E402
from models.reporte import calcular_comisiones  # noqa: E402


def _por_vendedor(app, inicio, fin):
    with app.app_context():
        return {f.vendedor: f for f in calcular_comisiones(inicio, fin)}


def test_agosto():
    app = create_app()
    r = _por_vendedor(app, date(2026, 8, 1), date(2026, 8, 31))
    assert r["Perico P"].total_ventas == 1500 and r["Perico P"].comision == 225
    assert r["Zoila B"].total_ventas == 1000 and r["Zoila B"].comision == 150
    assert r["Aquiles C"].total_ventas == 900 and r["Aquiles C"].comision == 90
    assert r["Johny M"].total_ventas == 1000 and r["Johny M"].comision == 150


def test_septiembre_reglas_bajas_y_sin_comision():
    app = create_app()
    r = _por_vendedor(app, date(2026, 9, 1), date(2026, 9, 30))
    assert r["Perico P"].comision == 0 and r["Perico P"].regla == "Sin comisión"
    assert r["Aquiles C"].comision == 30      # 500 * 6 %
    assert r["Johny M"].comision == 56        # 700 * 8 %


def test_fecha_fin_menor_que_inicio():
    app = create_app()
    resp = app.test_client().get("/?fecha_inicio=2026-09-30&fecha_fin=2026-09-01")
    assert resp.status_code == 400
    assert "no puede ser menor" in resp.get_data(as_text=True)


def test_pagina_inicial():
    app = create_app()
    resp = app.test_client().get("/")
    assert resp.status_code == 200
    assert "Reglas de comisión" in resp.get_data(as_text=True)
