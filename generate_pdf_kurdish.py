from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Arabic/Kurdish font - using a system font that supports RTL
# Note: You need to have a Kurdish-supporting font installed
try:
    # Try to use a font that supports Arabic/Kurdish script
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    font_name = 'Arial'
except:
    font_name = 'Helvetica'
    print("Note: Using default font. For proper Kurdish text, install a font that supports Arabic script.")

# Create PDF
pdf_path = r"docs/Newton-Raphson_Seminar_Script_KURDISH.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                        topMargin=0.75*inch, bottomMargin=0.75*inch,
                        leftMargin=0.75*inch, rightMargin=0.75*inch)

# Define styles
styles = getSampleStyleSheet()

# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1a1a1a'),
    spaceAfter=12,
    alignment=TA_RIGHT,
    fontName=font_name
)

subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Heading2'],
    fontSize=12,
    textColor=colors.HexColor('#404040'),
    spaceAfter=6,
    alignment=TA_RIGHT,
    fontName=font_name
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=13,
    textColor=colors.HexColor('#2c3e50'),
    spaceAfter=8,
    spaceBefore=12,
    fontName=font_name,
    borderColor=colors.HexColor('#3498db'),
    borderWidth=2,
    borderPadding=6,
    alignment=TA_RIGHT
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    textColor=colors.HexColor('#2c3e50'),
    alignment=TA_RIGHT,
    spaceAfter=10,
    leading=14,
    fontName=font_name
)

# Story container
story = []

# ===== TITLE PAGE =====
story.append(Spacer(1, 1.5*inch))

# Main title
title = Paragraph("نوێنەری - ڕاهێنانی نیوتن-رافسۆن", title_style)
story.append(title)

story.append(Spacer(1, 0.3*inch))

# Subtitle
subtitle = Paragraph("دەقی پێشکێشی سیمینار", subtitle_style)
story.append(subtitle)

story.append(Spacer(1, 0.2*inch))

# Description
description = Paragraph(
    "بەرنامەیەکی ڕاهێنگەرانەی ئیتریاکتیڤ بۆ تێگەیشتن<br/>میتۆدی ژمارەیی و ئالگۆریتمی دۆزینەوەی ڕیجە",
    ParagraphStyle('desc', parent=styles['Normal'], fontSize=11, alignment=TA_RIGHT, 
                   textColor=colors.HexColor('#555555'), spaceAfter=30, fontName=font_name)
)
story.append(description)

story.append(Spacer(1, 1.2*inch))

# Bottom info
info_text = f"<b>بۆ ڕاگەیاندنی:</b> {datetime.now().strftime('%B %d, %Y')}<br/><b>کاتی پێشکێشی:</b> 5 خولەک (تقریبی 725 وشە)"
info = Paragraph(info_text, ParagraphStyle('info', parent=styles['Normal'], fontSize=9, 
                                           alignment=TA_RIGHT, textColor=colors.HexColor('#666666'), fontName=font_name))
story.append(info)

story.append(PageBreak())

# ===== CONTENT =====

# Section 1: Introduction & Opening Hook
story.append(Paragraph("ناوپێچ و کردنەوەی هۆشیاری", heading_style))
story.append(Paragraph(
    "بەڕێز ئێوە. ئایا هیچ جار بیرتاندووتان کردووەتەوە کە چۆن کۆمپیوتەر تێدەگات حلی هاوکێشە ماتماتیکی مۆلّەکان بدۆزیتەوە؟ ئەمڕۆ من بە بێ دیگەلاڵ هیسبوومی بۆ پێشکێشکردنی بەرنامەیەکی ڕاهێنگەرانەی ئیتریاکتیڤ کە شێوەی تێگەیشتنی خوێندووان لە یەکێک لە هێزوەرترین ڕێگا و میتۆدەکانی ماتماتیک دێت دەگۆڕێت: میتۆدی نیوتن-رافسۆن.",
    body_style
))

# Section 2: Project Overview
story.append(Paragraph("دەربڕینی پڕۆژە", heading_style))
story.append(Paragraph(
    "نوێنەری - ڕاهێنانی نیوتن-رافسۆن بەرنامەیەکی فێرکاریانەیە کە تۆ کردووەتە دەسکاری بۆ خوێندووان تاکو میتۆدی نیوتن-رافسۆن تێ بگەن و بتوانن - میتۆدێکی بنچینەیی کە لە ماتماتیک و فیزیا و ئەندازیاردا بەکار دێت بۆ دۆزینەوەی ڕیجە ئەو هاوکێشانەی.",
    body_style
))
story.append(Paragraph(
    "بەرنامەکە پڕ نوێن بابەتەکان، ئەندام بەرنامەسازینە پێشتریان حاشاکراو، دەسکاریکردنی تێک کاری بەیانی تێبکاری، پاڵپشتی دو زمان (ئینگلیزی و کوردی)، و شێوەیەکی تایبەتی بڕێژ-بڕێژ کە دەشتێتە دەست خوێندووان هەتا خۆیان کۆنتڕۆل بکەن سیری خۆیان.",
    body_style
))

