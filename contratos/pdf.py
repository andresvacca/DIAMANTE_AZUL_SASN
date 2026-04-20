from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from io import BytesIO
import datetime


def generar_pdf_contrato(contrato):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # ── Encabezado ─────────────────────────────────────────────────────────────
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2*cm, height - 2*cm, "COMPRAVENTA DIAMANTE AZUL MV")
    c.setFont("Helvetica", 9)
    c.drawString(2*cm, height - 2.6*cm, "Nit 1030621484-6")
    c.drawString(2*cm, height - 3.1*cm, "CLL 56F SUR # 91D 21, Bosa Villa Alegría")
    c.drawString(2*cm, height - 3.6*cm, "E-mail: diamanteazulmv@gmail.com  Bogotá, D.C.")

    # Teléfono grande a la derecha
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(colors.HexColor("#1a5276"))
    c.drawRightString(width - 2*cm, height - 3.2*cm, "317 573 8074")
    c.setFillColor(colors.black)

    # Ciudad y Fecha
    c.setFont("Helvetica", 9)
    fecha = contrato.fecha_contrato.strftime("%d/%m/%Y") if contrato.fecha_contrato else "___________"
    c.drawString(10*cm, height - 4.4*cm, f"Ciudad: Bogotá D.C.")
    c.drawString(15*cm, height - 4.4*cm, f"Fecha: {fecha}")

    # Línea separadora
    c.setLineWidth(1)
    c.line(2*cm, height - 4.8*cm, width - 2*cm, height - 4.8*cm)

    # ── Título ──────────────────────────────────────────────────────────────────
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, height - 5.4*cm, "CONTRATO DE COMPRAVENTA CON PACTO DE RETROVENTA")
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(width/2, height - 5.9*cm, "CONTRATO QUE SE RIGE POR LAS SIGUIENTES CLAUSULAS:")

    # ── Datos del cliente (VENDEDOR) ────────────────────────────────────────────
    cliente = contrato.id_cliente
    articulo = contrato.id_articulo
    empeno = contrato.id_empeno

    nombre_cliente = cliente.nombre if cliente else "___________________________"
    doc_cliente    = cliente.documento_id if cliente else "_______________"
    tel_cliente    = cliente.telefono if cliente else "_______________"
    dir_cliente    = cliente.direccion if cliente else "_______________"

    y = height - 6.6*cm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(2*cm, y, "1. PARTES: Entre los suscritos:")
    c.setFont("Helvetica", 9)
    c.drawString(8.2*cm, y, f"{nombre_cliente}, mayor, identificado(a) con C.C. y/o Pasaporte No. {doc_cliente},")

    y -= 0.5*cm
    c.drawString(2*cm, y, f"expedida en Bogotá D.C., con domicilio en {dir_cliente}, teléfono {tel_cliente},")

    y -= 0.5*cm
    c.drawString(2*cm, y, "quien obra en nombre propio y para efectos del presente contrato será EL VENDEDOR de una parte;")

    y -= 0.5*cm
    c.drawString(2*cm, y, "y por la otra COMPRAVENTA DIAMANTE AZUL MV, identificado(a) con C.C. No. 1030621484-6,")

    y -= 0.5*cm
    c.drawString(2*cm, y, "obrando en nombre y representación de la COMPRAVENTA y quien para los efectos del presente")

    y -= 0.5*cm
    c.drawString(2*cm, y, "contrato se denominará EL COMPRADOR, manifestamos que hemos celebrado un contrato de")

    y -= 0.5*cm
    c.drawString(2*cm, y, "COMPRAVENTA sobre el (los) siguiente(s) bien(es):")

    # ── Artículo ────────────────────────────────────────────────────────────────
    y -= 0.7*cm
    nombre_articulo  = articulo.nombre if articulo else "___________________________"
    desc_articulo    = articulo.descripcion if articulo else ""
    quilataje        = f"{articulo.quilataje}k" if articulo and articulo.quilataje else "N/A"

    c.setFont("Helvetica-Bold", 9)
    c.drawString(2*cm, y, "2.")
    c.setFont("Helvetica", 9)
    c.drawString(2.8*cm, y, f"{nombre_articulo} - {desc_articulo}")
    y -= 0.5*cm
    c.drawString(2*cm, y, f"GRAMOS/QUILATAJE: {quilataje}")

    # ── Precio ──────────────────────────────────────────────────────────────────
    y -= 0.7*cm
    monto   = f"${empeno.monto_prestado:,.0f}" if empeno else "$_______________"
    retro   = f"${empeno.monto_prestado + (empeno.monto_prestado * empeno.tasa_interes / 100):,.0f}" if empeno else "$_______________"
    plazo   = "1"
    vence   = empeno.fecha_vencimiento.strftime("%d/%m/%Y") if empeno and empeno.fecha_vencimiento else "___________"

    c.setFont("Helvetica-Bold", 9)
    c.drawString(2*cm, y, f"3. EL PRECIO DE LA COMPRAVENTA ES LA SUMA DE: {monto}")

    # ── Cláusulas ───────────────────────────────────────────────────────────────
    y -= 0.8*cm
    clausulas = [
        "4. TRADICION: EL VENDEDOR transfiere al COMPRADOR a título DE COMPRAVENTA el derecho de dominio",
        "y posesión que tiene y ejerce sobre el(los) anterior(es) artículo(s) y declara que el(los) bien(es)",
        "que transfiere lo(s) adquirió lícitamente, no fue su importador, es(son) de su exclusiva propiedad",
        "y posesión, lo(s) posee de manera regular, pública y pacíficamente, está(n) libres de gravámenes,",
        "limitaciones al dominio, pleitos pendientes, embargos, con la obligación de salir al saneamiento en casos de ley.",
        "",
        "5. EXIMENTE DE RESPONSABILIDAD: Las partes convenimos, en caso de deterioro o pérdida de o los",
        "artículos arriba descritos, ocasionado por fuerza mayor o caso fortuito, EL COMPRADOR queda exento",
        "de toda responsabilidad.",
    ]
    c.setFont("Helvetica", 8.5)
    for linea in clausulas:
        c.drawString(2*cm, y, linea)
        y -= 0.45*cm

    # ── Cláusula accesoria ──────────────────────────────────────────────────────
    y -= 0.3*cm
    c.setLineWidth(0.5)
    c.line(2*cm, y + 0.2*cm, width - 2*cm, y + 0.2*cm)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(width/2, y - 0.2*cm, "CLAUSULA ACCESORIA DEL PACTO DE RETROVENTA, ASI:")
    y -= 0.7*cm

    accesoria = [
        f"PRIMERO: Conforme al Artículo 1939 del C. C. Colombiano, pactamos que EL VENDEDOR se reserva",
        f"la facultad de RECOMPRAR el(los) bien(s) vendido(s) pagando al COMPRADOR como PRECIO DE",
        f"RETROVENTA la suma de {retro}.",
        f"SEGUNDO: PLAZO. Acordamos que la facultad de RETROVENTA la podrá ejercer EL VENDEDOR dentro",
        f"del término de {plazo} mes(es) a partir de la firma del presente contrato y vence {vence}.",
        "TERCERO: PROHIBICIÓN DE CESION. El derecho que nace del PACTO DE RETROVENTA del presente",
        "contrato, no podrá cederse a ningún título, y en caso de pérdida de este contrato, EL VENDEDOR",
        "se obliga a dar noticia inmediata al COMPRADOR.",
        "CUARTO: EL VENDEDOR deberá dar noticia anticipada de la RETROVENTA para prever la logística.",
        "QUINTO: MARCO LEGAL DE LA PROTECCION DE DATOS PERSONALES: Ley 1581/12, Decreto 1377/13.",
        "SEXTO: ANEXOS. Fotocopia del documento de identidad; factura y/o Constancia de Propiedad; RUT.",
    ]
    c.setFont("Helvetica", 8.5)
    for linea in accesoria:
        if y < 5*cm:
            c.showPage()
            y = height - 2*cm
        c.drawString(2*cm, y, linea)
        y -= 0.45*cm

    # ── Firmas ──────────────────────────────────────────────────────────────────
    y -= 0.5*cm
    c.setFont("Helvetica", 9)
    c.drawString(2*cm, y, "TANTO VENDEDOR COMO COMPRADOR HEMOS LEIDO, COMPRENDIDO y ACEPTADO EL TEXTO DE ESTE CONTRATO.")

    y -= 1*cm
    c.line(2*cm,       y, 8*cm,        y)
    c.line(12*cm,      y, width - 2*cm, y)

    y -= 0.4*cm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(2*cm,  y, "EL VENDEDOR")
    c.drawString(12*cm, y, "COMPRADOR: COMPRAVENTA DIAMANTE AZUL MV")

    y -= 0.4*cm
    c.setFont("Helvetica", 9)
    c.drawString(2*cm,  y, f"C.C. Nº {doc_cliente}")
    c.drawString(12*cm, y, "C.C. Nº: 1030621484-6")

    # ── Resolución de contrato ──────────────────────────────────────────────────
    y -= 1.2*cm
    c.setLineWidth(1)
    c.line(2*cm, y, width - 2*cm, y)
    y -= 0.5*cm
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width/2, y, "RESOLUCION DE CONTRATO")

    y -= 0.6*cm
    c.setFont("Helvetica", 8.5)
    resolucion = [
        f"EL VENDEDOR hace uso de la facultad de recompra mencionada en la Segunda Cláusula Accesoria",
        f"de este Contrato, pagando la suma convenida de {retro}, recibiendo el bien objeto del presente",
        "contrato en las mismas condiciones que lo contrató, y qué al suscribir esta RETROVENTA deja",
        "constancia de su total satisfacción.",
    ]
    for linea in resolucion:
        c.drawString(2*cm, y, linea)
        y -= 0.45*cm

    y -= 0.8*cm
    c.line(2*cm, y, 8*cm, y)
    y -= 0.4*cm
    c.drawString(2*cm, y, "HUELLA:")
    c.drawString(6*cm, y, f"C.C. Nº {doc_cliente}")

    c.save()
    buffer.seek(0)
    return buffer
