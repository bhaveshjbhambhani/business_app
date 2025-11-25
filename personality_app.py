import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

import streamlit as st
import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def save_to_google_sheet(data_dict):
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        json.loads(st.secrets["gcp"]["service_account"]),
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    # Open your sheet by name
    sheet = client.open("Business Readiness Data").sheet1

    # Prepare a row
    row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

    for key in data_dict:
        row.append(data_dict[key])

    # Append row to sheet
    sheet.append_row(row)

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Business Personality & Readiness", page_icon="🧭", layout="centered")
st.title("🧭 Business Personality & Readiness Assessment")

# ---------------- INITIALIZE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = 1

if "data" not in st.session_state:
    st.session_state.data = {}

def go_next():
    st.session_state.stage += 1
    st.rerun()

def go_back():
    st.session_state.stage -= 1
    st.rerun()

# ============================================================
#                        STAGE 1
# ============================================================

if st.session_state.stage == 1:
    st.header("Stage 1 — Basic Details")

    reg_code = st.text_input("Registration Code")

    age_group = st.selectbox(
        "Age group",
        ["Select age group", "20–30", "31–40", "41–50", "51–60", "Above 60"]
    )

    gender = st.selectbox(
        "Gender",
        ["Select gender", "Male", "Female", "Other"]
    )

    kk_number = st.selectbox(
        "KK Number",
        ["Select KK number", "1", "2", "3", "4", "5", "6"]
    )

    if st.button("Next ➡️"):
        if (
            not reg_code
            or age_group.startswith("Select")
            or gender.startswith("Select")
            or kk_number.startswith("Select")
        ):
            st.error("⚠️ Please fill all fields before moving ahead.")
        else:
            st.session_state.data.update({
                "Registration Code": reg_code,
                "Age Group": age_group,
                "Gender": gender,
                "KK Number": kk_number
            })
            go_next()

# ============================================================
#                        STAGE 2
# ============================================================

