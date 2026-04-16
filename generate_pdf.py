from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from datetime import datetime

# Create PDF
pdf_path = r"docs/Newton-Raphson_Seminar_Script.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                        topMargin=0.75*inch, bottomMargin=0.75*inch,
                        leftMargin=0.75*inch, rightMargin=0.75*inch)

# Define styles
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=28,
    textColor=colors.HexColor('#1a1a1a'),
    spaceAfter=12,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#404040'),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName='Helvetica'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2c3e50'),
    spaceAfter=8,
    spaceBefore=12,
    fontName='Helvetica-Bold',
    borderColor=colors.HexColor('#3498db'),
    borderWidth=2,
    borderPadding=6,
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=11,
    textColor=colors.HexColor('#2c3e50'),
    alignment=TA_JUSTIFY,
    spaceAfter=10,
    leading=14,
    fontName='Helvetica'
)

# Story container
story = []

# ===== TITLE PAGE =====
story.append(Spacer(1, 1.5*inch))

# Main title
title = Paragraph("Newton–Raphson<br/>Learning GUI", title_style)
story.append(title)

story.append(Spacer(1, 0.3*inch))

# Subtitle
subtitle = Paragraph("Seminar Presentation Script", subtitle_style)
story.append(subtitle)

story.append(Spacer(1, 0.2*inch))

# Description
description = Paragraph(
    "An Interactive Educational Application for Understanding<br/>Numerical Methods and Root-Finding Algorithms",
    ParagraphStyle('desc', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, 
                   textColor=colors.HexColor('#555555'), spaceAfter=30)
)
story.append(description)

story.append(Spacer(1, 1.2*inch))

# Bottom info
info_text = f"<b>Presented on:</b> {datetime.now().strftime('%B %d, %Y')}<br/><b>Duration:</b> 5 Minutes (approximately 725 words)"
info = Paragraph(info_text, ParagraphStyle('info', parent=styles['Normal'], fontSize=10, 
                                           alignment=TA_CENTER, textColor=colors.HexColor('#666666')))
story.append(info)

story.append(PageBreak())

# ===== CONTENT =====

# Section 1: Introduction & Opening Hook
story.append(Paragraph("Introduction & Opening Hook", heading_style))
story.append(Paragraph(
    "Good morning, everyone. Have you ever wondered how computers find solutions to complex mathematical equations? "
    "Today, I'm excited to present an interactive learning application that transforms the way students understand one of "
    "the most powerful numerical methods in mathematics: the Newton-Raphson method.",
    body_style
))

# Section 2: Project Overview
story.append(Paragraph("Project Overview", heading_style))
story.append(Paragraph(
    "The Newton-Raphson Learning GUI is an educational application designed to help students visualize and understand "
    "the Newton-Raphson method—a fundamental algorithm used in mathematics, physics, and engineering to find the roots of equations. "
    "This project bridges the gap between theoretical knowledge and practical understanding by providing an interactive, step-by-step "
    "exploration of how this algorithm works.",
    body_style
))
story.append(Paragraph(
    "The application is packed with features including multiple pre-loaded functions, a real-time graphical visualization, "
    "bilingual support in English and Kurdish, and a unique step-by-step mode that allows learners to control their learning pace.",
    body_style
))

# Section 3: Main Idea and Purpose
story.append(Paragraph("Main Idea and Purpose", heading_style))
story.append(Paragraph(
    "The Newton-Raphson method can seem intimidating when presented only through equations and textbooks. Our mission is simple: "
    "make numerical methods accessible and engaging for students at all levels. Whether you're a high school student encountering "
    "this method for the first time or an engineer refreshing your knowledge, this application provides the perfect learning environment.",
    body_style
))
story.append(Paragraph(
    "The key purpose is to transform passive learning into active exploration. Instead of just reading about iterations and convergence, "
    "students can see them happen in real-time, manipulate parameters, and immediately observe the results.",
    body_style
))

# Section 4: How the Project Works
story.append(Paragraph("How the Project Works", heading_style))
story.append(Paragraph(
    "When you launch the application, you're presented with an intuitive interface organized into three main areas:",
    body_style
))

