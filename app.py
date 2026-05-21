import streamlit as st
import json
import requests
import anthropic  # Updated framework engine
from pypdf import PdfReader
import streamlit.components.v1 as components

# ==============================================================
# 1. PAGE LAYOUT CONFIGURATION & FRONTEND ASSET LOADING
# ==============================================================
st.set_page_config(page_title="AI Client PDF Generator", layout="wide")

def load_custom_frontend():
    try:
        # Open and read the HTML file from your root GitHub folder
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
            
        # Open and read your custom styles
        with open("style.css", "r", encoding="utf-8") as f:
            css_content = f.read()
            
        # Open and read your custom scripts
        with open("script.js", "r", encoding="utf-8") as f:
            js_content = f.read()
            
        # Splice them all together into a clean, running page payload
        full_frontend = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                {css_content}
            </style>
        </head>
        <body>
            {html_content}
            <script>
                {js_content}
            </script>
        </body>
        </html>
        """
        return full_frontend
    except FileNotFoundError:
        # Fallback layout if frontend assets are missing or loading incorrectly
        return None

# Attempt to mount your handcrafted frontend layout
frontend_html = load_custom_frontend()

if frontend_html:
    # Renders your index.html / style.css / script.js cleanly on screen
    components.html(frontend_html, height=680, scrolling=True)
else:
    # Standard Title layout fallback if files aren't found locally yet
    st.title("Client Report Generator (Premium Claude Engine)")


# ==============================================================
# 2. HELPER FUNCTIONS & ANTHROPIC AI ENGINE
# ==============================================================
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def generate_html_report(reference_text, client_json, api_key):
    # Initialize the official Anthropic Developer client connection
    client = anthropic.Anthropic(api_key=api_key)

    # Your highly optimized, street-smart consultant prompt variation
    prompt = f"""
You are a warm, sharp, street-smart business consultant who has spent 10+ years helping small café owners in the Philippines grow their repeat customer base. You write the way a trusted mentor talks — clear, direct, friendly, and deeply personal. You do NOT write like a corporate report. You write like a smart friend who genuinely wants this café to win.

You have just finished a deep consultation session with the café owner. Now you are writing their COMPLETE, PERSONALIZED BRAND BLUEPRINT — a document they will read, print, and return to every week. Every word must feel like it was written exclusively for THEM and their café — not a template, not a fill-in, not a generic guide.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR CORE WRITING RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULE 1 — TALK TO THEM, NOT AT THEM
Address the owner as "you" and "your café" at every opportunity. Never use generic phrases like "café owners should consider." Say: "Here's what YOU need to do this week." Make them feel like this document was handwritten for them after a real conversation.

RULE 2 — LAYMAN'S LANGUAGE ONLY
Avoid business jargon unless you immediately explain it in plain language. No buzzwords without a plain-English translation right after. If you say "psychographic profile," you follow it with "— basically, what makes your customer TICK, what they actually care about deep down."

RULE 3 — BE SPECIFIC WITH THEIR DATA
Every section MUST reference the client's actual café name, their specific answers, their actual location, their real challenges. Do not write "your peak hours." Write "Your rush happens [their actual hours] — and here's exactly how to milk every minute of that window." Pull from the client JSON aggressively.

RULE 4 — MAKE EVERY STAT FEEL REAL
When citing statistics or benchmarks from the reference guide, frame them conversationally. Not: "Studies show 67% more spending by loyal customers." Instead: "Think about it — a loyal regular spends 67% more than someone who just wandered in. That's not a small number. That's the difference between a slow week and a great one."

RULE 5 — WRITE WITH ENERGY AND WARMTH
This document should feel exciting to read. Use short punchy sentences for impact. Use longer sentences to build context and teach. Vary rhythm. Use emphasis. Write the way a passionate, experienced mentor coaches — not the way an accountant reports. The owner should feel motivated, not overwhelmed.

RULE 6 — NEVER SKIP OR SUMMARIZE A SECTION
Every section from the Reference Guide must be fully written out. No placeholders. No "[Insert here]". No "refer to section X." Every insight, every checklist, every table, every recommendation must be fully fleshed out and personalized to THIS client.

RULE 7 — EVERY RECOMMENDATION MUST HAVE A "DO THIS" MOMENT
After analysis and diagnosis, always close with a concrete, actionable next step written like a coach: "So here's your move:", "Your action this week:", "The one thing to do first:". Make it feel urgent and achievable.

RULE 8 — CURRENCY FORMATTING
All Philippine Peso amounts use the prefix "PHP" or "Php" (e.g., PHP 5,000 or Php 350). Never use raw peso symbols — they may break encoding.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION-BY-SECTION WRITING GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For EACH of the 12 sections below, follow these specific instructions IN ADDITION to the core writing rules above:

SECTION 1 — BRAND SNAPSHOT & POSITIONING ANALYSIS
- Fill in the Brand Identity at a Glance table COMPLETELY with real client data from their JSON
- Write the USP Breakdown as if you just had a 1-hour discovery call with them. Identify what truly makes their café irreplaceable — even if they didn't say it perfectly in their answers, help them SEE it. Say things like "You might not have phrased it this way, but what you're really offering is..."
- For the Brand Story section, take their origin story and show them how powerful it actually is. Make them feel proud of it.
- End with a bold, motivating line that anchors why their brand matters.

