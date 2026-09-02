"""Certificate PDF generation (next-steps item #2 from handover.md).

Kept separate from views.py since it's a chunk of layout/drawing code
rather than request handling.
"""
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def generate_certificate_pdf(certificate):
    """Return the certificate as PDF bytes (in-memory, nothing written to disk)."""
    enrollment = certificate.enrollment
    trainee = enrollment.trainee
    course = enrollment.course

    buffer = io.BytesIO()
    page_size = landscape(A4)
    width, height = page_size
    c = canvas.Canvas(buffer, pagesize=page_size)

    # Border
    c.setStrokeColor(colors.HexColor("#1e3a8a"))
    c.setLineWidth(3)
    c.rect(15 * mm, 15 * mm, width - 30 * mm, height - 30 * mm)
    c.setLineWidth(0.75)
    c.rect(19 * mm, 19 * mm, width - 38 * mm, height - 38 * mm)

    # Header
    c.setFillColor(colors.HexColor("#1e3a8a"))
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, height - 35 * mm, "INDIA METEOROLOGICAL DEPARTMENT")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 42 * mm, "Ministry of Earth Sciences, Government of India")

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.drawCentredString(width / 2, height - 60 * mm, "Certificate of Completion")

    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawCentredString(width / 2, height - 75 * mm, "This is to certify that")

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.HexColor("#1e3a8a"))
    c.drawCentredString(width / 2, height - 88 * mm, trainee.full_name)

    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawCentredString(width / 2, height - 100 * mm, "has successfully completed the course")

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#0f172a"))
    c.drawCentredString(width / 2, height - 112 * mm, course.title)

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#64748b"))
    issued_date = certificate.issued_at.strftime("%d %B %Y")
    c.drawCentredString(width / 2, height - 122 * mm, f"Subject: {course.subject.name}  |  Issued: {issued_date}")

    # Footer: certificate number + verification note
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.drawCentredString(
        width / 2, 25 * mm,
        f"Certificate No. {certificate.certificate_number}  --  verify at /certificates/verify/{certificate.certificate_number}/",
    )

    trainer = course.trainer
    if trainer:
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.HexColor("#334155"))
        c.drawString(30 * mm, 32 * mm, "_" * 28)
        c.drawString(30 * mm, 27 * mm, trainer.full_name)
        c.setFont("Helvetica", 8)
        c.setFillColor(colors.HexColor("#64748b"))
        c.drawString(30 * mm, 23 * mm, "Trainer")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
