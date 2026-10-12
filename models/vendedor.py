from . import db


class Vendedor(db.Model):
    """Persona que realiza ventas y recibe comisión."""

    __tablename__ = "vendedores"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    ventas = db.relationship("Venta", back_populates="vendedor", lazy=True)

    def ventas_entre(self, fecha_inicio, fecha_fin):
        """Devuelve las ventas del vendedor dentro del rango (ambas fechas incluidas)."""
        from .venta import Venta

        return (
            Venta.query.filter(
                Venta.vendedor_id == self.id,
                Venta.fecha >= fecha_inicio,
                Venta.fecha <= fecha_fin,
            )
            .order_by(Venta.fecha)
            .all()
        )

    def __repr__(self):
        return f"<Vendedor {self.nombre}>"
