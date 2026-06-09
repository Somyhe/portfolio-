# -*- coding: utf-8 -*-
"""
University Academic Calendar PDF - Najran University
التقويم الأكاديمي لجامعة نجران للعام ١٤٤٨-١٤٤٩ هـ
"""

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ─── Register Arabic Fonts (Traditional Arabic — full Presentation Form coverage) ─
FONTS_DIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("TradArabic",     os.path.join(FONTS_DIR, "trado.ttf")))
pdfmetrics.registerFont(TTFont("TradArabicBold", os.path.join(FONTS_DIR, "tradbdo.ttf")))
pdfmetrics.registerFont(TTFont("ArabType",       os.path.join(FONTS_DIR, "arabtype.ttf")))

FONT_REG  = "ArabType"
FONT_BOLD = "TradArabicBold"
FONT_BODY = "ArabType"

# ─── Colour palette ───────────────────────────────────────────────────────────
NAVY        = colors.HexColor("#1B3A6B")
BLUE_MED    = colors.HexColor("#2F5496")
BLUE_LIGHT  = colors.HexColor("#DEEAF6")
GOLD        = colors.HexColor("#C4951A")
WHITE       = colors.white
GRAY_LIGHT  = colors.HexColor("#F5F7FA")
TEXT_DARK   = colors.HexColor("#1A1A2E")
GREEN_DARK  = colors.HexColor("#1B6B3A")
GREEN_LIGHT = colors.HexColor("#E8F5EE")
GREEN_LIGHT2= colors.HexColor("#F4FBF7")

PAGE_W, PAGE_H = A4
MARGIN = 1.5 * cm

# ─── Arabic helper ────────────────────────────────────────────────────────────
def ar(text: str) -> str:
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

def arp(text: str, style) -> Paragraph:
    return Paragraph(ar(text), style)

# ─── Styles ───────────────────────────────────────────────────────────────────
def S(name, **kw) -> ParagraphStyle:
    defaults = dict(fontName=FONT_BODY, fontSize=9, leading=14, wordWrap="RTL",
                    leftIndent=0, rightIndent=0, spaceAfter=0, spaceBefore=0)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

ST = {
    # Banner
    "gov":      S("gov",  fontName=FONT_BOLD,  fontSize=10, alignment=TA_CENTER,
                  textColor=colors.HexColor("#BDD7EE"), leading=16, backColor=NAVY),
    "univ":     S("univ", fontName=FONT_BOLD,  fontSize=13, alignment=TA_CENTER,
                  textColor=colors.HexColor("#D9E8F7"), leading=20, backColor=NAVY),
    "title":    S("title",fontName=FONT_BOLD,  fontSize=21, alignment=TA_CENTER,
                  textColor=WHITE, leading=32, backColor=NAVY),
    "year":     S("year", fontName=FONT_BOLD,  fontSize=13, alignment=TA_CENTER,
                  textColor=GOLD,  leading=20, backColor=NAVY),
    # Section header
    "sec":      S("sec",  fontName=FONT_BOLD,  fontSize=13, alignment=TA_CENTER,
                  textColor=WHITE, leading=20),
    # Table header cell
    "thdr":     S("thdr", fontName=FONT_BOLD,  fontSize=9.5, alignment=TA_CENTER,
                  textColor=NAVY, leading=14),
    "thdr_g":   S("thdr_g",fontName=FONT_BOLD, fontSize=9.5, alignment=TA_CENTER,
                  textColor=colors.HexColor("#004d26"), leading=14),
    # Table data cells
    "act":      S("act",  fontName=FONT_BODY,  fontSize=9,   alignment=TA_RIGHT,
                  textColor=TEXT_DARK, leading=14),
    "ctr":      S("ctr",  fontName=FONT_BODY,  fontSize=9,   alignment=TA_CENTER,
                  textColor=TEXT_DARK, leading=14),
    "act_g":    S("act_g",fontName=FONT_BODY,  fontSize=9,   alignment=TA_RIGHT,
                  textColor=TEXT_DARK, leading=14),
    "ctr_g":    S("ctr_g",fontName=FONT_BODY,  fontSize=9,   alignment=TA_CENTER,
                  textColor=TEXT_DARK, leading=14),
    # Summary bar
    "sum_lbl":  S("sum_lbl", fontName=FONT_BOLD, fontSize=9,  alignment=TA_CENTER,
                  textColor=WHITE, leading=14),
    "sum_val":  S("sum_val", fontName=FONT_BOLD, fontSize=13, alignment=TA_CENTER,
                  textColor=GOLD,  leading=18),
    "sum_lbl_g":S("sum_lbl_g", fontName=FONT_BOLD, fontSize=9,  alignment=TA_CENTER,
                  textColor=WHITE, leading=14),
    "sum_val_g":S("sum_val_g", fontName=FONT_BOLD, fontSize=13, alignment=TA_CENTER,
                  textColor=colors.HexColor("#AAEECC"), leading=18),
    # Footer
    "foot":     S("foot",  fontName=FONT_BODY, fontSize=7.5, alignment=TA_CENTER,
                  textColor=WHITE, leading=11),
}

