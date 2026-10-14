# MiniCore – Cálculo de Comisiones (Flask · MVC)

Tarea 4 – Ingeniería Web (UDLA). Réplica del ejercicio **MiniCore** de semestres pasados: calcular la comisión de cada vendedor según el total vendido en un **rango de fechas**.

- **Deploy:** https://minicore-comisiones.onrender.com  
- **Video explicativo:**  https://youtu.be/UVXOWVTdLwU?si=eeUV4TVshPiloC8Z

## ¿Qué hace?

1. El usuario elige **fecha inicio** y **fecha fin**.
2. Por cada vendedor se suman sus ventas dentro de ese rango.
3. Se busca la regla de comisión más alta cuyo monto mínimo se cumple.
4. **Comisión = total vendido × porcentaje de la regla.**
5. Se valida que la fecha fin no sea menor que la fecha inicio.

| Regla | Ventas desde | Comisión |
|-------|-------------:|---------:|
| Regla 1 | $500 | 6 % |
| Regla 2 | $600 | 8 % |
| Regla 3 | $800 | 10 % |
| Regla 4 | $1000 | 15 % |

Si el total no llega a $500, la comisión es $0.

**Ejemplo (agosto 2026):** Perico P vendió $300 + $1200 = $1500 → Regla 4 (15 %) → **$225**.

## Patrón MVC

```
minicore-comisiones/
├── app.py                      # Arranque: config, BD, registro del controlador
├── seed.py                     # Datos de prueba (vendedores, ventas, reglas)
├── models/                     # MODELO
│   ├── vendedor.py             #   tabla vendedores + ventas_entre(fi, ff)
│   ├── venta.py                #   tabla ventas
│   ├── regla.py                #   tabla reglas + Regla.para_monto(total)
│   └── reporte.py              #   lógica de negocio: calcular_comisiones()
├── controllers/                # CONTROLADOR
│   └── comision_controller.py  #   lee fechas, valida, llama al modelo, elige la vista
├── templates/                  # VISTA (Jinja2)
│   ├── base.html
│   └── index.html
├── static/css/style.css
├── tests/test_comisiones.py    # Pruebas con pytest
├── requirements.txt
└── render.yaml                 # Configuración de deploy en Render
```

- **Model:** entidades `Vendedor`, `Venta`, `Regla` (SQLAlchemy) y el cálculo de comisiones.
- **View:** plantillas HTML que solo muestran datos (formulario, tabla de resultados, reglas).
- **Controller:** ruta `GET /` que recibe `fecha_inicio` y `fecha_fin`, valida y envía el resultado a la vista.

## Ejecutar en local

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```

Abrir http://127.0.0.1:5000. La base SQLite (`minicore.db`) se crea y llena sola la primera vez.

Pruebas:

```bash
pip install pytest
python -m pytest -q
```

## Deploy en Render

1. Subir este proyecto a un repositorio público de GitHub.
2. En https://render.com → **New → Web Service** → conectar el repositorio.
3. Configuración:
   - Runtime: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance type: **Free**
4. **Deploy**. La app queda en `https://<nombre>.onrender.com`.

> En el plan gratuito, la primera carga tras un rato sin uso tarda unos 50 s (el servicio "despierta").

## Tecnologías

Python 3.12 · Flask 3 · Flask-SQLAlchemy · SQLite · Jinja2 · CSS3 · Gunicorn · Render
