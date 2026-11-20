import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import pymupdf

pdf_path = "c:\\python\\Ai\\local-ai-chatbot\\Patil_Rushikesh_Resume.pdf"

# Document setup with tight professional margins to comfortably fit 1 page
margin = 36  # 0.5 inch
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=margin,
    rightMargin=margin,
    topMargin=32,
    bottomMargin=32
)

styles = getSampleStyleSheet()

# Custom styles
primary_color = colors.HexColor("#1A1A1A")
header_line_color = colors.HexColor("#222222")
link_color = colors.HexColor("#0D47A1")

name_style = ParagraphStyle(
    "ResumeName",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=18,
    leading=22,
    alignment=TA_CENTER,
    textColor=primary_color,
)

contact_style = ParagraphStyle(
    "ResumeContact",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=11.5,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#333333"),
)

section_heading_style = ParagraphStyle(
    "SectionHeading",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=10.5,
    leading=13,
    alignment=TA_LEFT,
    textColor=primary_color,
    spaceBefore=5,
    spaceAfter=2,
)

body_style = ParagraphStyle(
    "ResumeBody",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=11.5,
    alignment=TA_JUSTIFY,
    textColor=colors.HexColor("#262626"),
)

bold_label_style = ParagraphStyle(
    "BoldLabel",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.5,
    leading=11.5,
    textColor=primary_color,
)

bullet_style = ParagraphStyle(
    "ResumeBullet",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.3,
    leading=11,
    textColor=colors.HexColor("#2A2A2A"),
    leftIndent=12,
    firstLineIndent=-8,
    spaceAfter=1.5,
)

story = []

# --- Header ---
story.append(Paragraph("PATIL RUSHIKESH", name_style))
story.append(Spacer(1, 3))

contact_line_1 = (
    "Surat, Gujarat &nbsp;|&nbsp; +91 8347613073 &nbsp;|&nbsp; "
    "<a href='mailto:rushikesh14703@gmail.com' color='#0D47A1'>rushikesh14703@gmail.com</a>"
)
story.append(Paragraph(contact_line_1, contact_style))

contact_line_2 = (
    "<a href='https://www.linkedin.com/in/rushikesh-patil140703/' color='#0D47A1'>linkedin.com/in/rushikesh-patil140703</a>"
    " &nbsp;|&nbsp; "
    "<a href='https://github.com/RushikeshPatil1373' color='#0D47A1'>github.com/RushikeshPatil1373</a>"
)
story.append(Paragraph(contact_line_2, contact_style))
story.append(Spacer(1, 4))

def add_section_header(title):
    return [
        Paragraph(title, section_heading_style),
        HRFlowable(width="100%", thickness=0.8, color=header_line_color, spaceBefore=1, spaceAfter=4)
    ]

# --- Profile Summary ---
story.extend(add_section_header("PROFILE SUMMARY"))
summary_text = (
    "MCA (Semester 3) student with hands-on expertise in Python development, Machine Learning, and "
    "Generative AI / RAG architectures. Proficient in building end-to-end ML & RAG pipelines, working with "
    "LangChain, Vector Databases (ChromaDB), Scikit-learn, and Streamlit. Completed a 30-day AI/ML virtual internship. "
    "Seeking opportunities to leverage strong problem-solving and software development skills as a Python / AI-ML Developer."
)
story.append(Paragraph(summary_text, body_style))
story.append(Spacer(1, 4))

# --- Education ---
story.extend(add_section_header("EDUCATION"))

edu_items = [
    (
        "<b>MCA (Master of Computer Applications)</b> &mdash; SCET (Sarvajanik College of Engineering & Technology)",
        "2025 &ndash; 2027",
        "Pursuing, Semester 3 &nbsp;|&nbsp; CGPA: <b>8.59</b> (till Sem 2)"
    ),
    (
        "<b>BCA (Bachelor of Computer Applications)</b> &mdash; Vimal Tormal Poddar BCA College, Pandesara &mdash; VNSGU",
        "2021 &ndash; 2024",
        "CGPA: <b>7.94</b>"
    ),
    (
        "<b>HSC (12th)</b> &mdash; Shri Chhatrapati Shivaji Marathi Medium School &mdash; GSHSEB",
        "2022",
        "Score: <b>66%</b>"
    ),
    (
        "<b>SSC (10th)</b> &mdash; Suman High School No. 5 &mdash; GSHSEB",
        "2020",
        "Score: <b>65%</b>"
    ),
]

for title, year, grade in edu_items:
    table_data = [
        [
            Paragraph(f"{title} &nbsp;<font color='#555555'>({grade})</font>", body_style),
            Paragraph(f"<b>{year}</b>", ParagraphStyle("RightYear", parent=body_style, alignment=2))
        ]
    ]
    t = Table(table_data, colWidths=[450, 90])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t)

