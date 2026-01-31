from fpdf import FPDF
import datetime

class AnalystReport(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'QUANT ANALYST PRO - MARKET INTELLIGENCE REPORT', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}', align='C')

def generate_pdf_report(ticker, result_text, signals, fundamentals):
    pdf = AnalystReport()
    pdf.add_page()
    
    # 1. Ticker Header
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, f'ANALYSIS FOR: {ticker}', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    # 2. Fundamentals Table
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, 'Valuation Metrics', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 10)
    for k, v in fundamentals.items():
        pdf.cell(40, 7, f'{k}:')
        pdf.cell(0, 7, f'{v}', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    # 3. Technical Signals
    if signals:
        pdf.set_font('helvetica', 'B', 12)
        pdf.cell(0, 10, 'Expert Signals & Alerts', new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', '', 10)
        for sig in signals:
            if sig['type'] == 'BULLISH':
                pdf.set_text_color(0, 100, 0) 
            elif sig['type'] == 'BEARISH':
                pdf.set_text_color(150, 0, 0)
            else:
                pdf.set_text_color(100, 100, 0)
                
            # Sanitize signal label/desc
            s_label = sig['label'].encode('ascii', 'ignore').decode('ascii')
            s_desc = sig['desc'].encode('ascii', 'ignore').decode('ascii')
            pdf.cell(0, 7, f"[{sig['type']}] {s_label}: {s_desc}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(0)
        pdf.ln(5)

    # 4. Engine Summary
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, 'Quantitative Summary', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 10)
    
    # Sanitize text: Remove emojis and markdown and ensure it's standard ASCII/Latin
    clean_text = result_text.replace('###', '').replace('**', '').replace('🧬', '').replace('💹', '')
    # Remove any other non-ASCII characters that might crash standard fonts
    clean_text = clean_text.encode('ascii', 'ignore').decode('ascii')
    
    pdf.multi_cell(0, 7, clean_text)
    
    return bytes(pdf.output()) # Returns bytes directly in modern fpdf2
