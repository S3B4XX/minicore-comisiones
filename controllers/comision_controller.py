from datetime import date, datetime

from flask import Blueprint, render_template, request

from models import Regla
from models.reporte import calcular_comisiones

comision_bp = Blueprint("comisiones", __name__)


def _leer_fecha(valor):
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


@comision_bp.route("/", methods=["GET"])
def index():
    """Muestra el formulario y, si llegan fechas, el reporte de comisiones."""
    reglas = Regla.query.order_by(Regla.monto_minimo).all()
    inicio_txt = request.args.get("fecha_inicio", "")
    fin_txt = request.args.get("fecha_fin", "")

    # Primera visita: sin búsqueda todavía
    if not inicio_txt and not fin_txt:
        return render_template("index.html", reglas=reglas, filas=None,
                               fecha_inicio="", fecha_fin="", error=None)

    fecha_inicio = _leer_fecha(inicio_txt)
    fecha_fin = _leer_fecha(fin_txt)

    error = None
    if not fecha_inicio or not fecha_fin:
        error = "Ingresa una fecha de inicio y una fecha de fin válidas."
    elif fecha_fin < fecha_inicio:
        error = "La fecha de fin no puede ser menor que la fecha de inicio."

    if error:
        return render_template("index.html", reglas=reglas, filas=None,
                               fecha_inicio=inicio_txt, fecha_fin=fin_txt, error=error), 400

    filas = calcular_comisiones(fecha_inicio, fecha_fin)
    totales = {
        "ventas": round(sum(f.total_ventas for f in filas), 2),
        "comisiones": round(sum(f.comision for f in filas), 2),
    }
    return render_template("index.html", reglas=reglas, filas=filas, totales=totales,
                           fecha_inicio=inicio_txt, fecha_fin=fin_txt, error=None)


@comision_bp.app_context_processor
def inyectar_anio():
    return {"anio_actual": date.today().year}