# Bullet points with custom formatting
bullet_points = [
    ("<b>Function Selection Panel:</b> We provide eight pre-configured mathematical functions including quadratic equations, "
     "trigonometric functions, exponential equations, and more. Users simply select their function and the system displays it on a graph."),
    ("<b>Parameter Configuration Section:</b> Users input three critical parameters: the initial guess (x₀), the tolerance level, "
     "and the maximum number of iterations. These parameters are crucial because they directly influence how quickly the algorithm converges."),
    ("<b>Execution Engine:</b> Users can click the 'Run' button to execute the complete algorithm automatically, or use the 'Step' button "
     "to proceed iteration by iteration. This step-by-step mode is particularly valuable for learning.")
]

for point in bullet_points:
    story.append(Paragraph("• " + point, body_style))

story.append(Paragraph(
    "The application displays results in multiple formats: a detailed data table showing each iteration, and a dynamic graph "
    "illustrating the convergence visually.",
    body_style
))

story.append(PageBreak())

# Section 5: How Users Can Use the Application
story.append(Paragraph("How Users Can Use the Application", heading_style))
story.append(Paragraph(
    "Upon opening the application, users are greeted with a clean interface in their preferred language—they can toggle between "
    "English and Kurdish with a single click. Start by selecting a mathematical function from the dropdown menu. Next, enter your "
    "initial guess and adjust the tolerance to determine how precise you want the solution to be.",
    body_style
))
story.append(Paragraph(
    "Then, you have two paths: run the complete algorithm at once to see the final result, or step through it manually. "
    "For educational purposes, the step-by-step approach is highly recommended as it builds genuine understanding.",
    body_style
))

# Section 6: Benefits and Educational Value
story.append(Paragraph("Benefits and Educational Value", heading_style))
story.append(Paragraph(
    "This application offers multiple learning benefits. <b>First,</b> it makes abstract mathematical concepts concrete and visible. "
    "<b>Second,</b> it enables experimentation—users can try different functions and parameters. <b>Third,</b> it provides immediate feedback. "
    "Additionally, the bilingual interface ensures accessibility for Kurdish-speaking students, breaking down language barriers in STEM education.",
    body_style
))

# Section 7: Design Philosophy
story.append(Paragraph("Design Philosophy", heading_style))
story.append(Paragraph(
    "Why did we choose this particular design approach? The answer lies in our core educational principle: <b>simplicity without sacrificing functionality.</b> "
    "The interface features a dark theme that reduces eye strain during extended study sessions. Controls are logically grouped by function, "
    "following natural reading patterns and mental models.",
    body_style
))
story.append(Paragraph(
    "We deliberately kept the interface clean and focused. Every button, textbox, and graph serves a clear educational purpose. "
    "The aesthetic design is modern and professional, creating an environment where students take their learning seriously.",
    body_style
))

# Section 8: Conclusion
story.append(Paragraph("Conclusion", heading_style))
story.append(Paragraph(
    "The Newton-Raphson Learning GUI represents a commitment to making mathematics education more accessible, engaging, and effective. "
    "By combining rigorous mathematical accuracy with intuitive design and interactive features, we've created a tool that transforms how "
    "students understand numerical methods. It's completely standalone—simply download and run the executable file, no additional software required.",
    body_style
))
story.append(Paragraph(
    "Thank you for your attention. I'm confident this tool will enhance mathematical learning and make the Newton-Raphson method not just "
    "understandable, but genuinely interesting.",
    body_style
))

story.append(Spacer(1, 0.3*inch))

# Footer with metadata
footer_text = "<i>Seminar Script • Approximately 5 minutes speaking time • 725 words</i>"
footer = Paragraph(footer_text, ParagraphStyle('footer', parent=styles['Normal'], fontSize=9, 
                                               alignment=TA_CENTER, textColor=colors.HexColor('#999999')))
story.append(footer)

# Build PDF
doc.build(story)

print(f"✓ PDF created successfully: {pdf_path}")