SECTION 2 — CUSTOMER RETENTION DIAGNOSIS
- Open with the most eye-catching statistics from the reference guide, but frame each one as a direct implication for THIS owner: "What does 5x cheaper to retain mean for [Café Name]? It means every peso you spend chasing new customers instead of keeping your current ones is literally a bad investment."
- For The 6 Most Common Reasons Cafés Lose Customers — go through EVERY one and explicitly state whether this is a problem for THIS client based on their intake, and how severe it is. ("Based on what you shared, #1 Forgettability is your biggest threat right now, because...")
- For the Diagnostic Table — fill it out based on their situation. Make it feel like a medical diagnosis, not a template.

SECTION 3 — TARGET AUDIENCE DEEP DIVE
- Build a vivid, named, almost-fictional Customer Avatar using their intake data. Give the avatar a real Filipino name, a real daily routine, a real reason they walk into a café. ("Meet Carla, 26, a junior marketing executive in [their area]...")
- For the Audience Segments table — identify which 1-2 segments are their PRIMARY customer base and write 2-3 diagnosis paragraphs on how to serve those people better than any other café in their area.
- Make this section feel like the owner is seeing their customer clearly for the first time.

SECTION 4 — LOYALTY & RETENTION STRATEGY BLUEPRINT
- Walk through the 3-Layer Loyalty Architecture and explain which layer this café is currently strongest at and which layer needs the most work, based on their intake data.
- For the Loyalty Program Design Options table — recommend EXACTLY which model is right for this café and WHY, being very specific to their size, resources, and customer type.
- For the Digital Touchpoint Strategy table — personalize EVERY touchpoint with specific message ideas that match their brand voice and the Filipino context (Messenger, Viber, GCash-linked loyalty etc.).

SECTION 5 — CONTENT STRATEGY PLAYBOOK
- For The 5 Pillars — give 3 SPECIFIC content ideas for each pillar that match this café's personality, menu, and aesthetic. Not generic. Real ideas they can execute this week.
- For the Weekly Posting Schedule — fill in ACTUAL content ideas using their café name, actual menu items from their JSON, and their brand personality. Make it feel like a real editorial calendar.
- For the Repurposing section — identify which pieces of content they already have (from their intake) and show them how to get 5x more use from each one.

SECTION 6 — PEAK & SLOW HOUR ACTION PLAN
- Fill in their ACTUAL peak and slow hours from their intake.
- For each Peak Hour Strategy — give a real example with their actual price range: "At your PHP X average ticket, getting your staff to upsell even PHP 50 per transaction during your morning rush at [peak hour]..."
- For Slow Hour Strategies — name their actual slow period and write copy they could literally post on social media TODAY to drive traffic during that window. Make it feel urgent and doable.
- Close with a custom revenue calculation based on their current daily customer count.

SECTION 7 — MENU OPTIMIZATION FOR REPEAT VISITS
- Reference their top 3 sellers by name. Explain why each one is a loyalty ANCHOR and how to protect and amplify it.
- Write the Combo Offer recommendation with their ACTUAL items and their ACTUAL price range (e.g., "Your [Drink X] + [Pastry Y] could easily be a PHP [X] combo deal that saves customers PHP [Y]").
- Give seasonal menu ideas tied to real Philippine calendar events: Pasko, Valentine's, Undas, summer, back-to-school. Make it relevant to their specific café personality.

SECTION 8 — THE EXPERIENCE FACTOR — BUILDING YOUR THIRD PLACE
- Write this section as if you have physically walked through their café. Based on their intake, identify what their strongest physical comfort elements likely are and which ones they need to build.
- For Human Connection — write SPECIFIC staff training scripts they can actually use. ("When a regular walks in, barista says: 'Hey [name], the usual?' — This one sentence is worth PHP 500 in repeat visit value.")
- For Community Building — propose 2-3 SPECIFIC community event ideas that make sense for their neighborhood, audience type, and brand personality.

SECTION 9 — FEEDBACK & MEASUREMENT SYSTEM
- Make the 4-step Feedback Loop feel like a conversation, not a process diagram. Walk them through each step with an example from their café context.
- For the KPIs table — fill in their BASELINE numbers based on their intake data where available, and flag which 3 metrics should be their TOP priority to watch in Month 1.

SECTION 10 — 30-DAY ROADMAP OVERVIEW
- Write a brief but exciting intro paragraph for each of the 4 phases that sets the emotional context: "This week is about building your foundation. Before you post a single piece of content, you need to know who you ARE..."
- For each daily task — customize it slightly to match their café name, their content type, their audience. Make it feel like a real game plan, not a generic list.

SECTION 11 — QUICK-START ACTION CHECKLIST
- Keep the full checklist but add a short callout note beside their top 5 MOST URGENT actions based on what their intake revealed. ("START HERE — this is your biggest gap right now.")

