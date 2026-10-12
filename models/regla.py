from . import db


class Regla(db.Model):
    """Regla de comisión: si el total vendido alcanza `monto_minimo`,
    se aplica `porcentaje` sobre ese total."""

    __tablename__ = "reglas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    monto_minimo = db.Column(db.Float, nullable=False)
    porcentaje = db.Column(db.Float, nullable=False)  # 0.06 = 6 %

    @classmethod
    def para_monto(cls, total):
        """Busca la regla más alta cuyo monto mínimo se cumple.
        Devuelve None si el total no alcanza ninguna regla."""
        return (
            cls.query.filter(cls.monto_minimo <= total)
            .order_by(cls.monto_minimo.desc())
            .first()
        )

    def __repr__(self):
        return f"<Regla {self.nombre} >= {self.monto_minimo} -> {self.porcentaje:.0%}>"
