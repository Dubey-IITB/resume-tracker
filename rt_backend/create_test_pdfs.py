from reportlab.pdfgen import canvas
from pathlib import Path
import io

def create_test_pdf(filename: str, content: str = "Test Resume Content") -> Path:
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, content)
    p.drawString(100, 200, "Email: test@example.com")
    p.drawString(100, 300, "Experience: 5 years")
    p.drawString(100, 400, "Skills: Python, FastAPI, SQL")
    p.save()
    pdf_path = Path(filename)
    with open(pdf_path, "wb") as f:
        f.write(buffer.getvalue())
    return pdf_path

if __name__ == "__main__":
    test_dir = Path("test_resumes")
    test_dir.mkdir(exist_ok=True)
    
    # Create test PDFs
    create_test_pdf(test_dir / "resume1.pdf", "Resume 1 Content")
    create_test_pdf(test_dir / "resume2.pdf", "Resume 2 Content") 