# ─── Page background & footer ─────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4

    # Page background
    canvas.setFillColor(colors.HexColor("#FAFBFD"))
    canvas.rect(0, 0, w, h, fill=1, stroke=0)

    # Left/right accent stripes (within margin so they don't cover content)
    canvas.setFillColor(colors.HexColor("#EEF3FB"))
    canvas.rect(0, 0, 12, h, fill=1, stroke=0)
    canvas.rect(w - 12, 0, 12, h, fill=1, stroke=0)

    # Footer bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 22, w, 2, fill=1, stroke=0)

    # Footer text
    canvas.setFont(FONT_BODY, 7)
    canvas.setFillColor(WHITE)
    ft = ar("جامعة نجران  |  التقويم الأكاديمي للعام الجامعي ١٤٤٨-١٤٤٩ هـ")
    canvas.drawCentredString(w / 2, 7, ft)

    # Page number
    canvas.setFont(FONT_BODY, 7)
    canvas.setFillColor(colors.HexColor("#AAAAAA"))
    canvas.drawRightString(w - 16, 7, f"{doc.page}")

    canvas.restoreState()


# ─── Table builder (RTL: columns reversed so action is on the RIGHT) ──────────
#
# Visual column order (right → left in Arabic reading direction):
#   الإجراء | تبدأ يوم | التاريخ | تنتهي يوم | التاريخ
#
# In LTR reportlab rendering we reverse to:
#   [التاريخ, تنتهي يوم, التاريخ, تبدأ يوم, الإجراء]
#   col idx:  0            1          2          3          4

def _row(action, sd, sdate, ed, edate, a_st, c_st):
    """Build one data row in RTL-reversed column order."""
    return [
        arp(edate or "—", c_st),
        arp(ed    or "—", c_st),
        arp(sdate or "—", c_st),
        arp(sd    or "—", c_st),
        arp(action,       a_st),
    ]

