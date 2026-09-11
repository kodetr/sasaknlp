#!/usr/bin/env python3
"""Script to generate publication-ready Word DOCX manuscripts in both English and Indonesian,
conforming strictly to the ECTI template specifications.

Enhancement:
- Wide tables and figures that do not fit in a narrow 3.2" single column span the full page width (6.5")
  using continuous 1-column sections, then seamlessly resume the 2-column body layout.
- Prevents table row splitting across pages (<w:cantSplit/>).
- Keeps captions together with figures and tables (<w:keepNext/>).

Journal Target: ECTI Transactions on Computer and Information Technology (ECTI-CIT)
"""

import os
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Set shading background color for a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    """Set inner cell padding (in dxa: 20 dxa = 1 pt)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)

def set_table_borders(table, color="000000", sz="4", val="single"):
    """Set standard academic three-line borders (top, header bottom, bottom)."""
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tbl_pr.append(borders)

def set_section_cols(section, num_cols=2, space_pt=18):
    """Set multi-column layout on a word section."""
    sectPr = section._sectPr
    for child in list(sectPr):
        if child.tag.endswith('cols'):
            sectPr.remove(child)
    col = OxmlElement('w:cols')
    col.set(qn('w:num'), str(num_cols))
    if num_cols > 1:
        col.set(qn('w:space'), str(int(space_pt * 20))) # 20 dxa = 1 pt
    sectPr.append(col)


def make_eq1_omml():
    """Generate native Word OMML for Equation 1: Dialect Confidence Score."""
    return '''<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:rPr><m:scr m:val="roman"/><m:sty m:val="p"/></m:rPr><m:t>Confidence</m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>d</m:t></m:r></m:e></m:d><m:r><m:t> = </m:t></m:r><m:f><m:fPr><m:type m:val="bar"/></m:fPr><m:num><m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/><m:subHide m:val="0"/><m:supHide m:val="1"/></m:naryPr><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r><m:r><m:t>∈</m:t></m:r><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>T</m:t></m:r></m:sub><m:sup/><m:e><m:r><m:t>𝕀</m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r><m:r><m:t>∈</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>M</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>d</m:t></m:r></m:sub></m:sSub></m:e></m:d><m:r><m:t>⋅</m:t></m:r><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>ω</m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r></m:e></m:d></m:e></m:nary></m:num><m:den><m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/><m:subHide m:val="0"/><m:supHide m:val="1"/></m:naryPr><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>d</m:t></m:r><m:r><m:t>'∈</m:t></m:r><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>D</m:t></m:r></m:sub><m:sup/><m:e><m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/><m:subHide m:val="0"/><m:supHide m:val="1"/></m:naryPr><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r><m:r><m:t>∈</m:t></m:r><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>T</m:t></m:r></m:sub><m:sup/><m:e><m:r><m:t>𝕀</m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r><m:r><m:t>∈</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>M</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>d'</m:t></m:r></m:sub></m:sSub></m:e></m:d><m:r><m:t>⋅</m:t></m:r><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>ω</m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r></m:e></m:d></m:e></m:nary></m:e></m:nary></m:den></m:f></m:oMath>'''


def make_eq2_omml():
    """Generate native Word OMML for Equation 2: Multi-Criteria Candidate Ranking Score."""
    return '''<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"><m:r><m:rPr><m:scr m:val="roman"/><m:sty m:val="p"/></m:rPr><m:t>Score</m:t></m:r><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>c</m:t></m:r></m:e></m:d><m:r><m:t> = </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>lex</m:t></m:r></m:sub></m:sSub><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>lex</m:t></m:r></m:sub></m:sSub><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>c</m:t></m:r></m:e></m:d><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>morph</m:t></m:r></m:sub></m:sSub><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>morph</m:t></m:r></m:sub></m:sSub><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>c</m:t></m:r></m:e></m:d><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>conf</m:t></m:r></m:sub></m:sSub><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>conf</m:t></m:r></m:sub></m:sSub><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>c</m:t></m:r></m:e></m:d><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>freq</m:t></m:r></m:sub></m:sSub><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>freq</m:t></m:r></m:sub></m:sSub><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>c</m:t></m:r></m:e></m:d><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>w</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>dial</m:t></m:r></m:sub></m:sSub><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>S</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>dial</m:t></m:r></m:sub></m:sSub><m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>c</m:t></m:r></m:e></m:d></m:oMath>'''


# ==============================================================================
# 1. ENGLISH VERSION BUILDER (ECTI-CIT SUBMISSION FORMAT)
# ==============================================================================
def build_ecti_docx_en(output_path="artikel/jurnal_sasaknlp_en.docx", is_anonymous=False):
    doc = Document()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # SECTION 1: Single Column Header (Title & Authors)
    s1 = doc.sections[0]
    s1.page_width = Inches(8.27)   # A4 width (21.0 cm)
    s1.page_height = Inches(11.69) # A4 height (29.7 cm)
    s1.top_margin = Inches(1.0)    # 2.5 cm
    s1.bottom_margin = Inches(1.0) # 2.5 cm
    s1.left_margin = Inches(0.8)   # 2.0 cm
    s1.right_margin = Inches(0.8)  # 2.0 cm

    # Running Header
    header = s1.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hdr_title = "ECTI Transactions on Computer and Information Technology (ECTI-CIT)" if not is_anonymous else "ECTI Transactions on Computer and Information Technology (Anonymous Submission)"
    hrun = hp.add_run(hdr_title)
    hrun.font.name = "Times New Roman"
    hrun.font.size = Pt(8.5)
    hrun.font.italic = True
    hrun.font.color.rgb = RGBColor(120, 120, 120)

    # Title_text style: 20 pt Bold, Spacing Before 0 pt, Spacing After 24 pt, Centered
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(24)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run("SasakNLP: A Hybrid Framework for Morphological Processing of the Low-Resource Sasak Language")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(20)
    r_title.font.bold = True

    # Authors_name style: 12 pt Bold, Spacing Before 0 pt, Spacing After 12 pt, Centered
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_before = Pt(0)
    p_auth.paragraph_format.space_after = Pt(8)
    auth_str = "kodetr" if not is_anonymous else "[ANONYMOUS AUTHOR(S)]"
    r_auth = p_auth.add_run(auth_str)
    r_auth.font.name = "Times New Roman"
    r_auth.font.size = Pt(12)
    r_auth.font.bold = True

    # Authors_aff style: 10 pt Regular, Spacing Before 0 pt, Spacing After 0 pt, Centered
    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aff.paragraph_format.space_before = Pt(0)
    p_aff.paragraph_format.space_after = Pt(16)
    if is_anonymous:
        aff_str = "[AFFILIATION WITHHELD FOR DOUBLE-BLIND PEER REVIEW]\nLombok, West Nusa Tenggara, Indonesia\nCorrespondence and Repository Withheld During Review"
    else:
        aff_str = "Regional Language Computational Research Group, kodetr.com\nLombok, West Nusa Tenggara, Indonesia\nCorrespondence: https://kodetr.com | Code Repository: https://github.com/kodetr/sasaknlp"
    r_aff = p_aff.add_run(aff_str)
    r_aff.font.name = "Times New Roman"
    r_aff.font.size = Pt(10)
    r_aff.font.italic = True

    # SECTION 2: Continuous Break into Two Columns
    s2 = doc.add_section(WD_SECTION.CONTINUOUS)
    s2.top_margin = Inches(1.0)
    s2.bottom_margin = Inches(1.0)
    s2.left_margin = Inches(0.8)
    s2.right_margin = Inches(0.8)
    set_section_cols(s2, 2, 18) # 2 columns with 0.25 in spacing

    def add_sec_heading(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        return p

    def add_subsec_heading(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        return p

    def add_body(text, indent=True):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.25)
        else:
            p.paragraph_format.first_line_indent = Inches(0.0)
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        return p

    def add_equation(math_text_or_type, eq_num):
        """Insert an academic standard equation formatted as native Word Equation (OMML) with right-aligned numbering."""
        tbl = doc.add_table(rows=1, cols=2)
        tbl.autofit = False
        tbl.columns[0].width = Inches(2.7)
        tbl.columns[1].width = Inches(0.5)

        for cell in tbl.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
            tcPr.append(tcBorders)
            tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="80" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tcMar>')
            tcPr.append(tcMar)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        p_eq = tbl.rows[0].cells[0].paragraphs[0]
        p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.paragraph_format.space_before = Pt(6)
        p_eq.paragraph_format.space_after = Pt(6)

        if "Confidence" in str(math_text_or_type) or str(math_text_or_type).strip() == "1" or "confidence" in str(math_text_or_type).lower():
            p_eq._p.append(parse_xml(make_eq1_omml()))
        elif "Score" in str(math_text_or_type) or str(math_text_or_type).strip() == "2" or "score" in str(math_text_or_type).lower():
            p_eq._p.append(parse_xml(make_eq2_omml()))
        else:
            r = p_eq.add_run(str(math_text_or_type))
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.font.italic = True

        p_num = tbl.rows[0].cells[1].paragraphs[0]
        p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_num.paragraph_format.space_before = Pt(6)
        p_num.paragraph_format.space_after = Pt(6)
        r_num = p_num.add_run(f"({eq_num})")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(10)
        return tbl

    def add_fig(img_rel_path, fig_no, caption_text, full_page_width=True, width_in=6.5):
        """Add a figure. If full_page_width is True, spans full page width (6.5 inches) across columns."""
        full_p = os.path.join(base_dir, img_rel_path)
        if not os.path.exists(full_p):
            print(f"Warning: Figure image not found: {full_p}")
            return

        if full_page_width:
            s_fig = doc.add_section(WD_SECTION.CONTINUOUS)
            s_fig.top_margin = Inches(1.0)
            s_fig.bottom_margin = Inches(1.0)
            s_fig.left_margin = Inches(0.8)
            s_fig.right_margin = Inches(0.8)
            set_section_cols(s_fig, 1)

        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(0)
        p_img.paragraph_format.keep_with_next = True # Ensure image and caption stay on the same page
        p_img.add_run().add_picture(full_p, width=Inches(width_in if full_page_width else 3.1))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(12)
        r_num = p_cap.add_run(f"Fig. {fig_no}: ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(10)
        r_num.font.bold = True
        r_num.font.italic = True
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True

        if full_page_width:
            s_resume = doc.add_section(WD_SECTION.CONTINUOUS)
            s_resume.top_margin = Inches(1.0)
            s_resume.bottom_margin = Inches(1.0)
            s_resume.left_margin = Inches(0.8)
            s_resume.right_margin = Inches(0.8)
            set_section_cols(s_resume, 2, 18)

    def add_tbl(tbl_no, caption_text, headers, data, col_widths=None, full_page_width=True):
        """Add a table. If full_page_width is True, spans full page width (6.5 inches) across columns."""
        if full_page_width:
            s_tbl = doc.add_section(WD_SECTION.CONTINUOUS)
            s_tbl.top_margin = Inches(1.0)
            s_tbl.bottom_margin = Inches(1.0)
            s_tbl.left_margin = Inches(0.8)
            s_tbl.right_margin = Inches(0.8)
            set_section_cols(s_tbl, 1)

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(12)
        p_cap.paragraph_format.space_after = Pt(6)
        p_cap.paragraph_format.keep_with_next = True # Ensure caption stays with table

        r_num = p_cap.add_run(f"Table {tbl_no}: ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(10)
        r_num.font.bold = True
        r_num.font.italic = True
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True

        tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="000000", sz="4")

        # Header Row
        header_row = tbl.rows[0]
        header_trPr = header_row._tr.get_or_add_trPr()
        header_trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        header_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        for i, h in enumerate(headers):
            cell = header_row.cells[i]
            cell.text = h
            set_cell_background(cell, "F1F5F9")
            set_cell_margins(cell, top=90, bottom=90, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(9)
                run.font.bold = True

        # Data Rows
        for r_idx, row_data in enumerate(data):
            row = tbl.rows[r_idx + 1]
            row_trPr = row._tr.get_or_add_trPr()
            row_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

            for c_idx, val in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.text = str(val)
                bg_col = "FAFAFA" if r_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg_col)
                set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
                p = cell.paragraphs[0]
                if str(val).endswith("%") or str(val).replace(".", "").replace(",", "").isdigit():
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(8.5)

        if col_widths:
            for row in tbl.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Inches(w)

        p_post = doc.add_paragraph()
        p_post.paragraph_format.space_before = Pt(0)
        p_post.paragraph_format.space_after = Pt(12)

        if full_page_width:
            s_resume = doc.add_section(WD_SECTION.CONTINUOUS)
            s_resume.top_margin = Inches(1.0)
            s_resume.bottom_margin = Inches(1.0)
            s_resume.left_margin = Inches(0.8)
            s_resume.right_margin = Inches(0.8)
            set_section_cols(s_resume, 2, 18)

        return tbl

    # Abstract & Keywords
    p_ab_title = doc.add_paragraph()
    p_ab_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_ab_title.paragraph_format.space_before = Pt(0)
    p_ab_title.paragraph_format.space_after = Pt(4)
    r_abt = p_ab_title.add_run("ABSTRACT")
    r_abt.font.name = "Times New Roman"
    r_abt.font.size = Pt(10)
    r_abt.font.bold = True

    p_ab_body = doc.add_paragraph()
    p_ab_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ab_body.paragraph_format.space_before = Pt(0)
    p_ab_body.paragraph_format.space_after = Pt(12)
    p_ab_body.paragraph_format.line_spacing = 1.0
    r_abb = p_ab_body.add_run(
        "Bahasa Sasak is an Austronesian regional language spoken by approximately 3 million people across Lombok Island, "
        "West Nusa Tenggara, Indonesia. Despite its demographic vitality, it remains a digitally underrepresented low-resource "
        "language lacking standardized computational linguistic infrastructure [1], [6]. Standard Indonesian morphological analyzers fail "
        "when applied to Sasak due to distinct morphophonemic alternations, complex clitic attachments, and sharp cross-island "
        "dialectal variation [9], [11], [13]. This paper presents SasakNLP, a dialect-aware morphological processing framework "
        "engineered specifically for Sasak orthographic normalization, reduplication-aware tokenization, shibboleth-driven "
        "dialect contextualization, and dictionary-validated multi-candidate lemmatization [10], [16], [17]. Empirical evaluation across "
        "an extensive 100,000-pair morphological benchmark and an authentic folklore corpus of 12,591 sentences demonstrates that "
        "SasakNLP achieves an overall lemmatization accuracy of 80.44% (80,438 correct extractions) on the full 100k stress-test "
        "benchmark, decisively outperforming pure lexicon lookup (1.01%) and greedy affix-stripping baselines (55.21%) with strong "
        "statistical significance (McNemar's test, χ² = 14,962.14, p < 0.0001). On the 10,000-pair core morphological benchmark, the "
        "system achieves an accuracy of 93.23%. Error taxonomy analysis confirms that dictionary-gating restricts overstemming to 2.28%, "
        "with understemming restricted to 15.86% primarily occurring on complex multi-layered affixations. Computationally, SasakNLP delivers "
        "high-throughput execution at 7,826 words per second on full 100k batches and up to 16,272 words per second on standard sequences, "
        "maintaining an average per-token latency of 0.044 ms with zero heavy machine learning framework dependencies. All source code, datasets, "
        "and interactive web demos are publicly released under permissive open-source licenses [16]."
    )
    r_abb.font.name = "Times New Roman"
    r_abb.font.size = Pt(10)

    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.space_before = Pt(12)
    p_kw.paragraph_format.space_after = Pt(12)
    p_kw.paragraph_format.line_spacing = 1.0
    r_kwt = p_kw.add_run("Keywords: ")
    r_kwt.font.name = "Times New Roman"
    r_kwt.font.size = Pt(10)
    r_kwt.font.bold = True
    r_kwb = p_kw.add_run("Sasak Language, Natural Language Processing, Computational Morphology, Lemmatization, Low-Resource NLP, Dialectology, Open Science.")
    r_kwb.font.name = "Times New Roman"
    r_kwb.font.size = Pt(10)

    # 1. INTRODUCTION
    add_sec_heading("1. INTRODUCTION")
    add_body(
        "Recent breakthroughs in Natural Language Processing (NLP) and Large Language Models (LLMs) have been overwhelmingly "
        "concentrated on high-resource languages [1], [2]. In Indonesia, while the national language (Bahasa Indonesia) enjoys mature "
        "computational infrastructure and pre-trained language representations [3], [4], empirical evaluations indicate that state-of-the-art "
        "LLMs suffer catastrophic performance degradation when evaluated on indigenous regional languages and local Indonesian reasoning "
        "tasks [5]. More than 700 indigenous regional languages across Indonesia remain critically neglected and digitally underrepresented "
        "[1], [6]. This digital resource scarcity creates acute vocabulary mismatch and tokenization fragmentation in downstream NLP pipelines [7], "
        "exacerbated by the wide cultural and linguistic nuances across Indonesian provinces [8]."
    )
    add_body(
        "Bahasa Sasak (Basa Sasak) is the predominant indigenous language of Lombok Island in West Nusa Tenggara, spoken by approximately "
        "3 million native speakers [9], [10]. Categorized typologically within the Western Malayo-Polynesian branch of the Austronesian "
        "language family, Sasak exhibits distinct grammatical and sociopragmatic characteristics [11], [12]:"
    )
    add_body(
        "1) Complex Morphophonemics: Stem formation incorporates active prefixes (te-, ka-, se-, pe-), archaic passive infixes (-in-, -um-), "
        "causative/applicative suffixes (-ang, -an, -i, -in), iterative circumfixes (pe-...-an, te-...-ang, be-...-an), and intricate nasal "
        "substitutions (N-) [10], [13]."
    )
    add_body(
        "2) Enclitic Compounding and Sociopragmatics: Pronominal possessive enclitics (-ku, -m, -ne) and honorific sociolinguistic particles "
        "(-de, -te) append directly to root words, reflecting strict social strata and politeness registers [11], while frequently triggering "
        "severe overstemming or understemming in naive heuristic parsers [13]."
    )
    add_body(
        "3) Dialectal Diversity: The language is partitioned into five distinct dialect clusters separated by isoglosses and diagnostic "
        "lexical markers (shibboleths) [9], [12]."
    )
    add_body(
        "Prior computational morphology research in Indonesia has predominantly addressed Javanese and Sundanese [1], [13], [14], while "
        "computational methods for ethnic languages in Eastern Indonesia remain largely confined to bilingual lexicon induction [15]. "
        "Systematic literature reviews confirm that the absence of structured digital lexicons and morphological analyzers remains the primary "
        "barrier to regional language lemmatization [13]."
    )
    add_body(
        "To overcome these barriers, we present SasakNLP, an open-source, reproducible computational framework [16]. Grounded in two-level "
        "computational morphology [17] and morphological segmentation standards [18], the primary contributions of this work are:"
    )
    add_body(
        "• Contribution 1 (SasakLex Machine Resource): Digitalization and structuring of the official Balai Bahasa Provinsi NTB integrated "
        "dictionary into 2,761 machine-readable entries [10], [16]."
    )
    add_body(
        "• Contribution 2 (Hybrid Morphological Framework): A deterministic architecture combining two-pass affix stripping, O(L) dictionary "
        "validation via PrefixTrie, and multi-criteria candidate ranking [13], [17]."
    )
    add_body(
        "• Contribution 3 (Structured Morphological Analysis): Explicit morpheme segmentation identifying prefixes, infixes, suffixes, "
        "circumfixes, clitics, and reduplication with confidence scores [17], [18]."
    )
    add_body(
        "• Contribution 4 (Dialect-Aware Architecture): Configurable dialect contextualization using diagnostic shibboleth density across "
        "the five Sasak dialect regions [9], [12]."
    )
    add_body(
        "• Contribution 5 (Open Research Infrastructure): Public release of the 100,000-pair gold-standard benchmark, the 12,591-sentence "
        "authentic corpus, the PyPI package (sasaknlp), and Hugging Face Hub datasets [16]."
    )

    # 2. RELATED WORK AND LINGUISTIC FOUNDATIONS
    add_sec_heading("2. RELATED WORK AND LINGUISTIC FOUNDATIONS")
    add_subsec_heading("2.1 Regional Austronesian NLP Landscape")
    add_body(
        "Underrepresented language technologies in Indonesia suffer from persistent data scarcity [1], [2], [6]. Collaborative initiatives "
        "like NusaCrowd [6] and NusaX [7] have aggregated regional language resources for classification tasks, while NusaWrites [19] "
        "underscored the paramount importance of native speaker text curation over machine translation to avoid syntactic distortion. "
        "However, token-level morphological processing for regional languages outside Java remains sparse, largely relying on ad-hoc heuristics [13]."
    )
    add_body(
        "In Indonesian regional languages, canonical affix-level segmentation has proven superior to naive subword tokenization for preserving "
        "morphemic integrity [14]. Furthermore, formal finite-state morphological evaluations indicate that structured lexicon grounding is "
        "indispensable for resolving grammatical ambiguity [20]. The systematic literature review by Abidin et al. [13] established that affix "
        "stripping and lemmatization for Indonesian regional languages require domain-specific digital dictionaries and explicit morphophonemic "
        "rules to mitigate overstemming and understemming. Resiandi et al. [15] further proved the critical role of structured dictionaries in "
        "modeling regional vocabulary transformations. Hence, integrating a curated lexicon as an active verification gate is crucial for preserving "
        "root integrity in low-resource setups [13], [17]."
    )

    add_subsec_heading("2.2 Morphological System of Bahasa Sasak")
    add_body(
        "According to official grammatical codification by Balai Bahasa Provinsi NTB [10], sociopragmatic studies [11], and contemporary dialectological "
        "research [9], [12], Sasak bound morphemes comprise:"
    )
    add_body(
        "1) Prefixes: Passive te- (tepinaq 'is made'), stative ka- (kasolah 'beautified'), equative se- (sebale 'one house'), nominalizer "
        "pe-/peng- (pegawi 'worker'), and nasal assimilation N- (nulis, minaq)."
    )
    add_body(
        "2) Suffixes: Causative/applicative -ang (tulungang 'help for someone'), locative/resultative -an (kelororan 'waterway'), iterative "
        "-i/-in (sirami)."
    )
    add_body(
        "3) Infixes: Archaic passive -in- (tinulung 'received assistance') and intransitive -um- (gumingsir 'shift')."
    )
    add_body(
        "4) Circumfixes: Abstract nominal pe-...-an (pegawian 'occupation'), passive applicative te-...-ang (tetulungang), stative ka-...-an, "
        "reciprocal be-...-an (betulungan)."
    )
    add_body(
        "5) Enclitics: First person -ku, second person -m, third person -ne, and polite register markers -de, -te (baturne, balende) [11]."
    )
    add_body(
        "6) Reduplication: Full reduplication with hyphens (bareng-bareng, mangan-mangan)."
    )

    add_subsec_heading("2.3 Dialect Taxonomy of Bahasa Sasak")
    add_body(
        "Following regional dialectological studies [9], [10], [12], Bahasa Sasak is grouped into five primary dialect clusters based on "
        "diagnostic shibboleths (Table 1)."
    )

    # TABLE 1: Full-Page Width (6.5 inches)
    t1_headers = ["No", "Dialect Cluster", "Geographical Range", "Diagnostic Markers", "Phonological & Sociolinguistic Features"]
    t1_data = [
        ["1", "Meno-Mene (Selaparang)", "East & Central Lombok", "menu, meni, tiyang, kaji", "Polite register (krama/alus), glottal stop retention /-q/, characteristic vowel /-e/"],
        ["2", "Ngeno-Ngene", "Mataram & West Lombok", "ngeno, ngene, ente, aku", "Urban dialect, rapid vocalic articulation, maritime trade contact"],
        ["3", "Merikuq-Merikaq (Mriak-Mriku)", "Central-South (Praya, Pujut)", "mriak, mriku, meriq, merik", "Spatial directional deictics (towards here / towards there), vowels /-a/ and /-u/"],
        ["4", "Kuto-Kute (Ngeto-Ngete)", "North & Northeast Lombok (Bayan, Sembalun)", "kuto, kute, ngeto, wetu", "Archaic Austronesian retention, customary Wetu Telu tradition, highland communities"],
        ["5", "General Standard Sasak", "Cross-Island Standard", "wah, ndeq, mangan, batur", "Inter-dialectal lingua franca in public domains, aligns with Balai Bahasa NTB lexicon"]
    ]
    add_tbl(1, "Taxonomy of the Five Major Sasak Dialect Clusters in Lombok [9], [10], [12]", t1_headers, t1_data, col_widths=[0.4, 1.4, 1.4, 1.3, 2.0], full_page_width=True)

    # 3. METHODOLOGY AND SYSTEM ARCHITECTURE
    add_sec_heading("3. METHODOLOGY AND SYSTEM ARCHITECTURE")
    add_subsec_heading("3.1 System Overview")
    add_body(
        "SasakNLP implements a deterministic six-stage modular pipeline designed without external deep learning framework dependencies, "
        "ensuring predictable, reproducible, and millisecond-level execution latency."
    )

    add_subsec_heading("3.2 Orthographic Normalization")
    add_body(
        "The normalization stage enforces Unicode NFC composition, standardizes typographical variations in Sasak glottal stop graphemes "
        "(unifying curly apostrophes ’ and backticks into canonical glottal characters q or '), and cleans non-standard ASCII artifacts while "
        "preserving accented vowel distinctions (è, é) [1], [6]."
    )

    add_subsec_heading("3.3 Reduplication-Aware Tokenization")
    add_body(
        "The tokenizer detects full hyphenated reduplications ([Root]-[Root]) as unified morphological constructs, preventing incorrect "
        "splitting of iterative verbs and repetitive adverbs into disjoint tokens [13], [17]."
    )

    add_subsec_heading("3.4 Diagnostic Shibboleth Dialect Contextualization")
    add_body(
        "The dialect detector module calculates dialect confidence using relative shibboleth density across geographical clusters [9], [12]:"
    )
    add_equation("confidence", "1")
    add_body(
        "where T represents the input tokens, Md is the set of diagnostic lexical markers for dialect d, and ω(w) denotes the lexical uniqueness weight."
    )

    add_subsec_heading("3.5 Two-Pass Candidate Generation and PrefixTrie Validation")
    add_body(
        "Unrecognized surface forms are submitted to candidate generation. Two-pass affix stripping peels enclitics, outer circumfixes, "
        "prefixes, suffixes, and infixes. Each candidate root is verified against the 2,761-word Balai Bahasa NTB dictionary using an O(L) "
        "PrefixTrie data structure [10], [17], [18]."
    )

    add_subsec_heading("3.6 Multi-Criteria Candidate Ranking")
    add_body(
        "Morphological ambiguities are resolved using a weighted scoring objective [17]:"
    )
    add_equation("score", "2")
    add_body(
        "with empirically optimized weights: w_lex = 0.40, w_morph = 0.25, w_conf = 0.15, w_freq = 0.10, and w_dial = 0.10."
    )

    add_subsec_heading("3.7 Structured Morphological Output")
    add_body(
        "The final pipeline generates structured JSON-compatible tuples containing base lemmas, grammatical affix breakdown, dialect classification, "
        "and normalized confidence scores."
    )

    # 4. EXPERIMENTAL SETUP AND DATASET PROTOCOL
    add_sec_heading("4. EXPERIMENTAL SETUP AND DATASET PROTOCOL")
    add_subsec_heading("4.1 Research Data Resources")
    add_body(
        "The benchmark datasets were curated via a rigorous three-phase acquisition protocol (Fig. 1):\n"
        "1) Benchmark 100k (benchmark_100k.csv): 100,000 controlled morphological test pairs annotated with surface words, gold-standard lemmas, "
        "affixation categories, and dialect metadata.\n"
        "2) Benchmark 10k (benchmark_10k.csv): 10,000 core morphological pairs representing canonical daily vocabulary.\n"
        "3) Authentic Corpus (sasak_sentences_large.csv): 12,591 authentic sentences (188,881 tokens) compiled from oral folklore (Putri Mandalika, "
        "Dewi Anjani, Datu Doyan Nada), regional periodicals, and Balai Bahasa NTB archival records [10], [16], [21].\n"
        "4) Lexicon Dictionary (kamus_balai_bahasa_ntb.csv): 2,761 verified lemma entries from Balai Bahasa Provinsi NTB [10]."
    )

    # FIGURE 1: Full-Page Width (6.5 inches)
    add_fig("figures/fig5_dataset_acquisition_pipeline.png", 1, "Three-Phase Scientific Acquisition and Quality Curation Protocol for SasakNLP Research Artifacts.", full_page_width=True, width_in=6.5)

    add_subsec_heading("4.2 Baseline Models")
    add_body(
        "We evaluate SasakNLP against two standard baseline algorithms on the 100,000-sample benchmark:\n"
        "• Baseline 1 (Direct Lexicon Lookup): Exact lexicon matching without affix stripping.\n"
        "• Baseline 2 (Greedy Affix Stripping): Longest-match affix removal without dictionary verification [13]."
    )

    add_subsec_heading("4.3 Evaluation Metrics and Experimental Environment")
    add_body(
        "Evaluation metrics include exact lemmatization accuracy, throughput (words/second), per-token latency (ms), overstemming rate, understemming rate, "
        "and out-of-vocabulary (OOV) rate. Experiments were executed on Apple Silicon (8-Core) and Intel Core i7 x86_64 CPUs with 16 GB RAM under Python 3.10+, "
        "guaranteeing 100% deterministic reproducibility."
    )

    # 5. EXPERIMENTAL RESULTS
    add_sec_heading("5. EXPERIMENTAL RESULTS")
    add_subsec_heading("5.1 Baseline Comparison on the 100,000-Sample Benchmark")
    add_body(
        "Experimental results across the 100,000 morphological test pairs demonstrate the decisive superiority of SasakNLP (Table 2). Baseline 1 achieves "
        "only 1.01% accuracy due to complete failure on affixed words. Baseline 2 obtains 55.21% but suffers from severe overstemming. SasakNLP achieves "
        "80.44% accuracy (80,438 correct predictions)."
    )

    # TABLE 2: Full-Page Width (6.5 inches)
    t2_headers = ["Model / Algorithm", "Computational Principle", "Correct (N=100k)", "Accuracy (%)", "Throughput (wps)"]
    t2_data = [
        ["Baseline 1: Direct Lookup", "Exact Dictionary Matching", "1,006", "1.01%", "24,500"],
        ["Baseline 2: Greedy Stripping", "Longest-Match Affix Stripping", "55,205", "55.21%", "18,200"],
        ["Proposed SasakNLP", "Dictionary-Enhanced Multi-Candidate", "80,438", "80.44%", "7,826"]
    ]
    add_tbl(2, "Comparative Lemmatization Evaluation On 100,000 Morphological Samples", t2_headers, t2_data, col_widths=[1.7, 1.8, 1.0, 0.9, 1.1], full_page_width=True)

    add_body(
        "McNemar's paired statistical test comparing SasakNLP and Baseline 2 yields contingency matrix: "
        "a = 46,546 (both correct), b = 33,892 (SasakNLP correct, Baseline 2 incorrect), "
        "c = 8,659 (SasakNLP incorrect, Baseline 2 correct), and d = 10,903 (both incorrect). "
        "The test statistic is chi-squared = 14,962.14 (df = 1, p < 0.0001), confirming that "
        "SasakNLP's performance advantage is statistically significant at alpha = 0.001."
    )

    add_subsec_heading("5.2 Performance on the Core 10k Benchmark")
    add_body(
        "On the 10,000-pair core morphological benchmark (benchmark_10k.csv), SasakNLP achieves 9,323 correct predictions (93.23% accuracy) "
        "at 16,272 words per second, reflecting high precision on natural morpheme distributions without multi-layer nesting anomalies."
    )

    add_subsec_heading("5.3 Architectural Component Ablation Study")
    add_body(
        "To quantify the contribution of each algorithmic module, we conducted an ablation study on the 100,000-sample benchmark (Table 3). "
        "Adding PrefixTrie dictionary gating improves accuracy by +13.24% over greedy stripping, while candidate generation and ranking provide "
        "an additional +11.99% accuracy gain."
    )

    # TABLE 3: Full-Page Width (6.5 inches)
    t3_headers = ["Configuration", "Rules", "Dict", "Gen", "Rank", "Dialect", "Acc (%)", "Throughput"]
    t3_data = [
        ["M1: Direct Lookup", "No", "Yes", "No", "No", "No", "1.01%", "24,500 wps"],
        ["M2: Greedy Stripping", "Yes", "No", "No", "No", "No", "55.21%", "18,200 wps"],
        ["M3: Rules + Dict Gate", "Yes", "Yes", "No", "No", "No", "68.45%", "14,100 wps"],
        ["M4: Rules + Gen + First Match", "Yes", "Yes", "Yes", "No", "No", "74.12%", "10,350 wps"],
        ["M5: Full Proposed SasakNLP", "Yes", "Yes", "Yes", "Yes", "Yes", "80.44%", "7,826 wps"]
    ]
    add_tbl(3, "Ablation Study Across SasakNLP Architectural Components (100k Data)", t3_headers, t3_data, col_widths=[1.7, 0.6, 0.6, 0.6, 0.6, 0.6, 0.8, 1.0], full_page_width=True)

    add_subsec_heading("5.4 Morpheme-Level Performance Disaggregation")
    add_body(
        "Performance breakdown across grammatical categories (Fig. 2 and Table 4) confirms robust handling of single affixes and reduplication. "
        "Reduplication achieves 100.00%, passive prefixes reach 97.36%, stative prefixes reach 96.79%, and possessive clitics exceed 94.6%–96.5%."
    )

    # FIGURE 2: Full-Page Width (6.5 inches)
    add_fig("figures/fig1_morphology_accuracy.png", 2, "Morphological Rule Accuracy Across Grammatical Affix Classes (100k Data).", full_page_width=True, width_in=6.5)

    # TABLE 4: Full-Page Width (6.5 inches)
    t4_headers = ["Category", "Pattern", "Samples", "Accuracy (%)", "Linguistic Characteristics"]
    t4_data = [
        ["Reduplication", "root-root", "1,789", "100.00%", "Perfect handling of full reduplication (mangan-mangan)"],
        ["Passive Prefix", "te-", "1,783", "97.36%", "Passive verbs (tetulung, tepinaq)"],
        ["Stative Prefix", "ka-", "1,745", "96.79%", "Stative condition markers (kasolah, kabeleq)"],
        ["Nominal Prefix", "peng-", "1,781", "96.91%", "Agentive and instrument nominalizer (penggawi)"],
        ["Equative Prefix", "se-", "1,748", "96.22%", "Equative and collective prefix (sebale, sekance)"],
        ["Clitic Possessive 1", "-ku", "1,782", "96.58%", "First-person possessive enclitic (baleku, jaranku)"],
        ["Clitic Possessive 2", "-m", "1,778", "96.18%", "Second-person familiar enclitic (matam, bajum)"],
        ["Clitic Possessive 3", "-ne", "3,571", "94.62%", "Third-person possessive enclitic (baturne, kawanne)"],
        ["Iterative Suffix", "-i", "1,771", "91.53%", "Iterative action suffix (sirami, antoli)"],
        ["Infixes", "-in-, -um-", "2,346", "89.98%", "Archaic passive and intransitive infixes (tinulung)"],
        ["Polite Clitics", "-de, -te", "6,312", "88.39%", "Honorific polite enclitics (balende, balente)"],
        ["Circumfix Passive", "te-...-ang", "4,578", "96.96%", "Passive applicative circumfix (tetulungang)"],
        ["Circumfix Nominal", "pe-...-an", "5,915", "88.32%", "Abstract nominalizer (pegawian)"],
        ["Causative Suffix", "-ang", "6,170", "83.70%", "Active causative/applicative suffix (tulungang)"],
        ["Locative Suffix", "-an, -in", "10,545", "76.52%", "Locative and resultative suffix (kaduan, siramin)"],
        ["Reciprocal", "be-...-an", "1,710", "65.09%", "Reciprocal mutual action circumfix (betulungan)"]
    ]
    add_tbl(4, "Disaggregated Performance Across 16 Major Representative Morpheme Categories (N = 55,324) on the 100,000-Sample Benchmark", t4_headers, t4_data, col_widths=[1.4, 0.9, 0.8, 0.9, 2.5], full_page_width=True)
    add_body(
        "Note: The 16 categories displayed in Table 4 represent canonical major single-affix and primary circumfix formations (N = 55,324). "
        "The remaining 44,676 samples in the 100,000-pair benchmark comprise complex multi-tier nested combinations, compounding, and dialectal "
        "derivations documented in the supplementary dataset repository.",
        indent=False
    )

    add_subsec_heading("5.5 Cross-Dialect Evaluation")
    add_body(
        "Cross-dialect evaluation across the five Sasak dialect regions (Fig. 3 and Table 5) confirms strong generalization across Lombok Island."
    )

    # FIGURE 3: Full-Page Width (6.5 inches)
    add_fig("figures/fig2_dialect_performance.png", 3, "Cross-Dialect Lemmatization Accuracy Across Five Major Sasak Dialect Clusters.", full_page_width=True, width_in=6.5)

    # TABLE 5: Full-Page Width (6.5 inches)
    t5_headers = ["Region", "Dialect Cluster", "Samples", "Accuracy (%)", "Primary Vocalic & Phonemic Features"]
    t5_data = [
        ["Mataram / West Lombok", "General Standard Sasak", "43,254", "85.73%", "Aligns with official Balai Bahasa NTB standard lexicon"],
        ["North Lombok", "Kuto-Kute (Ngeto-Ngete)", "10,475", "80.31%", "Final vowels /-e/ and /-o/ (kuto, kute), archaic retention"],
        ["South Lombok", "Merikuq-Merikaq (Mriak-Mriku)", "10,535", "79.79%", "Vowels /-a/ and /-u/ with persistent glottal stop /-q/"],
        ["Central Lombok", "Meno-Mene (Selaparang)", "23,023", "77.04%", "Characteristic vowel /-e/, largest speaker population"],
        ["East Lombok", "Ngeno-Ngene", "12,713", "69.24%", "Nasal vocalic shifts and final velar consonant /-k/"]
    ]
    add_tbl(5, "Lemmatization Performance Across Five Major Sasak Dialect Clusters (100k Data)", t5_headers, t5_data, col_widths=[1.3, 1.3, 0.8, 0.9, 2.2], full_page_width=True)

    add_subsec_heading("5.6 Computational Scalability and Runtime Latency")
    add_body(
        "Computational profiling indicates linear O(N) scaling (Fig. 4). Throughput reaches 7,826 words/second on 100k batches and 16,272 words/second "
        "on 10k benchmarks, with average per-token latency of 0.044 ms."
    )

    # FIGURE 4: Full-Page Width (6.5 inches)
    add_fig("figures/fig4_pipeline_benchmark.png", 4, "Computational Scalability and Latency Profile of SasakNLP Across Token Lengths.", full_page_width=True, width_in=6.5)

    add_subsec_heading("5.7 Extrinsic Feature Space Dimensionality Reduction")
    add_body(
        "In downstream evaluation, applying SasakNLP lemmatization compressed the vocabulary feature space of the authentic corpus from 5,913 unique "
        "surface tokens to 4,022 base lemmas (31.98% dimensional reduction, Table 6), directly reducing matrix sparsity for downstream classification "
        "and retrieval pipelines [13], [22]."
    )

    # TABLE 6: Full-Page Width (6.5 inches)
    t6_headers = ["Corpus / Dataset Parameter", "Unique Surface Tokens", "Base Root Lemmas", "Dimensional Reduction Ratio", "Impact on Downstream NLP"]
    t6_data = [
        ["Benchmark Morfologi (100k)", "100,000 unique forms", "1,790 root lemmas", "98.21%", "Reduces lexical lookup search space by 55x"],
        ["Authentic Corpus (189k tokens)", "5,913 unique words", "4,022 root lemmas", "31.98%", "Reduces feature matrix sparsity by 32%"]
    ]
    add_tbl(6, "Evaluation of Vocabulary Feature Space Compression on Research Datasets", t6_headers, t6_data, col_widths=[1.6, 1.3, 1.2, 1.1, 1.3], full_page_width=True)

    # 6. DISCUSSION AND ERROR ANALYSIS
    add_sec_heading("6. DISCUSSION AND ERROR ANALYSIS")
    add_subsec_heading("6.1 Error Taxonomy and Failure Mode Analysis")
    add_body(
        "A comprehensive diagnostic evaluation on the 100,000-sample benchmark classifies failure modes into four categories (Fig. 5, Table 7)."
    )

    # FIGURE 5: Full-Page Width (6.5 inches)
    add_fig("figures/fig3_error_taxonomy.png", 5, "Distribution of Lemmatization Error Taxonomy (left) and Failure Mode Diagnostic Matrix (right).", full_page_width=True, width_in=6.5)

    # TABLE 7: Full-Page Width (6.5 inches)
    t7_headers = ["Classification", "Computational Definition", "Example Input -> Pred", "Count", "Pct (%)", "Root Linguistic Cause"]
    t7_data = [
        ["Correct", "Predicted lemma matches gold lemma", "tepinaq -> pinaq", "80,438", "80.44%", "Exact match in rules and lexicon"],
        ["Understemming", "Predicted lemma length > gold lemma", "pegawianne -> pegawian", "15,856", "15.86%", "Triple-layer nesting (circumfix + clitic) not fully stripped"],
        ["Overstemming", "Root character mistakenly removed", "jaran -> jar (-an stripped)", "2,279", "2.28%", "Root ending resembles bound suffix"],
        ["Incorrect Lemma", "Equal length, mismatched characters", "mangan -> pangan", "1,427", "1.43%", "Nasal alternation ambiguity (m -> p vs m -> m)"],
        ["OOV Error", "Root absent from machine lexicon", "Loanwords / neologisms", "0", "0.00%", "All benchmark roots covered by dictionary"]
    ]
    add_tbl(7, "Error Taxonomy Analysis on 100,000 Morphological Benchmark Samples", t7_headers, t7_data, col_widths=[1.2, 1.5, 1.2, 0.7, 0.7, 1.2], full_page_width=True)

    add_subsec_heading("6.2 Algorithmic Strengths of Dictionary-Gated Parsing")
    add_body(
        "SasakNLP's high precision stems from PrefixTrie dictionary gating [10], [17]. In naive greedy stripping (Baseline 2), roots ending in -an "
        "(such as jaran 'horse') are truncated to jar. In SasakNLP, jaran matches the verified lexicon on pass one, preventing unnecessary truncation."
    )

    add_subsec_heading("6.3 Complexity Discrepancy between Benchmarks")
    add_body(
        "The accuracy difference between the 100k benchmark (80.44%) and the 10k core benchmark (93.23%) reflects morphological complexity. "
        "The 100k benchmark functions as an exhaustive stress-test with triple-layer nested affixations (e.g., pe-...-an with -ne and te-), "
        "whereas the 10k core benchmark mirrors natural daily distribution."
    )

    add_subsec_heading("6.4 Implications for Underrepresented Indigenous NLP")
    add_body(
        "These results demonstrate that underrepresented regional languages in Indonesia can achieve robust morphological processing through "
        "dictionary-grounded rule architectures without expensive GPU infrastructure [1], [6], [13]."
    )

    # 7. LIMITATIONS
    add_sec_heading("7. LIMITATIONS")
    add_body(
        "We transparently document three primary limitations of this study:\n"
        "1) Controlled Vocabulary Scope: The 100k benchmark evaluates systematic morpheme combinations grounded in verified dictionary lemmas. "
        "Open social media text with contemporary slang neologisms requires ongoing lexicon expansion.\n"
        "2) Dialect Corpus Balance: Authentic folklore sentences are currently skewed toward General and East Lombok dialects due to historical textual availability.\n"
        "3) Absence of Syntactic Context: The current pipeline operates at word and token levels without sentence-level Part-of-Speech tagging context."
    )

    # 8. CONCLUSION AND FUTURE DIRECTIONS
    add_sec_heading("8. CONCLUSION AND FUTURE DIRECTIONS")
    add_body(
        "This paper presented SasakNLP, a hybrid morphological framework for Bahasa Sasak. Evaluated across 100,000 benchmark pairs, "
        "SasakNLP achieves 80.44% accuracy on the full stress-test benchmark and 93.23% on the core 10k benchmark, restricting overstemming to 2.28%, "
        "with throughput exceeding 7,800–16,000 words/second and 0.044 ms latency."
    )
    add_body(
        "Future directions include: 1) Integrating lightweight sequence-to-sequence models (ByT5 / Char-BiLSTM) for OOV neologism handling, "
        "2) Constructing the first annotated Sasak Dependency Treebank, and 3) Training bidirectional Sasak-Indonesian Neural Machine Translation models [1], [2], [6]."
    )

    # DATA AND CODE AVAILABILITY
    add_sec_heading("DATA AND CODE AVAILABILITY")
    if is_anonymous:
        add_body(
            "The complete source code, curated lexical resources, 100k benchmark pairs, and reproducibility execution scripts are withheld to "
            "preserve author anonymity during the double-blind peer review process. All research artifacts will be released publicly under open-source "
            "licenses upon manuscript acceptance."
        )
    else:
        add_body(
            "To ensure scientific transparency and research reproducibility, all software, data, and models are publicly accessible: "
            "Official PyPI Package (pip install sasaknlp), GitHub Repository (https://github.com/kodetr/sasaknlp), and "
            "Hugging Face Datasets (https://huggingface.co/datasets/kodetr/sasak-benchmark-100k)."
        )

    # ACKNOWLEDGMENT
    add_sec_heading("ACKNOWLEDGMENT")
    if is_anonymous:
        add_body("[ACKNOWLEDGMENTS WITHHELD DURING DOUBLE-BLIND REVIEW]")
    else:
        add_body(
            "The author expresses sincere gratitude to the native speakers and cultural custodians across Lombok Island, previous dialectological researchers, "
            "and Balai Bahasa Provinsi Nusa Tenggara Barat for standardizing the Sasak-Indonesian dictionary that provided the foundational lexical ground truth."
        )

    # REFERENCES
    add_sec_heading("REFERENCES")
    refs = [
        "[1] A. F. Aji, G. I. Winata, F. Koto, S. Cahyawijaya, A. Romadhony, R. Mahendra, K. Kurniawan, D. Moeljadi, R. E. Prasojo, T. Baldwin, J. H. Lau, and S. Ruder, \"One Country, 700+ Languages: NLP Challenges for Underrepresented Languages and Dialects in Indonesia,\" in Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 2022, pp. 722--745. doi: 10.18653/v1/2022.acl-long.498.",
        "[2] S. Ranathunga, E.-S. A. Lee, M. P. Skenduli, R. Shekhar, M. Alam, and R. Kaur, \"Neural Machine Translation for Low-Resource Languages: A Survey,\" ACM Computing Surveys, vol. 55, no. 11, pp. 229:1--229:37, 2023. doi: 10.1145/3567592.",
        "[3] S. Cahyawijaya, G. I. Winata, B. Wilie, K. Vincentio, X. Li, A. Kuncoro, S. Rai, M. Lyman, K. Kurniawan, A. Azaria, S. Bahar, R. Mahendra, P. Fung, and A. Purwarianti, \"IndoNLG: Benchmark and Resources for Evaluating Indonesian Natural Language Generation,\" in Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, 2021, pp. 8878--8898. doi: 10.18653/v1/2021.emnlp-main.699.",
        "[4] F. Koto, J. H. Lau, and T. Baldwin, \"IndoBERTweet: A Pretrained Language Model for Indonesian Twitter with Effective Domain-Specific Vocabulary Initialization,\" in Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, 2021, pp. 10660--10668. doi: 10.18653/v1/2021.emnlp-main.833.",
        "[5] F. Koto, N. Aisyah, H. Li, and T. Baldwin, \"Large Language Models Only Pass Primary School Exams in Indonesia: A Comprehensive Test on IndoMMLU,\" in Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, 2023, pp. 12359--12374. doi: 10.18653/v1/2023.emnlp-main.760.",
        "[6] G. I. Winata, A. F. Aji, S. Cahyawijaya, R. Mahendra, F. Koto, A. Romadhony, K. Kurniawan, D. Moeljadi, and R. E. Prasojo, \"NusaCrowd: Open Source Initiative for Indonesian NLP and Regional Languages Resources,\" in Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 2023, pp. 8321--8345. doi: 10.18653/v1/2023.acl-long.462.",
        "[7] S. Cahyawijaya, H. Lovenia, A. F. Aji, G. I. Winata, B. Wilie, F. Koto, R. Mahendra, C. Wibisono, and P. Fung, \"NusaX: Multilingual Parallel Sentiment Dataset for 10 Indonesian Local Languages,\" in Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics, 2023, pp. 2562--2578. doi: 10.18653/v1/2023.eacl-main.189.",
        "[8] F. Koto, R. Mahendra, N. Aisyah, and T. Baldwin, \"IndoCulture: Exploring Geographically Influenced Cultural Commonsense Reasoning Across Eleven Indonesian Provinces,\" Transactions of the Association for Computational Linguistics, vol. 12, pp. 1703--1719, 2024. doi: 10.1162/tacl_a_00726.",
        "[9] L. Hakim, Roveneldo, N. U. al Jamiliyati, and Arjulayana, \"Medan Makna Aktivitas Kaki dalam Bahasa Sasak Dialek A-E,\" MABASAN: Jurnal Ilmiah Bahasa dan Sastra, vol. 17, no. 1, pp. 109--128, 2023. doi: 10.26499/mab.v17i1.626.",
        "[10] Balai Bahasa Provinsi Nusa Tenggara Barat, Kamus Terpadu Sasambo (Sasak, Samawa, Mbojo). Mataram, Indonesia: Balai Bahasa Provinsi Nusa Tenggara Barat, Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi Republik Indonesia, 2022.",
        "[11] L. N. Yaqin, T. Shanmuganathan, W. Fauzanna, Mohzana, and A. Jaya, \"Sociopragmatic parameters of politeness strategies among the Sasak in the post elopement rituals,\" Studies in English Language and Education, vol. 9, no. 2, pp. 797--811, 2022. doi: 10.24815/siele.v9i2.22569.",
        "[12] L. Hakim, \"Makian dalam Bahasa Sasak Dialek E-E,\" MABASAN: Jurnal Ilmiah Bahasa dan Sastra, vol. 16, no. 1, pp. 83--98, 2022. doi: 10.26499/mab.v16i1.503.",
        "[13] Z. Abidin, A. Junaidi, and Wamiliana, \"Text Stemming and Lemmatization of Regional Languages in Indonesia: A Systematic Literature Review,\" Journal of Information Systems Engineering and Business Intelligence (JISEBI), vol. 10, no. 2, pp. 217--231, 2024. doi: 10.20473/jisebi.10.2.217-231.",
        "[14] S. H. Wijono, M. R. Alhamidi, M. H. Hilman, and W. Jatmiko, \"Canonical Segmentation Using Affix Characters as a Unit on Transformer for Javanese Language,\" in Proceedings of the 2021 6th International Workshop on Big Data and Information Security (IWBIS), 2021, pp. 67--72. doi: 10.1109/IWBIS53353.2021.9631839.",
        "[15] K. Resiandi, Y. Murakami, and A. H. Nasution, \"Neural Network-Based Bilingual Lexicon Induction for Indonesian Ethnic Languages,\" Applied Sciences, vol. 13, no. 15, p. 8666, 2023. doi: 10.3390/app13158666.",
        "[16] [Reference to Author's Previous Software Artifact Withheld for Double-Blind Review], 2026." if is_anonymous else "[16] kodetr, \"SasakNLP: A Hybrid Framework and 100k Benchmark for the Low-Resource Sasak Language,\" PyPI, GitHub, and Hugging Face Datasets, 2026. [Online]. Available: https://github.com/kodetr/sasaknlp.",
        "[17] D. Jurafsky and J. H. Martin, Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition, 3rd ed. Upper Saddle River, NJ: Prentice Hall, 2024.",
        "[18] K. Batsuren, G. Bella, A. Arora, V. Martinovic, K. Gorman, Z. Žabokrtský, A. Ganbold, Š. Dohnalová, M. Ševčíková, K. Pelegrinová, F. Giunchiglia, R. Cotterell, and E. Vylomova, \"The SIGMORPHON 2022 Shared Task on Morpheme Segmentation,\" in Proceedings of the 19th SIGMORPHON Workshop on Computational Research in Phonetics, Phonology, and Morphology, 2022, pp. 103--116. doi: 10.18653/v1/2022.sigmorphon-1.11.",
        "[19] S. Cahyawijaya, H. Lovenia, F. Koto, D. Adhista, E. Dave, S. Oktavianti, S. Akbar, J. Lee, N. Shadieq, T. W. Cenggoro, H. Linuwih, B. Wilie, G. Muridan, G. Winata, D. Moeljadi, A. F. Aji, A. Purwarianti, and P. Fung, \"NusaWrites: Constructing High-Quality Corpora for Underrepresented and Extremely Low-Resource Languages,\" in Proceedings of the 13th International Joint Conference on Natural Language Processing and the 3rd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (Volume 1: Long Papers), 2023, pp. 921--945. doi: 10.18653/v1/2023.ijcnlp-main.60.",
        "[20] Prihantoro, \"An evaluation of MorphInd's morphological annotation scheme for Indonesian,\" Corpora, vol. 16, no. 2, pp. 287--299, 2021. doi: 10.3366/cor.2021.0223.",
        "[21] L. N. Setra, Rondiyah, A. Kurniawaty, and R. Gayatri, \"Distribusi Pemakaian Kata Mamiq dalam Korpus Bahasa Sasak: Naskah Cilinaya dan Majalah Tambori,\" MABASAN: Jurnal Ilmiah Bahasa dan Sastra, vol. 17, no. 2, pp. 293--308, 2023. doi: 10.62107/mab.v17i2.814.",
        "[22] A. Romadhony, S. Al Faraby, R. Rismala, U. N. Wisesti, and A. Arifianto, \"Sentiment Analysis on a Large Indonesian Product Review Dataset,\" Journal of Information Systems Engineering and Business Intelligence (JISEBI), vol. 10, no. 1, pp. 167--178, 2024. doi: 10.20473/jisebi.10.1.167-178."
    ]

    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.0
        run_ref = p_ref.add_run(r)
        run_ref.font.name = "Times New Roman"
        run_ref.font.size = Pt(10)

    doc.save(output_path)
    print(f"✅ English ECTI-CIT Manuscript successfully generated: {output_path}")


# ==============================================================================
# 2. INDONESIAN VERSION BUILDER (EDISI BAHASA INDONESIA)
# ==============================================================================
def build_ecti_docx_id(output_path="artikel/jurnal_sasaknlp_id.docx"):
    doc = Document()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # SECTION 1: Single Column Header (Title & Authors)
    s1 = doc.sections[0]
    s1.page_width = Inches(8.27)
    s1.page_height = Inches(11.69)
    s1.top_margin = Inches(1.0)
    s1.bottom_margin = Inches(1.0)
    s1.left_margin = Inches(0.8)
    s1.right_margin = Inches(0.8)

    # Running Header
    header = s1.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run("Jurnal Riset Ilmu Komputer dan Teknologi Informasi (Format Standar Dua Kolom)")
    hrun.font.name = "Times New Roman"
    hrun.font.size = Pt(8.5)
    hrun.font.italic = True
    hrun.font.color.rgb = RGBColor(120, 120, 120)

    # Judul Artikel: 20 pt Bold, Spacing Before 0 pt, Spacing After 24 pt, Centered
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(24)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run("SasakNLP: Kerangka Kerja Hibrida untuk Pemrosesan Morfologi Bahasa Daerah Sasak Berdaya Komputasi Rendah")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(20)
    r_title.font.bold = True

    # Penulis: 12 pt Bold, Centered
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_before = Pt(0)
    p_auth.paragraph_format.space_after = Pt(8)
    r_auth = p_auth.add_run("kodetr")
    r_auth.font.name = "Times New Roman"
    r_auth.font.size = Pt(12)
    r_auth.font.bold = True

    # Afiliasi: 10 pt Italic, Centered
    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aff.paragraph_format.space_before = Pt(0)
    p_aff.paragraph_format.space_after = Pt(16)
    r_aff = p_aff.add_run("Riset Komputasi Bahasa Daerah Nusantara, kodetr.com\nLombok, Nusa Tenggara Barat, Indonesia\nKorespondensi: https://kodetr.com | Repositori Kode: https://github.com/kodetr/sasaknlp")
    r_aff.font.name = "Times New Roman"
    r_aff.font.size = Pt(10)
    r_aff.font.italic = True

    # SECTION 2: Continuous Break into Two Columns
    s2 = doc.add_section(WD_SECTION.CONTINUOUS)
    s2.top_margin = Inches(1.0)
    s2.bottom_margin = Inches(1.0)
    s2.left_margin = Inches(0.8)
    s2.right_margin = Inches(0.8)
    set_section_cols(s2, 2, 18)

    def add_sec_heading(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        return p

    def add_subsec_heading(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        return p

    def add_body(text, indent=True):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.25)
        else:
            p.paragraph_format.first_line_indent = Inches(0.0)
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        return p

    def add_equation(math_text_or_type, eq_num):
        """Insert an academic standard equation formatted as native Word Equation (OMML) with right-aligned numbering."""
        tbl = doc.add_table(rows=1, cols=2)
        tbl.autofit = False
        tbl.columns[0].width = Inches(2.7)
        tbl.columns[1].width = Inches(0.5)

        for cell in tbl.rows[0].cells:
            tcPr = cell._tc.get_or_add_tcPr()
            tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/></w:tcBorders>')
            tcPr.append(tcBorders)
            tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="80" w:type="dxa"/><w:left w:w="0" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tcMar>')
            tcPr.append(tcMar)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

        p_eq = tbl.rows[0].cells[0].paragraphs[0]
        p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_eq.paragraph_format.space_before = Pt(6)
        p_eq.paragraph_format.space_after = Pt(6)

        if "Confidence" in str(math_text_or_type) or str(math_text_or_type).strip() == "1" or "confidence" in str(math_text_or_type).lower():
            p_eq._p.append(parse_xml(make_eq1_omml()))
        elif "Score" in str(math_text_or_type) or str(math_text_or_type).strip() == "2" or "score" in str(math_text_or_type).lower():
            p_eq._p.append(parse_xml(make_eq2_omml()))
        else:
            r = p_eq.add_run(str(math_text_or_type))
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            r.font.italic = True

        p_num = tbl.rows[0].cells[1].paragraphs[0]
        p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_num.paragraph_format.space_before = Pt(6)
        p_num.paragraph_format.space_after = Pt(6)
        r_num = p_num.add_run(f"({eq_num})")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(10)
        return tbl

    def add_fig(img_rel_path, fig_no, caption_text, full_page_width=True, width_in=6.5):
        """Add a figure. If full_page_width is True, spans full page width (6.5 inches) across columns."""
        full_p = os.path.join(base_dir, img_rel_path)
        if not os.path.exists(full_p):
            print(f"Warning: Figure image not found: {full_p}")
            return

        if full_page_width:
            s_fig = doc.add_section(WD_SECTION.CONTINUOUS)
            s_fig.top_margin = Inches(1.0)
            s_fig.bottom_margin = Inches(1.0)
            s_fig.left_margin = Inches(0.8)
            s_fig.right_margin = Inches(0.8)
            set_section_cols(s_fig, 1)

        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(0)
        p_img.paragraph_format.keep_with_next = True
        p_img.add_run().add_picture(full_p, width=Inches(width_in if full_page_width else 3.1))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(12)
        r_num = p_cap.add_run(f"Gambar {fig_no}: ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(10)
        r_num.font.bold = True
        r_num.font.italic = True
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True

        if full_page_width:
            s_resume = doc.add_section(WD_SECTION.CONTINUOUS)
            s_resume.top_margin = Inches(1.0)
            s_resume.bottom_margin = Inches(1.0)
            s_resume.left_margin = Inches(0.8)
            s_resume.right_margin = Inches(0.8)
            set_section_cols(s_resume, 2, 18)

    def add_tbl(tbl_no, caption_text, headers, data, col_widths=None, full_page_width=True):
        """Add a table. If full_page_width is True, spans full page width (6.5 inches) across columns."""
        if full_page_width:
            s_tbl = doc.add_section(WD_SECTION.CONTINUOUS)
            s_tbl.top_margin = Inches(1.0)
            s_tbl.bottom_margin = Inches(1.0)
            s_tbl.left_margin = Inches(0.8)
            s_tbl.right_margin = Inches(0.8)
            set_section_cols(s_tbl, 1)

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(12)
        p_cap.paragraph_format.space_after = Pt(6)
        p_cap.paragraph_format.keep_with_next = True

        r_num = p_cap.add_run(f"Tabel {tbl_no}: ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(10)
        r_num.font.bold = True
        r_num.font.italic = True
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True

        tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="000000", sz="4")

        # Header Row
        header_row = tbl.rows[0]
        header_trPr = header_row._tr.get_or_add_trPr()
        header_trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        header_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        for i, h in enumerate(headers):
            cell = header_row.cells[i]
            cell.text = h
            set_cell_background(cell, "F1F5F9")
            set_cell_margins(cell, top=90, bottom=90, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(9)
                run.font.bold = True

        # Data Rows
        for r_idx, row_data in enumerate(data):
            row = tbl.rows[r_idx + 1]
            row_trPr = row._tr.get_or_add_trPr()
            row_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

            for c_idx, val in enumerate(row_data):
                cell = row.cells[c_idx]
                cell.text = str(val)
                bg_col = "FAFAFA" if r_idx % 2 == 1 else "FFFFFF"
                set_cell_background(cell, bg_col)
                set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
                p = cell.paragraphs[0]
                if str(val).endswith("%") or str(val).replace(".", "").replace(",", "").isdigit():
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(8.5)

        if col_widths:
            for row in tbl.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Inches(w)

        p_post = doc.add_paragraph()
        p_post.paragraph_format.space_before = Pt(0)
        p_post.paragraph_format.space_after = Pt(12)

        if full_page_width:
            s_resume = doc.add_section(WD_SECTION.CONTINUOUS)
            s_resume.top_margin = Inches(1.0)
            s_resume.bottom_margin = Inches(1.0)
            s_resume.left_margin = Inches(0.8)
            s_resume.right_margin = Inches(0.8)
            set_section_cols(s_resume, 2, 18)

        return tbl

    # Abstrak Bahasa Indonesia
    p_ab_title = doc.add_paragraph()
    p_ab_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_ab_title.paragraph_format.space_before = Pt(0)
    p_ab_title.paragraph_format.space_after = Pt(4)
    r_abt = p_ab_title.add_run("ABSTRAK")
    r_abt.font.name = "Times New Roman"
    r_abt.font.size = Pt(10)
    r_abt.font.bold = True

    p_ab_body = doc.add_paragraph()
    p_ab_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ab_body.paragraph_format.space_before = Pt(0)
    p_ab_body.paragraph_format.space_after = Pt(12)
    p_ab_body.paragraph_format.line_spacing = 1.0
    r_abb = p_ab_body.add_run(
        "Bahasa Sasak (Basa Sasak) merupakan bahasa daerah berakar Austronesia yang dituturkan oleh lebih dari 3 juta penduduk "
        "di Pulau Lombok, Nusa Tenggara Barat, Indonesia. Meskipun memiliki vitalitas demografis yang tinggi, Bahasa Sasak tergolong "
        "sebagai bahasa dengan sumber daya komputasi rendah (low-resource language) akibat kelangkaan korpus teks teranotasi, variasi "
        "dialektal yang tajam lintas wilayah geografis, serta ketiadaan pustaka pemrosesan bahasa alami (NLP) terstandar [1], [6]. "
        "Analisis morfologi Bahasa Indonesia standar gagal diterapkan pada Bahasa Sasak akibat perbedaan alternasi morfofonemik, "
        "penempelan klitika bertingkat, dan variasi leksikal dialek antardaerah [9], [11], [13]. Artikel ini memperkenalkan SasakNLP, sebuah "
        "kerangka kerja pemrosesan morfologi sadar dialek yang dirancang khusus untuk standardisasi ortografi, tokenisasi reduplikasi, deteksi "
        "dialek berbasis penanda leksikal diagnostik (shibboleths), serta lematisasi bertingkat yang divalidasi leksikon resmi Balai Bahasa "
        "Provinsi NTB [9], [10], [13]. Evaluasi empiris dilakukan secara ketat pada tolok ukur baku emas 100.000 pasangan morfem dan korpus "
        "autentik 12.591 kalimat. SasakNLP membukukan akurasi lematisasi sebesar 80,44% (80.438 prediksi benar) pada benchmark 100k, mengungguli "
        "Direct Lexicon Lookup (1,01%) dan Greedy Affix Stripping (55,21%) secara signifikan berdasarkan uji McNemar (χ² = 14.962,14, p < 0,0001). "
        "Pada benchmark inti 10.000 data, akurasi lematisasi mencapai 93,23%. Analisis taksonomi kesalahan membuktikan overstemming ditekan hingga "
        "2,28% dan understemming sebesar 15,86% pada imbuhan bertingkat. SasakNLP membukukan throughput 7.826 kata per detik pada pemrosesan batch 100k "
        "dan hingga 16.272 kata per detik pada benchmark standar dengan latensi rata-rata 0,044 milidetik per kata tanpa dependensi pustaka pihak ketiga. "
        "Seluruh kode sumber, dataset, dan tolok ukur dirilis secara terbuka demi keterulangan riset [16]."
    )
    r_abb.font.name = "Times New Roman"
    r_abb.font.size = Pt(10)

    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.space_before = Pt(12)
    p_kw.paragraph_format.space_after = Pt(12)
    p_kw.paragraph_format.line_spacing = 1.0
    r_kwt = p_kw.add_run("Kata Kunci: ")
    r_kwt.font.name = "Times New Roman"
    r_kwt.font.size = Pt(10)
    r_kwt.font.bold = True
    r_kwb = p_kw.add_run("Bahasa Sasak, Pemrosesan Bahasa Alami, Lematisasi Komputasional, Morfologi Austronesia, Dialektologi Komputasi, Low-Resource Language, Balai Bahasa NTB, Open Science.")
    r_kwb.font.name = "Times New Roman"
    r_kwb.font.size = Pt(10)

    # 1. PENDAHULUAN
    add_sec_heading("1. PENDAHULUAN")
    add_body(
        "Kemajuan kontemporer dalam bidang Pemrosesan Bahasa Alami (Natural Language Processing / NLP) dan Model Bahasa Skala Besar "
        "(Large Language Models / LLM) sebagian besar terkonsentrasi pada bahasa-bahasa berdaya komputasi tinggi (high-resource languages) [1], [2]. "
        "Di Indonesia, pemodelan komputasional berskala besar telah berkembang untuk Bahasa Indonesia standar [3], [4], namun evaluasi empiris "
        "membuktikan bahwa LLM mutakhir masih mengalami penurunan akurasi drastis saat diuji pada domain dan bahasa lokal nusantara [5]. "
        "Dari 700 lebih bahasa daerah di Indonesia, mayoritas besar masih tergolong sebagai bahasa dengan keterwakilan digital sangat rendah "
        "(underrepresented low-resource languages) yang mengalami kelangkaan korpus teks teranotasi dan ketiadaan perkakas komputasi dasar [1], [6]. "
        "Penurunan kinerja model hilir pada bahasa lokal ini sangat dipicu oleh ketidaksesuaian kosakata (vocabulary mismatch) dan variasi "
        "morfologi yang tidak terakomodasi dalam tokenisasi standar [7], terlebih lagi setiap wilayah di Indonesia memiliki karakteristik budaya "
        "dan ragam ekspresi lokal yang sangat heterogen lintas provinsi [8]."
    )
    add_body(
        "Bahasa Sasak (Basa Sasak) merupakan salah satu bahasa daerah Austronesia terbesar di wilayah Indonesia bagian tengah, dituturkan oleh "
        "lebih dari 3 juta penduduk di Pulau Lombok, Provinsi Nusa Tenggara Barat [9], [10]. Secara morfologis, fonologis, dan sosiopragmatik, "
        "Bahasa Sasak memiliki karakteristik unik yang membedakannya secara tegas dari Bahasa Indonesia maupun bahasa-bahasa Austronesia tetangganya:"
    )
    add_body(
        "1) Afiksasi Morfofonemik yang Kompleks: Pembentukan kata turunan melibatkan prefiksasi pasif (te-), statif (ka-), ekuatif (se-), "
        "dan nominalizer (pe-/peng-); infiksasi arkais (-in-, -um-); sufiksasi kausatif dan lokatif (-ang, -an, -i, -in); serta konfiksasi gabung "
        "bertingkat (pe-...-an, te-...-ang, be-...-an) dan alternasi nasal produktif (N-) [10], [13]."
    )
    add_body(
        "2) Klitika Pronomina dan Kesantunan Sosial: Enklitika posesif (-ku, -m, -ne) dan penanda kesantunan sosial (-de, -te) kerap melekat "
        "berlapis pada ujung kata (misalnya pegawianne, balende), yang mencerminkan hierarki pragmatik dan tingkat tutur masyarakat Sasak [11] "
        "serta kerap memicu pemotongan berlebihan (overstemming) atau kegagalan pengupasan (understemming) pada algoritma heuristik konvensional [13]."
    )
    add_body(
        "3) Fragmentasi Dialektal Lintas Wilayah: Bahasa Sasak terdistribusi ke dalam lima klaster dialek utama yang ditandai oleh penanda diagnostik "
        "leksikal (shibboleths) yang kontras, mulai dari dialek Selaparang (Menu-Meni) di Lombok Timur hingga dialek arkais Kuto-Kute di Lombok Utara [9], [12]."
    )
    add_body(
        "Penelitian pemrosesan morfologi komputasional terdahulu pada bahasa daerah nusantara umumnya terkonsentrasi pada Bahasa Jawa dan Bahasa Sunda "
        "[1], [13], [14], sedangkan telaah komputasi untuk bahasa etnik di kawasan timur Indonesia masih sangat terbatas pada induksi leksikon dwibahasa [15]. "
        "Tinjauan literatur sistematis terkini oleh Abidin, Junaidi, dan Wamiliana [13] menegaskan bahwa ketiadaan kamus digital terstandar dan aturan morfologi "
        "formal menjadi hambatan utama dalam pembangunan sistem lematisasi bahasa daerah."
    )
    add_body(
        "Untuk menjawab tantangan ilmiah tersebut, penelitian ini memperkenalkan SasakNLP, sebuah kerangka kerja pemrosesan morfologi dan NLP sadar dialek "
        "berstandar riset yang dirancang dari nol dengan prinsip clean architecture, efisiensi deterministik tanpa dependensi eksternal berat, serta integrasi "
        "langsung dengan kamus terpadu Balai Bahasa Provinsi NTB [10], [16]. Mengadopsi prinsip morfologi dua tingkat [17] dan segmentasi morfem kanonik [18], "
        "SasakNLP mengatasi batas segmentasi morfem pada bahasa berdaya komputasi rendah."
    )
    add_body(
        "Kontribusi utama penelitian ini dirumuskan sebagai berikut:\n"
        "• C1. Sumber Daya Leksikal Mesin SasakLex: Digitalisasi kamus terpadu Balai Bahasa NTB sebanyak 2.761 entri terstruktur dengan penanda kelas kata dan dialek [10], [16].\n"
        "• C2. Kerangka Morfologi Hibrida: Arsitektur lematisasi deterministik menggabungkan two-pass affix stripping, validasi kamus O(L) via PrefixTrie, dan perankingan multi-kriteria [13], [17].\n"
        "• C3. Analisis Morfologi Terstruktur: Penguraian morfonemik eksplisit yang mengidentifikasi prefiks, infiks, sufiks, konfiks, klitika, dan reduplikasi beserta skor keyakinan [17], [18].\n"
        "• C4. Arsitektur Sadar Dialek: Mekanisme deteksi densitas penanda shibboleth lintas lima dialek Pulau Lombok [9], [12].\n"
        "• C5. Tolok Ukur Terbuka: Rilis tolok ukur baku emas 100.000 pasangan morfem, korpus 12.591 kalimat autentik, paket PyPI (sasaknlp), dan dataset Hugging Face Hub [16]."
    )

    # 2. KAJIAN PUSTAKA DAN LANDASAN LINGUISTIK
    add_sec_heading("2. KAJIAN PUSTAKA DAN LANDASAN LINGUISTIK")
    add_subsec_heading("2.1 Lanskap NLP Bahasa Daerah Nusantara")
    add_body(
        "Pengembangan teknologi bahasa daerah di Indonesia menghadapi tantangan kelangkaan data anotasi yang persisten [1], [2], [6]. Inisiatif "
        "NusaCrowd [6] dan tolok ukur NusaX [7] telah berhasil memetakan puluhan bahasa daerah ke dalam tugas evaluasi klasifikasi sentimen, sementara "
        "NusaWrites [19] membuktikan pentingnya pengumpulan teks autentik dari penutur asli untuk menghindari distorsi terjemahan mesin. Namun, pada "
        "tataran pemrosesan morfologi mendasar, model subword berbasis BPE sering memecah kata berimbuhan bahasa daerah menjadi serpihan karakter tanpa makna [3], [14]."
    )
    add_body(
        "Pada ranah bahasa daerah, Wijono et al. [14] menunjukkan bahwa segmentasi kanonik berbasis karakter afiks eksplisit mampu mempertahankan integritas "
        "morfologis pada Bahasa Jawa melampaui tokenisasi subword standar. Di sisi lain, evaluasi skema morfologi formal seperti MorphInd membuktikan bahwa aturan "
        "leksikon terstruktur esensial untuk membatasi ambiguitas gramatikal [20]. Tinjauan literatur sistematis oleh Abidin et al. [13] menyimpulkan bahwa penggabungan "
        "kamus digital rujukan dengan aturan afiksasi bertingkat merupakan pendekatan paling efektif untuk meminimalkan overstemming dan understemming pada bahasa "
        "berdaya komputasi rendah. Strategi integrasi leksikon kamus terverifikasi sebagai pengontrol gerbang juga selaras dengan temuan induksi leksikon bahasa etnik "
        "oleh Resiandi et al. [15] serta prinsip morfologi komputasional klasik [17]."
    )

    add_subsec_heading("2.2 Sistem Morfologi dan Afiksasi Bahasa Sasak")
    add_body(
        "Merujuk pada kodifikasi tata bahasa dan leksikon resmi Balai Bahasa Provinsi NTB [10], kajian sosiopragmatik kesantunan Sasak [11], serta studi morfoleksikal "
        "mutakhir [9], [12], inventaris morfem terikat Bahasa Sasak terdiri atas:\n"
        "1) Prefiks: Pasif te- (tepinaq 'dibuat'), statif ka- (kasolah 'diperbagus'), ekuatif se- (sebale 'serumah'), nominalizer pe-/peng- (pegawi 'pekerja'), dan asimilasi nasal N- (nulis, minaq).\n"
        "2) Sufiks: Kausatif -ang (tulungang 'tolongkan'), lokatif/hasil -an (kelororan 'aliran'), iteratif -i/-in (sirami).\n"
        "3) Infiks: Pasif arkais -in- (tinulung 'diberi pertolongan') dan intransitif -um- (gumingsir 'bergeser').\n"
        "4) Konfiks: Nomina proses pe-...-an (pegawian 'pekerjaan'), pasif kausatif te-...-ang (tetulungang), statif ka-...-an, resiprokal be-...-an (betulungan).\n"
        "5) Enklitika: Posesif -ku, -m, -ne, serta ragam santun krama -de, -te (baturne, balende) [11].\n"
        "6) Reduplikasi: Kata ulang penuh bertanda hubung (bareng-bareng, mangan-mangan)."
    )

    add_subsec_heading("2.3 Taksonomi Dialek Bahasa Sasak")
    add_body(
        "Studi dialektologi kebahasaan di Nusa Tenggara Barat [9], [10], [12] memetakan variasi geolinguistik Bahasa Sasak ke dalam lima klaster dialek utama "
        "berdasarkan kata diagnostik pembeda (Tabel 1)."
    )

    # TABEL 1: Full-Page Width (6.5 inches)
    t1_headers = ["No", "Klaster Dialek", "Sebaran Wilayah Geografis", "Penanda Diagnostik (Shibboleths)", "Ciri Fonologis & Sosiolek"]
    t1_data = [
        ["1", "Meno-Mene (Selaparang)", "Lombok Timur & Lombok Tengah", "menu, meni, tiyang, kaji", "Ragam krama (alus), retensi hentian glotal /-q/, ciri vokal /-e/"],
        ["2", "Ngeno-Ngene", "Kota Mataram & Lombok Barat", "ngeno, ngene, ente, aku", "Dialek perkotaan, artikulasi vokal cepat, kontak maritim"],
        ["3", "Merikuq-Merikaq (Mriak-Mriku)", "Lombok Tengah Selatan (Praya, Pujut)", "mriak, mriku, meriq, merik", "Deiksis spasial arah (ke mari / ke sana), vokal /-a/ dan /-u/"],
        ["4", "Kuto-Kute (Ngeto-Ngete)", "Lombok Utara & Sembalun (Bayan, Suela)", "kuto, kute, ngeto, wetu", "Retensi arkais Austronesia tua, tradisi adat Wetu Telu, komunitas dataran tinggi"],
        ["5", "Sasak Umum (General Standard)", "Lintas Wilayah Pulau Lombok", "wah, ndeq, mangan, batur", "Bahasa pergaulan antardialek di ruang publik, rujukan leksikon Balai Bahasa NTB"]
    ]
    add_tbl(1, "Taksonomi 5 Klaster Dialek Utama Bahasa Sasak di Pulau Lombok [9], [10], [12]", t1_headers, t1_data, col_widths=[0.4, 1.4, 1.4, 1.3, 2.0], full_page_width=True)

    # 3. METODOLOGI DAN ARSITEKTUR SISTEM SASAKNLP
    add_sec_heading("3. METODOLOGI DAN ARSITEKTUR SISTEM SASAKNLP")
    add_subsec_heading("3.1 Gambaran Umum Sistem")
    add_body(
        "SasakNLP mengimplementasikan arsitektur modular deterministik enam tahap yang dirancang tanpa memerlukan dependensi pustaka deep learning eksternal, "
        "menjamin latensi eksekusi sub-milidetik yang deterministik dan konsisten."
    )

    add_subsec_heading("3.2 Normalisasi Ortografi dan Teks")
    add_body(
        "Tahap normalisasi mengatasi variasi representasi digital pada teks bahasa daerah [1], [6]: standarisasi Unicode NFC, penyeragaman variasi grafem hentian "
        "glotal (mengubah tanda petik miring menjadi karakter kanonik q atau '), dan konversi vokal beraksen (è, é) ke vokal Latin standar tanpa merusak fonem pembeda."
    )

    add_subsec_heading("3.3 Tokenisasi Sadar Reduplikasi")
    add_body(
        "Algoritma tokenisasi mendeteksi pola dwilingga bertanda hubung ([Kata]-[Kata]) sebagai entitas morfologis tunggal, sehingga mencegah pemisahan kata ulang "
        "menjadi dua token parsial yang keliru [13], [17]."
    )

    add_subsec_heading("3.4 Kontekstualisasi Dialek Berbasis Penanda Shibboleth")
    add_body(
        "Modul DialectDetector menghitung densitas relatif kemunculan penanda shibboleth dalam teks masukan [9], [12]:"
    )
    add_equation("confidence", "1")
    add_body(
        "di mana T adalah himpunan token kalimat masukan, Md adalah himpunan penanda leksikal diagnostik (shibboleth) untuk dialek d, dan ω(w) adalah bobot keunikan leksikal kata."
    )

    add_subsec_heading("3.5 Pembangkitan Kandidat Dua Tahap dan Validasi PrefixTrie")
    add_body(
        "Token yang tidak ditemukan dalam leksikon melalui Direct Lookup diproses oleh CandidateGenerator. Aturan afiksasi diterapkan secara bertahap (two-pass "
        "affix stripping): pengupasan enklitika, konfiks terpanjang, prefiks/sufiks, inversi infiks, dan reduplikasi. Kandidat lema divalidasi ke leksikon Balai "
        "Bahasa NTB (2.761 entri) menggunakan struktur data PrefixTrie berkecepatan O(L) [10], [17], [18]."
    )

    add_subsec_heading("3.6 Perankingan Kandidat Multi-Kriteria")
    add_body(
        "Ambiguitas morfologis diselesaikan menggunakan fungsi perankingan multi-kriteria terbobot [17]:"
    )
    add_equation("score", "2")
    add_body(
        "dengan bobot empiris teroptimasi: w_lex = 0,40, w_morph = 0,25, w_conf = 0,15, w_freq = 0,10, dan w_dial = 0,10."
    )

    add_subsec_heading("3.7 Keluaran Morfologi Terstruktur")
    add_body(
        "Sistem menghasilkan keluaran terstruktur kompatibel JSON yang memuat lema dasar, penguraian afiks gramatikal, klasifikasi dialek, dan skor keyakinan."
    )

    # 4. PENGATURAN EKSPERIMEN DAN PROTOKOL DATASET
    add_sec_heading("4. PENGATURAN EKSPERIMEN DAN PROTOKOL DATASET")
    add_subsec_heading("4.1 Sumber Daya Data Riset (Protokol 3-Fase)")
    add_body(
        "Dataset tolok ukur dikurasi melalui protokol ilmiah 3-fase terstruktur untuk menjamin keaslian data (Gambar 1):\n"
        "1) Tolok Ukur Morfologi 100k (benchmark_100k.csv): 100.000 pasangan data uji morfologi terkontrol mencakup anotasi bentuk turunan, lema dasar baku emas, afiksasi, dan dialek.\n"
        "2) Tolok Ukur Morfologi Inti 10k (benchmark_10k.csv): 10.000 pasangan morfem inti untuk pengujian lematisasi reguler harian.\n"
        "3) Korpus Kalimat Autentik (sasak_sentences_large.csv): 12.591 kalimat autentik (188.881 kata) yang dihimpun dari sastra lisan (Putri Mandalika, Dewi Anjani, Datu Doyan Nada), media bahasa daerah, dan arsip Balai Bahasa NTB [10], [16], [21].\n"
        "4) Leksikon Kamus NTB (kamus_balai_bahasa_ntb.csv): 2.761 entri leksikon kamus dwibahasa terpadu Balai Bahasa Provinsi NTB [10]."
    )

    # GAMBAR 1: Full-Page Width (6.5 inches)
    add_fig("figures/fig5_dataset_acquisition_pipeline.png", 1, "Protokol Ilmiah 3-Fase Akuisisi Data Dan Kurasi Kualitas Artefak Riset SasakNLP.", full_page_width=True, width_in=6.5)

    add_subsec_heading("4.2 Model Acuan Pembanding (Baselines)")
    add_body(
        "Pengujian komparatif dilakukan terhadap dua model acuan konvensional pada 100.000 data:\n"
        "• Baseline 1 (Direct Lexicon Lookup): Pencocokan eksak kamus leksikon tanpa aturan pengupasan afiks.\n"
        "• Baseline 2 (Greedy Affix Stripping): Pemotongan afiks terpanjang tanpa validasi kamus pengontrol [13]."
    )

    add_subsec_heading("4.3 Metrik Evaluasi dan Lingkungan Komputasi")
    add_body(
        "Metrik evaluasi mencakup akurasi lematisasi eksak, throughput (kata/detik), latensi per token (ms), tingkat overstemming, understemming, dan out-of-vocabulary (OOV). "
        "Pengujian dijalankan pada CPU Apple Silicon (8-Core) dan Intel Core i7 x86_64 dengan RAM 16 GB di bawah Python 3.10+, menjamin replikabilitas deterministik 100% [16]."
    )

    # 5. HASIL EVALUASI EMPIRIS
    add_sec_heading("5. HASIL EVALUASI EMPIRIS")
    add_subsec_heading("5.1 Evaluasi Komparatif terhadap Model Acuan pada 100.000 Sampel")
    add_body(
        "Pengujian komparatif pada 100.000 pasangan data morfologi membuktikan keunggulan mutlak SasakNLP (Tabel 2). Baseline 1 hanya meraih akurasi 1,01% karena "
        "gagal menangani kata berimbuhan. Baseline 2 meraih 55,21% namun mengalami overstemming parah. SasakNLP meraih akurasi 80,44% (80.438 prediksi benar)."
    )

    # TABEL 2: Full-Page Width (6.5 inches)
    t2_headers = ["Model / Algoritma", "Prinsip Komputasi", "Prediksi Benar (N=100k)", "Akurasi (%)", "Throughput (kata/detik)"]
    t2_data = [
        ["Baseline 1: Direct Lookup", "Exact Dictionary Matching", "1.006", "1,01%", "24.500"],
        ["Baseline 2: Greedy Stripping", "Longest-Match Affix Stripping", "55.205", "55,21%", "18.200"],
        ["Proposed SasakNLP", "Dictionary-Enhanced Multi-Candidate", "80.438", "80,44%", "7.826"]
    ]
    add_tbl(2, "Evaluasi Komparatif terhadap Model Acuan pada 100.000 Sampel Morfologi", t2_headers, t2_data, col_widths=[1.7, 1.8, 1.0, 0.9, 1.1], full_page_width=True)

    add_body(
        "Uji berpasangan McNemar antara SasakNLP dan Baseline 2 menghasilkan matriks kontinjensi: "
        "a = 46.546 (keduanya benar), b = 33.892 (SasakNLP benar, Baseline 2 salah), "
        "c = 8.659 (SasakNLP salah, Baseline 2 benar), dan d = 10.903 (keduanya salah). "
        "Statistik uji chi-squared = 14.962,14 (df = 1, p < 0,0001), membuktikan keunggulan "
        "SasakNLP signifikan secara statistik pada alpha = 0,001."
    )

    add_subsec_heading("5.2 Kinerja pada Tolok Ukur Inti 10k")
    add_body(
        "Pada tolok ukur inti 10.000 pasangan morfem (benchmark_10k.csv), SasakNLP mencatatkan 9.323 prediksi benar dari 10.000 sampel uji (akurasi 93,23%) "
        "dengan kecepatan eksekusi 16.272 kata per detik, membuktikan presisi tinggi pada distribusi bahasa alami harian."
    )

    add_subsec_heading("5.3 Studi Ablasi Komponen Arsitektur")
    add_body(
        "Studi ablasi bertahap pada 100.000 data mengisolasi kontribusi masing-masing komponen (Tabel 3). Penambahan validasi kamus PrefixTrie meningkatkan "
        "akurasi sebesar +13,24%, dan modul Candidate Generator + Ranker memberikan peningkatan tambahan sebesar +11,99%."
    )

    # TABEL 3: Full-Page Width (6.5 inches)
    t3_headers = ["Konfigurasi", "Aturan", "Kamus", "Gen", "Rank", "Dialek", "Akurasi (%)", "Throughput"]
    t3_data = [
        ["M1: Direct Lookup", "Tidak", "Ya", "Tidak", "Tidak", "Tidak", "1,01%", "24.500 wps"],
        ["M2: Greedy Stripping", "Ya", "Tidak", "Tidak", "Tidak", "Tidak", "55,21%", "18.200 wps"],
        ["M3: Rules + Dict Gate", "Ya", "Ya", "Tidak", "Tidak", "Tidak", "68,45%", "14.100 wps"],
        ["M4: Rules + Gen + Match 1", "Ya", "Ya", "Ya", "Tidak", "Tidak", "74,12%", "10.350 wps"],
        ["M5: Full SasakNLP", "Ya", "Ya", "Ya", "Ya", "Ya", "80,44%", "7.826 wps"]
    ]
    add_tbl(3, "Studi Ablasi Kontribusi Komponen Sistem SasakNLP (100k Data)", t3_headers, t3_data, col_widths=[1.7, 0.6, 0.6, 0.6, 0.6, 0.6, 0.8, 1.0], full_page_width=True)

    add_subsec_heading("5.4 Evaluasi Kinerja per Kategori Morfem")
    add_body(
        "Evaluasi disaggregasi morfologis (Gambar 2 dan Tabel 4) menunjukkan performa stabil pada afiks tunggal dan reduplikasi. Reduplikasi meraih 100,00%, "
        "prefiks pasif mencapai 97,36%, prefiks statif mencapai 96,79%, dan klitika posesif melampaui 94,6%–96,5%."
    )

    # GAMBAR 2: Full-Page Width (6.5 inches)
    add_fig("figures/fig1_morphology_accuracy.png", 2, "Rincian Akurasi Aturan Morfologi SasakNLP pada Seluruh Kelas Afiksasi (100k Data).", full_page_width=True, width_in=6.5)

    # TABEL 4: Full-Page Width (6.5 inches)
    t4_headers = ["Kategori Morfologi", "Pola Morfem", "Jumlah", "Akurasi (%)", "Karakteristik Linguistik & Penanganan"]
    t4_data = [
        ["Reduplikasi", "root-root", "1.789", "100,00%", "Penanganan sempurna kata ulang dwilingga (mangan-mangan)"],
        ["Prefiks Pasif", "te-", "1.783", "97,36%", "Verba pasif (tetulung, tepinaq)"],
        ["Prefiks Statif", "ka-", "1.745", "96,79%", "Penanda keadaan (kasolah, kabeleq)"],
        ["Prefiks Peng-", "peng-", "1.781", "96,91%", "Nomina pelaku/alat (penggawi, pengonang)"],
        ["Prefiks Ekuatif", "se-", "1.748", "96,22%", "Penanda kesatuan (sebale, sekance)"],
        ["Klitika Posesif 1", "-ku", "1.782", "96,58%", "Enklitika orang pertama (baleku, jaranku)"],
        ["Klitika Posesif 2", "-m", "1.778", "96,18%", "Enklitika orang kedua akrab (matam, bajum)"],
        ["Klitika Posesif 3", "-ne", "3.571", "94,62%", "Enklitika orang ketiga (baturne, kawanne)"],
        ["Sufiks Iteratif", "-i", "1.771", "91,53%", "Sufiks pengulangan tindakan (sirami, antoli)"],
        ["Infiks Pasif/Kausatif", "-in-, -um-", "2.346", "89,98%", "Sisipan produktif Sasak (tinulung, gumingsir)"],
        ["Klitika Santun", "-de, -te", "6.312", "88,39%", "Klitika ragam halus Sasak (balende, balente)"],
        ["Konfiks Pasif", "te-...-ang", "4.578", "96,96%", "Konfiks pasif aplikatif (tetulungang)"],
        ["Konfiks Nomina", "pe-...-an", "5.915", "88,32%", "Pembentuk nomina abstrak (pegawian)"],
        ["Sufiks Transitif", "-ang", "6.170", "83,70%", "Sufiks kausatif aktif (tulungang, pinaqang)"],
        ["Sufiks Lokatif", "-an, -in", "10.545", "76,52%", "Penanda lokatif/tujuan (kaduan, siramin)"],
        ["Konfiks Resiprokal", "be-...-an", "1.710", "65,09%", "Tindakan berbalasan (betulungan, besambatan)"]
    ]
    add_tbl(4, "Rincian Kinerja Lematisasi pada 16 Kategori Morfem Representatif Utama (N = 55.324) pada Tolok Ukur 100.000 Sampel Uji", t4_headers, t4_data, col_widths=[1.4, 0.9, 0.8, 0.9, 2.5], full_page_width=True)
    add_body(
        "Catatan: 16 kategori yang ditampilkan pada Tabel 4 merepresentasikan bentuk afiks tunggal dan konfiks utama yang umum dijumpai (N = 55.324). "
        "Sebanyak 44.676 sampel lainnya pada tolok ukur 100.000 data mencakup kombinasi afiksasi bertingkat tiga lapis yang lebih kompleks, pemajemukan, "
        "dan variasi turunan dialek yang didokumentasikan secara lengkap pada repositori dataset riset.",
        indent=False
    )

    add_subsec_heading("5.5 Evaluasi Lintas Lima Dialek Sasak")
    add_body(
        "Evaluasi pada lima klaster dialek mengonfirmasi ketahanan leksikal model di seluruh Pulau Lombok (Gambar 3 dan Tabel 5)."
    )

    # GAMBAR 3: Full-Page Width (6.5 inches)
    add_fig("figures/fig2_dialect_performance.png", 3, "Perbandingan Performa Lematisasi SasakNLP Lintas Lima Klaster Dialek Utama Bahasa Sasak.", full_page_width=True, width_in=6.5)

    # TABEL 5: Full-Page Width (6.5 inches)
    t5_headers = ["Wilayah Penutur", "Klaster Dialek Sasak", "Jumlah", "Akurasi (%)", "Ciri Fonologis & Fonem Utama"]
    t5_data = [
        ["Kota Mataram & Lombok Barat", "Sasak Umum (General Standard)", "43.254", "85,73%", "Sesuai ragam baku kamus Balai Bahasa NTB"],
        ["Lombok Utara", "Kuto-Kute (Ngeto-Ngete)", "10.475", "80,31%", "Vokal akhir /-e/ dan /-o/ (kuto, kute), retensi arkais"],
        ["Lombok Selatan", "Merikuq-Merikaq (Mriak-Mriku)", "10.535", "79,79%", "Vokal /-a/ dan /-u/ dengan hentian glotal /-q/"],
        ["Lombok Tengah", "Meno-Mene (Selaparang)", "23.023", "77,04%", "Vokal /-e/, dialek dengan penutur terbanyak"],
        ["Lombok Timur", "Ngeno-Ngene", "12.713", "69,24%", "Variasi vokal sengau dan konsonan velar /-k/"]
    ]
    add_tbl(5, "Performa Lematisasi Lintas 5 Klaster Dialek Utama Sasak (100k Data)", t5_headers, t5_data, col_widths=[1.3, 1.3, 0.8, 0.9, 2.2], full_page_width=True)

    add_subsec_heading("5.6 Skalabilitas Komputasi dan Latensi Waktu Nyata")
    add_body(
        "Pengukuran profil komputasi membuktikan skalabilitas linier O(N) terhadap panjang teks (Gambar 4). Throughput mencapai 7.826 kata/detik "
        "pada pemrosesan batch 100k dan 16.272 kata/detik pada benchmark 10k, dengan latensi rata-rata 0,044 ms per token."
    )

    # GAMBAR 4: Full-Page Width (6.5 inches)
    add_fig("figures/fig4_pipeline_benchmark.png", 4, "Kinerja Komputasi SasakNLP: Throughput Kata per Detik Dan Profil Latensi per Kalimat.", full_page_width=True, width_in=6.5)

    add_subsec_heading("5.7 Evaluasi Ekstrinsik Reduksi Ruang Fitur Kosakata")
    add_body(
        "Pada evaluasi hilir, lematisasi SasakNLP mereduksi ruang dimensi kosakata korpus teks autentik dari 5.913 kata unik menjadi 4.022 lema dasar "
        "(kompresi sebesar 31,98%, Tabel 6), memangkas tingkat sparsity matriks representasi teks untuk tugas klasifikasi dan temu balik informasi [13], [22]."
    )

    # TABEL 6: Full-Page Width (6.5 inches)
    t6_headers = ["Parameter Korpus / Dataset", "Bentuk Permukaan", "Lema Dasar", "Rasio Reduksi", "Dampak pada Pemodelan NLP Hilir"]
    t6_data = [
        ["Benchmark Morfologi (100k)", "100.000 kata unik", "1.790 lema", "98,21%", "Mengurangi beban pencarian leksikal hingga 55× lipat"],
        ["Korpus Teks Riil (189k token)", "5.913 kata unik", "4.022 lema", "31,98%", "Memangkas sparsity matriks representasi teks sebesar 32%"]
    ]
    add_tbl(6, "Evaluasi Kompresi Ruang Fitur Kosakata pada Dataset Riset", t6_headers, t6_data, col_widths=[1.6, 1.1, 1.1, 0.9, 1.8], full_page_width=True)

    # 6. PEMBAHASAN DAN ANALISIS TAKSONOMI KESALAHAN
    add_sec_heading("6. PEMBAHASAN DAN ANALISIS TAKSONOMI KESALAHAN")
    add_subsec_heading("6.1 Analisis Taksonomi Kesalahan dan Modus Kegagalan")
    add_body(
        "Diagnosis komprehensif atas kegagalan morfologis pada 100.000 data benchmark dipetakan ke dalam empat klasifikasi (Gambar 5, Tabel 7)."
    )

    # GAMBAR 5: Full-Page Width (6.5 inches)
    add_fig("figures/fig3_error_taxonomy.png", 5, "Distribusi Taksonomi Kesalahan Lematisasi (Kiri) Dan Matriks Diagnosis Kegagalan Linguistik (Kanan).", full_page_width=True, width_in=6.5)

    # TABEL 7: Full-Page Width (6.5 inches)
    t7_headers = ["Klasifikasi", "Definisi Komputasional", "Contoh Masukan -> Pred", "Jumlah", "Persen (%)", "Akar Penyebab Linguistik"]
    t7_data = [
        ["Prediksi Benar", "Lema prediksi identik dengan lema kamus", "tepinaq -> pinaq", "80.438", "80,44%", "Aturan afiksasi dan leksikon cocok tepat"],
        ["Understemming", "Panjang prediksi > panjang lema dasar", "pegawianne -> pegawian (gawi)", "15.856", "15,86%", "Imbuhan 3 lapis belum tuntas terkelupas di pass 1"],
        ["Overstemming", "Huruf akar kata asli terpotong", "jaran -> jar (akhiran -an)", "2.279", "2,28%", "Huruf akhir akar kata mirip morfem terikat"],
        ["Incorrect Lemma", "Panjang sama namun karakter beda", "mangan -> pangan (mangan)", "1.427", "1,43%", "Ambiguitas alternasi nasal (m -> p vs m -> m)"],
        ["OOV Error", "Lema tidak ada di kamus rujukan", "Kata serapan / neologisme", "0", "0,00%", "Semua lema benchmark tercakup dalam kamus"]
    ]
    add_tbl(7, "Analisis Taksonomi Kesalahan pada 100.000 Sampel Tolok Ukur Morfologi", t7_headers, t7_data, col_widths=[1.1, 1.4, 1.3, 0.7, 0.6, 1.4], full_page_width=True)

    add_subsec_heading("6.2 Kekuatan Algoritmik Validasi Kamus PrefixTrie")
    add_body(
        "Keunggulan performa SasakNLP bersumber dari validasi PrefixTrie sebagai gerbang verifikasi kamus [10], [17]. Pada pendekatan naif greedy "
        "(Baseline 2), kata seperti jaran ('kuda') secara keliru dipotong menjadi jar karena akhiran -an disangka sufiks. Dalam SasakNLP, kata jaran "
        "cocok dengan kamus Balai Bahasa NTB pada lintasan pertama, sehingga pemotongan keliru dapat dicegah sepenuhnya."
    )

    add_subsec_heading("6.3 Analisis Kesenjangan Kinerja Tolok Ukur 100k vs 10k")
    add_body(
        "Perbedaan akurasi antara benchmark 100k (80,44%) dan benchmark 10k (93,23%) mencerminkan perbedaan kompleksitas linguistik. Benchmark 100k "
        "berfungsi sebagai uji tekanan (stress-test) dengan kombinasi imbuhan berlapis tiga (misalnya pe-...-an ditambah -ne dan te-), sedangkan benchmark "
        "10k mencerminkan distribusi alami tuturan sehari-hari."
    )

    add_subsec_heading("6.4 Implikasi bagi Ekosistem NLP Bahasa Daerah")
    add_body(
        "Temuan ini membuktikan bahwa bahasa daerah berdaya komputasi rendah di Indonesia dapat diproses secara efektif melalui rekayasa representasi "
        "morfologi berbasis leksikon kamus resmi tanpa harus bergantung pada infrastruktur komputasi GPU berbiaya tinggi [1], [6], [13]."
    )

    # 7. KETERBATASAN PENELITIAN
    add_sec_heading("7. KETERBATASAN PENELITIAN")
    add_body(
        "Secara transparan, kami mengidentifikasi tiga keterbatasan utama dalam penelitian ini:\n"
        "1) Cakupan Kosakata Terkontrol: Benchmark 100k menguji kombinasi morfem teratur berbasis lema kamus terdaftar. Teks media sosial dengan neologisme slang memerlukan ekspansi leksikon berkelanjutan.\n"
        "2) Keseimbangan Korpus Dialek: Korpus kalimat autentik saat ini masih didominasi dialek Sasak Umum dan Lombok Timur akibat ketersediaan arsip teks tertulis.\n"
        "3) Ketiadaan Konteks Sintaksis: Sistem saat ini beroperasi pada tingkat kata dan token tanpa konteks penanda kelas kata (POS Tagger) tingkat kalimat."
    )

    # 8. KESIMPULAN DAN ARAH RISET MASA DEPAN
    add_sec_heading("8. KESIMPULAN DAN ARAH RISET MASA DEPAN")
    add_body(
        "Penelitian ini memperkenalkan SasakNLP, kerangka kerja morfologi sadar dialek pertama untuk Bahasa Sasak. Evaluasi pada 100.000 pasangan data "
        "membuktikan akurasi lematisasi 80,44% pada benchmark penuh dan 93,23% pada benchmark inti 10k, menekan overstemming hingga 2,28%, serta membukukan "
        "throughput 7.826–16.272 kata/detik dan latensi 0,044 ms tanpa dependensi pustaka eksternal."
    )
    add_body(
        "Agenda riset masa depan mencakup: 1) Integrasi model sequence-to-sequence probabilistik ringan (ByT5 / Char-BiLSTM) untuk neologisme OOV, "
        "2) Pembangunan korpus beranotasi Sasak Dependency Treebank pertama, dan 3) Pelatihan model penerjemahan mesin saraf (NMT) dwiarah Sasak-Indonesia [1], [2], [6]."
    )

    # KETERSEDIAAN DATA DAN KODE
    add_sec_heading("KETERSEDIAAN DATA DAN KODE")
    add_body(
        "Demi menjamin transparansi ilmiah dan replikabilitas riset, seluruh perangkat lunak, dataset tolok ukur, dan modul pendukung dapat diakses secara publik: "
        "Paket Resmi PyPI (pip install sasaknlp), Repositori GitHub (https://github.com/kodetr/sasaknlp), dan "
        "Dataset Hugging Face (https://huggingface.co/datasets/kodetr/sasak-benchmark-100k)."
    )

    # UCAPAN TERIMA KASIH
    add_sec_heading("UCAPAN TERIMA KASIH")
    add_body(
        "Penulis menyampaikan terima kasih kepada para penutur asli dan pemangku adat di Pulau Lombok, peneliti dialektologi terdahulu, serta Balai Bahasa "
        "Provinsi Nusa Tenggara Barat atas standarisasi kamus dwibahasa Sasak-Indonesia yang menjadi landasan leksikal bagi riset ini."
    )

    # DAFTAR PUSTAKA
    add_sec_heading("DAFTAR PUSTAKA")
    refs = [
        "[1] A. F. Aji, G. I. Winata, F. Koto, S. Cahyawijaya, A. Romadhony, R. Mahendra, K. Kurniawan, D. Moeljadi, R. E. Prasojo, T. Baldwin, J. H. Lau, and S. Ruder, \"One Country, 700+ Languages: NLP Challenges for Underrepresented Languages and Dialects in Indonesia,\" in Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 2022, pp. 722--745. doi: 10.18653/v1/2022.acl-long.498.",
        "[2] S. Ranathunga, E.-S. A. Lee, M. P. Skenduli, R. Shekhar, M. Alam, and R. Kaur, \"Neural Machine Translation for Low-Resource Languages: A Survey,\" ACM Computing Surveys, vol. 55, no. 11, pp. 229:1--229:37, 2023. doi: 10.1145/3567592.",
        "[3] S. Cahyawijaya, G. I. Winata, B. Wilie, K. Vincentio, X. Li, A. Kuncoro, S. Rai, M. Lyman, K. Kurniawan, A. Azaria, S. Bahar, R. Mahendra, P. Fung, and A. Purwarianti, \"IndoNLG: Benchmark and Resources for Evaluating Indonesian Natural Language Generation,\" in Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, 2021, pp. 8878--8898. doi: 10.18653/v1/2021.emnlp-main.699.",
        "[4] F. Koto, J. H. Lau, and T. Baldwin, \"IndoBERTweet: A Pretrained Language Model for Indonesian Twitter with Effective Domain-Specific Vocabulary Initialization,\" in Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, 2021, pp. 10660--10668. doi: 10.18653/v1/2021.emnlp-main.833.",
        "[5] F. Koto, N. Aisyah, H. Li, and T. Baldwin, \"Large Language Models Only Pass Primary School Exams in Indonesia: A Comprehensive Test on IndoMMLU,\" in Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, 2023, pp. 12359--12374. doi: 10.18653/v1/2023.emnlp-main.760.",
        "[6] G. I. Winata, A. F. Aji, S. Cahyawijaya, R. Mahendra, F. Koto, A. Romadhony, K. Kurniawan, D. Moeljadi, and R. E. Prasojo, \"NusaCrowd: Open Source Initiative for Indonesian NLP and Regional Languages Resources,\" in Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 2023, pp. 8321--8345. doi: 10.18653/v1/2023.acl-long.462.",
        "[7] S. Cahyawijaya, H. Lovenia, A. F. Aji, G. I. Winata, B. Wilie, F. Koto, R. Mahendra, C. Wibisono, and P. Fung, \"NusaX: Multilingual Parallel Sentiment Dataset for 10 Indonesian Local Languages,\" in Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics, 2023, pp. 2562--2578. doi: 10.18653/v1/2023.eacl-main.189.",
        "[8] F. Koto, R. Mahendra, N. Aisyah, and T. Baldwin, \"IndoCulture: Exploring Geographically Influenced Cultural Commonsense Reasoning Across Eleven Indonesian Provinces,\" Transactions of the Association for Computational Linguistics, vol. 12, pp. 1703--1719, 2024. doi: 10.1162/tacl_a_00726.",
        "[9] L. Hakim, Roveneldo, N. U. al Jamiliyati, and Arjulayana, \"Medan Makna Aktivitas Kaki dalam Bahasa Sasak Dialek A-E,\" MABASAN: Jurnal Ilmiah Bahasa dan Sastra, vol. 17, no. 1, pp. 109--128, 2023. doi: 10.26499/mab.v17i1.626.",
        "[10] Balai Bahasa Provinsi Nusa Tenggara Barat, Kamus Terpadu Sasambo (Sasak, Samawa, Mbojo). Mataram, Indonesia: Balai Bahasa Provinsi Nusa Tenggara Barat, Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi Republik Indonesia, 2022.",
        "[11] L. N. Yaqin, T. Shanmuganathan, W. Fauzanna, Mohzana, and A. Jaya, \"Sociopragmatic parameters of politeness strategies among the Sasak in the post elopement rituals,\" Studies in English Language and Education, vol. 9, no. 2, pp. 797--811, 2022. doi: 10.24815/siele.v9i2.22569.",
        "[12] L. Hakim, \"Makian dalam Bahasa Sasak Dialek E-E,\" MABASAN: Jurnal Ilmiah Bahasa dan Sastra, vol. 16, no. 1, pp. 83--98, 2022. doi: 10.26499/mab.v16i1.503.",
        "[13] Z. Abidin, A. Junaidi, and Wamiliana, \"Text Stemming and Lemmatization of Regional Languages in Indonesia: A Systematic Literature Review,\" Journal of Information Systems Engineering and Business Intelligence (JISEBI), vol. 10, no. 2, pp. 217--231, 2024. doi: 10.20473/jisebi.10.2.217-231.",
        "[14] S. H. Wijono, M. R. Alhamidi, M. H. Hilman, and W. Jatmiko, \"Canonical Segmentation Using Affix Characters as a Unit on Transformer for Javanese Language,\" in Proceedings of the 2021 6th International Workshop on Big Data and Information Security (IWBIS), 2021, pp. 67--72. doi: 10.1109/IWBIS53353.2021.9631839.",
        "[15] K. Resiandi, Y. Murakami, and A. H. Nasution, \"Neural Network-Based Bilingual Lexicon Induction for Indonesian Ethnic Languages,\" Applied Sciences, vol. 13, no. 15, p. 8666, 2023. doi: 10.3390/app13158666.",
        "[16] kodetr, \"SasakNLP: A Dialect-Aware Morphological Processing Framework and 100k Benchmark for the Low-Resource Sasak Language,\" PyPI, GitHub, and Hugging Face Datasets, 2026. [Online]. Tersedia: https://github.com/kodetr/sasaknlp.",
        "[17] D. Jurafsky and J. H. Martin, Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition, 3rd ed. Upper Saddle River, NJ: Prentice Hall, 2024.",
        "[18] K. Batsuren, G. Bella, A. Arora, V. Martinovic, K. Gorman, Z. Žabokrtský, A. Ganbold, Š. Dohnalová, M. Ševčíková, K. Pelegrinová, F. Giunchiglia, R. Cotterell, and E. Vylomova, \"The SIGMORPHON 2022 Shared Task on Morpheme Segmentation,\" in Proceedings of the 19th SIGMORPHON Workshop on Computational Research in Phonetics, Phonology, and Morphology, 2022, pp. 103--116. doi: 10.18653/v1/2022.sigmorphon-1.11.",
        "[19] S. Cahyawijaya, H. Lovenia, F. Koto, D. Adhista, E. Dave, S. Oktavianti, S. Akbar, J. Lee, N. Shadieq, T. W. Cenggoro, H. Linuwih, B. Wilie, G. Muridan, G. Winata, D. Moeljadi, A. F. Aji, A. Purwarianti, and P. Fung, \"NusaWrites: Constructing High-Quality Corpora for Underrepresented and Extremely Low-Resource Languages,\" in Proceedings of the 13th International Joint Conference on Natural Language Processing and the 3rd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (Volume 1: Long Papers), 2023, pp. 921--945. doi: 10.18653/v1/2023.ijcnlp-main.60.",
        "[20] Prihantoro, \"An evaluation of MorphInd's morphological annotation scheme for Indonesian,\" Corpora, vol. 16, no. 2, pp. 287--299, 2021. doi: 10.3366/cor.2021.0223.",
        "[21] L. N. Setra, Rondiyah, A. Kurniawaty, and R. Gayatri, \"Distribusi Pemakaian Kata Mamiq dalam Korpus Bahasa Sasak: Naskah Cilinaya dan Majalah Tambori,\" MABASAN: Jurnal Ilmiah Bahasa dan Sastra, vol. 17, no. 2, pp. 293--308, 2023. doi: 10.62107/mab.v17i2.814.",
        "[22] A. Romadhony, S. Al Faraby, R. Rismala, U. N. Wisesti, and A. Arifianto, \"Sentiment Analysis on a Large Indonesian Product Review Dataset,\" Journal of Information Systems Engineering and Business Intelligence (JISEBI), vol. 10, no. 1, pp. 167--178, 2024. doi: 10.20473/jisebi.10.1.167-178."
    ]

    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(3)
        p_ref.paragraph_format.line_spacing = 1.0
        run_ref = p_ref.add_run(r)
        run_ref.font.name = "Times New Roman"
        run_ref.font.size = Pt(10)

    doc.save(output_path)
    print(f"✅ Indonesian Academic Manuscript successfully generated: {output_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Generate English ECTI-CIT Camera-Ready Manuscript
    en_path = os.path.join(base_dir, "jurnal_sasaknlp_en.docx")
    build_ecti_docx_en(en_path, is_anonymous=False)
    
    # 2. Generate English ECTI-CIT Double-Blind Anonymous Manuscript
    anon_path = os.path.join(base_dir, "jurnal_sasaknlp_anonymous.docx")
    build_ecti_docx_en(anon_path, is_anonymous=True)
    print(f"✅ Anonymous Double-Blind Manuscript generated: {anon_path}")

    # Also keep default jurnal_sasaknlp.docx pointing to the English ECTI paper
    default_path = os.path.join(base_dir, "jurnal_sasaknlp.docx")
    shutil.copyfile(en_path, default_path)
    print(f"✅ Default ECTI Manuscript updated: {default_path}")

    # 3. Generate Indonesian Academic Manuscript
    id_path = os.path.join(base_dir, "jurnal_sasaknlp_id.docx")
    build_ecti_docx_id(id_path)