story.append(Spacer(1, 4))

# --- Technical Skills ---
story.extend(add_section_header("TECHNICAL SKILLS"))

skills = [
    ("Languages", "Python, Java, C, C++, PHP, HTML, CSS, JavaScript"),
    ("AI / LLM & RAG", "LangChain, ChromaDB, Ollama (Llama, Qwen), PyMuPDF, RAG Pipeline, Embeddings"),
    ("Frameworks & Libraries", "Streamlit, Scikit-learn, Django, CodeIgniter, Pandas, NumPy, Polars"),
    ("Databases", "MySQL, SQLite3, MongoDB"),
    ("Tools & Platforms", "Git/GitHub, VS Code, PyCharm, Postman, Pytest")
]

skill_table_data = []
for cat, items in skills:
    skill_table_data.append([
        Paragraph(f"<b>{cat}:</b>", bold_label_style),
        Paragraph(items, body_style)
    ])

st_table = Table(skill_table_data, colWidths=[125, 415])
st_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
    ('TOPPADDING', (0, 0), (-1, -1), 1.5),
    ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ('RIGHTPADDING', (0, 0), (-1, -1), 0),
]))
story.append(st_table)
story.append(Spacer(1, 4))

# --- Projects ---
story.extend(add_section_header("PROJECTS"))

# Project 1: Local AI Chatbot with Multi-Format RAG
story.append(Paragraph("<b>Local AI Chatbot with Multi-Format RAG (PDF & TXT)</b>", bold_label_style))
story.append(Paragraph(
    "<i><b>Tech Stack:</b> Python, Streamlit, LangChain, ChromaDB, Ollama, PyMuPDF, Nomic Embeddings, Pytest</i>",
    ParagraphStyle("TechStack", parent=body_style, fontSize=8.2, textColor=colors.HexColor("#444444"), spaceAfter=2)
))
p1_bullets = [
    "Architected an end-to-end local <b>Retrieval-Augmented Generation (RAG)</b> system enabling conversational Q&amp;A over uploaded <b>TXT and multi-page PDF documents</b>.",
    "Integrated <b>PyMuPDF</b> for high-speed page extraction, <b>RecursiveCharacterTextSplitter</b> for chunking, and <b>ChromaDB vector store</b> with <b>Ollama embeddings</b> for semantic similarity search.",
    "Built a modern <b>Streamlit</b> interface featuring multi-file uploads, real-time relevant chunk inspection, and conversational memory management.",
    "Engineered a comprehensive automated test suite with <b>Pytest</b> covering single/multi-page PDF parsing, error cases, and vector store operations."
]
for b in p1_bullets:
    story.append(Paragraph(f"&bull; &nbsp;{b}", bullet_style))

story.append(Spacer(1, 3))

# Project 2: Spam Email Classifier
story.append(Paragraph("<b>Spam Email Classifier</b>", bold_label_style))
story.append(Paragraph(
    "<i><b>Tech Stack:</b> Python, Scikit-learn, Multinomial Naive Bayes, Streamlit, Pandas, Polars, NumPy, Pickle</i>",
    ParagraphStyle("TechStack2", parent=body_style, fontSize=8.2, textColor=colors.HexColor("#444444"), spaceAfter=2)
))
p2_bullets = [
    "Developed a robust Email Spam Classifier utilizing <b>Multinomial Naive Bayes</b> in Python with Scikit-learn.",
    "Designed an optimized data pipeline for text preprocessing, tokenization, feature extraction, and model training using <b>Pandas, Polars, and NumPy</b>.",
    "Built and deployed an interactive <b>Streamlit</b> web application for real-time spam prediction with model serialization via <b>Pickle</b>."
]
for b in p2_bullets:
    story.append(Paragraph(f"&bull; &nbsp;{b}", bullet_style))

story.append(Spacer(1, 4))

# --- Certifications ---
story.extend(add_section_header("CERTIFICATIONS"))
cert_text = (
    "&bull; &nbsp;<b>30-Day Virtual Internship Programme on Artificial Intelligence and Machine Learning</b> &mdash; "
    "Kodacy, in association with SPACE (Scientific Platforms And Cosmic Explorations) &mdash; September 2025."
)
story.append(Paragraph(cert_text, bullet_style))

doc.build(story)
print(f"Resume generated at: {pdf_path}")

# Check page count
doc_pdf = pymupdf.open(pdf_path)
print(f"Total Page Count: {len(doc_pdf)}")
doc_pdf.close()
