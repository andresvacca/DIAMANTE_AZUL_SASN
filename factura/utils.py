from decimal import Decimal
from .models import Factura, DetalleFactura

def generar_factura_automatica(usuario, cliente, tipo_movimiento, monto, id_empeno=None, articulo=None, descripcion=""):
    """
    Función universal para registrar cualquier movimiento financiero de Diamante Azul en la caja.
    """
    # 1. Crear la cabecera de la factura
    factura = Factura.objects.create(
        id_cliente=cliente,
        id_usuario=usuario,
        total_neto=Decimal(str(monto)),
        monto_pagado=Decimal(str(monto)),
        metodo_pago='Efectivo',  # Puedes dinamizarlo si pasas el método por parámetro
        tipo_movimiento=tipo_movimiento,
        id_empeno_asociado=id_empeno
    )
    
    # 2. Crear el detalle asociado
    DetalleFactura.objects.create(
        id_factura=factura,
        id_articulo=articulo, # Si viene un artículo (en venta o desembolso inicial)
        descripcion_servicio=descripcion if not articulo else f"Artículo: {articulo.nombre}",
        precio_venta=Decimal(str(monto))
    )
    
    return factura