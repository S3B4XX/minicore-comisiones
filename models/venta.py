from . import db


class Venta(db.Model):
    """Una venta registrada por un vendedor en una fecha."""

    __tablename__ = "ventas"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False, index=True)
    monto = db.Column(db.Float, nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey("vendedores.id"), nullable=False)

    vendedor = db.relationship("Vendedor", back_populates="ventas")

    def __repr__(self):
        return f"<Venta {self.fecha} ${self.monto}>"
