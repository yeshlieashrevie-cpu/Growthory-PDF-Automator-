import streamlit as st
import json
from groq import Groq
from pypdf import PdfReader
from fpdf import FPDF
import io

# 1. Configure Page
st.set_page_config(page_title="AI Client PDF Generator", layout="wide")
st.title("Client Report Generator (Free Groq Engine)")

# 2. API Key Setup
api_key = st.text_input("Enter your Free Groq API Key (starts with gsk_):", type="password")

# 3. Helper Functions
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def generate_report_content(reference_text, client_json, api_key):
    client = Groq(api_key=api_key)
    
    prompt = f"""
    You are an expert system designed to generate structured client reports. 
    
    Rules:
    1. You will be provided with a REFERENCE GUIDE and a set of CLIENT ANSWERS (JSON).
    2. Cross-reference the client answers against the reference guide and tailor your advice strictly based on it.
    3. Output your response as a clean, valid JSON list of objects representing a table. Do not output markdown code blocks, just raw JSON.
    4. Each item in the list must have exactly three fields: "Section", "Client_Data", and "Recommendation".

    Format Example:
    [
      {{"Section": "Introduction", "Client_Data": "John Doe", "Recommendation": "Apply standard framework."}}
    ]

    REFERENCE GUIDE:
    {reference_text}
    
    CLIENT ANSWERS:
    {client_json}
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    clean_text = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_text)

def create_pdf(report_data):
    pdf = FPDF()
    pdf.configure_core_fonts_substitution()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", 'B', size=16)
    pdf.cell(200, 10, txt="Tailored Client Report", ln=True, align='C')
    pdf.ln(10)
    
    def clean_text(text):
        if not text:
            return "N/A"
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
        return text.encode('latin-1', 'ignore').decode('latin-1')

    # Write Sections
    for row in report_data:
        section = clean_text(f"Section: {row.get('Section', 'N/A')}")
        client_input = clean_text(f"Client Input: {row.get('Client_Data', 'N/A')}")
        recommendation = clean_text(f"Recommendation: {row.get('Recommendation', 'N/A')}")
        
        pdf.set_font("Helvetica", 'B', size=12)
        pdf.cell(200, 8, txt=section, ln=True)
        
        pdf.set_font("Helvetica", 'I', size=11)
        pdf.cell(200, 6, txt=client_input, ln=True)
        
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 6, txt=recommendation)
        pdf.ln(6)
        
    return pdf.output(dest='S')

# 4. User Interface
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Reference Guide")
    reference_pdf = st.file_uploader("Upload Master PDF Guide", type=["pdf"])

with col2:
    st.subheader("2. Paste Client Answers")
    client_json_input = st.text_area("Paste JSON Data here", height=200, placeholder='{"client_name": "John Doe"}')

# 5. Generation Logic
if st.button("Generate Final PDF", type="primary"):
    if not api_key:
        st.error("Please enter your Groq API Key at the top.")
    elif not reference_pdf:
        st.error("Please upload the Reference PDF.")
    elif not client_json_input:
        st.error("Please paste the client JSON data.")
    else:
        try:
            json.loads(client_json_input)
            
            with st.spinner("Step 1: Extracting text from Reference Guide..."):
                reference_text = extract_text_from_pdf(reference_pdf)
                
            with st.spinner("Step 2: Free Llama Model is analyzing data..."):
                report_data = generate_report_content(reference_text, client_json_input, api_key)
                
            with st.spinner("Step 3: Creating PDF..."):
                pdf_bytes = create_pdf(report_data)
                
            if pdf_bytes:
                st.success("PDF Generated Successfully!")
                st.download_button(
                    label="Download Client PDF",
                    data=pdf_bytes,
                    file_name="Tailored_Client_Report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Failed to build PDF binary.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
