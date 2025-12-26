import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import datetime
import smtplib
from email.message import EmailMessage
import os

# -----------------------------
# Database setup
# -----------------------------
engine = create_engine("sqlite:///issues.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    reference_id = Column(String(50), unique=True)
    email = Column(String(100))
    city = Column(String(50))
    area = Column(String(100))
    street = Column(String(50))
    issue_type = Column(String(100))
    description = Column(Text)
    photo_path = Column(String(200))
    status = Column(String(20), default="Submitted")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)

# -----------------------------
# Helper functions
# -----------------------------
def generate_reference_id():
    year = datetime.datetime.now().year
    rand = random.randint(10000, 99999)
    return f"ISS-{year}-{rand}"

def send_email(to_email, ref_id):
    msg = EmailMessage()
    msg["Subject"] = f"Issue Reported Successfully - {ref_id}"
    msg["From"] = "mukundarama123@gmail.com"
    msg["To"] = to_email
    msg.set_content(f"""
Dear Citizen,

Your issue has been successfully reported.

Reference ID: {ref_id}

Thank you for helping improve Andhra Pradesh.
""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("mukundarama123@gmail.com", "rtrj ecly zclk wrmq")
        smtp.send_message(msg)

# -----------------------------
# Andhra Pradesh Areas
# -----------------------------
AP_DISTRICTS = [
    "Anantapur", "Chittoor", "East Godavari", "West Godavari",
    "Guntur", "Krishna", "Kurnool", "Nellore",
    "Prakasam", "Srikakulam", "Visakhapatnam",
    "Vizianagaram", "Kadapa"
]

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Citizen Issue Reporting System", layout="centered")

st.title("🏙️ Citizen Issue Reporting System – Andhra Pradesh")
st.write("Report infrastructure-related issues across Andhra Pradesh")

with st.form("issue_form"):
    email = st.text_input("Email")

    city = st.selectbox("City", ["Andhra Pradesh"])
    area = st.selectbox("District", [""] + AP_DISTRICTS)
    street = st.text_input("Street / Locality")

    issue_type = st.selectbox(
        "Issue Type",
        ["", "Road Damage", "Street Light Not Working", "Water Leakage",
         "Garbage Overflow", "Drainage Problem"]
    )

    description = st.text_area("Issue Description")

    photo = st.file_uploader("Upload Issue Photo (optional)", type=["jpg", "png", "jpeg"])

    submitted = st.form_submit_button("Submit Issue")

# -----------------------------
# Submission Logic
# -----------------------------
if submitted:
    if not all([email, area, street, issue_type, description]):
        st.error("⚠️ Please fill all required fields")
    else:
        ref_id = generate_reference_id()

        photo_path = None
        if photo:
            photo_path = os.path.join(UPLOAD_DIR, f"{ref_id}_{photo.name}")
            with open(photo_path, "wb") as f:
                f.write(photo.getbuffer())

        issue = Issue(
            reference_id=ref_id,
            email=email,
            city=city,
            area=area,
            street=street,
            issue_type=issue_type,
            description=description,
            photo_path=photo_path
        )

        session.add(issue)
        session.commit()

        try:
            send_email(email, ref_id)
            st.success("✅ Issue submitted successfully!")
            st.info(f"📌 Reference ID: **{ref_id}**")
            st.write("A confirmation email has been sent.")
        except:
            st.warning("Issue saved, but email could not be sent.")
            st.info(f"Reference ID: {ref_id}")
