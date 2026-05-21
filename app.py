import streamlit as st
import json
import google.generativeai as genai
from pypdf import PdfReader
from xhtml2pdf import pisa
import io

# 1. Configure Page
st.set_page_config(page_title="AI Client PDF Generator", layout="wide")
st.title("Client Report Generator")

# 2. API Key Setup
api_key = st.text_input("Enter your Gemini API Key:", type="password")
if api_key:
    genai.configure(api_key=api_key)

# 3. Helper Functions
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def generate_html_report(reference_text, client_json):
    # Use Gemini 1.5 Pro for its massive context window
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    You are an expert system designed to generate client reports. 
    
    Rules:
    1. You will be provided with a REFERENCE GUIDE and a set of CLIENT ANSWERS (JSON).
    2. You must cross-reference the client answers against the reference guide.
    3. Tailor all advice and explanations STRICTLY based on the reference guide. Do not invent outside information.
    4. Output the final result as a clean, professional HTML document containing an ordered HTML table. 
    5. The HTML must include basic inline CSS for styling (borders, padding, fonts) so it looks good when converted to a PDF.
    6. DO NOT output markdown. Output RAW HTML only. Do not include ```html blocks, just the pure HTML code starting with <!DOCTYPE html>.

    REFERENCE GUIDE:
    {reference_text}
    
    CLIENT ANSWERS:
    {client_json}
    """
    
    response = model.generate_content(prompt)
    # Clean up any potential markdown formatting the AI might add
    html_output = response.text.replace("
```html", "").replace("```", "").strip()
    return html_output

def convert_html_to_pdf(html_string):
    pdf_buffer = io.BytesIO()
    # pisa converts HTML to PDF
    pisa_status = pisa.CreatePDF(io.StringIO(html_string), dest=pdf_buffer)
    if pisa_status.err:
        return None
    return pdf_buffer.getvalue()

# 4. User Interface
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Reference Guide")
    reference_pdf = st.file_uploader("Upload Master PDF Guide", type=["pdf"])

with col2:
    st.subheader("2. Paste Client Answers")
    client_json_input = st.text_area("Paste JSON Data here", height=200, placeholder='{"client_name": "John Doe", "goal": "weight loss"...}')

# 5. Generation Logic
if st.button("Generate Final PDF", type="primary"):
    if not api_key:
        st.error("Please enter your API Key at the top.")
    elif not reference_pdf:
        st.error("Please upload the Reference PDF.")
    elif not client_json_input:
        st.error("Please paste the client JSON data.")
    else:
        try:
            # Validate JSON
            json.loads(client_json_input)
            
            with st.spinner("Step 1: Extracting text from Reference Guide..."):
                reference_text = extract_text_from_pdf(reference_pdf)
                
            with st.spinner("Step 2: AI is analyzing answers and generating tailored table..."):
                html_report = generate_html_report(reference_text, client_json_input)
                
            with st.spinner("Step 3: Converting output to Final PDF..."):
                pdf_bytes = convert_html_to_pdf(html_report)
                
            if pdf_bytes:
                st.success("PDF Generated Successfully!")
                st.download_button(
                    label="Download Client PDF",
                    data=pdf_bytes,
                    file_name="Tailored_Client_Report.pdf",
                    mime="application/pdf"
                )
                
                with st.expander("Preview Generated HTML Table"):
                    st.components.v1.html(html_report, height=400, scrolling=True)
            else:
                st.error("Failed to generate PDF from HTML.")
                
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please check your client answers data.")
        except Exception as e:
            st.error(f"An error occurred: {e}")