SECTION 12 — KPIs & TRACKING DASHBOARD
- Fill in their Baseline column with whatever data they provided in their intake (daily customer average, estimated ATV, etc.)
- Write a 1-paragraph personal closing message to the café owner — warm, specific, and motivating. End with a line that makes them feel proud and ready to start.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HTML/CSS DESIGN INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Output a beautifully styled, professional, print-ready HTML document. Follow every rule below:

1. Start IMMEDIATELY with <!DOCTYPE html>. Do NOT use markdown code blocks, backticks, or any wrapper. End with </html>.
2. Use an embedded <style> tag in the <head>. Do NOT use external CSS files or CDN links.
3. FONTS: Use Google Fonts import for 'Playfair Display' (headings) and 'Lato' (body). Add this at the top of your style block:
   @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@300;400;700&display=swap');
4. COLOR PALETTE:
   - Primary heading color: #1a1a2e (deep navy)
   - Accent / highlight color: #c8963e (warm gold)
   - Section background strips: #f9f6f0 (warm cream)
   - Body text: #2d2d2d (soft charcoal)
   - Table header rows: #1a1a2e with white text
   - Alternating table rows: #f4f0ea and #ffffff
   - Stat callout boxes: gold border left, cream background
5. LAYOUT & SPACING:
   - Max content width: 900px, centered on page
   - Section padding: 40px top and bottom
   - Body font size: 15px, line-height: 1.8
   - H1 (cover title): 42px, centered, Playfair Display
   - H2 (section headers): 26px, Playfair Display, with gold underline border-bottom
   - H3: 18px, Lato Bold, uppercase letter-spacing
6. COVER PAGE: Create a beautiful cover page first. Include:
   - Café name in large Playfair Display heading
   - Document title: "Your Complete Brand & Repeat Customer Blueprint"
   - A styled horizontal gold divider
   - The 3 key stats (5x cheaper, 67% more spend, 75% profit boost) as styled stat boxes
   - Report delivery date
   - A short 2-line personalized welcome message
7. TABLE OF CONTENTS: Style it cleanly with dotted leaders and section numbers.
8. SECTION BREAKS: Add a styled section header bar before each of the 12 sections with the section number and title.
9. CALLOUT BOXES: For key insights, tips, and "Your Action" moments — use a styled blockquote or div with a gold left border and light cream background.
10. TABLES: All tables must have full borders, alternating row colors, bold headers in navy, and be 100% width within the content area.
11. PAGE BREAKS: Add page-break-before: always CSS on each new section header so it prints cleanly.
12. CHECKLIST ITEMS: Style all checklist items with a square checkbox icon (unicode: ☐) and clean spacing.
13. STAT BOXES (for Section 2 stats): Use flex-row cards with large bold numbers in gold, descriptor text in navy below, subtle shadow.
14. CLOSING PAGE: End the document with a styled final page — a warm gold-bordered box with the personal closing message and a motivational sign-off line.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REFERENCE GUIDE TEMPLATE STRUCTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{reference_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLIENT INTAKE DATA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{client_json}
"""

    # Calling Claude 3.5 Sonnet structure via Anthropic Messages SDK
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8192,  # Maximum content generation threshold
        temperature=0.45,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Retrieve raw text from Claude payload
    raw_html = response.content[0].text
    html_output = raw_html.replace("```html", "").replace("```", "").strip()
    return html_output

def convert_html_to_pdf_via_api(html_string):
    try:
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
        return None
    except Exception:
        try:
            response = requests.post("https://api.html2pdf.app/v1/generate", json={"html": html_string}, timeout=60)
            if response.status_code == 200:
                return response.content
        except Exception:
            return None

# ==============================================================
# 3. CONTROL PANEL INPUTS & LOGIC EXECUTION
# ==============================================================
with st.sidebar:
    st.header("⚙️ App Engine Control Panel")
    api_key = st.text_input("Enter Anthropic API Key (starts with sk-ant-):", type="password")
    reference_pdf = st.file_uploader("Upload Master PDF Guide", type=["pdf"])
    client_json_input = st.text_area("Paste JSON Data here", height=150, placeholder='{"client_name": "John Doe"}')
    submit_btn = st.button("Generate Final PDF", type="primary")

if submit_btn:
    if not api_key:
        st.error("Please enter your Anthropic API Key at the top left.")
    elif not reference_pdf:
        st.error("Please upload the Reference PDF.")
    elif not client_json_input:
        st.error("Please paste the client JSON data.")
    else:
        try:
            json.loads(client_json_input)

            with st.spinner("Step 1: Extracting structure from Reference Guide..."):
                reference_text = extract_text_from_pdf(reference_pdf)

            with st.spinner("Step 2: Claude Senior Consultant is building your custom HTML blueprint..."):
                html_report = generate_html_report(reference_text, client_json_input, api_key)

            with st.spinner("Step 3: Compiling HTML styles into a Premium PDF eBook..."):
                pdf_bytes = convert_html_to_pdf_via_api(html_report)

            if pdf_bytes:
                st.success("Premium PDF Generated Successfully!")
                st.download_button(
                    label="📥 Download Complete Claude Blueprint",
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