elif st.session_state.stage == 2:
    st.header("Stage 2 — Personality & Lifestyle")
    st.write("Please answer honestly. Use the dropdowns to select the best option.")

    # ---------------- FAMILY ----------------
    st.subheader("Family Background")
    family1 = st.selectbox("1. How would you describe your relationship with your family members?",
        ["Select an option", "Very close and understanding", "Supportive but sometimes distant",
         "Occasionally conflicting", "Difficult or strained"])

    st.markdown("""
        <p style="margin-bottom:1px; font-size:15px;">
        How much support do you receive from your family in your
        <a href="https://eastohio.edu/personal-growth-what-it-is-and-why-it-matters/" target="_blank"><b>personal growth</b></a>?
        </p>
        """, unsafe_allow_html=True)
    family2 = st.selectbox(
        "",
        ["Select an option", "Always supportive", "Supportive when needed",
         "Neutral or limited support", "Rarely supportive"])

    st.markdown("""
        <p style="margin-bottom:1px; font-size:15px;">
        How often do you spend
        <a href="https://www.betterup.com/blog/quality-time-with-family" target="_blank"><b>quality time with your family</b></a>?
        </p>
        """, unsafe_allow_html=True)
    family3 = st.selectbox(
        "",
        ["Select an option", "Every day", "Few times a week", "Occasionally", "Rarely"])

    # ---------------- PHYSICAL ----------------
    st.subheader("Physical Update")
    physical1 = st.selectbox("1. How active are you physically in your daily routine?",
        ["Select an option", "Very active (daily exercise)", "Moderately active",
         "Occasionally active", "Mostly inactive"])

    st.markdown("""
        <p style="margin-bottom:1px; font-size:15px;">
        Do you maintain a 
        <a href="https://www.sleepfoundation.org/physical-health/diet-exercise-sleep" target="_blank"><b>healthy diet and sleeping pattern</b></a>?
        </p>
        """, unsafe_allow_html=True)
    physical2 = st.selectbox(
        "",
        ["Select an option", "Always maintain", "Most of the time", "Sometimes", "Rarely"])


    physical3 = st.selectbox("3. Do you feel your physical health affects your confidence and overall personality?",
        ["Select an option", "Yes, strongly", "Somewhat", "Not much", "No impact"])

    # ---------------- MENTAL ----------------
    st.subheader("Mental Stability")
    mental1 = st.selectbox("1. How well do you handle stress or unexpected challenges?",
        ["Select an option", "Very well", "Manageable", "Sometimes struggle", "Find it difficult"])

    st.markdown("""
        <p style="margin-bottom:1px; font-size:15px;">
        Do you often feel positive and confident about your 
        <a href="https://vitalitylivingcollege.info/what-are-goals-and-why-are-they-important/" target="_blank"><b>goals</b></a>?
        </p>
        """, unsafe_allow_html=True
    )

    mental2 = st.selectbox(
        "",
        ["Select an option", "Always confident and focused", "Usually positive with minor doubts",
         "Sometimes uncertain", "Often lack clarity or motivation"]
    )

    mental3 = st.selectbox("3. How frequently do you take time to relax or clear your mind?",
        ["Select an option", "Daily", "Few times a week", "Occasionally", "Rarely"])

    # ---------------- SOCIAL ----------------
    st.subheader("Social Activity")
    social1 = st.selectbox("1. How frequently do you meet or interact with friends or social groups?",
        ["Select an option", "Very frequently", "Occasionally", "Rarely", "Almost never"])

    social2 = st.selectbox("2. Are you comfortable expressing your thoughts in social situations?",
        ["Select an option", "Very comfortable", "Somewhat comfortable",
         "Uncomfortable", "Avoid social interaction"])

    social3 = st.selectbox("3. How do you usually contribute to your community or social circles?",
        ["Select an option", "Actively volunteer or participate", "Support occasionally",
         "Prefer to stay uninvolved"])

    # ---------------- FINANCIAL ----------------
    st.subheader("Financial Background")
    financial1 = st.selectbox("1. Current Status of Income",
        ["Select an option", "I have a regular and stable source of income", "I am self-employed or doing freelance work",
         "I am currently unemployed but actively seeking opportunities", "I am a student or dependent on family",
         "Retired or not seeking employment"])

    financial2 = st.selectbox("2. Primary Source of Income or Support",
        ["Select an option", "Salary or professional income", "Business or self-employment",
         "Parental/family support", "Savings or pension", "No fixed source of income"])

    financial3 = st.selectbox("3. Financial Goal or Priority",
        ["Select an option", "To find a stable source of income", "To grow my business or income level",
         "To save and invest wisely", "To clear debts or improve stability",
         "I am financially comfortable"])

    # ---------------- SPIRITUAL ----------------
    st.subheader("Spiritual Involvement")
    spiritual1 = st.selectbox("1. How connected do you feel with your inner self or spiritual side?",
        ["Select an option", "Strongly connected", "Moderately connected", "Slightly connected", "Not connected"])

    spiritual2 = st.selectbox("2. Do you engage in activities like meditation, prayer, or self-reflection?",
        ["Select an option", "Daily", "Few times a week", "Occasionally", "Rarely or never"])

    spiritual3 = st.selectbox("3. How important is spiritual growth in your daily life?",
        ["Select an option", "Very important", "Somewhat important",
         "Not very important", "Not important at all"])

    # ---------------- BUTTONS ----------------
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back"):
            go_back()

    with col2:
        if st.button("Next ➡️"):

            # VALIDATION
            missing = any([
                family1.startswith("Select"), family2.startswith("Select"), family3.startswith("Select"),
                physical1.startswith("Select"), physical2.startswith("Select"), physical3.startswith("Select"),
                mental1.startswith("Select"), mental2.startswith("Select"), mental3.startswith("Select"),
                social1.startswith("Select"), social2.startswith("Select"), social3.startswith("Select"),
                financial1.startswith("Select"), financial2.startswith("Select"), financial3.startswith("Select"),
                spiritual1.startswith("Select"), spiritual2.startswith("Select"), spiritual3.startswith("Select")
            ])

            if missing:
                st.error("⚠️ Please answer all Stage 2 questions before continuing.")
            else:
                st.session_state.data.update({
                    "family1": family1, "family2": family2, "family3": family3,
                    "physical1": physical1, "physical2": physical2, "physical3": physical3,
                    "mental1": mental1, "mental2": mental2, "mental3": mental3,
                    "social1": social1, "social2": social2, "social3": social3,
                    "financial1": financial1, "financial2": financial2, "financial3": financial3,
                    "spiritual1": spiritual1, "spiritual2": spiritual2, "spiritual3": spiritual3
                })
                go_next()

# ============================================================
#                        STAGE 3
# ============================================================