def build_table(rows_data, TW, header_start_label="تبدأ يوم",
                header_end_label="تنتهي يوم",
                th_style="thdr", act_style="act", ctr_style="ctr",
                hdr_bg=BLUE_LIGHT, hdr_txt=NAVY, border=NAVY):
    # Widths: reversed order [end_date, end_day, start_date, start_day, action]
    col_w = [TW*0.19, TW*0.10, TW*0.16, TW*0.10, TW*0.45]
    header = [
        arp("التاريخ",          ST[th_style]),
        arp(header_end_label,   ST[th_style]),
        arp("التاريخ",          ST[th_style]),
        arp(header_start_label, ST[th_style]),
        arp("الإجراء",          ST[th_style]),
    ]
    data = [header] + [_row(a, sd, sdt, ed, edt, ST[act_style], ST[ctr_style])
                       for (a, sd, sdt, ed, edt) in rows_data]

    tbl = Table(data, colWidths=col_w, repeatRows=1)
    alt = [GRAY_LIGHT, WHITE]
    tbl.setStyle(TableStyle([
        ("BACKGROUND",      (0, 0), (-1, 0),  hdr_bg),
        ("ROWBACKGROUNDS",  (0, 1), (-1, -1), alt),
        ("VALIGN",          (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN",           (0, 0), (-1, 0),  "CENTER"),
        ("ALIGN",           (0, 1), (-2, -1), "CENTER"),
        ("ALIGN",           (-1, 1),(-1, -1), "RIGHT"),
        ("LINEBELOW",       (0, 0), (-1, 0),  1.5, border),
        ("LINEBELOW",       (0, 1), (-1, -1), 0.3, colors.HexColor("#CCCCCC")),
        ("BOX",             (0, 0), (-1, -1), 1,   border),
        ("TOPPADDING",      (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",   (0, 0), (-1, -1), 5),
        ("LEFTPADDING",     (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",    (0, 0), (-1, -1), 5),
    ]))
    return tbl


def summary_bar(weeks, days, TW, is_green=False):
    lbl = "sum_lbl_g" if is_green else "sum_lbl"
    val = "sum_val_g" if is_green else "sum_val"
    bg  = GREEN_DARK if is_green else NAVY
    brd = colors.HexColor("#AAEECC") if is_green else GOLD

    data = [[
        arp(days,             ST[val]),
        arp("عدد الأيام الدراسية", ST[lbl]),
        arp(weeks,            ST[val]),
        arp("عدد الأسابيع",  ST[lbl]),
    ]]
    col_w = [TW*0.20, TW*0.30, TW*0.20, TW*0.30]
    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), bg),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("BOX",          (0, 0), (-1, -1), 1.5, brd),
        ("LINEAFTER",    (1, 0), (1, 0),   1, brd),
    ]))
    return t


def sec_header(text, TW, bg=BLUE_MED, accent=GOLD, txt_style="sec"):
    data = [[arp(text, ST[txt_style])]]
    t = Table(data, colWidths=[TW])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, -1), bg),
        ("TOPPADDING",   (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("LEFTPADDING",  (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("LINEABOVE",    (0, 0), (-1, 0),  3, accent),
        ("LINEBELOW",    (0, -1),(-1, -1), 1, NAVY),
    ]))
    return t


# ─── Data ─────────────────────────────────────────────────────────────────────
SEM1 = [
    ("استقبال طلبات إعادة القيد (للمنسحب والمطوي قيده) وطلبات الفرص الإضافية إلكترونياً للفصل الأول",
     "الأحد", "٢٨-١٢-١٤٤٧ هـ / 14-6-2026", "الثلاثاء", "١-١-١٤٤٨ هـ / 16-6-2026"),
    ("استقبال طلبات التحويل الخارجي (من وإلى جامعة نجران) إلكترونياً للفصل الأول",
     "الأربعاء", "٢-١-١٤٤٨ هـ / 17-6-2026", "الأحد", "٦-١-١٤٤٨ هـ / 21-6-2026"),
    ("التقديم على التحويل الداخلي للفصل الأول وطلبات تأجيل الدراسة إلكترونياً",
     "الإثنين", "٢٧-٢-١٤٤٨ هـ / 10-8-2026", "الأربعاء", "٢٩-٢-١٤٤٨ هـ / 12-8-2026"),
    ("تسجيل المقررات والحذف والإضافة للفصل الدراسي الأول",
     "الأحد", "٣-٣-١٤٤٨ هـ / 16-8-2026", "الثلاثاء", "٥-٣-١٤٤٨ هـ / 18-8-2026"),
    ("طلبات الزيارة (من وإلى جامعة نجران) إلكترونياً",
     "الأحد", "٣-٣-١٤٤٨ هـ / 16-8-2026", "الخميس", "٧-٣-١٤٤٨ هـ / 20-8-2026"),
    ("معادلة المقررات الدراسية",
     "الأحد", "٣-٣-١٤٤٨ هـ / 16-8-2026", "الخميس", "٧-٣-١٤٤٨ هـ / 20-8-2026"),
    ("عودة أعضاء هيئة التدريس",
     "الأحد", "٣-٣-١٤٤٨ هـ / 16-8-2026", None, None),
    ("بداية الدراسة للفصل الدراسي الأول",
     "الأحد", "١٠-٣-١٤٤٨ هـ / 23-8-2026", None, None),
    ("آخر موعد للرفع بنتائج الاختبارات البديلة",
     "الخميس", "١٤-٣-١٤٤٨ هـ / 27-8-2026", None, None),
    ("إجازة اليوم الوطني",
     "الأربعاء", "١٢-٤-١٤٤٨ هـ / 23-9-2026", "السبت", "١٥-٤-١٤٤٨ هـ / 26-9-2026"),
    ("إجازة منتصف الفصل الدراسي الأول (إجازة الخريف)",
     "الخميس (نهاية الدوام)", "٩-٦-١٤٤٨ هـ / 19-11-2026", None, None),
    ("استئناف الدراسة بعد إجازة منتصف الفصل الأول",
     "الأحد", "١٩-٦-١٤٤٨ هـ / 29-11-2026", None, None),
    ("آخر موعد للاعتذار عن الفصل / آخر موعد للاعتذار عن مقرر",
     "الخميس", "١-٧-١٤٤٨ هـ / 10-12-2026", None, None),
    ("الاختبارات النهائية للفصل الدراسي الأول",
     "الأحد", "١١-٧-١٤٤٨ هـ / 20-12-2026", "الخميس", "٢٩-٧-١٤٤٨ هـ / 7-1-2027"),
    ("بداية إجازة منتصف العام الجامعي",
     "الخميس (نهاية الدوام)", "٢٩-٧-١٤٤٨ هـ / 7-1-2027", None, None),
]

SEM2 = [
    ("استقبال طلبات إعادة القيد (للمنسحب والمطوي قيده) وطلبات الفرص الإضافية إلكترونياً للفصل الثاني",
     "الخميس", "٢٩-٧-١٤٤٨ هـ / 7-1-2027", "الأحد", "٢-٨-١٤٤٨ هـ / 10-1-2027"),
    ("التقديم على التحويل الداخلي للفصل الثاني إلكترونياً",
     "الإثنين", "٣-٨-١٤٤٨ هـ / 11-1-2027", "الأربعاء", "٥-٨-١٤٤٨ هـ / 13-1-2027"),
    ("طلبات تأجيل الدراسة / التحويل الخارجي / طلبات الزائرين إلكترونياً",
     "الخميس", "٦-٨-١٤٤٨ هـ / 14-1-2027", "الإثنين", "١٠-٨-١٤٤٨ هـ / 18-1-2027"),
    ("تسجيل المقررات والحذف والإضافة للفصل الدراسي الثاني",
     "الخميس", "٦-٨-١٤٤٨ هـ / 14-1-2027", "الإثنين", "١٠-٨-١٤٤٨ هـ / 18-1-2027"),
    ("بداية الدراسة للفصل الدراسي الثاني",
     "الأحد", "٩-٨-١٤٤٨ هـ / 17-1-2027", None, None),
    ("معادلة المقررات الدراسية",
     "الأحد", "٩-٨-١٤٤٨ هـ / 17-1-2027", "الخميس", "١٣-٨-١٤٤٨ هـ / 21-1-2027"),
    ("آخر موعد للرفع بنتائج الاختبارات البديلة",
     "الإثنين", "١٧-٨-١٤٤٨ هـ / 25-1-2027", None, None),
    ("إجازة يوم التأسيس",
     "الجمعة", "١٢-٩-١٤٤٨ هـ / 19-2-2027", "الإثنين", "١٥-٩-١٤٤٨ هـ / 22-2-2027"),
    ("بداية إجازة عيد الفطر",
     "الخميس (نهاية الدوام)", "١٨-٩-١٤٤٨ هـ / 25-2-2027", None, None),
    ("استئناف الدراسة بعد إجازة عيد الفطر",
     "الأحد", "٦-١٠-١٤٤٨ هـ / 14-3-2027", None, None),
    ("إجازة عيد الأضحى",
     "الخميس (نهاية الدوام)", "٢٩-١١-١٤٤٨ هـ / 6-5-2027", None, None),
    ("آخر موعد للاعتذار عن الفصل / آخر موعد للاعتذار عن مقرر",
     "الخميس", "٢١-١٢-١٤٤٨ هـ / 27-5-2027", None, None),
    ("بدء وانتهاء الاختبارات النهائية للفصل الدراسي الثاني",
     "الأحد", "٢٤-١٢-١٤٤٨ هـ / 30-5-2027", "الخميس", "١٢-١-١٤٤٩ هـ / 17-6-2027"),
    ("بداية إجازة العام الدراسي ١٤٤٨-١٤٤٩ هـ للطلاب",
     "الخميس (نهاية الدوام)", "١٢-١-١٤٤٩ هـ / 17-6-2027", None, None),
    ("بداية إجازة العام الدراسي لأعضاء هيئة التدريس",
     "الإثنين (نهاية الدوام)", "١٦-١-١٤٤٩ هـ / 21-6-2027", None, None),
    ("عودة أعضاء هيئة التدريس",
     "الأحد", "١٣-٣-١٤٤٩ هـ / 15-8-2027", None, None),
    ("بداية الدراسة للعام الجامعي ١٤٤٩-١٤٥٠ هـ",
     "الأحد", "٢٠-٣-١٤٤٩ هـ / 22-8-2027", None, None),
]

SUMMER = [
    ("بداية فترة التسجيل والحذف والإضافة",
     "الأحد", "١-١-١٤٤٩ هـ / 6-6-2027", "الخميس", "١٢-١-١٤٤٩ هـ / 17-6-2027"),
    ("بداية الدراسة للفصل الصيفي",
     "الأحد", "١٥-١-١٤٤٩ هـ / 20-6-2027", None, None),
    ("بداية الاختبارات النهائية للفصل الصيفي",
     "الأحد", "١٣-٣-١٤٤٩ هـ / 15-8-2027", None, None),
    ("نهاية اختبارات الفصل الصيفي",
     "الثلاثاء", "١٥-٣-١٤٤٩ هـ / 17-8-2027", None, None),
    ("إغلاق أعمال الفصل الصيفي",
     "الثلاثاء", "١٥-٣-١٤٤٩ هـ / 17-8-2027", None, None),
]


# ─── Build PDF ────────────────────────────────────────────────────────────────
def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=1.8 * cm,
        onFirstPage=on_page, onLaterPages=on_page,
    )

    TW = PAGE_W - 2 * MARGIN
    story = []

    # ── Header banner ─────────────────────────────────────────────────────────
    banner_rows = [
        [arp("المملكة العربية السعودية  |  وزارة التعليم", ST["gov"])],
        [arp("جامعة نجران", ST["univ"])],
        [arp("التقويم الأكاديمي للعام الجامعي", ST["title"])],
        [arp("١٤٤٨ – ١٤٤٩ هـ", ST["year"])],
    ]
    banner = Table(banner_rows, colWidths=[TW])
    banner.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), NAVY),
        ("TOPPADDING",    (0, 0), (-1, 0),  12),
        ("TOPPADDING",    (0, 1), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -2), 2),
        ("BOTTOMPADDING", (0, -1),(-1, -1), 12),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("LINEABOVE",     (0, 0), (-1, 0),  5, GOLD),
        ("LINEBELOW",     (0, -1),(-1, -1), 3, GOLD),
    ]))
    story.append(banner)
    story.append(Spacer(1, 5 * mm))

    # ── Semester 1 ────────────────────────────────────────────────────────────
    story.append(sec_header("الفصل الدراسي الأول   |   ١٤٤٨ – ١٤٤٩ هـ", TW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(build_table(SEM1, TW))
    story.append(Spacer(1, 2 * mm))
    story.append(summary_bar("١٩", "٩٣", TW))
    story.append(Spacer(1, 6 * mm))

    # ── Semester 2 ────────────────────────────────────────────────────────────
    story.append(sec_header("الفصل الدراسي الثاني   |   ١٤٤٨ – ١٤٤٩ هـ", TW))
    story.append(Spacer(1, 1.5 * mm))
    story.append(build_table(SEM2, TW))
    story.append(Spacer(1, 2 * mm))
    story.append(summary_bar("١٨", "٨٨", TW))
    story.append(Spacer(1, 6 * mm))

    # ── Summer ────────────────────────────────────────────────────────────────
    story.append(sec_header("الفصل الدراسي الصيفي   |   ١٤٤٨ – ١٤٤٩ هـ", TW,
                             bg=GREEN_DARK, accent=GOLD))
    story.append(Spacer(1, 1.5 * mm))
    story.append(build_table(
        SUMMER, TW,
        header_start_label="اليوم",
        header_end_label="اليوم",
        th_style="thdr_g", act_style="act_g", ctr_style="ctr_g",
        hdr_bg=GREEN_LIGHT, hdr_txt=colors.HexColor("#004d26"),
        border=GREEN_DARK,
    ))
    story.append(Spacer(1, 2 * mm))

    # Summer summary (weeks only)
    s_sum = [[
        arp("٨",          ST["sum_val_g"]),
        arp("عدد الأسابيع", ST["sum_lbl_g"]),
    ]]
    s_sum_t = Table(s_sum, colWidths=[TW * 0.20, TW * 0.80])
    s_sum_t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), GREEN_DARK),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("BOX",           (0, 0), (-1, -1), 1.5, GOLD),
    ]))
    story.append(s_sum_t)

    doc.build(story)
    print(f"✓ PDF saved: {output_path}")


if __name__ == "__main__":
    out = r"C:\Users\sarah\portfolio\التقويم_الأكاديمي_١٤٤٨.pdf"
    build_pdf(out)
