def create_pdf(report_data):
    # 1. Initialize PDF with Core Font Substitution enabled
    pdf = FPDF()
    pdf.configure_core_fonts_substitution()
    pdf.add_page()
    
    # 2. Setup standard clean fonts that support standard text mapping
    # We use 'Helvetica' but ensure we clean the text strings first
    
    # Title
    pdf.set_font("Helvetica", 'B', size=16)
    pdf.cell(200, 10, txt="Tailored Client Report", ln=True, align='C')
    pdf.ln(10)
    
    # Helper to safely replace or encode tricky characters like ₱
    def clean_text(text):
        if not text:
            return "N/A"
        # Map common currency and punctuation symbols to things standard Helvetica can print
        replacements = {
            "₱": "PHP ",
            "–": "-",
            "—": "-",
            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'"
        }
        for bad_char, good_char in replacements.items():
            text = text.replace(bad_char, good_char)
        
        # Fallback: Encode to latin-1 and ignore anything it still can't read
        return text.encode('latin-1', 'ignore').decode('latin-1')

    # Write Sections
    for row in report_data:
        section = clean_text(f"Section: {row.get('Section', 'N/A')}")
        client_input = clean_text(f"Client Input: {row.get('Client_Data', 'N/A')}")
        recommendation = clean_text(f"Recommendation: {row.get('Recommendation', 'N/A')}")
        
        # Draw Section Header
        pdf.set_font("Helvetica", 'B', size=12)
        pdf.cell(200, 8, txt=section, ln=True)
        
        # Draw Client Input
        pdf.set_font("Helvetica", 'I', size=11)
        pdf.cell(200, 6, txt=client_input, ln=True)
        
        # Draw Multi-line Recommendation
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 6, txt=recommendation)
        pdf.ln(6)
        
    return pdf.output(dest='S')
