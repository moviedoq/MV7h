import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

REPORTS_DIR = "test_reports"
REPORT_PREFIX = "report"

def get_next_report_number():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    existing_files = [f for f in os.listdir(REPORTS_DIR) if f.startswith(REPORT_PREFIX) and f.endswith('.pdf')]
    existing_numbers = [int(f[len(REPORT_PREFIX):-4]) for f in existing_files if f[len(REPORT_PREFIX):-4].isdigit()]
    next_number = max(existing_numbers, default=0) + 1
    return next_number

def generate_pdf_report(report_content, report_number):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    filename = f"{REPORT_PREFIX}{report_number}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica", 14)
    c.drawString(50, height - 50, f"Test Report #{report_number}")
    c.setFont("Helvetica", 12)

    y_position = height - 100
    for line in report_content:
        c.drawString(50, y_position, line)
        y_position -= 20

        if y_position < 50:  # Salto de página automático
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 50

    c.save()
    print(f"✅ Report saved as: {filepath}")