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
        footer_text = f"Ringkasan Integrasi & Panduan Cepat Modul 3 (README) | v2.0 (draf) | Halaman {self._pageNumber} dari {page_count}"
        self.drawString(36, 18, footer_text)
        self.drawRightString(559, 18, "Dokumen Acuan Cepat Tim Modul 3")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 28, 559, 28)
        self.restoreState()


def build_pdf():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(output_dir, "01_Ringkasan_Integrasi_M3_README.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#1E3A8A")
    c_accent = colors.HexColor("#2563EB")
    c_dark = colors.HexColor("#0F172A")
    c_body = colors.HexColor("#334155")
    c_light = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=c_body,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=c_dark,
        spaceAfter=4
    )

    tbl_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9.5,
        textColor=colors.white
    )

    tbl_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=9,
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
        borderPadding=3,
        spaceAfter=5
    )

    story = []

    # ==========================================
    # HALAMAN 1: IDENTITAS, QUICK START & PANDUAN KELOMPOK
    # ==========================================
    story.append(Paragraph("Ringkasan Integrasi & Panduan Cepat (Modul 3)", title_style))
    story.append(Paragraph("Araya Business Hub Platform — Modul 3: Manajemen Partner (Partner Management)", subtitle_style))

    meta_data = [
        [Paragraph("Versi Dokumen", tbl_cell_bold), Paragraph("v2.0 (draf) — Cheat Sheet & README Integrasi Lintas Modul", tbl_cell)],
        [Paragraph("Tanggal", tbl_cell_bold), Paragraph("8 November 2026", tbl_cell)],
        [Paragraph("Status", tbl_cell_bold), Paragraph("Mengikuti Panduan API Bersama v1.0 (draf, 28 Okt 2026) & selaras dengan <code>02_API_Contract_Modul_3.pdf</code>", tbl_cell)],
        [Paragraph("Target Pembaca", tbl_cell_bold), Paragraph("Kelompok A1 (Auth), A2 (Dashboard & Unit Usaha), A4 (Penjualan), A5 (Katalog & Website), Tim Pengembang Frontend, Backend, QA, dan Analis", tbl_cell)],
    ]
    t_meta = Table(meta_data, colWidths=[105, 418])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Peran & Tanggung Jawab Modul 3", h1_style))
    story.append(Paragraph(
        "Modul 3 (Manajemen Partner) berperan sebagai <b>Sumber Kebenaran Tunggal (Single Source of Truth)</b> untuk: "
        "(1) Pendaftaran mandiri calon mitra UMKM/usaha, (2) Verifikasi legalitas identitas penanggung jawab (NIK 16 digit, Foto KTP, dan Foto Selfie KTP), "
        "(3) Pengelolaan kredensial akun mitra yang diamankan (password hashing write-only untuk Modul 1), (4) Penerbitan kode referensi publik otomatis berformat <code>PRT-YYYYMMDD-XXXX</code>, "
        "(5) Pelacakan status pendaftaran (pending, terverifikasi, ditolak, ditangguhkan) via Dual Lookup (ID numerik / string PRT), "
        "serta (6) Penyedia resmi master data partner terverifikasi untuk etalase publik Modul 5 dan hak transaksi Modul 4 (Kontrak K-06).",
        body_style
    ))

    story.append(Paragraph("2. Konfigurasi Cepat Koneksi (Quick-Start)", h1_style))
    quick_cfg = [
        [Paragraph("Komponen", tbl_header), Paragraph("Aturan / Nilai Standar", tbl_header), Paragraph("Contoh Implementasi", tbl_header)],
        [Paragraph("Alamat Dasar (Base URL)", tbl_cell_bold), Paragraph("Pola seragam /api/m3/v1/{resource}", tbl_cell), Paragraph("http://127.0.0.1:8000/api/m3/v1/partners/", tbl_cell_code)],
        [Paragraph("Swagger UI / OpenAPI", tbl_cell_bold), Paragraph("Dokumentasi interaktif & kontrak mesin", tbl_cell), Paragraph("GET /api/m3/v1/docs/ & docs/openapi.yaml", tbl_cell_code)],
        [Paragraph("Autentikasi Pengguna", tbl_cell_bold), Paragraph("Token JWT dari Modul 1 (berlaku 8 jam)", tbl_cell), Paragraph("Authorization: Bearer &lt;token_jwt_m1&gt;", tbl_cell_code)],
        [Paragraph("Autentikasi Antar-Modul", tbl_cell_bold), Paragraph("Komunikasi server-to-server tanpa login", tbl_cell), Paragraph("X-Service-Key: &lt;kunci_modul_m3&gt;", tbl_cell_code)],
        [Paragraph("Validasi NIK", tbl_cell_bold), Paragraph("String tepat 16 digit angka murni (T5.2)", tbl_cell), Paragraph('"penanggung_jawab_nik": "3201234567890001"', tbl_cell_code)],
        [Paragraph("Berkas Dokumen Identitas", tbl_cell_bold), Paragraph("Multipart file JPG/PNG maksimal 5 MB (T5.2)", tbl_cell), Paragraph('foto_ktp & foto_memegang_ktp', tbl_cell_code)],
        [Paragraph("Kredensial Password", tbl_cell_bold), Paragraph("Min 8 karakter kombinasi huruf & angka (T5.2)", tbl_cell), Paragraph('"password": "ArayaPartner2026" (write-only)', tbl_cell_code)],
        [Paragraph("Kode Pendaftaran Publik", tbl_cell_bold), Paragraph("PRT-YYYYMMDD-XXXX (4 digit acak)", tbl_cell), Paragraph('"partner_id": "PRT-20261108-A9F2"', tbl_cell_code)],
        [Paragraph("Format Waktu & Status", tbl_cell_bold), Paragraph("ISO 8601 WIB (+07:00); status snake_case", tbl_cell), Paragraph('"2026-11-08T09:15:00+07:00", "pending"', tbl_cell_code)],
    ]
    t_quick = Table(quick_cfg, colWidths=[110, 195, 218])
    t_quick.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_quick)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3. Panduan Cepat per Kelompok Modul (Siapa Memakai Apa?)", h1_style))
    who_uses = [
        [Paragraph("Kelompok", tbl_header), Paragraph("Kontrak", tbl_header), Paragraph("Endpoint / Mekanisme", tbl_header), Paragraph("Keterangan Integrasi", tbl_header)],
        [Paragraph("Kel. A1 (Modul 1)<br/>User & Auth", tbl_cell_bold), Paragraph("K-01", tbl_cell_bold), Paragraph("POST /api/m3/v1/partners/<br/>(kredensial email & password)", tbl_cell_code), Paragraph("M3 menerima akun pendaftaran, mengenkripsi password dengan make_password(), dan menghubungkan user_id bila terautentikasi.", tbl_cell)],
        [Paragraph("Kel. A2 (Modul 2)<br/>Unit Usaha", tbl_cell_bold), Paragraph("M2-Ref", tbl_cell_bold), Paragraph("unit_usaha_id<br/>(relasi kategori usaha)", tbl_cell_code), Paragraph("M3 menyimpan referensi ID Master Unit Usaha dari M2 untuk mengklasifikasikan unit bisnis mitra.", tbl_cell)],
        [Paragraph("Kel. A5 (Modul 5)<br/>Website & Katalog", tbl_cell_bold), Paragraph("K-06", tbl_cell_bold), Paragraph("GET /api/m3/v1/partners/<br/>?status=terverifikasi", tbl_cell_code), Paragraph("M5 memanggil endpoint K-06 untuk menyajikan daftar toko mitra resmi di etalase publik (dengan pagination & q).", tbl_cell)],
        [Paragraph("Kel. A4 (Modul 4)<br/>Penjualan & Produk", tbl_cell_bold), Paragraph("K-06 /<br/>M4-Prereq", tbl_cell_bold), Paragraph("GET /api/m3/v1/partners/{id}/<br/>(Cek status partner)", tbl_cell_code), Paragraph("M4 memverifikasi bahwa status partner bernilai 'terverifikasi' sebelum memperbolehkan mitra menginput produk/jasa.", tbl_cell)],
        [Paragraph("Frontend Modul 3<br/>(Melda)", tbl_cell_bold), Paragraph("UI-Flow", tbl_cell_bold), Paragraph("POST /partners/ (multipart)<br/>GET /partners/{partner_id}/", tbl_cell_code), Paragraph("Mengirim form pendaftaran lengkap berkas KTP & selfie. Menampilkan status: kunci tombol back saat pending, render alasan saat ditolak, tombol login M1 saat terverifikasi.", tbl_cell)],
    ]
    t_who = Table(who_uses, colWidths=[80, 50, 160, 233])
    t_who.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_who)

    # ==========================================
    # HALAMAN 2: STANDAR AMPLOP & KATALOG RINGKAS ENDPOINT
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("4. Standar Amplop Respons (Response Envelope)", h1_style))
    story.append(Paragraph("Seluruh respons API Modul 3 selalu dibungkus dalam amplop JSON standar Panduan API Bersama:", body_style))

    story.append(Paragraph("<b>Respons Sukses (200 OK / 201 Created):</b>", body_style))
    resp_success_snippet = """{
  "success": true,
  "status": "success",
  "message": "Pendaftaran partner berhasil dikirim dan menunggu verifikasi.",
  "data": {
    "id": 1,
    "partner_id": "PRT-20261108-A9F2",
    "nama_usaha": "Toko Berkah Mandiri",
    "kategori_usaha": "Produk",
    "status": "pending",
    "penanggung_jawab_nik": "3201234567890001",
    "foto_ktp": "/media/partner_documents/ktp/ktp.png",
    "rejection_reason": null,
    "created_at": "2026-11-08T09:15:00+07:00"
  }
}"""
    story.append(Preformatted(resp_success_snippet, code_block))

    story.append(Paragraph("<b>Respons Galat (400 / 401 / 403 / 404 / 409 / 422):</b>", body_style))
    resp_err_snippet = """{
  "success": false,
  "status": "error",
  "message": "Isian tidak lolos validasi. Periksa kelengkapan data.",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Isian tidak lolos validasi. Periksa kelengkapan data.",
    "fields": {
      "penanggung_jawab_nik": "NIK penanggung jawab harus tepat 16 digit angka.",
      "foto_ktp": "Ukuran berkas foto KTP maksimal 5 MB."
    }
  },
  "errors": { ... }
}"""
    story.append(Preformatted(resp_err_snippet, code_block))

    story.append(Paragraph("• <b>Aturan Kode Galat</b>: Modul pemakai wajib memeriksa <code>error.code</code> (HURUF_BESAR_SNAKE_CASE), bukan teks message.", body_style))
    story.append(Paragraph("• <b>Data Kosong Bukan Galat</b>: Bila pencarian/katalog kosong, Modul 3 menjawab 200 OK dengan <code>\"data\": []</code> dan objek <code>meta</code> pagination.", body_style))

    story.append(Paragraph("5. Katalog Ringkas Endpoint Modul 3", h1_style))
    ep_catalog = [
        [Paragraph("Method", tbl_header), Paragraph("Endpoint (Base: /api/m3/v1)", tbl_header), Paragraph("Hak Akses", tbl_header), Paragraph("Kegunaan Utama", tbl_header)],
        [Paragraph("POST", tbl_cell_bold), Paragraph("/partners/", tbl_cell_code), Paragraph("Publik (Tanpa Token)", tbl_cell), Paragraph("Pendaftaran calon partner baru (M3-US1). Menerima multipart dokumen, NIK 16 digit, password kuat, auto-generate PRT.", tbl_cell)],
        [Paragraph("GET", tbl_cell_bold), Paragraph("/partners/{id}/", tbl_cell_code), Paragraph("Publik / Partner / Admin", tbl_cell), Paragraph("Detail & pelacakan status pendaftaran (M3-US3). Mendukung Dual Lookup via ID integer atau kode string PRT-YYYYMMDD-XXXX.", tbl_cell)],
        [Paragraph("GET", tbl_cell_bold), Paragraph("/partners/?status=terverifikasi", tbl_cell_code), Paragraph("Semua / Publik (K-06)", tbl_cell), Paragraph("Katalog partner terverifikasi untuk konsumsi Modul 5 dan Modul 4 dengan fitur pencarian (?q=) dan pagination.", tbl_cell)],
        [Paragraph("GET", tbl_cell_bold), Paragraph("/openapi.yaml", tbl_cell_code), Paragraph("Semua Tim", tbl_cell), Paragraph("Mengunduh spesifikasi OpenAPI 3.0.3 lengkap dalam format YAML.", tbl_cell)],
        [Paragraph("GET", tbl_cell_bold), Paragraph("/docs/", tbl_cell_code), Paragraph("Semua Tim", tbl_cell), Paragraph("Dokumentasi interaktif Swagger UI untuk eksplorasi dan uji coba API langsung melalui browser.", tbl_cell)],
    ]
    t_ep = Table(ep_catalog, colWidths=[40, 140, 110, 233])
    t_ep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_ep)

    # ==========================================
    # HALAMAN 3: ATURAN VALIDASI, SIKLUS STATUS & POSTMAN
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("6. Aturan Validasi Kritis & Siklus Status", h1_style))
    story.append(Paragraph("Sesuai standar audit dan keamanan data, Modul 3 menerapkan validasi ketat (Task T5.2 & T11):", body_style))

    val_rules = [
        [Paragraph("Parameter", tbl_header), Paragraph("Aturan Validasi", tbl_header), Paragraph("Respons Galat", tbl_header)],
        [Paragraph("NIK Penanggung Jawab", tbl_cell_bold), Paragraph("Wajib berupa 16 digit angka murni (regex ^\\d{16}$). Kurang, lebih, atau berhuruf ditolak.", tbl_cell), Paragraph("422 VALIDATION_ERROR: 'NIK penanggung jawab harus tepat 16 digit angka.'", tbl_cell)],
        [Paragraph("Foto KTP & Selfie KTP", tbl_cell_bold), Paragraph("Wajib format gambar JPG, JPEG, atau PNG. Ukuran berkas maksimal 5 MB (5,242,880 bytes).", tbl_cell), Paragraph("422 VALIDATION_ERROR: 'Format berkas foto KTP harus berupa gambar JPG atau PNG.' / 'Ukuran maksimal 5 MB.'", tbl_cell)],
        [Paragraph("Password Akun", tbl_cell_bold), Paragraph("Minimal 8 karakter dan wajib kombinasi huruf serta angka. Bersifat write-only dan di-hash aman.", tbl_cell), Paragraph("422 VALIDATION_ERROR: 'Password minimal 8 karakter dan mengandung kombinasi huruf serta angka.'", tbl_cell)],
        [Paragraph("Email Usaha", tbl_cell_bold), Paragraph("Format email valid dan belum pernah terdaftar sebelumnya di database.", tbl_cell), Paragraph("409 EMAIL_DUPLICATE: 'Email sudah terdaftar.' / 422 EMAIL_INVALID.", tbl_cell)],
    ]
    t_val = Table(val_rules, colWidths=[105, 205, 213])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_val)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Pemetaan Status & Perilaku Antarmuka (Task T11):", h1_style))
    status_flow = [
        [Paragraph("Status API", tbl_header), Paragraph("Label UI & Badge", tbl_header), Paragraph("Perilaku Logika & Tampilan Halaman Status", tbl_header)],
        [Paragraph("pending", tbl_cell_code), Paragraph("Menunggu Verifikasi (Kuning/Oranye)", tbl_cell), Paragraph("Pendaftaran baru berhasil dikirim. Pengguna menunggu verifikasi admin; tombol 'Kembali' ke formulir pendaftaran dinonaktifkan.", tbl_cell)],
        [Paragraph("terverifikasi", tbl_cell_code), Paragraph("Terverifikasi (Hijau)", tbl_cell), Paragraph("Admin menyetujui pendaftaran. Mitra otomatis masuk ke katalog K-06; tombol 'Masuk ke Akun Toko' mengarahkan mitra login ke Modul 1.", tbl_cell)],
        [Paragraph("ditolak", tbl_cell_code), Paragraph("Ditolak (Merah)", tbl_cell), Paragraph("Admin menolak pendaftaran. Pesan alasan penolakan (rejection_reason) ditampilkan persisten dan tombol 'Daftar Ulang' mengarahkan ke form perbaikan.", tbl_cell)],
        [Paragraph("ditangguhkan", tbl_cell_code), Paragraph("Ditangguhkan (Abu-abu)", tbl_cell), Paragraph("Akun dinonaktifkan sementara karena pelanggaran. Menampilkan nomor kontak bantuan admin.", tbl_cell)],
    ]
    t_status_flow = Table(status_flow, colWidths=[70, 140, 313])
    t_status_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_status_flow)
    story.append(Spacer(1, 6))

    story.append(Paragraph("7. Panduan Penggunaan Paket Folder Shared Ini", h1_style))
    story.append(Paragraph("Di dalam direktori <code>flow/docs/</code> telah disediakan berkas lengkap untuk mempercepat integrasi tim:", body_style))

    shared_files = [
        [Paragraph("Nama Berkas", tbl_header), Paragraph("Fungsi & Cara Penggunaan", tbl_header)],
        [Paragraph("01_Ringkasan_Integrasi_M3_README.pdf", tbl_cell_bold), Paragraph("Dokumen ini — panduan orientasi cepat (cheat sheet) bagi seluruh tim modul.", tbl_cell)],
        [Paragraph("02_API_Contract_Modul_3.pdf", tbl_cell_bold), Paragraph("Spesifikasi lengkap seluruh endpoint, parameter multipart, respons data, katalog kode galat, dan aturan kontrak.", tbl_cell)],
        [Paragraph("03_openapi_modul3.yaml", tbl_cell_bold), Paragraph("Kontrak mesin standar OpenAPI 3.0.3 YAML untuk code-generator atau import ke Postman/Insomnia.", tbl_cell)],
        [Paragraph("04_Matriks_Event_&_Hubungan_Antarmodul.pdf", tbl_cell_bold), Paragraph("Rincian matriks ketergantungan lintas modul (K-06, K-01, M2), payload event, diagram sequence, dan checklist integrasi.", tbl_cell)],
        [Paragraph("05_Postman_Collection_M3.json", tbl_cell_bold), Paragraph("Koleksi Postman siap pakai mencakup seluruh skenario pendaftaran sukses, dual lookup, validasi galat, dan katalog.", tbl_cell)],
    ]
    t_shared = Table(shared_files, colWidths=[170, 353])
    t_shared.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_shared)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Langkah Cepat Import & Uji Coba di Postman:", h1_style))
    story.append(Paragraph("1. Buka aplikasi <b>Postman</b> → klik tombol <b>Import</b> di kiri atas → pilih file <code>05_Postman_Collection_M3.json</code>.", body_style))
    story.append(Paragraph("2. Pada tab <b>Variables</b> koleksi, pastikan <code>base_url</code> mengarah ke <code>http://127.0.0.1:8000/api/m3/v1</code>.", body_style))
    story.append(Paragraph("3. Jalankan folder <b>01. Pendaftaran Calon Partner</b> untuk menguji registrasi (tersedia skenario sukses dan galat 422/409).", body_style))
    story.append(Paragraph("4. Jalankan folder <b>02. Pelacakan Status & Detail Partner</b> untuk menguji Dual Lookup via ID integer maupun string kode <code>PRT-...</code>.", body_style))
    story.append(Paragraph("5. Jalankan folder <b>03. Kontrak K-06</b> untuk memverifikasi daftar mitra terverifikasi yang dikonsumsi oleh Modul 5 dan Modul 4.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Ringkasan Integrasi Modul 3 berhasil dibuat: {pdf_path}")


if __name__ == "__main__":
    build_pdf()

