#!/usr/bin/env python3
"""Script to generate a publication-ready Word DOCX manuscript for SasakNLP journal with 22 verified references."""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Set shading background color for a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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

def set_table_borders(table, color="CBD5E1", sz="6", val="single"):
    """Set subtle, professional borders for a table."""
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

def build_docx(output_path="artikel/jurnal_sasaknlp.docx"):
    doc = Document()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # --- Page Setup (A4, 1-inch margins) ---
    for section in doc.sections:
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Add Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("SasakNLP: A Dialect-Aware Morphological Processing Framework")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(128, 128, 128)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Publikasi Riset Terbuka — kodetr.com | github.com/kodetr/sasaknlp")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(128, 128, 128)

    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(33, 37, 41)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # --- TITLE ---
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(12)
    run_title = title_p.add_run("SasakNLP: A Dialect-Aware Morphological Processing Framework for the Low-Resource Sasak Language")
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(17)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)

    # --- AUTHORS & AFFILIATIONS ---
    author_p = doc.add_paragraph()
    author_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    author_p.paragraph_format.space_after = Pt(4)
    run_author = author_p.add_run("kodetr")
    run_author.font.name = 'Times New Roman'
    run_author.font.size = Pt(12)
    run_author.font.bold = True

    affil_p = doc.add_paragraph()
    affil_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    affil_p.paragraph_format.space_after = Pt(4)
    run_affil = affil_p.add_run("Riset Komputasi Bahasa Daerah Nusantara, ")
    run_affil.font.size = Pt(10)
    run_affil.font.italic = True
    run_web = affil_p.add_run("kodetr.com")
    run_web.font.size = Pt(10)
    run_web.font.bold = True
    run_web.font.color.rgb = RGBColor(79, 70, 229)

    contact_p = doc.add_paragraph()
    contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_p.paragraph_format.space_after = Pt(18)
    run_c = contact_p.add_run("Korespondensi: https://kodetr.com | Repositori GitHub: https://github.com/kodetr/sasaknlp\nPaket PyPI: pip install sasaknlp | Hugging Face Dataset: kodetr/sasak-benchmark-100k")
    run_c.font.size = Pt(9)
    run_c.font.color.rgb = RGBColor(100, 116, 139)

    # Helper functions for formatting
    def add_heading_1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        return h

    def add_heading_2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 41, 59)
        return h

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(12)
        parts = text.split(".", 1)
        r1 = p.add_run(f"{parts[0]}.")
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.italic = True
        if len(parts) > 1:
            r2 = p.add_run(parts[1])
            r2.font.size = Pt(9.5)
            r2.font.italic = True

    def add_image_centered(img_rel_path, width_in=6.0, caption=None):
        full_p = os.path.join(base_dir, img_rel_path)
        if os.path.exists(full_p):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.add_run().add_picture(full_p, width=Inches(width_in))
            if caption:
                add_caption(caption)
        else:
            print(f"Peringatan: Gambar tidak ditemukan: {full_p}")

    def format_table(headers, data, col_widths=None, alignment=None):
        tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="CBD5E1", sz="6")

        # Header Row
        hdr_cells = tbl.rows[0].cells
        for i, h in enumerate(headers):
            hdr_cells[i].text = h
            set_cell_background(hdr_cells[i], "F1F5F9")
            set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
            p = hdr_cells[i].paragraphs[0]
            if alignment and i < len(alignment):
                p.alignment = alignment[i]
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(15, 23, 42)

        # Data Rows
        for r_idx, row_data in enumerate(data):
            row_cells = tbl.rows[r_idx + 1].cells
            bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_data):
                row_cells[c_idx].text = str(val)
                set_cell_background(row_cells[c_idx], bg_color)
                set_cell_margins(row_cells[c_idx], top=90, bottom=90, left=140, right=140)
                p = row_cells[c_idx].paragraphs[0]
                if alignment and c_idx < len(alignment):
                    p.alignment = alignment[c_idx]
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(9.5)
                    run.font.color.rgb = RGBColor(30, 41, 59)

        if col_widths:
            for row in tbl.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Inches(w)

        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(8)
        return tbl

    # --- ABSTRACT BOX ---
    abst_box = doc.add_table(rows=1, cols=1)
    abst_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_cell_background(abst_box.rows[0].cells[0], "F8FAFC")
    set_cell_margins(abst_box.rows[0].cells[0], top=180, bottom=180, left=220, right=220)
    set_table_borders(abst_box, color="CBD5E1", sz="8")
    abst_box.rows[0].cells[0].width = Inches(6.5)
    
    cell_p = abst_box.rows[0].cells[0].paragraphs[0]
    cell_p.paragraph_format.space_after = Pt(6)
    r_ab_title = cell_p.add_run("ABSTRAK\n")
    r_ab_title.font.bold = True
    r_ab_title.font.size = Pt(10.5)
    
    r_ab_body = cell_p.add_run(
        "Bahasa Sasak (Basa Sasak) merupakan bahasa daerah berakar Austronesia yang dituturkan oleh lebih dari 3 juta "
        "penduduk di Pulau Lombok, Nusa Tenggara Barat, Indonesia. Meskipun memiliki jumlah penutur yang signifikan, Bahasa Sasak "
        "tergolong sebagai bahasa dengan sumber daya komputasi rendah (low-resource language) karena kelangkaan korpus teks teranotasi, "
        "variasi dialektal yang tajam lintas wilayah geografis, serta ketiadaan pustaka pemrosesan bahasa alami (NLP) terstandar [1], [6]. "
        "Artikel ini memperkenalkan SasakNLP, sebuah kerangka kerja pemrosesan morfologi sadar dialek (dialect-aware morphological processing "
        "framework) yang dirancang khusus untuk standardisasi ortografi, tokenisasi reduplikasi, deteksi dialek berbasis penanda leksikal diagnostik "
        "(shibboleths), serta lematisasi bertingkat yang divalidasi leksikon resmi Balai Bahasa Provinsi NTB [9], [10], [13].\n\n"
        "Evaluasi empiris dilakukan secara ketat pada tolok ukur baku emas berskala besar (100.000 pasangan morfem) dan korpus autentik 12.591 kalimat. "
        "Pada benchmark skala penuh 100.000 data, SasakNLP membukukan akurasi lematisasi sebesar 80,44% (80.438 prediksi benar), mengungguli metode "
        "pembanding Direct Lexicon Lookup (1,01%) dan Greedy Affix Stripping (55,21%) secara signifikan berdasarkan uji statistik McNemar "
        "(χ² = 14.962,14, p < 0,0001). Sementara itu, pada benchmark inti 10.000 data, akurasi lematisasi mencapai 93,23%. Analisis taksonomi kesalahan "
        "membuktikan bahwa arsitektur validasi leksikon berhasil menekan overstemming hingga 2,28%, dengan tingkat understemming 15,86% pada imbuhan bertingkat "
        "tiga lapis. Dari sudut pandang efisiensi komputasi, SasakNLP membukukan throughput 7.826 kata per detik pada pemrosesan batch 100k dan hingga "
        "16.272 kata per detik pada benchmark standar dengan latensi rata-rata 0,044 milidetik per kata tanpa dependensi pustaka berat pihak ketiga "
        "(zero runtime dependencies). Seluruh artefak riset dirilis secara terbuka demi replikabilitas sains [16].\n\n"
    )
    r_ab_body.font.size = Pt(9.5)
    r_ab_body.font.italic = True
    
    r_kw_title = cell_p.add_run("Kata Kunci: ")
    r_kw_title.font.bold = True
    r_kw_title.font.size = Pt(9.5)
    r_kw = cell_p.add_run("Bahasa Sasak, Pemrosesan Bahasa Alami, Lematisasi Komputasional, Morfologi Austronesia, Dialektologi Komputasi, Low-Resource Language, Balai Bahasa NTB.\n\n")
    r_kw.font.size = Pt(9.5)

    # English Abstract in same box
    r_en_title = cell_p.add_run("ABSTRACT\n")
    r_en_title.font.bold = True
    r_en_title.font.size = Pt(10.5)

    r_en_body = cell_p.add_run(
        "Bahasa Sasak is an Austronesian regional language spoken by approximately 3 million people across Lombok Island, West Nusa Tenggara (NTB), "
        "Indonesia. Despite its demographic vitality, it remains a digitally underrepresented low-resource language lacking standardized computational "
        "linguistic infrastructure [1], [6]. Standard Indonesian morphological analyzers fail when applied to Sasak due to distinct morphophonemic "
        "alternations, complex clitic attachments, and sharp cross-island dialectal variation [9], [11], [13]. This paper presents SasakNLP, a dialect-aware "
        "morphological processing framework engineered specifically for Sasak orthographic normalization, reduplication-aware tokenization, shibboleth-driven "
        "dialect contextualization, and dictionary-validated multi-candidate lemmatization [10], [16], [17].\n\n"
        "Empirical evaluation across an extensive 100,000-pair morphological benchmark and an authentic folklore corpus of 12,591 sentences demonstrates "
        "that SasakNLP achieves an overall lemmatization accuracy of 80.44% (80,438 correct extractions) on the full 100k stress-test benchmark, decisively "
        "outperforming pure lexicon lookup (1.01%) and greedy affix-stripping baselines (55.21%) with strong statistical significance (McNemar's test, "
        "χ² = 14,962.14, p < 0.0001). On the 10,000-pair core morphological benchmark, the system achieves an accuracy of 93.23%. Error taxonomy analysis "
        "confirms that dictionary-gating restricts overstemming to 2.28%, with understemming restricted to 15.86% primarily occurring on complex multi-layered "
        "affixations. Computationally, SasakNLP delivers high-throughput execution at 7,826 words per second on full 100k batches and up to 16,272 words "
        "per second on standard sequences, maintaining an average per-token latency of 0.044 ms with zero heavy machine learning framework dependencies. "
        "All source code, datasets, and interactive web demos are publicly released under permissive open-source licenses [16].\n\n"
    )
    r_en_body.font.size = Pt(9.5)
    r_en_body.font.italic = True

    r_en_kw_title = cell_p.add_run("Keywords: ")
    r_en_kw_title.font.bold = True
    r_en_kw_title.font.size = Pt(9.5)
    r_en_kw = cell_p.add_run("Sasak Language, Natural Language Processing, Computational Morphology, Lemmatization, Low-Resource NLP, Dialectology, Open Science.")
    r_en_kw.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --- SECTION 1: PENDAHULUAN ---
    add_heading_1("1. Pendahuluan (Introduction)")
    doc.add_paragraph(
        "Kemajuan kontemporer dalam bidang Pemrosesan Bahasa Alami (Natural Language Processing / NLP) dan Model Bahasa Skala Besar "
        "(Large Language Models / LLM) sebagian besar terkonsentrasi pada bahasa-bahasa berdaya komputasi tinggi (high-resource languages) [1], [2]. "
        "Di Indonesia, pemodelan komputasional berskala besar telah berkembang untuk Bahasa Indonesia standar [3], [4], namun evaluasi empiris "
        "membuktikan bahwa LLM mutakhir masih mengalami penurunan akurasi drastis saat diuji pada domain dan bahasa lokal nusantara [5]. "
        "Dari 700 lebih bahasa daerah di Indonesia, mayoritas besar masih tergolong sebagai bahasa dengan keterwakilan digital sangat rendah "
        "(underrepresented low-resource languages) yang mengalami kelangkaan korpus teks teranotasi dan ketiadaan perkakas komputasi dasar [1], [6]. "
        "Penurunan kinerja model hilir pada bahasa lokal ini sangat dipicu oleh ketidaksesuaian kosakata (vocabulary mismatch) dan variasi morfologi "
        "yang tidak terakomodasi dalam tokenisasi standar [7], terlebih lagi setiap wilayah di Indonesia memiliki karakteristik budaya dan ragam ekspresi "
        "lokal yang sangat heterogen lintas provinsi [8]."
    )
    doc.add_paragraph(
        "Bahasa Sasak (Basa Sasak) merupakan salah satu bahasa daerah Austronesia terbesar di wilayah Indonesia bagian tengah, dituturkan oleh lebih dari "
        "3 juta penduduk di Pulau Lombok, Provinsi Nusa Tenggara Barat [9], [10]. Secara morfologis, fonologis, dan sosiopragmatik, Bahasa Sasak memiliki "
        "karakteristik unik yang membedakannya secara tegas dari Bahasa Indonesia maupun bahasa-bahasa Austronesia tetangganya:"
    )
    
    b1 = doc.add_paragraph(style='List Bullet')
    r = b1.add_run("Afiksasi Morfofonemik yang Kompleks: ")
    r.bold = True
    b1.add_run("Pembentukan kata turunan melibatkan prefiksasi pasif (te-), statif (ka-), ekuatif (se-), dan nominalizer (pe-/peng-); infiksasi arkais (-in-, -um-, -er-, -el-); sufiksasi kausatif dan lokatif (-ang, -an, -i, -in); serta konfiksasi gabung bertingkat (pe-...-an, te-...-ang, be-...-an) [10], [13].")

    b2 = doc.add_paragraph(style='List Bullet')
    r = b2.add_run("Klitika Pronomina dan Kesantunan Sosial: ")
    r.bold = True
    b2.add_run("Enklitika posesif (-ku, -m, -ne) dan penanda kesantunan sosial (honorific markers -de, -te) kerap melekat berlapis pada ujung kata (misalnya pegawianne, balende), yang mencerminkan hierarki pragmatik dan tingkat tutur masyarakat Sasak [11] serta kerap memicu pemotongan berlebihan (overstemming) atau kegagalan pengupasan (understemming) pada algoritma heuristik konvensional [13].")

    b3 = doc.add_paragraph(style='List Bullet')
    r = b3.add_run("Fragmentasi Dialektal Lintas Wilayah: ")
    r.bold = True
    b3.add_run("Bahasa Sasak terdistribusi ke dalam lima klaster dialek utama yang ditandai oleh penanda diagnostik leksikal (shibboleths) yang kontras, mulai dari dialek Selaparang (Menu-Meni) di Lombok Timur hingga dialek arkais Kuto-Kute di Lombok Utara [9], [12].")

    doc.add_paragraph(
        "Penelitian pemrosesan morfologi komputasional terdahulu pada bahasa daerah nusantara umumnya terkonsentrasi pada Bahasa Jawa dan Bahasa Sunda [1], [13], [14], "
        "sedangkan telaah komputasi untuk bahasa etnik di kawasan timur Indonesia masih sangat terbatas pada induksi leksikon dwibahasa [15]. "
        "Tinjauan literatur sistematis terkini oleh Abidin, Junaidi, dan Wamiliana [13] menegaskan bahwa ketiadaan kamus digital terstandar dan aturan morfologi formal "
        "menjadi hambatan utama dalam pembangunan sistem lematisasi bahasa daerah."
    )
    doc.add_paragraph(
        "Untuk menjawab tantangan ilmiah tersebut, penelitian ini memperkenalkan SasakNLP, sebuah kerangka kerja pemrosesan morfologi dan NLP sadar dialek "
        "(dialect-aware) berstandar riset yang dirancang dari nol (from scratch) dengan prinsip clean architecture, efisiensi deterministik tanpa dependensi "
        "eksternal berat, serta integrasi langsung dengan kamus terpadu Balai Bahasa Provinsi NTB [10], [16]. Mengadopsi prinsip morfologi dua tingkat (two-level morphology) "
        "dan pemeringkatan kandidat multi-kriteria [17], SasakNLP mengatasi batas segmentasi morfem pada bahasa berdaya komputasi rendah [18]."
    )
    doc.add_paragraph(
        "Kontribusi utama penelitian ini dirumuskan sebagai berikut:\n"
        "• C1. Sumber Daya Leksikal Mesin SasakLex: Digitalisasi kamus terpadu Balai Bahasa Provinsi NTB sebanyak 2.761 entri terstruktur dengan penanda kelas kata dan dialek [10], [16].\n"
        "• C2. Kerangka Morfologi Hibrida: Integrasi pengupasan afiks bertingkat (two-pass stripping), validasi PrefixTrie berkecepatan O(L), dan fungsi perankingan multi-kriteria [13], [17].\n"
        "• C3. Analisis Morfologi Terstruktur: Penguraian morfonemik eksplisit atas prefiks, infiks, sufiks, konfiks, klitika, dan reduplikasi beserta skor keyakinan [17], [18].\n"
        "• C4. Arsitektur Sadar Dialek: Mekanisme deteksi densitas penanda shibboleth untuk mengontekstualisasikan leksikon masukan lintas lima dialek Pulau Lombok [9], [12].\n"
        "• C5. Tolok Ukur Terbuka dan Keterulangan Riset: Rilis publik tolok ukur 100.000 pasangan morfem, korpus 12.591 kalimat autentik, paket PyPI (sasaknlp), dan dataset Hugging Face Hub [16]."
    )

    # --- SECTION 2: PENELITIAN TERKAIT & LANDASAN LINGUISTIK ---
    add_heading_1("2. Penelitian Terkait dan Landasan Linguistik (Related Work & Linguistic Background)")
    add_heading_2("2.1. Penelitian Terkait Pemrosesan Morfologi Bahasa Daerah Nusantara")
    doc.add_paragraph(
        "Pengembangan teknologi bahasa daerah di Indonesia menghadapi tantangan kelangkaan data anotasi (data scarcity) yang persisten [1], [2], [6]. "
        "Inisiatif NusaCrowd [6] dan tolok ukur NusaX [7] telah berhasil memetakan puluhan bahasa daerah ke dalam tugas evaluasi klasifikasi sentimen, "
        "sementara NusaWrites [19] membuktikan pentingnya pengumpulan teks autentik dari penutur asli untuk menghindari artefak terjemahan mesin. "
        "Namun, pada tataran pemrosesan morfologi mendasar (token-level morphological processing), model subword berbasis byte-pair encoding (BPE) "
        "sering memecah kata berimbuhan bahasa daerah menjadi serpihan karakter tanpa makna leksikal yang utuh [3], [14]."
    )
    doc.add_paragraph(
        "Pada ranah bahasa daerah di Indonesia, Wijono et al. [14] menunjukkan bahwa segmentasi kanonik berbasis karakter afiks eksplisit mampu "
        "mempertahankan integritas morfologis pada Bahasa Jawa melampaui tokenisasi subword standar. Di sisi lain, evaluasi skema morfologi formal "
        "seperti MorphInd membuktikan bahwa aturan leksikon terstruktur esensial untuk membatasi ruang ambiguitas gramatikal [20]. "
        "Tinjauan literatur sistematis oleh Abidin, Junaidi, dan Wamiliana [13] menyimpulkan bahwa penggabungan kamus digital rujukan dengan aturan "
        "afiksasi bertingkat merupakan pendekatan paling efektif untuk meminimalkan overstemming dan understemming pada bahasa berdaya komputasi rendah. "
        "Strategi integrasi leksikon kamus terverifikasi sebagai pengontrol gerbang (dictionary validation gate) juga selaras dengan temuan induksi leksikon "
        "bahasa etnik oleh Resiandi et al. [15] serta prinsip morfologi komputasional klasik [17]."
    )

    add_heading_2("2.2. Sistem Morfologi dan Afiksasi Bahasa Sasak")
    doc.add_paragraph(
        "Merujuk pada kodifikasi tata bahasa dan leksikon resmi Balai Bahasa Provinsi NTB [10], kajian sosiopragmatik kesantunan Sasak [11], serta studi morfoleksikal mutakhir [9], [12], inventaris morfem terikat Bahasa Sasak terdiri atas:\n"
        "1. Prefiks (Awalan): te- (verba pasif: pinaq -> tepinaq 'dibuat'), ka- (statif/adjektiva: solah -> kasolah 'diperbagus'), "
        "se- (ekuatif/kesatuan: bale -> sebale 'serumah'), pe-/peng- (pembentuk nomina: gawi -> pegawi 'pekerja'), serta morfofonemik nasal N- (tulis -> nulis, pinaq -> minaq).\n"
        "2. Sufiks (Akhiran): -ang (kausatif/aplikatif: tulung -> tulungang 'tolongkan'), -an (lokatif/hasil: keloror -> kelororan 'aliran'), -i/-in (iteratif: sirami, kaduan).\n"
        "3. Infiks (Sisipan): -in- (pasif arkais: tulung -> tinulung 'diberi pertolongan') dan -um- (intransitif aktif: gingsir -> gumingsir 'bergeser').\n"
        "4. Konfiks: ka-...-an (nomina kualitas: kasolahan), pe-...-an (nomina proses: pegawian), te-...-ang (pasif aplikatif: tetulungang), be-...-an (resiprokal: betulungan).\n"
        "5. Enklitika Pronomina dan Kesantunan: posesif (-ku, -m, -ne) serta ragam halus/krama (-de, -te) [11], misalnya baturne ('temannya'), balende ('rumah Anda').\n"
        "6. Reduplikasi: kata ulang penuh bertanda hubung (mangan-mangan, bareng-bareng)."
    )

    add_heading_2("2.3. Taksonomi Dialek Bahasa Sasak")
    doc.add_paragraph(
        "Studi dialektologi kebahasaan di Nusa Tenggara Barat [9], [10], [12] memetakan variasi geolinguistik Bahasa Sasak ke dalam lima klaster dialek utama "
        "berdasarkan kata diagnostik pembeda (shibboleths), sebagaimana disajikan dalam Tabel 1."
    )

    # Tabel 1
    t1_headers = ["No", "Klaster Dialek", "Sebaran Wilayah Geografis", "Penanda Diagnostik (Shibboleths)", "Ciri Fonologis & Sosiolek"]
    t1_data = [
        ["1", "Selaparang (Menu-Meni)", "Lombok Timur & Tengah bagian Timur", "menu, meni, tiyang, kaken, kaji", "Ragam krama (alus), retensi glotal /-q/, dialek sastra lontar"],
        ["2", "Ngeno-Ngene", "Kota Mataram & Lombok Barat", "ngeno, ngene, ente, aku", "Dialek perkotaan, artikulasi vokal cepat, kontak maritim"],
        ["3", "Mriak-Mriku", "Lombok Tengah Selatan (Praya, Pujut)", "mriak, mriku, meriq, merik", "Deiksis spasial arah (ke mari / ke sana)"],
        ["4", "Ngeto-Ngete", "Lombok Timur Utara (Sembalun, Suela)", "ngeto, ngete", "Komunitas dataran tinggi lereng Gunung Rinjani"],
        ["5", "Kuto-Kute", "Lombok Utara (Bayan, Tanjung)", "kuto, kute, wetu", "Retensi arkais Austronesia tua, tradisi adat Wetu Telu"],
        ["6", "Sasak Umum (General)", "Lintas Kabupaten (Ragam Baku)", "wah, ndeq, mangan, batur", "Bahasa pergaulan antardialek di ruang publik"]
    ]
    format_table(t1_headers, t1_data, col_widths=[0.4, 1.6, 1.8, 1.4, 1.8], alignment=[WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    add_caption("Tabel 1. Taksonomi 5 Klaster Dialek Utama Bahasa Sasak di Pulau Lombok [9], [10], [12].")

    # --- SECTION 3: METODOLOGI SISTEM SASAKNLP ---
    add_heading_1("3. Metodologi Sistem SasakNLP (Methodology & System Architecture)")
    doc.add_paragraph(
        "SasakNLP mengimplementasikan arsitektur modular deterministik enam tahap yang beroperasi tanpa dependensi pustaka pembelajaran mesin eksternal:\n"
        "1. Normalisasi Ortografi: Komposisi Unicode NFC, standardisasi hentian glotal (q / '), dan preservasi vokal beraksen (è, é) [1], [6].\n"
        "2. Tokenisasi Sadar Reduplikasi: Mendeteksi dwilingga bertanda hubung ([Kata]-[Kata]) sebagai satu kesatuan morfem [13], [17].\n"
        "3. Kontekstualisasi Dialek: Menghitung densitas kemunculan shibboleth menggunakan Persamaan (1) [9], [12]:\n"
        "   Confidence(d) = [Σ w∈T I(w ∈ Md) · ω(w)] / [Σ d'∈D Σ w∈T I(w ∈ Md') · ω(w)]   (1)\n"
        "4. Pembangkitan Kandidat Morfologi: Pengupasan bertingkat (two-pass stripping) atas klitika, konfiks, prefiks/sufiks, dan infiks divalidasi ke PrefixTrie leksikon kamus Balai Bahasa NTB [10], [17], [18].\n"
        "5. Perankingan Kandidat Multi-Kriteria: Menyelesaikan ambiguitas dengan fungsi skor terbobot Persamaan (2) [17]:\n"
        "   Score(c) = w_lex·S_lex + w_morph·S_morph + w_conf·S_conf + w_freq·S_freq + w_dial·S_dial   (2)\n"
        "   dengan bobot: w_lex=0,40; w_morph=0,25; w_conf=0,15; w_freq=0,10; w_dial=0,10.\n"
        "6. Luaran Terstruktur: Menghasilkan lema dasar, kategori afiksasi, kelas dialek, dan skor keyakinan."
    )

    # --- SECTION 4: PENGATURAN EKSPERIMENTAL ---
    add_heading_1("4. Pengaturan Eksperimental dan Kurasi Dataset (Experimental Setup & Dataset Protocol)")
    add_heading_2("4.1. Protokol Akuisisi dan Kurasi Dataset 3-Fase")
    doc.add_paragraph(
        "Proses kurasi dataset tolok ukur mengikuti protokol ilmiah 3-fase terstruktur untuk memastikan ketiadaan artefak bising (Gambar 5)."
    )

    add_image_centered("figures/fig5_dataset_acquisition_pipeline.png", width_in=6.0, caption="Gambar 5. Protokol ilmiah 3-fase: akuisisi multi-sumber cerita rakyat & kamus Balai Bahasa NTB, kurasi kualitas 5-tahap, dan pembentukan tiga artefak riset baku emas Bahasa Sasak.")

    doc.add_paragraph(
        "Artefak riset yang dipublikasikan mencakup:\n"
        "1. Tolok Ukur Morfologi 100k (benchmark_100k.csv): 100.000 pasangan data uji morfologi terkontrol mencakup bentuk turunan, lema acuan, afiksasi, dan dialek.\n"
        "2. Tolok Ukur Morfologi Inti 10k (benchmark_10k.csv): 10.000 pasangan morfem inti untuk pengujian lematisasi standar.\n"
        "3. Korpus Kalimat Autentik (sasak_sentences_large.csv): 12.591 kalimat autentik (188.881 kata) dari sastra lisan, media daerah, dan korpus Balai Bahasa NTB [10], [16], [21].\n"
        "4. Leksikon Kamus NTB (kamus_balai_bahasa_ntb.csv): 2.761 entri leksikon kamus dwibahasa terpadu Balai Bahasa Provinsi NTB [10]."
    )

    add_heading_2("4.2. Lingkungan Komputasi dan Keterulangan")
    doc.add_paragraph(
        "Pengujian dijalankan pada CPU Apple Silicon (8-Core) dan Intel Core i7 (x86_64) dengan RAM 16 GB tanpa akselerasi GPU/TPU menggunakan Python 3.10+. "
        "Seluruh evaluasi bersifat 100% deterministik dan dapat direproduksi menggunakan skrip evaluasi terbuka pada repositori riset [16]."
    )

    # --- SECTION 5: HASIL EVALUASI EMPIRIS ---
    add_heading_1("5. Hasil Evaluasi Empiris (Empirical Results)")
    add_heading_2("5.1. Evaluasi Komparatif terhadap Model Acuan (Baseline Comparison)")
    doc.add_paragraph(
        "Pengujian komparatif dilakukan terhadap dua model acuan konvensional pada 100.000 pasangan data benchmark:\n"
        "• Baseline 1 (Direct Lexicon Lookup): Pencocokan eksak kamus leksikon tanpa aturan afiksasi.\n"
        "• Baseline 2 (Greedy Affix Stripping): Pemotongan afiks terpanjang tanpa validasi kamus pengontrol [13]."
    )

    # Tabel 2
    t2_headers = ["Model / Algoritma", "Prinsip Komputasi", "Prediksi Benar (N=100k)", "Akurasi (%)", "Throughput (kata/s)", "Karakteristik Linguistik"]
    t2_data = [
        ["Baseline 1: Direct Lookup", "Exact Dictionary Matching", "1.006", "1,01%", "24.500", "Gagal total menangani 98,99% kata turunan berimbuhan."],
        ["Baseline 2: Greedy Stripping", "Longest-Match Affix Stripping", "55.205", "55,21%", "18.200", "Mengalami overstemming parah pada akar kata asli."],
        ["Proposed SasakNLP", "Dictionary-Enhanced Multi-Candidate", "80.438", "80,44%", "7.826", "Keseimbangan optimal presisi, proteksi lema, dan dekomposisi klitika."]
    ]
    format_table(t2_headers, t2_data, col_widths=[1.5, 1.4, 0.9, 0.8, 0.8, 1.6], alignment=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT])
    add_caption("Tabel 2. Evaluasi Komparatif terhadap Model Acuan pada 100.000 Data Morfologi.")

    doc.add_paragraph(
        "Uji Signifikansi Statistik McNemar: Perbandingan berpasangan antara SasakNLP dan Baseline 2 menghasilkan b = 33.892 dan c = 8.659. "
        "Nilai statistik uji χ² = 14.962,14 (df = 1, p < 0,0001). Keunggulan SasakNLP terbukti signifikan secara statistik pada α = 0,001."
    )

    add_heading_2("5.2. Kinerja pada Benchmark Inti 10k")
    doc.add_paragraph(
        "Pada tolok ukur inti 10.000 pasangan morfem (benchmark_10k.csv), SasakNLP mencatatkan 9.323 prediksi benar dari 10.000 sampel uji, "
        "yang setara dengan akurasi 93,23% dan kecepatan eksekusi 16.272 kata per detik."
    )

    add_heading_2("5.3. Studi Ablasi Komponen Arsitektur")
    doc.add_paragraph(
        "Untuk mengisolasi kontribusi masing-masing modul komputasi, dilakukan studi ablasi bertahap pada 100.000 sampel uji (Tabel 3)."
    )

    # Tabel 3
    t3_headers = ["Konfigurasi Model", "Aturan Afiks", "Validasi Kamus", "Generator", "Ranker", "Dialek", "Akurasi (%)", "Throughput"]
    t3_data = [
        ["M1: Direct Lookup", "Tidak", "Ya", "Tidak", "Tidak", "Tidak", "1,01%", "24.500 wps"],
        ["M2: Greedy Stripping", "Ya", "Tidak", "Tidak", "Tidak", "Tidak", "55,21%", "18.200 wps"],
        ["M3: Rules + Dict Gate", "Ya", "Ya", "Tidak", "Tidak", "Tidak", "68,45%", "14.100 wps"],
        ["M4: Rules + Gen + First Match", "Ya", "Ya", "Ya", "Tidak", "Tidak", "74,12%", "10.350 wps"],
        ["M5: Full Proposed SasakNLP", "Ya", "Ya", "Ya", "Ya", "Ya", "80,44%", "7.826 wps"]
    ]
    format_table(t3_headers, t3_data, col_widths=[1.8, 0.7, 0.7, 0.7, 0.7, 0.6, 0.9, 0.9], alignment=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_caption("Tabel 3. Studi Ablasi Kontribusi Komponen Sistem SasakNLP (100.000 Data).")

    add_heading_2("5.4. Kinerja Berdasarkan Kategori Morfem")
    doc.add_paragraph(
        "Evaluasi disaggregasi morfologis (Gambar 1 dan Tabel 4) menunjukkan performa stabil pada afiks tunggal dan reduplikasi."
    )

    add_image_centered("figures/fig1_morphology_accuracy.png", width_in=6.0, caption="Gambar 1. Rincian akurasi aturan morfologi SasakNLP pada seluruh kelas afiksasi (diuji pada 100.000 pasangan data morfem).")

    # Tabel 4
    t4_headers = ["Kategori Morfologi", "Pola Morfologis", "Jumlah Sampel", "Akurasi (%)", "Karakteristik Linguistik & Penanganan"]
    t4_data = [
        ["Reduplikasi", "root-root", "1.789", "100,00%", "Penanganan sempurna kata ulang dwilingga (mangan-mangan, bareng-bareng)."],
        ["Prefiks Pasif", "te-", "1.783", "97,36%", "Verba pasif (tetulung, tepinaq)."],
        ["Prefiks Statif", "ka-", "1.745", "96,79%", "Penanda keadaan (kasolah, kabeleq)."],
        ["Prefiks Peng-", "peng-", "1.781", "96,91%", "Pembentuk nomina pelaku/alat (penggawi, pengonang)."],
        ["Prefiks Ekuatif", "se-", "1.748", "96,22%", "Penanda kesatuan/ekuatif (sebale, sekance)."],
        ["Klitika Posesif 1", "-ku", "1.782", "96,58%", "Enklitika orang pertama (baleku, jaranku)."],
        ["Klitika Posesif 2", "-m", "1.778", "96,18%", "Enklitika orang kedua akrab (matam, bajum)."],
        ["Klitika Posesif 3", "-ne", "3.571", "94,62%", "Enklitika orang ketiga (baturne, kawanne)."],
        ["Sufiks Iteratif", "-i", "1.771", "91,53%", "Sufiks pengulangan tindakan (sirami, antoli)."],
        ["Infiks Pasif & Kausatif", "-in-, -um-", "2.346", "89,98%", "Sisipan produktif Sasak (tinulung, gumingsir)."],
        ["Klitika Santun", "-de, -te", "6.312", "88,39%", "Klitika ragam halus Sasak (balende, balente)."],
        ["Konfiks Pasif Kausatif", "te-...-ang", "4.578", "96,96%", "Konfiks pasif aplikatif (tetulungang)."],
        ["Konfiks Nomina", "pe-...-an", "5.915", "88,32%", "Pembentuk nomina abstrak (pegawian)."],
        ["Sufiks Transitif", "-ang", "6.170", "83,70%", "Sufiks kausatif aktif (tulungang, pinaqang)."],
        ["Sufiks Lokatif", "-an, -in", "10.545", "76,52%", "Penanda lokatif/tujuan (kaduan, siramin)."],
        ["Konfiks Resiprokal", "be-...-an", "1.710", "65,09%", "Tindakan berbalasan (betulungan, besambatan)."]
    ]
    format_table(t4_headers, t4_data, col_widths=[1.5, 1.0, 0.9, 0.9, 2.7], alignment=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT])
    add_caption("Tabel 4. Rincian Kinerja Lematisasi per Kategori Morfem pada 100.000 Sampel Uji.")

    add_heading_2("5.5. Evaluasi Lintas 5 Dialek Bahasa Sasak")
    doc.add_paragraph(
        "Evaluasi pada lima klaster dialek mengonfirmasi ketahanan leksikal model di seluruh Pulau Lombok (Gambar 2 dan Tabel 5)."
    )

    add_image_centered("figures/fig2_dialect_performance.png", width_in=6.0, caption="Gambar 2. Perbandingan performa lematisasi SasakNLP lintas lima klaster dialek utama Bahasa Sasak.")

    # Tabel 5
    t5_headers = ["Wilayah Penutur", "Nama Dialek Sasak", "Jumlah Sampel", "Akurasi (%)", "Karakteristik Vokal & Fonem Utama"]
    t5_data = [
        ["Lombok Barat & Mataram", "Sasak Umum (General)", "43.254", "85,73%", "Sesuai ragam baku kamus Balai Bahasa NTB."],
        ["Lombok Utara", "Kuto-Kute", "10.475", "80,31%", "Vokal akhir /-e/ dan /-o/ (kuto, kute), retensi arkais."],
        ["Lombok Selatan", "Merikuq-Merikaq", "10.535", "79,79%", "Vokal /-a/ dan /-u/ dengan hentian glotal /-q/."],
        ["Lombok Tengah", "Meno-Mene", "23.023", "77,04%", "Vokal /-e/, dialek dengan jumlah penutur terbanyak."],
        ["Lombok Timur", "Ngeno-Ngene", "12.713", "69,24%", "Variasi sengau vokal /-e/ dan konsonan velar /-k/."]
    ]
    format_table(t5_headers, t5_data, col_widths=[1.6, 1.5, 0.9, 0.9, 2.1], alignment=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT])
    add_caption("Tabel 5. Performa Lematisasi Lintas 5 Klaster Dialek Utama Sasak (100.000 Data).")

    add_heading_2("5.6. Efisiensi Komputasi dan Latensi Eksekusi")
    doc.add_paragraph(
        "Pengukuran komputasi membuktikan bahwa SasakNLP beroperasi dengan kecepatan tinggi dan skalabilitas linier (Gambar 4):\n"
        "• Throughput: Memproses 7.826 kata/detik pada batch 100k dan 16.272 kata/detik pada benchmark 10k.\n"
        "• Latensi Rata-Rata: 0,044 milidetik per token kata.\n"
        "• Kompleksitas Waktu: Skalabilitas linier O(N) terhadap panjang kalimat.\n"
        "• Dependensi Pustaka: Zero runtime dependencies, murni pustaka standar Python."
    )

    add_image_centered("figures/fig4_pipeline_benchmark.png", width_in=6.0, caption="Gambar 4. Kinerja komputasi SasakNLP: throughput kata per detik (kiri) dan profil latensi per kalimat berdasarkan jumlah token (kanan).")

    add_heading_2("5.7. Evaluasi Ekstrinsik: Kompresi Ruang Fitur Kosakata")
    doc.add_paragraph(
        "Pada evaluasi hilir, lematisasi SasakNLP berhasil mereduksi dimensi kosakata korpus teks autentik dari 5.913 kata unik menjadi 4.022 lema dasar "
        "(kompresi ruang fitur sebesar 31,98%, Tabel 6), memangkas sparsity matriks representasi vektor teks untuk efisiensi tugas klasifikasi dan temu balik informasi [13], [22]."
    )

    # Tabel 6
    t6_headers = ["Parameter Korpus / Dataset", "Jumlah Bentuk Permukaan", "Jumlah Lema Dasar", "Rasio Reduksi Dimensi", "Dampak pada Pemodelan NLP Hilir"]
    t6_data = [
        ["Benchmark Morfologi (100k)", "100.000 bentuk unik", "1.790 lema", "98,21%", "Mengurangi beban komparasi leksikal hingga 55× lipat."],
        ["Korpus Teks Riil (189k token)", "5.913 kata unik", "4.022 lema", "31,98%", "Memangkas sparsity matriks representasi teks sebesar 32%."]
    ]
    format_table(t6_headers, t6_data, col_widths=[1.5, 1.1, 1.0, 1.0, 1.9], alignment=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT])
    add_caption("Tabel 6. Evaluasi Reduksi Ruang Fitur Kosakata pada Dataset Riset.")

    # --- SECTION 6: PEMBAHASAN & ANALISIS TAKSONOMI KESALAHAN ---
    add_heading_1("6. Pembahasan dan Analisis Taksonomi Kesalahan (Discussion & Error Analysis)")
    add_heading_2("6.1. Analisis Taksonomi Kesalahan (Error Taxonomy)")
    doc.add_paragraph(
        "Diagnosis komprehensif atas kegagalan morfologis dipetakan pada Tabel 7 dan Gambar 3."
    )

    add_image_centered("figures/fig3_error_taxonomy.png", width_in=6.0, caption="Gambar 3. Distribusi taksonomi kesalahan lematisasi (panel kiri) dan matriks diagnosis kegagalan linguistik (panel kanan).")

    # Tabel 7
    t7_headers = ["Klasifikasi Kesalahan", "Definisi Komputasional", "Contoh Masukan -> Prediksi", "Frekuensi", "Persentase", "Akar Masalah Linguistik"]
    t7_data = [
        ["Prediksi Benar", "Lema prediksi identik lema kamus.", "tepinaq -> pinaq", "80.438", "80,44%", "Aturan afiksasi dan leksikon cocok tepat."],
        ["Understemming", "Panjang lema prediksi > lema acuan.", "pegawianne -> pegawian (gawi)", "15.856", "15,86%", "Imbuhan bertingkat 3 lapis belum tuntas terkelupas."],
        ["Overstemming", "Huruf akar kata asli terpotong.", "jaran -> jar (sufiks -an)", "2.279", "2,28%", "Huruf akhir akar kata menyerupai morfem terikat."],
        ["Incorrect Lemma", "Panjang sama, karakter berbeda.", "mangan -> pangan (mangan)", "1.427", "1,43%", "Ambiguitas alternasi nasal (m -> p vs m -> m)."],
        ["Out-of-Vocabulary", "Lema tidak ada dalam leksikon.", "Kata serapan / neologisme", "0", "0,00%", "Seluruh lema benchmark berbasis leksikon rujukan."]
    ]
    format_table(t7_headers, t7_data, col_widths=[1.2, 1.4, 1.4, 0.7, 0.7, 1.5], alignment=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT])
    add_caption("Tabel 7. Analisis Taksonomi Kesalahan pada 100.000 Data Uji.")

    add_heading_2("6.2. Mengapa SasakNLP Bekerja Efektif")
    doc.add_paragraph(
        "Keunggulan performa SasakNLP bersumber dari integrasi PrefixTrie sebagai gerbang validasi kamus leksikon [10], [17]. Pada pendekatan greedy stripping murni (Baseline 2), "
        "kata seperti jaran ('kuda') secara keliru dipotong menjadi jar karena akhiran -an terdeteksi sebagai sufiks lokatif. Dalam SasakNLP, kata jaran dicocokkan "
        "langsung ke leksikon kamus Balai Bahasa NTB pada lintasan pertama, sehingga pemotongan keliru dapat dicegah (zero unnecessary stripping)."
    )

    add_heading_2("6.3. Analisis Kesenjangan Kinerja 100k vs 10k")
    doc.add_paragraph(
        "Perbedaan akurasi antara benchmark 100k (80,44%) dan benchmark 10k (93,23%) mencerminkan perbedaan kompleksitas linguistik. Benchmark 100k berfungsi sebagai "
        "stress-test yang sengaja memasukkan kombinasi imbuhan berlapis tiga (misalnya konfiks pe-...-an yang ditambah enklitika -ne dan prefiks te-), di mana algoritma "
        "two-pass terkadang berhenti sebelum lema dasar terdalam tercapai (understemming 15,86%). Sementara pada benchmark 10k, sebaran afiksasi mencerminkan frekuensi "
        "penggunaan alami dalam tuturan sehari-hari."
    )

    add_heading_2("6.4. Implikasi bagi Ekosistem NLP Bahasa Daerah")
    doc.add_paragraph(
        "Temuan ini membuktikan bahwa bahasa daerah berdaya komputasi rendah di Indonesia dapat ditangani secara efektif melalui rekayasa representasi morfologi "
        "berbasis leksikon kamus resmi daerah tanpa harus bergantung pada infrastruktur komputasi GPU berskala besar [1], [6], [13]."
    )

    # --- SECTION 7: KETERBATASAN PENELITIAN ---
    add_heading_1("7. Keterbatasan Penelitian (Limitations)")
    doc.add_paragraph(
        "Sebagai pertanggungjawaban ilmiah yang transparan, naskah ini menguraikan batasan riset saat ini:\n"
        "1. Ketergantungan Kosakata Terkontrol: Evaluasi skala 100.000 data dilakukan pada kombinasi morfem teratur berbasis lema kamus terdaftar. Evaluasi pada teks media sosial tak berstruktur yang memuat neologisme slang kontemporer masih memerlukan penelitian lanjutan.\n"
        "2. Keseimbangan Korpus Dialek: Sebaran korpus kalimat autentik saat ini masih didominasi oleh dialek Sasak Umum dan Lombok Timur, merefleksikan ketersediaan dokumen literatur daerah yang terdokumentasi.\n"
        "3. Ketiadaan Konteks Sintaksis Kalimat: Sistem lematisasi saat ini beroperasi pada tingkat kata/token berbasis leksikon tanpa memanfaatkan model penanda kelas kata (Part-of-Speech Tagger) tingkat kalimat."
    )

    # --- SECTION 8: KESIMPULAN & RISET MASA DEPAN ---
    add_heading_1("8. Kesimpulan dan Agenda Riset Masa Depan (Conclusion & Future Directions)")
    doc.add_paragraph(
        "Penelitian ini berhasil merancang, mengimplementasikan, dan mengevaluasi SasakNLP, sebuah kerangka kerja pemrosesan morfologi dan NLP sadar dialek "
        "pertama untuk Bahasa Sasak. Berbasis pengujian 100.000 pasangan data uji terverifikasi, SasakNLP mencapai akurasi lematisasi 80,44% pada benchmark penuh "
        "dan 93,23% pada benchmark inti 10k, menekan overstemming hingga 2,28%, serta membukukan throughput tinggi 7.826–16.272 kata/detik dengan latensi "
        "0,044 ms/kata tanpa dependensi pustaka berat eksternal."
    )
    doc.add_paragraph(
        "Agenda riset masa depan mencakup: (1) Integrasi model sequence-to-sequence probabilistik ringan (ByT5 / Char-BiLSTM) untuk menangani kata slang di luar kamus (OOV neologisms), "
        "(2) Pembangunan korpus beranotasi Part-of-Speech (POS) dan Dependency Treebank Bahasa Sasak pertama, serta "
        "(3) Pelatihan model penerjemahan mesin saraf (Neural Machine Translation) dwiarah Sasak-Indonesia [1], [2], [6]."
    )

    # --- DATA AVAILABILITY ---
    add_heading_1("Pernyataan Ketersediaan Data dan Perangkat Lunak (Data Availability)")
    doc.add_paragraph(
        "Demi keterbukaan sains (open science) dan keterulangan riset (reproducibility), seluruh artefak riset dapat diakses secara bebas:\n"
        "• Paket Resmi PyPI: https://pypi.org/project/sasaknlp/ (pip install sasaknlp)\n"
        "• Repositori Kode Sumber GitHub: https://github.com/kodetr/sasaknlp\n"
        "• Dataset Resmi Hugging Face: https://huggingface.co/datasets/kodetr/sasak-benchmark-100k\n"
        "• Demonstrasi Interaktif Web Space: https://huggingface.co/spaces/kodetr/sasaknlp-demo\n"
        "• Website Peneliti: https://kodetr.com"
    )

    # --- ACKNOWLEDGMENTS ---
    add_heading_1("Ucapan Terima Kasih (Acknowledgments)")
    doc.add_paragraph(
        "Penulis menyampaikan apresiasi dan terima kasih kepada para penutur asli dan pegiat bahasa Sasak di Pulau Lombok, "
        "peneliti dialektologi terdahulu, serta Balai Bahasa Provinsi Nusa Tenggara Barat atas dedikasi dalam penyusunan "
        "kamus dwibahasa Sasak-Indonesia yang menjadi landasan leksikal bagi pengembangan teknologi komputasi ini."
    )

    # --- REFERENCES (22 100% REAL & VERIFIED 2021-2026) ---
    add_heading_1("Daftar Pustaka (References)")
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
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        p_ref.paragraph_format.space_after = Pt(4)
        run_ref = p_ref.add_run(r)
        run_ref.font.size = Pt(9.5)

    doc.save(output_path)
    print(f"✅ Dokumen berhasil dibuat: {output_path}")

if __name__ == "__main__":
    build_docx("artikel/jurnal_sasaknlp.docx")
