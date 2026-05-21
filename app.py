import streamlit as st
import json
import requests
from groq import Groq
from pypdf import PdfReader
import io

# 1. Configure Page Layout
st.set_page_config(page_title="AI Client PDF Generator", layout="wide")
st.title("Client Report Generator (Premium PDF Engine)")

# 2. API Key Setup
api_key = st.text_input("Enter your Free Groq API Key (starts with gsk_):", type="password")

# 3. Helper Functions
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def generate_html_report(reference_text, client_json, api_key):
    client = Groq(api_key=api_key)
    
    prompt = f"""
    You are an elite, senior business consultant specializing in café operations, brand strategy, and customer retention systems. Your task is to generate a comprehensive, highly customized, professional business report for a client based strictly on the provided Master Reference Guide template structure and the client's intake data.

    CRITICAL RULES FOR ANALYSIS & WRITING QUALITY:
    1. DO NOT summarize, outline, or skip sections. You must fully write out every single page, section, checklist, and data matrix completely as modeled in the reference text. 
    2. Write with a highly detailed, professional, authoritative corporate tone. Every observation must be deeply expanded into dense, diagnostic paragraphs. Replace any generic placeholders with personalized strategies for the client.
    3. Cross-reference the Client Answers explicitly with the facts, statistics, benchmarks, and frameworks found within the Reference Guide.
    4. Currency Symbol Handling: If you output currency numbers, always use standard text prefix 'PHP ' or 'Php ' (e.g., PHP 5,000) instead of the raw symbol to ensure document encoding is clean.

    HTML/CSS DESIGN RULES:
    - Output the final result as a beautifully stylized, clean, professional HTML document starting with <!DOCTYPE html>.
    - Include basic inline CSS or an embedded <style> tag to style the document beautifully for print. Use a clean font like Arial/Helvetica, professional colors (e.g., deep charcoal headers, light gray table rows), clean padding, clean table borders, and explicit page breaks if needed.
    - DO NOT enclose your response inside markdown code blocks (e.g., do not use ```html or ```). Start your text immediately with <!DOCTYPE html> and end with </html>.

    REFERENCE GUIDE TEMPLATE STRUCTURE:
    {reference_text}
    
    CLIENT ANSWERS DATA:
    {client_json}
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3 # Lower temperature ensures stricter alignment with template facts
    )
    
    # Strip away any accidental markdown blocks if the model includes them
    html_output = response.choices[0].message.content.replace("```html", "").replace("```", "").strip()
    return html_output

def convert_html_to_pdf_via_api(html_string):
    try:
        # Utilizing an open-source, zero-config HTML-to-PDF compiler pipeline
        # It takes the HTML/CSS template and turns it into a perfectly formatted PDF binary
        response = requests.post(
            "https://html-to-pdf-converter.open-api.io/pdf",
            json={
                "html": html_string,
                "options": {
                    "format": "A4",
                    "margin": {"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"},
                    "printBackground": True
                }
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.content
        else:
            return None
    except Exception:
        # Fallback to an alternate microservice endpoint if the main pipeline is busy
        try:
            response = requests.post("https://api.html2pdf.app/v1/generate", json={"html": html_string}, timeout=60)
            if response.status_code == 200:
                return response.content
        except Exception:
            return None

# 4. User Interface Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Reference Guide")
    reference_pdf = st.file_uploader("Upload Master PDF Guide", type=["pdf"])

with col2:
    st.subheader("2. Paste Client Answers")
    client_json_input = st.text_area("Paste JSON Data here", height=200, placeholder='{"client_name": "John Doe"}')

# 5. Generation and Processing Logic
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
            
            with st.spinner("Step 1: Extracting structure from Reference Guide..."):
                reference_text = extract_text_from_pdf(reference_pdf)
                
            with st.spinner("Step 2: Senior AI Consultant is formulating your comprehensive HTML report..."):
                html_report = generate_html_report(reference_text, client_json_input, api_key)
                
            with st.spinner("Step 3: Compiling HTML styles into a Premium PDF eBook..."):
                pdf_bytes = convert_html_to_pdf_via_api(html_report)
                
            if pdf_bytes:
                st.success("Premium PDF Generated Successfully!")
                st.download_button(
                    label="📥 Download Complete Client Blueprint",
                    data=pdf_bytes,
                    file_name="Tailored_Complete_Brand_Blueprint.pdf",
                    mime="application/pdf"
                )
                
                with st.expander("Preview HTML Layout Structure"):
                    st.code(html_report[:1000] + "\n... [Truncated Code Preview] ...", language="html")
            else:
                st.error("The PDF conversion service timed out. Please try hitting generate again.")
                
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please double-check your client data brackets.")
        except Exception as e:
            st.error(f"An error occurred during operations: {e}")
