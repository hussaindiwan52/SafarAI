import streamlit as st
import requests
import tempfile
import re
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

def clean_text(text):
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"#+", "", text)
    text = text.replace("*", "")
    return text.strip()


def format_lines(text):
    text = clean_text(text)
    lines = text.split("\n")

    formatted = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if ":" in line:
            key, val = line.split(":", 1)
            formatted.append(f"<b>{key}:</b> {val}")
        else:
            formatted.append(line)

    return "<br/>".join(formatted)


def generate_pdf(data, meta):
    styles = getSampleStyleSheet()

    title = ParagraphStyle("title", parent=styles["Title"], alignment=TA_CENTER, spaceAfter=20)
    route_style = ParagraphStyle("route", parent=styles["Heading1"], alignment=TA_CENTER, textColor=colors.darkblue, spaceAfter=10)
    section_title = ParagraphStyle("section", parent=styles["Heading3"], spaceBefore=10, spaceAfter=5)
    body = ParagraphStyle("body", parent=styles["Normal"], leading=14)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(temp_file.name)

    elements = []

    elements.append(Paragraph("✈️ BOARDING PASS", title))
    elements.append(Paragraph(f"{meta['origin']} ➝ {meta['destination']}", route_style))

    info_table = Table([
        ["Passenger", "TRAVELER"],
        ["Date", f"{meta['start_date']}"],
        ["Return", f"{meta['end_date']}"],
        ["Class", meta["type"]],
        ["Budget", f"₹{meta['budget']}"]
    ], colWidths=[120, 250])

    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("BOX", (0, 0), (-1, -1), 1, colors.grey),
        ("INNERPADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("✈️ Flight Details", section_title))
    elements.append(Paragraph(format_lines(data["flights"]), body))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("🏨 Stay Details", section_title))
    elements.append(Paragraph(format_lines(data["stay"]), body))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("🗺️ Activities", section_title))
    elements.append(Paragraph(format_lines(data["activities"]), body))

    doc.build(elements)
    return temp_file.name


st.title("✈️ AI Travel Planner")
st.caption("Plan your perfect trip in seconds")


left, right = st.columns([1, 2])


with left:
    origin = st.text_input("Source", placeholder="e.g., Pune")
    destination = st.text_input("Destination", placeholder="e.g., Goa")

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date")

    with col2:
        end_date = st.date_input("End Date")

    budget = st.number_input("Budget (INR)", min_value=1000, step=500)

    type_of_travel = st.selectbox(
        "Travel Type",
        ["Leisure", "Business", "Adventure", "Family", "Other"]
    )

    plan_clicked = st.button("✨ Plan My Trip", use_container_width=True)

    if st.session_state.latest_result:
        data = st.session_state.latest_result
        pdf_path = generate_pdf(data, {
            "origin": origin,
            "destination": destination,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "budget": budget,
            "type": type_of_travel
        })

        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download Boarding Pass PDF",
                f,
                file_name="boarding_pass_itinerary.pdf",
                use_container_width=True
            )


with right:
    if st.session_state.latest_result:
        st.subheader("Your Travel Plan")

        data = st.session_state.latest_result

        with st.expander("✈️ Flights", expanded=True):
            st.write(clean_text(data["flights"]))

        with st.expander("🏨 Stays", expanded=True):
            st.write(clean_text(data["stay"]))

        with st.expander("🗺️ Activities", expanded=True):
            st.write(clean_text(data["activities"]))

        


if plan_clicked:
    if not all([origin, destination, start_date, end_date, budget]):
        st.warning("Please fill all fields.")
    else:
        payload = {
            "origin": origin,
            "destination": destination,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "budget": budget,
            "type_of_travel": type_of_travel
        }

        with st.spinner("Planning your trip..."):
            response = requests.post("http://localhost:8000/run", json=payload)

        if response.ok:
            data = response.json()

            st.session_state.latest_result = data
            st.session_state.history.append({
                "origin": origin,
                "destination": destination,
                "data": data
            })

            st.rerun()
        else:
            st.error("Failed to fetch travel plan.")