elif st.session_state.stage == 3:
    st.header("Stage 3 — Mandatory Requirements")

    reqs = {}
    def q(txt):
        return st.radio(txt, ["Select", "Yes", "No"])

    reqs["Daily Account Review"] = q("1. Do you review your business accounts daily (zero-zero balance)?")
    reqs["Minimize Financial Burden"] = q("2. Do you maintain minimum loans and debts?")
    reqs["Complete Technical Knowledge"] = q("3. Do you have complete technical knowledge of your business?")
    reqs["Complete Equipment Knowledge"] = q("4. Do you have complete knowledge of your equipment (if any)?")
    reqs["Fixed Duty Hours"] = q("5. Do you follow fixed duty hours?")
    reqs["Accounting Course"] = q("6. Have you completed a share/purchase or accounting course?")
    reqs["Tax & Compliance"] = q("7. Do you understand GST, tax, banking, and other government compliance?")
    reqs["Worker Insurance"] = q("8. Have you insured your workers?")
    reqs["Firm Insurance"] = q("9. Is your firm insured?")
    reqs["Fire Safety"] = q("10. Do you have fire safety arrangements at the firm?")
    reqs["Labour Rules"] = q("11. Do you understand basic labour rules?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Back"):
            go_back()

    with col2:
        if st.button("Generate Report 🧾"):

            if any(v == "Select" for v in reqs.values()):
                st.error("⚠️ Please answer all mandatory requirement questions.")
            else:
                st.session_state.data.update(reqs)

                # 👉 SAVE USER DATA TO GOOGLE SHEET
                save_to_google_sheet(st.session_state.data)

                # ---------------- PDF GENERATION START ----------------

                pdf_buffer = io.BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=A4,
                                        rightMargin=40, leftMargin=40,
                                        topMargin=60, bottomMargin=40)
                styles = getSampleStyleSheet()
                elements = []

                # Title
                title_style = ParagraphStyle(
                    name='TitleStyle',
                    fontSize=18,
                    alignment=1,
                    textColor=colors.HexColor("#023e8a")
                )
                elements.append(Paragraph("<b>Business Personality & Readiness Report</b>", title_style))
                elements.append(Spacer(1, 0.2 * inch))

                date_str = datetime.now().strftime("%d %B %Y, %I:%M %p")
                elements.append(Paragraph(f"Generated on {date_str}", styles["Normal"]))
                elements.append(Spacer(1, 0.2 * inch))

                # Stage 1
                heading = ParagraphStyle(name='Heading', fontSize=14, textColor="#0077b6")
                elements.append(Paragraph("<b>Stage 1 – Personal Information</b>", heading))

                for key in ["Registration Code", "Age Group", "Gender", "KK Number"]:
                    elements.append(Paragraph(f"<b>{key}:</b> {st.session_state.data.get(key)}", styles["Normal"]))
                elements.append(Spacer(1, 0.2 * inch))

                # Stage 2 Labels
                stage2_labels = {
                    "family1": "How would you describe your relationship with your family members?",
                    "family2": "How much support do you receive from your family in your personal growth?",
                    "family3": "How often do you spend quality time with your family?",
                    "physical1": "How active are you physically in your daily routine?",
                    "physical2": "Do you maintain a healthy diet and sleeping pattern?",
                    "physical3": "Do you feel your physical health affects your confidence and overall personality?",
                    "mental1": "How well do you handle stress or unexpected challenges?",
                    "mental2": "Do you often feel positive and confident about your goals?",
                    "mental3": "How frequently do you take time to relax or clear your mind?",
                    "social1": "How frequently do you meet or interact with friends or social groups?",
                    "social2": "Are you comfortable expressing your thoughts in social situations?",
                    "social3": "How do you usually contribute to your community or social circles?",
                    "financial1": "Current Status of Income",
                    "financial2": "Primary Source of Income or Support",
                    "financial3": "Financial Goal or Priority",
                    "spiritual1": "How connected do you feel with your inner self or spiritual side?",
                    "spiritual2": "Do you engage in activities like meditation, prayer, or self-reflection?",
                    "spiritual3": "How important is spiritual growth in your daily life?"
                }

                elements.append(Paragraph("<b>Stage 2 – Personality & Lifestyle</b>", heading))

                for key, label in stage2_labels.items():
                    ans = st.session_state.data.get(key)
                    elements.append(Paragraph(f"<b>{label}:</b> {ans}", styles["Normal"]))
                    elements.append(Spacer(1, 0.05 * inch))
                elements.append(Spacer(1, 0.2 * inch))

                # Stage 3 Table
                elements.append(Paragraph("<b>Stage 3 – Mandatory Requirements</b>", heading))
                table_data = [["Requirement", "Status"]]

                for k, v in reqs.items():
                    table_data.append([k, v])

                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0077b6")),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('GRID', (0, 0), (-1, -1), 0.4, colors.grey)
                ]))
                elements.append(t)
                elements.append(Spacer(1, 0.2 * inch))

                # Note Box
                note_text = (
                    "<b>Note:</b> The firm must fulfil all mandatory requirements. "
                    "After all requirements are met, a verification visit will be conducted "
                    "by our team to validate completion and compliance."
                )

                note = Table(
                    [[Paragraph(note_text, styles["Normal"])]],
                    colWidths=[6.3 * inch],
                    style=[
                        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFF8C4")),
                        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#B8860B"))
                    ]
                )
                elements.append(note)

                doc.build(elements)
                pdf_buffer.seek(0)

                st.download_button(
                    "⬇️ Download Professional PDF Report",
                    data=pdf_buffer,
                    file_name=f"Business_Readiness_Report.pdf",
                    mime="application/pdf"
                )

                st.success("Report generated successfully!")
                st.session_state.stage = 4
                

# ============================================================
#                        THANK YOU
# ============================================================

elif st.session_state.stage == 4:
    st.header("🎉 Thank You!")
    st.write("Your personalized Business Personality & Readiness Report has been generated successfully.")

    if st.button("Start New Assessment"):
        st.session_state.stage = 1
        st.session_state.data = {}
        st.rerun()

