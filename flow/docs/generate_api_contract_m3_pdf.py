import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header (Halaman > 1)
        if self._pageNumber > 1:
            self.drawRightString(559, 814, "Araya Business Hub | Modul 3: Manajemen Partner")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 808, 559, 808)

        # Running Footer (Semua halaman)
        footer_text = f"Spesifikasi API & Event Modul 3 | v2.0 (draf) | Halaman {self._pageNumber} dari {page_count}"
        self.drawString(36, 18, footer_text)
        self.drawRightString(559, 18, "Dokumen Acuan Resmi Tim Modul 3")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 28, 559, 28)
        self.restoreState()


def build_pdf():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(output_dir, "02_API_Contract_Modul_3.pdf")

    # Margins: 36pt (0.5 inch) left/right, printable width = 595.27 - 72 = 523.27 pt
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Color Palette matching Modul 4
    c_primary = colors.HexColor("#1E3A8A")     # Navy 900
    c_accent = colors.HexColor("#2563EB")      # Blue 600
    c_dark = colors.HexColor("#0F172A")        # Slate 900
    c_body = colors.HexColor("#334155")        # Slate 700
    c_light = colors.HexColor("#F8FAFC")       # Slate 50
    c_border = colors.HexColor("#CBD5E1")      # Slate 300

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=c_body,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_accent,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_dark,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'BodyBoldCustom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    list_style = ParagraphStyle(
        'ListCustom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    tbl_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white
    )

    tbl_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9.5,
        textColor=c_dark
    )

    tbl_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=tbl_cell,
        fontName='Helvetica-Bold'
    )

    tbl_cell_code = ParagraphStyle(
        'TableCellCode',
        parent=tbl_cell,
        fontName='Courier',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor("#0F172A")
    )

    code_block = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.5,
        textColor=colors.HexColor("#1E293B"),
        backColor=c_light,
        borderColor=c_border,
        borderWidth=0.5,
        borderPadding=4,
        spaceAfter=6
    )

    endpoint_badge = ParagraphStyle(
        'EndpointBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1E3A8A"),
        backColor=colors.HexColor("#EFF6FF"),
        borderColor=colors.HexColor("#BFDBFE"),
        borderWidth=0.5,
        borderPadding=3,
        spaceBefore=4,
        spaceAfter=4
    )

    story = []

    # ==========================================
    # HALAMAN 1: JUDUL & RINGKASAN PERUBAHAN
    # ==========================================
    story.append(Paragraph("Spesifikasi API & Event Antar-Modul<br/>(Modul 3)", title_style))
    story.append(Paragraph("Araya Business Hub Platform — Modul 3: Manajemen Partner (Partner Management)", subtitle_style))

    meta_data = [
        [Paragraph("Versi Dokumen", tbl_cell_bold), Paragraph("v2.0 (draf)", tbl_cell)],
        [Paragraph("Tanggal", tbl_cell_bold), Paragraph("8 November 2026", tbl_cell)],
        [Paragraph("Status", tbl_cell_bold), Paragraph("Draf Resmi. Mengikuti Panduan API Bersama v1.0 (draf, 28 Okt 2026) dan mengintegrasikan seluruh hasil Sprint 1 (Task T4.2, T5.2, T11, K-06).", tbl_cell)],
        [Paragraph("OpenAPI Specification", tbl_cell_bold), Paragraph("docs/openapi.yaml (tersedia di <code>http://127.0.0.1:8000/api/m3/v1/docs/</code>)", tbl_cell)],
    ]
    t_meta = Table(meta_data, colWidths=[110, 413])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Ringkasan Perubahan dari v1.0", h1_style))
    story.append(Paragraph("Panduan API Bersama mewajibkan bentuk yang sama di semua modul Araya Hub. Karena itu kontrak Modul 3 diselaraskan pada hal-hal berikut:", body_style))

    changes_data = [
        [Paragraph("Aspek", tbl_header), Paragraph("v1.0 (lama)", tbl_header), Paragraph("v2.0 (mengikuti panduan)", tbl_header)],
        [Paragraph("Alamat dasar", tbl_cell_bold), Paragraph("/api/partners/register/", tbl_cell), Paragraph("/api/m3/v1/partners/", tbl_cell_bold)],
        [Paragraph("Respons sukses", tbl_cell_bold), Paragraph("Objek langsung", tbl_cell), Paragraph("{ success: true, status: 'success', data, meta }", tbl_cell_code)],
        [Paragraph("Respons galat", tbl_cell_bold), Paragraph("Format tidak seragam", tbl_cell), Paragraph("{ success: false, error: { code, message, fields } }", tbl_cell_code)],
        [Paragraph("Galat validasi", tbl_cell_bold), Paragraph("400 Bad Request", tbl_cell), Paragraph("422 Unprocessable Entity (VALIDATION_ERROR)", tbl_cell_bold)],
        [Paragraph("Galat email duplikat", tbl_cell_bold), Paragraph("400 Bad Request", tbl_cell), Paragraph("409 Conflict (EMAIL_DUPLICATE)", tbl_cell_bold)],
        [Paragraph("Identitas Dokumen", tbl_cell_bold), Paragraph("NPWP usaha (opsional)", tbl_cell), Paragraph("Foto KTP & Foto Selfie Pegang KTP (JPG/PNG maks 5MB)", tbl_cell_bold)],
        [Paragraph("Validasi NIK", tbl_cell_bold), Paragraph("Tidak divalidasi", tbl_cell), Paragraph("Wajib tepat 16 digit angka murni (T5.2)", tbl_cell_bold)],
        [Paragraph("Kredensial Akun", tbl_cell_bold), Paragraph("Tidak ada pendaftaran akun", tbl_cell), Paragraph("Password minimal 8 char kombinasi huruf & angka, write-only hashed PBKDF2", tbl_cell_bold)],
        [Paragraph("Kode Pendaftaran", tbl_cell_bold), Paragraph("ID numerik saja (1, 2...)", tbl_cell), Paragraph("PRT-YYYYMMDD-XXXX (kode publik unik otomatis)", tbl_cell_bold)],
        [Paragraph("Pencarian Status", tbl_cell_bold), Paragraph("Hanya lewat ID integer", tbl_cell), Paragraph("Dual Lookup: ID integer ATAU kode string partner_id", tbl_cell_bold)],
        [Paragraph("Alasan Penolakan", tbl_cell_bold), Paragraph("Field alasan_penolakan statis", tbl_cell), Paragraph("rejection_reason & alasan_penolakan hanya tampil bila status ditolak (T11)", tbl_cell_bold)],
        [Paragraph("Katalog M5 (K-06)", tbl_cell_bold), Paragraph("Belum didefinisikan", tbl_cell), Paragraph("GET /api/m3/v1/partners/?status=terverifikasi (pagination meta)", tbl_cell_bold)],
        [Paragraph("Panggilan antar-modul", tbl_cell_bold), Paragraph("Tidak diatur", tbl_cell), Paragraph("Header X-Service-Key dan Bearer Token JWT M1", tbl_cell_bold)],
    ]
    t_changes = Table(changes_data, colWidths=[95, 140, 288])
    t_changes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_changes)

    # ==========================================
    # HALAMAN 2: KONVENSI UMUM & FORMAT DATA
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("2. Konvensi Umum", h1_style))
    story.append(Paragraph("1. <b>Pola alamat</b>: <code>https://[server-bersama]/api/m3/v1/{resource}</code>. Kode modul m3 dan versi selalu disertakan.", list_style))
    story.append(Paragraph("2. <b>Resource</b>: kata benda jamak bahasa Inggris huruf kecil: <code>partners</code>.", list_style))
    story.append(Paragraph("3. <b>Satu data</b>: resource + ID atau kode publik: <code>/partners/1</code> atau <code>/partners/PRT-20261108-A9F2</code>.", list_style))
    story.append(Paragraph("4. <b>Nama field JSON</b>: snake_case bahasa Indonesia/Inggris sesuai model domain: <code>nama_usaha</code>, <code>penanggung_jawab_nik</code>, <code>partner_id</code>, <code>unit_usaha_id</code>.", list_style))
    story.append(Paragraph("5. <b>Method HTTP</b>: GET tidak mengubah data; POST membuat data atau registrasi (berhasil: 201); PATCH/PUT mengubah data; DELETE menonaktifkan data.", list_style))
    story.append(Paragraph("6. <b>Dokumentasi</b>: <code>docs/openapi.yaml</code> di repositori dan halaman interaktif Swagger di <code>/api/m3/v1/docs/</code>.", list_style))

    story.append(Paragraph("2.1 Format Data", h2_style))
    fmt_data = [
        [Paragraph("Data", tbl_header), Paragraph("Format di API", tbl_header), Paragraph("Contoh", tbl_header)],
        [Paragraph("Tanggal", tbl_cell_bold), Paragraph("ISO 8601 YYYY-MM-DD", tbl_cell), Paragraph('"1990-05-15"', tbl_cell_code)],
        [Paragraph("Tanggal dan Jam", tbl_cell_bold), Paragraph("ISO 8601 zona WIB (+07:00)", tbl_cell), Paragraph('"2026-11-08T09:15:00+07:00"', tbl_cell_code)],
        [Paragraph("NIK", tbl_cell_bold), Paragraph("String 16 digit angka murni", tbl_cell), Paragraph('"3201234567890001"', tbl_cell_code)],
        [Paragraph("Kode Pendaftaran", tbl_cell_bold), Paragraph("PREFIKS-YYYYMMDD-XXXX (4 digit acak)", tbl_cell), Paragraph('"PRT-20261108-A9F2"', tbl_cell_code)],
        [Paragraph("Status Partner", tbl_cell_bold), Paragraph("Teks huruf kecil snake_case", tbl_cell), Paragraph('"pending", "terverifikasi", "ditolak"', tbl_cell_code)],
        [Paragraph("ID Internal", tbl_cell_bold), Paragraph("Bilangan bulat positif (integer PK)", tbl_cell), Paragraph('1, 42', tbl_cell_code)],
        [Paragraph("ID Modul 2", tbl_cell_bold), Paragraph("Bilangan bulat rujukan Master Unit Usaha", tbl_cell), Paragraph('"unit_usaha_id": 1', tbl_cell_code)],
        [Paragraph("Berkas Gambar", tbl_cell_bold), Paragraph("Multipart file (JPG, JPEG, PNG maks 5MB)", tbl_cell), Paragraph('foto_ktp: Binary stream', tbl_cell_code)],
        [Paragraph("Password", tbl_cell_bold), Paragraph("String minimal 8 char (huruf & angka), write-only", tbl_cell), Paragraph('Di-hash dengan PBKDF2 di DB', tbl_cell_code)],
        [Paragraph("Kosong / Null", tbl_cell_bold), Paragraph("null, bukan string kosong", tbl_cell), Paragraph('"rejection_reason": null', tbl_cell_code)],
    ]
    t_fmt = Table(fmt_data, colWidths=[90, 210, 223])
    t_fmt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_fmt)
    story.append(Spacer(1, 6))

    story.append(Paragraph("2.2 Daftar, Filter, dan Pagination (K-06)", h2_style))
    query_data = [
        [Paragraph("Parameter", tbl_header), Paragraph("Arti & Keterangan", tbl_header), Paragraph("Contoh", tbl_header)],
        [Paragraph("status", tbl_cell_bold), Paragraph("Filter status partner (default: terverifikasi untuk katalog M5)", tbl_cell), Paragraph("?status=terverifikasi", tbl_cell_code)],
        [Paragraph("page, per_page", tbl_cell_bold), Paragraph("Nomor halaman dan jumlah item per halaman (bawaan 20, maks 100)", tbl_cell), Paragraph("?page=1&per_page=20", tbl_cell_code)],
        [Paragraph("q", tbl_cell_bold), Paragraph("Pencarian nama toko/usaha secara case-insensitive", tbl_cell), Paragraph("?q=berkah", tbl_cell_code)],
    ]
    t_query = Table(query_data, colWidths=[90, 250, 183])
    t_query.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_query)

    # ==========================================
    # HALAMAN 3: AUTENTIKASI DAN HAK AKSES
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("3. Autentikasi dan Hak Akses", h1_style))
    auth_data = [
        [Paragraph("Situasi", tbl_header), Paragraph("Header", tbl_header), Paragraph("Keterangan", tbl_header)],
        [Paragraph("Pengguna Login (Admin/Partner)", tbl_cell_bold), Paragraph("Authorization: Bearer &lt;token&gt;", tbl_cell_code), Paragraph("Token JWT dari M1 (berlaku 8 jam)", tbl_cell)],
        [Paragraph("Panggilan Antarmodul Tanpa Pengguna", tbl_cell_bold), Paragraph("X-Service-Key: &lt;kunci modul&gt;", tbl_cell_code), Paragraph("Satu kunci per modul, disimpan di .env", tbl_cell)],
        [Paragraph("Endpoint Publik (Pendaftaran)", tbl_cell_bold), Paragraph("Tanpa header", tbl_cell_bold), Paragraph("Calon partner mendaftar mandiri (M3-US1)", tbl_cell)],
    ]
    t_auth = Table(auth_data, colWidths=[130, 170, 223])
    t_auth.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_auth)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Contoh payload Token JWT dari Modul 1 (M1):", body_style))
    jwt_snippet = """{
  "user_id": 42,
  "name": "Budi Santoso",
  "role": "partner",
  "email": "toko.berkah@example.com",
  "exp": 1793180400
}"""
    story.append(Preformatted(jwt_snippet, code_block))

    story.append(Paragraph("3.1 Matriks Hak Akses per Endpoint", h2_style))
    matrix_data = [
        [Paragraph("Endpoint", tbl_header), Paragraph("Publik", tbl_header), Paragraph("Calon Partner", tbl_header), Paragraph("Partner Terverifikasi", tbl_header), Paragraph("Administrator", tbl_header), Paragraph("Modul Eksternal", tbl_header)],
        [Paragraph("POST /partners/ (Daftar)", tbl_cell_code), Paragraph("Ya", tbl_cell_bold), Paragraph("Ya", tbl_cell_bold), Paragraph("Tidak", tbl_cell), Paragraph("Ya", tbl_cell), Paragraph("n/a", tbl_cell)],
        [Paragraph("GET /partners/{id}/ (Status)", tbl_cell_code), Paragraph("Ya (via PRT)", tbl_cell_bold), Paragraph("Ya (Milik sendiri)", tbl_cell_bold), Paragraph("Ya", tbl_cell), Paragraph("Semua", tbl_cell_bold), Paragraph("M1 / M2", tbl_cell)],
        [Paragraph("GET /partners/?status=terverifikasi", tbl_cell_code), Paragraph("Ya (K-06)", tbl_cell_bold), Paragraph("Ya", tbl_cell), Paragraph("Ya", tbl_cell), Paragraph("Semua", tbl_cell_bold), Paragraph("M4, M5 (Katalog)", tbl_cell_bold)],
        [Paragraph("GET /docs/ & /openapi.yaml", tbl_cell_code), Paragraph("Ya", tbl_cell_bold), Paragraph("Ya", tbl_cell_bold), Paragraph("Ya", tbl_cell_bold), Paragraph("Ya", tbl_cell_bold), Paragraph("Semua Tim", tbl_cell_bold)],
    ]
    t_matrix = Table(matrix_data, colWidths=[150, 60, 75, 85, 75, 78])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_matrix)

    # ==========================================
    # HALAMAN 4: BENTUK RESPONS & KODE STATUS
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("4. Bentuk Respons dan Kode Status", h1_style))
    story.append(Paragraph("<b>Respons Sukses Satu Data (201 Created / 200 OK):</b>", body_style))
    resp_single = """{
  "success": true,
  "status": "success",
  "message": "Pendaftaran partner berhasil dikirim dan menunggu verifikasi.",
  "data": {
    "id": 1,
    "partner_id": "PRT-20261108-A9F2",
    "unit_usaha_id": 1,
    "nama_usaha": "Toko Berkah Sejahtera",
    "kategori_usaha": "Produk",
    "status": "pending",
    "penanggung_jawab_nik": "3201234567890001",
    "foto_ktp": "/media/partner_documents/ktp/ktp.png",
    "foto_memegang_ktp": "/media/partner_documents/selfie/selfie_ktp.png",
    "rejection_reason": null,
    "created_at": "2026-11-08T09:15:00+07:00"
  }
}"""
    story.append(Preformatted(resp_single, code_block))

    story.append(Paragraph("<b>Respons Galat Validasi (422 Unprocessable Entity):</b>", body_style))
    resp_error = """{
  "success": false,
  "status": "error",
  "message": "Isian tidak lolos validasi. Periksa kelengkapan data.",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Isian tidak lolos validasi. Periksa kelengkapan data.",
    "fields": {
      "penanggung_jawab_nik": "NIK penanggung jawab harus tepat 16 digit angka.",
      "foto_ktp": "Format berkas foto KTP harus berupa gambar JPG atau PNG.",
      "password": "Password minimal 8 karakter dan mengandung kombinasi huruf serta angka."
    }
  },
  "errors": { ... }
}"""
    story.append(Preformatted(resp_error, code_block))

    story.append(Paragraph("Katalog Kode Status HTTP:", h2_style))
    http_codes = [
        [Paragraph("Kode", tbl_header), Paragraph("Arti", tbl_header), Paragraph("Penerapan pada Modul 3", tbl_header)],
        [Paragraph("200", tbl_cell_bold), Paragraph("Berhasil (OK)", tbl_cell), Paragraph("Pengambilan status partner atau daftar katalog partner terverifikasi.", tbl_cell)],
        [Paragraph("201", tbl_cell_bold), Paragraph("Data Baru Dibuat", tbl_cell), Paragraph("Pendaftaran calon partner baru berhasil terkirim (status: pending).", tbl_cell)],
        [Paragraph("400", tbl_cell_bold), Paragraph("Bad Request", tbl_cell), Paragraph("Format request cacat (malformed JSON).", tbl_cell)],
        [Paragraph("404", tbl_cell_bold), Paragraph("Not Found", tbl_cell), Paragraph("Data partner tidak ditemukan baik via ID maupun partner_id.", tbl_cell)],
        [Paragraph("409", tbl_cell_bold), Paragraph("Conflict", tbl_cell), Paragraph("Email usaha sudah terdaftar pada sistem (EMAIL_DUPLICATE).", tbl_cell)],
        [Paragraph("422", tbl_cell_bold), Paragraph("Unprocessable Entity", tbl_cell), Paragraph("Isian tidak lolos validasi: NIK bukan 16 digit, file > 5MB, password lemah.", tbl_cell)],
        [Paragraph("500", tbl_cell_bold), Paragraph("Internal Server Error", tbl_cell), Paragraph("Gangguan tak terduga pada server/basis data.", tbl_cell)],
    ]
    t_http = Table(http_codes, colWidths=[40, 110, 373])
    t_http.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_http)

    # ==========================================
    # HALAMAN 5: KONTRAK ANTARMODUL
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("5. Kontrak Antarmodul yang Melibatkan Modul 3", h1_style))
    story.append(Paragraph("Modul 3 berinteraksi dengan modul-modul lain di dalam ekosistem Araya Business Hub:", body_style))

    contract_data = [
        [Paragraph("ID", tbl_header), Paragraph("Kontrak", tbl_header), Paragraph("Arah", tbl_header), Paragraph("Bentuk Integrasi", tbl_header), Paragraph("Modul Terkait", tbl_header)],
        [Paragraph("K-06", tbl_cell_bold), Paragraph("Katalog Partner Terverifikasi", tbl_cell_bold), Paragraph("M3 menyediakan,<br/>M5 & M4 memakai", tbl_cell), Paragraph("GET /api/m3/v1/partners/?status=terverifikasi", tbl_cell_code), Paragraph("Modul 5 (Katalog Publik),<br/>Modul 4 (Penjualan)", tbl_cell)],
        [Paragraph("K-01", tbl_cell_bold), Paragraph("Akun & Autentikasi Mitra", tbl_cell_bold), Paragraph("M1 menyediakan,<br/>M3 mengintegrasikan", tbl_cell), Paragraph("Kredensial email & password_hash, user_id", tbl_cell), Paragraph("Modul 1 (User & Auth)", tbl_cell)],
        [Paragraph("M2-Ref", tbl_cell_bold), Paragraph("Master Kategori Unit Usaha", tbl_cell_bold), Paragraph("M2 menyediakan,<br/>M3 mengaitkan", tbl_cell), Paragraph("GET /api/m2/v1/unit-usaha/ & unit_usaha_id", tbl_cell_code), Paragraph("Modul 2 (Master Usaha)", tbl_cell)],
        [Paragraph("M4-Prereq", tbl_cell_bold), Paragraph("Prasyarat Input Produk Mitra", tbl_cell_bold), Paragraph("M4 mengecek ke M3", tbl_cell), Paragraph("Hanya partner berstatus 'terverifikasi' yang boleh input produk/jasa di M4", tbl_cell), Paragraph("Modul 4 (Katalog Produk)", tbl_cell)],
    ]
    t_contract = Table(contract_data, colWidths=[55, 120, 100, 150, 98])
    t_contract.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_contract)
    story.append(Spacer(1, 10))

    # ==========================================
    # HALAMAN 6: ENDPOINT POST PENDAFTARAN (T4.2 & T5.2)
    # ==========================================
    story.append(Paragraph("6. Endpoint Spesifikasi Modul 3", h1_style))
    story.append(Paragraph("6.1 Pendaftaran Calon Partner Baru (M3-US1, T4.2, T5.2)", h2_style))
    story.append(Paragraph("POST /api/m3/v1/partners/", endpoint_badge))
    story.append(Paragraph("• <b>Tujuan</b>: Menerima berkas pendaftaran mandiri calon partner, memvalidasi NIK 16 digit, memvalidasi berkas gambar (KTP & selfie KTP maks 5MB), memvalidasi password kuat, auto-generate kode publik <code>partner_id</code> (PRT-YYYYMMDD-XXXX), dan menyimpan dengan status awal <code>pending</code>.", list_style))
    story.append(Paragraph("• <b>Content-Type</b>: <code>multipart/form-data</code> (direkomendasikan) atau <code>application/json</code>.", list_style))
    story.append(Paragraph("• <b>Akses</b>: Publik tanpa token.", list_style))

    post_fields = [
        [Paragraph("Field", tbl_header), Paragraph("Tipe Data", tbl_header), Paragraph("Wajib", tbl_header), Paragraph("Aturan Validasi & Keterangan", tbl_header)],
        [Paragraph("nama_usaha", tbl_cell_bold), Paragraph("String", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Nama toko/usaha pemohon (maks 255 karakter).", tbl_cell)],
        [Paragraph("kategori_usaha", tbl_cell_bold), Paragraph("String (Enum)", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Pilihan: 'Produk' atau 'Jasa'.", tbl_cell)],
        [Paragraph("unit_usaha_id", tbl_cell_bold), Paragraph("Integer", tbl_cell), Paragraph("Tidak", tbl_cell), Paragraph("ID unit usaha dari Modul 2.", tbl_cell)],
        [Paragraph("deskripsi_usaha", tbl_cell_bold), Paragraph("String", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Uraian bidang usaha.", tbl_cell)],
        [Paragraph("alamat_usaha", tbl_cell_bold), Paragraph("String", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Alamat operasional lengkap.", tbl_cell)],
        [Paragraph("nomor_telepon_usaha", tbl_cell_bold), Paragraph("String", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Nomor telepon / WhatsApp aktif.", tbl_cell)],
        [Paragraph("email_usaha", tbl_cell_bold), Paragraph("String (Email)", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Email unik usaha. Galat 409 jika duplikat.", tbl_cell)],
        [Paragraph("penanggung_jawab_nama", tbl_cell_bold), Paragraph("String", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Nama lengkap penanggung jawab sesuai KTP.", tbl_cell)],
        [Paragraph("penanggung_jawab_nik", tbl_cell_bold), Paragraph("String", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Wajib tepat 16 digit angka murni (T5.2).", tbl_cell_bold)],
        [Paragraph("tempat_lahir", tbl_cell_bold), Paragraph("String", tbl_cell), Paragraph("Tidak", tbl_cell), Paragraph("Kota kelahiran penanggung jawab.", tbl_cell)],
        [Paragraph("tanggal_lahir", tbl_cell_bold), Paragraph("Date (ISO)", tbl_cell), Paragraph("Tidak", tbl_cell), Paragraph("Format: YYYY-MM-DD.", tbl_cell)],
        [Paragraph("password", tbl_cell_bold), Paragraph("String (Write-only)", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Minimal 8 karakter kombinasi huruf & angka (T5.2).", tbl_cell_bold)],
        [Paragraph("foto_ktp", tbl_cell_bold), Paragraph("File (Binary)", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Foto KTP: Format JPG/PNG, ukuran maks 5 MB.", tbl_cell_bold)],
        [Paragraph("foto_memegang_ktp", tbl_cell_bold), Paragraph("File (Binary)", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Selfie memegang KTP: JPG/PNG maks 5 MB.", tbl_cell_bold)],
        [Paragraph("profil_usaha", tbl_cell_bold), Paragraph("File (Binary)", tbl_cell), Paragraph("Tidak", tbl_cell), Paragraph("Logo/foto toko opsional (JPG/PNG maks 5 MB).", tbl_cell)],
    ]
    t_post = Table(post_fields, colWidths=[95, 65, 35, 328])
    t_post.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_post)

    # ==========================================
    # HALAMAN 7: DETAIL STATUS & DUAL LOOKUP (T10 & T11)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("6.2 Detail dan Status Pendaftaran Partner (M3-US3, T10, T11)", h2_style))
    story.append(Paragraph("GET /api/m3/v1/partners/{id}/", endpoint_badge))
    story.append(Paragraph("• <b>Tujuan</b>: Melacak status pengajuan pendaftaran partner. Mendukung <b>Dual Lookup</b>:", list_style))
    story.append(Paragraph("  1. Pencarian via ID internal numerik: <code>/api/m3/v1/partners/1/</code>", list_style))
    story.append(Paragraph("  2. Pencarian via kode string publik: <code>/api/m3/v1/partners/PRT-20261108-A9F2/</code>", list_style))
    story.append(Paragraph("• <b>Aturan Backend Logika Rejection Reason (Task T11)</b>:", list_style))
    story.append(Paragraph("  - Bila status <code>ditolak</code>: Mengembalikan pesan alasan penolakan pada field <code>alasan_penolakan</code> dan <code>rejection_reason</code>.", list_style))
    story.append(Paragraph("  - Bila status selain <code>ditolak</code> (mis. <code>pending</code> atau <code>terverifikasi</code>): Field <code>alasan_penolakan</code> dan <code>rejection_reason</code> dijamin bernilai <code>null</code> agar alasan penolakan masa lalu tidak bocor.", list_style))

    story.append(Paragraph("Contoh Respons Detail Berstatus Ditolak (200 OK):", body_style))
    detail_ditolak = """{
  "success": true,
  "data": {
    "id": 1,
    "partner_id": "PRT-20261108-A9F2",
    "nama_usaha": "Toko Berkah Sejahtera",
    "status": "ditolak",
    "alasan_penolakan": "Foto KTP buram dan NIK tidak terdaftar di Disdukcapil.",
    "rejection_reason": "Foto KTP buram dan NIK tidak terdaftar di Disdukcapil.",
    "created_at": "2026-11-08T09:15:00+07:00"
  }
}"""
    story.append(Preformatted(detail_ditolak, code_block))

    story.append(Paragraph("6.3 Katalog Partner Terverifikasi untuk Modul 5 & 4 (Kontrak K-06)", h2_style))
    story.append(Paragraph("GET /api/m3/v1/partners/?status=terverifikasi", endpoint_badge))
    story.append(Paragraph("• <b>Tujuan</b>: Sumber data resmi bagi Modul 5 (Katalog Publik) untuk menampilkan daftar mitra aktif, serta Modul 4 untuk validasi hak posting produk.", list_style))
    story.append(Paragraph("• <b>Contoh Respons Katalog (200 OK):</b>", body_style))
    k06_resp = """{
  "success": true,
  "data": [
    {
      "id": 1,
      "partner_id": "PRT-20261108-A9F2",
      "nama_usaha": "Toko Berkah Sejahtera",
      "kategori_usaha": "Produk",
      "deskripsi_usaha": "Menjual sembako berkualitas.",
      "alamat_usaha": "Jl. Gatot Subroto No. 45, Bandung",
      "nomor_telepon_usaha": "081234567890",
      "profil_usaha": "/media/partner_profiles/logo.png",
      "status": "terverifikasi"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 1,
    "total_pages": 1
  }
}"""
    story.append(Preformatted(k06_resp, code_block))

    # ==========================================
    # HALAMAN 8: KATALOG KODE GALAT LENGKAP
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("7. Katalog Kode Galat (Error Catalog)", h1_style))
    story.append(Paragraph("Seluruh respons galat mengikuti kontrak baku dengan kode HURUF_BESAR_DENGAN_GARIS_BAWAH:", body_style))

    err_catalog = [
        [Paragraph("error.code", tbl_header), Paragraph("HTTP", tbl_header), Paragraph("Kapan Terjadi", tbl_header), Paragraph("Pesan Resmi (Bahasa Indonesia)", tbl_header)],
        [Paragraph("VALIDATION_ERROR", tbl_cell_code), Paragraph("422", tbl_cell_bold), Paragraph("NIK bukan 16 digit, ukuran file > 5MB, format berkas non-gambar, password kurang kuat, atau isian wajib kosong.", tbl_cell), Paragraph("Isian tidak lolos validasi. Periksa kelengkapan data.", tbl_cell)],
        [Paragraph("EMAIL_DUPLICATE", tbl_cell_code), Paragraph("409", tbl_cell_bold), Paragraph("Email usaha yang dimasukkan sudah terdaftar pada database partner.", tbl_cell), Paragraph("Email sudah terdaftar.", tbl_cell)],
        [Paragraph("EMAIL_INVALID", tbl_cell_code), Paragraph("422", tbl_cell_bold), Paragraph("Format penulisan email salah atau tidak valid.", tbl_cell), Paragraph("Format email tidak valid.", tbl_cell)],
        [Paragraph("NOT_FOUND", tbl_cell_code), Paragraph("404", tbl_cell_bold), Paragraph("ID numerik atau kode unik partner_id tidak ditemukan.", tbl_cell), Paragraph("Data partner tidak ditemukan.", tbl_cell)],
        [Paragraph("UNAUTHENTICATED", tbl_cell_code), Paragraph("401", tbl_cell_bold), Paragraph("Token JWT tidak ada, salah, atau kedaluwarsa pada endpoint admin.", tbl_cell), Paragraph("Silakan login terlebih dahulu.", tbl_cell)],
        [Paragraph("FORBIDDEN", tbl_cell_code), Paragraph("403", tbl_cell_bold), Paragraph("Pengguna tidak berhak mengakses atau mengubah data partner milik pihak lain.", tbl_cell), Paragraph("Anda tidak berhak mengakses data ini.", tbl_cell)],
        [Paragraph("METHOD_NOT_ALLOWED", tbl_cell_code), Paragraph("405", tbl_cell_bold), Paragraph("Menggunakan method HTTP yang tidak diizinkan pada endpoint.", tbl_cell), Paragraph("Metode HTTP tidak diizinkan.", tbl_cell)],
        [Paragraph("INTERNAL_ERROR", tbl_cell_code), Paragraph("500", tbl_cell_bold), Paragraph("Kesalahan server tak terduga.", tbl_cell), Paragraph("Terjadi kesalahan internal pada server.", tbl_cell)],
    ]
    t_err = Table(err_catalog, colWidths=[105, 30, 200, 188])
    t_err.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_err)
    story.append(Spacer(1, 10))

    # ==========================================
    # HALAMAN 9: PEMETAAN STATUS & ATURAN FRONTEND
    # ==========================================
    story.append(Paragraph("8. Pemetaan Status (API dan Tampilan)", h1_style))
    status_map = [
        [Paragraph("Objek", tbl_header), Paragraph("Nilai di API", tbl_header), Paragraph("Label di UI", tbl_header), Paragraph("Warna Badge", tbl_header), Paragraph("Aksi Pengguna di Antarmuka", tbl_header)],
        [Paragraph("Partner", tbl_cell_bold), Paragraph("pending", tbl_cell_code), Paragraph("Menunggu Verifikasi", tbl_cell), Paragraph("Kuning / Oranye", tbl_cell_bold), Paragraph("Kunci tombol 'Kembali' ke formulir pendaftaran.", tbl_cell)],
        [Paragraph("Partner", tbl_cell_bold), Paragraph("terverifikasi", tbl_cell_code), Paragraph("Terverifikasi", tbl_cell), Paragraph("Hijau", tbl_cell_bold), Paragraph("Tampilkan tombol 'Masuk ke Akun Toko' (redirect ke Login Modul 1).", tbl_cell)],
        [Paragraph("Partner", tbl_cell_bold), Paragraph("ditolak", tbl_cell_code), Paragraph("Ditolak", tbl_cell), Paragraph("Merah", tbl_cell_bold), Paragraph("Tampilkan pesan alasan penolakan secara persisten dan tombol 'Daftar Ulang'.", tbl_cell)],
        [Paragraph("Partner", tbl_cell_bold), Paragraph("ditangguhkan", tbl_cell_code), Paragraph("Ditangguhkan", tbl_cell), Paragraph("Abu-abu", tbl_cell), Paragraph("Tampilkan petunjuk kontak bantuan administrator.", tbl_cell)],
    ]
    t_status = Table(status_map, colWidths=[55, 80, 105, 75, 208])
    t_status.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_status)

    # ==========================================
    # HALAMAN 10: ALUR KOMUNIKASI & SEQUENCE
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("9. Alur Komunikasi Antarmodul", h1_style))
    story.append(Paragraph("Diagram alur interaksi mulai dari pendaftaran mitra hingga katalog publik Modul 5:", body_style))

    flow_box = """[Calon Mitra / UI Melda]
       |
       | 1. Form submit multipart (Foto KTP, Selfie, NIK 16 digit, Password)
       v
[Backend Modul 3] ---> Validasi data (NIK, file <= 5MB, format JPG/PNG, password)
       |
       | 2. Simpan DB (Password di-hash, auto-generate kode PRT, status: pending)
       v
[Database Modul 3]
       |
       | 3. Respon 201 Created { success: true, partner_id: "PRT-..." }
       v
[Halaman Status Mitra] ---> Poll / Cek Status: GET /api/m3/v1/partners/{partner_id}/
       |
       | [Setelah Admin memverifikasi di M3-US2 -> Status berubah: 'terverifikasi']
       v
[Modul 5 (Katalog Publik)] & [Modul 4 (Katalog Produk)]
       |
       +--> Memanggil GET /api/m3/v1/partners/?status=terverifikasi (Kontrak K-06)
       +--> Menampilkan etalase toko partner aktif & izinkan upload produk di M4."""
    story.append(Preformatted(flow_box, code_block))
    story.append(Spacer(1, 10))

    # ==========================================
    # HALAMAN 11: DAFTAR PERIKSA INTEGRASI & KEPUTUSAN TERBUKA
    # ==========================================
    story.append(Paragraph("10. Daftar Periksa Integrasi (Integration Checklist)", h1_style))
    checklist_data = [
        [Paragraph("Kriteria Evaluasi Panduan API Bersama", tbl_header), Paragraph("Status Modul 3", tbl_header), Paragraph("Bukti / Lokasi Implementasi", tbl_header)],
        [Paragraph("Pola URL alamat dasar /api/m3/v1/...", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("partners/api_urls.py", tbl_cell_code)],
        [Paragraph("Amplop standar respons success / data / error", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("partners/views.py", tbl_cell_code)],
        [Paragraph("Unggah berkas multipart foto KTP & selfie KTP", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("Task T4.2 (MultiPartParser)", tbl_cell_code)],
        [Paragraph("Validasi NIK 16 digit angka murni", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("Task T5.2 (validate_nik)", tbl_cell_code)],
        [Paragraph("Validasi berkas gambar JPG/PNG maks 5 MB", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("Task T5.2 (validate_image_document)", tbl_cell_code)],
        [Paragraph("Validasi password minimal 8 char huruf & angka", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("Task T5.2 (validate_strong_password)", tbl_cell_code)],
        [Paragraph("Kode unik publik partner_id (PRT-YYYYMMDD-XXXX)", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("partners/models.py", tbl_cell_code)],
        [Paragraph("Dual lookup detail partner (ID & PRT string)", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("partners/views.py (PartnerDetailView)", tbl_cell_code)],
        [Paragraph("Logika rejection_reason hanya aktif saat ditolak", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("Task T11 (to_representation)", tbl_cell_code)],
        [Paragraph("Katalog partner terverifikasi (Kontrak K-06)", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("GET /api/m3/v1/partners/?status=terverifikasi", tbl_cell_code)],
        [Paragraph("Spesifikasi OpenAPI 3.0 & Swagger UI", tbl_cell), Paragraph("Lolos (Sesuai)", tbl_cell_bold), Paragraph("docs/openapi.yaml & /api/m3/v1/docs/", tbl_cell_code)],
        [Paragraph("Automated Tests 100% Pass (Zero Regression)", tbl_cell), Paragraph("Lolos (36 Tests)", tbl_cell_bold), Paragraph("partners/tests.py & tests_qa.py", tbl_cell_code)],
    ]
    t_chk = Table(checklist_data, colWidths=[200, 85, 238])
    t_chk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_chk)

    # ==========================================
    # HALAMAN 12: ATURAN PERUBAHAN KONTRAK
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("11. Aturan Perubahan Kontrak", h1_style))
    story.append(Paragraph("Kontrak API hanya sah bila tercatat pada berkas OpenAPI resmi di <code>docs/openapi.yaml</code> dan disetujui tim:", body_style))
    story.append(Paragraph("• <b>Perubahan yang Boleh Dilakukan Langsung (Non-Breaking)</b>: Menambah field respons opsional, menambah endpoint baru, menambah nilai kode galat baru.", list_style))
    story.append(Paragraph("• <b>Perubahan Merusak (Breaking Changes)</b>: Mengubah tipe data, menghapus field yang sudah dipakai, mengubah format URL, atau mengubah field opsional menjadi wajib. Wajib dikoordinasikan minimal 1 minggu sebelumnya kepada seluruh pemakai kontrak.", list_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("12. Atribusi Tim Modul 3", h1_style))
    team_data = [
        [Paragraph("Peran / Tanggung Jawab", tbl_header), Paragraph("Nama Personel", tbl_header), Paragraph("Fokus Kerja", tbl_header)],
        [Paragraph("Backend Developer", tbl_cell_bold), Paragraph("Moch Hary", tbl_cell_bold), Paragraph("Endpoint API, Serializer, Validasi, Dual Lookup, Testing", tbl_cell)],
        [Paragraph("Frontend Developer", tbl_cell_bold), Paragraph("Melda", tbl_cell_bold), Paragraph("Form Multipart Registrasi, Halaman Status, Integrasi UI", tbl_cell)],
        [Paragraph("Database Specialist", tbl_cell_bold), Paragraph("Akbar", tbl_cell_bold), Paragraph("Skema Tabel Partners, Logs, Migrasi, Relasi M2", tbl_cell)],
        [Paragraph("QA / Tester", tbl_cell_bold), Paragraph("Atha", tbl_cell_bold), Paragraph("Pengujian Fungsional, Acceptance Criteria M3-US1 s/d M3-US4", tbl_cell)],
        [Paragraph("Analis & Desain", tbl_cell_bold), Paragraph("Milda", tbl_cell_bold), Paragraph("Analisis Kebutuhan Sistem, Wireframe, UI/UX Workflow", tbl_cell)],
    ]
    t_team = Table(team_data, colWidths=[120, 110, 293])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_team)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Kontrak API Modul 3 berhasil dibuat: {pdf_path}")


if __name__ == "__main__":
    build_pdf()

