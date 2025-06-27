from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph,
                                Spacer)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"
REPORT_DIR.mkdir(exist_ok=True)          # crea carpeta si no existe
XML_FILE = Path("results.xml")           # generado por pytest

def next_number() -> int:
    """Devuelve el próximo número secuencial (1-based, 4 dígitos con ceros)."""
    existing = sorted(int(p.stem) for p in REPORT_DIR.glob("*.pdf") if p.stem.isdigit())
    return (existing[-1] + 1) if existing else 1

def parse_xml(xml_path: Path):
    """Devuelve filas [[test, estado, tiempo]] a partir del JUnit XML."""
    root = ET.parse(xml_path).getroot()
    rows = [["Test", "Estado", "Tiempo (s)"]]
    for tc in root.iter("testcase"):
        name  = tc.attrib["name"]
        time  = tc.attrib.get("time", "0")
        state = "PASÓ" if not list(tc) else "FALLÓ"
        rows.append([name, state, time])
    return rows

def build_pdf(rows, seq):
    styles = getSampleStyleSheet()
    title  = Paragraph(f"Reporte automático de pruebas #{seq:04d}",
                       styles["Heading1"])
    date   = Paragraph(datetime.now().strftime("%d de %b de %Y — %H:%M:%S"),
                       styles["Normal"])

    # tabla con estilo
    table  = Table(rows, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  colors.grey),
        ("TEXTCOLOR",   (0,0), (-1,0),  colors.whitesmoke),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("GRID",        (0,0), (-1,-1), 0.25, colors.black),
        ("ROWBACKGROUNDS", (0,1), (-1,-1),
         [colors.whitesmoke, colors.lightgrey]),
    ]))

    doc = SimpleDocTemplate(REPORT_DIR / f"{seq:04d}.pdf", pagesize=A4)
    doc.build([title, date, Spacer(1, 12), table])

def main():
    if not XML_FILE.exists():
        raise SystemExit("❌  No se encontró 'results.xml'. "
                         "Ejecuta primero pytest.")
    rows = parse_xml(XML_FILE)
    build_pdf(rows, next_number())
    print("✅  PDF generado en", REPORT_DIR)

if __name__ == "__main__":
    main()