# Section 3: Main Idea and Purpose
story.append(Paragraph("بیرۆکەی سەرەکی و مەبەستی", heading_style))
story.append(Paragraph(
    "میتۆدی نیوتن-رافسۆن دەتوانێت تێخۆش و خێرایتێنار بێت کاتێک تەنیا لە ڕیکلام و پەڕە کتێبدا پێشکێش بکرێت. مەبەستمان سادەیە: ئامادە کردنی میتۆدی ژمارەیی تاکو بچووک و خۆشبینانە بن بۆ خوێندووانی ئێستا.",
    body_style
))
story.append(Paragraph(
    "مەبەستی سەرەکی ئەمە بریاری سێوان یان فێرکاریی ئاسایی بۆ دەرفەتی ئاتیۆمی. خوێندووان تۆماری دەکەن تەنیا گۆڕانکاری و هەڵگرتن، ئێستا دەتوانن بیبینن بەیانی بڕێژ بڕێژ.",
    body_style
))

# Section 4: How the Project Works
story.append(Paragraph("چۆن پڕۆژەکە کاردەکات", heading_style))
story.append(Paragraph(
    "کاتێک بەرنامەکە بکەیت، تۆ هیسبووتی دێت پێ رووپێلی رێک تیاتەر چێتر بر:",
    body_style
))

story.append(Paragraph(
    "<b>یەكەم</b>: پەنجەرەی دەرچوونی ئەندامەکان. ئێمە شەش پێشتری ئەندام ماتماتیکی حاشاکراو دیتان تێ.",
    body_style
))
story.append(Paragraph(
    "<b>دووەم</b>: بەشی سازکردنی پاڕامیتر. خوێندووان سێ پاڕامیتری زۆر گرینگ تێوە: بیرۆکەی ئابووری، لا قبولاندن، و بەر خشتاندنی ژمارەیی.",
    body_style
))
story.append(Paragraph(
    "<b>سێيەم</b>: چاپکەری ڕاسپاردە. خوێندووان دەتوانن دۆڤەی \"ڕاگەیاندن\" تێ کلیک بکەن یاخود دۆڤەی \"گام\" بۆ گام بڕێژ بڕێژ.",
    body_style
))

story.append(PageBreak())

# Section 5: How Users Can Use the Application
story.append(Paragraph("چۆن خوێندووان بەرنامەکە بەکار بێنن", heading_style))
story.append(Paragraph(
    "ئەم تەجریبە نیسە سادەیە و سەلیم. کاتێک بەرنامەکە بکەیت، خوێندووان هیسبووتی دێ رووپێلی بە زمانی خۆیانی فێرکاری.",
    body_style
))
story.append(Paragraph(
    "ئەتە بە ئەندام ماتماتیکی لە مەنیویی دەرچوونە دیاریبکە. خوالیف بیرۆکەی خۆت تێ دا و بیرۆکەی قبول و ئیمتیجان دەبێتە سێتڤ تاکو هیسبووتی لێ ببینی چەندە درووست.",
    body_style
))

# Section 6: Benefits and Educational Value
story.append(Paragraph("فیدەی فێرکاری", heading_style))
story.append(Paragraph(
    "ئەم بەرنامەیە چه فیدەیی فێرکاری دیت. خوێندووان دەتوانن بیبینن هاوکێشە پێک دێن لە یەبار ئاستی. خوێندووان دەتوانن ئەندام، بیرۆکە ئابووری، و پاڕامیتری جیاواز تریسن. رێزبەری دوو زمان تێدا هێنانی بۆ دەسکاری بۆ خوێندووانی کوردی.",
    body_style
))

# Section 7: Design Philosophy
story.append(Paragraph("فیلسفەی دیزاین", heading_style))
story.append(Paragraph(
    "بۆ چی ئێمە ئەم شێوازی دیزاین هەڵبژاردمان؟ وەڵام نیسە لە بیرۆکە سەرەکی <b>سادگی بە بێ بە کهداری سفت</b>. رووپێلی رێکی نرۆ تاریخ بینی بەبێ تێل چاوی خوێندوو.",
    body_style
))
story.append(Paragraph(
    "ئێمە بھۆشیاری خستمان رووپێلی بە دەسنیت و فۆکوس. هەریەک لە دۆڤە، بۆکس نووسین، و تێک کاری فانکشنی خۆ ڕێ دێت.",
    body_style
))

# Section 8: Conclusion
story.append(Paragraph("بنکەم", heading_style))
story.append(Paragraph(
    "نوێنەری - ڕاهێنانی نیوتن-رافسۆن تێدا وێنایە پڕستیڕی بۆ کردنی فێرکاری ماتماتیک بیرتۆڕ، بەخۆشی، و کاریگەر.",
    body_style
))
story.append(Paragraph(
    "ئایا تۆ وانگێڕی کورسی کالکۆلۆس، فێرکاری خۆت، یا تێی فانکشنی میتۆدی ژمارەیی - ئەم بەرنامەیە بە دروستی و ئیتریاکتیڤیتێتی تێ دەپێویستی. سپاس بۆ توان گوێم لێ بدی!",
    body_style
))

story.append(Spacer(1, 0.3*inch))

# Footer with metadata
footer_text = "<i>دەقی سیمینار • تقریبی 5 خولەک سێی قسی • 725 وشە</i>"
footer = Paragraph(footer_text, ParagraphStyle('footer', parent=styles['Normal'], fontSize=9, 
                                               alignment=TA_CENTER, textColor=colors.HexColor('#999999'), fontName=font_name))
story.append(footer)

# Build PDF
doc.build(story)

print(f"✓ PDF Kurdish created successfully: {pdf_path}")
