from fpdf import FPDF

def generate_report(stock: str, price: str, sentiment: str, recommendation: str, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Market Research Report", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Stock: {stock}")
    pdf.multi_cell(0, 10, f"Latest Price: {price}")
    pdf.multi_cell(0, 10, f"Sentiment: {sentiment}")
    pdf.multi_cell(0, 10, f"Recommendation: {recommendation}")

    pdf.output(filename)
    return f"Report generated: {filename}"
