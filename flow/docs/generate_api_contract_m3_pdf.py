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
        footer_text = f"Kontrak API Modul 3 (v2.0 draf) | Halaman {self._pageNumber} dari {page_count}"
        self.drawString(36, 18, footer_text)
        self.drawRightString(559, 18, "Dokumen Acuan Resmi Lintas Modul")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 28, 559, 28)
        self.restoreState()


def build_pdf():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(output_dir, "02_API_Contract_Modul_3.pdf")

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
        fontSize=9,
        leading=12.5,
        textColor=c_body,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=c_primary,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_accent,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=9.5,
        textColor=c_dark,
        spaceAfter=2.5
    )

    tbl_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.3,
        leading=8.5,
        textColor=colors.white
    )

    tbl_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.2,
        leading=8.2,
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
        fontSize=5.8,
        leading=7.8,
        textColor=colors.HexColor("#0F172A")
    )

    code_block = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=5.6,
        leading=7.4,
        textColor=colors.HexColor("#1E293B"),
        backColor=c_light,
        borderColor=c_border,
        borderWidth=0.5,
        borderPadding=2.5,
        spaceAfter=3
    )

    story = []

    # ==========================================
    # HALAMAN 1: IDENTITAS & DAFTAR ISI KONTRAK
    # ==========================================
    story.append(Paragraph("Kontrak API & Event Antarmodul", title_style))
    story.append(Paragraph("Araya Business Hub Platform — Modul 3: Manajemen Partner (Partner Management)", subtitle_style))

    meta_data = [
        [Paragraph("Versi Dokumen", tbl_cell_bold), Paragraph("v2.0 (draf) — Revisi Sesuai Panduan API Bersama v1.0", tbl_cell)],
        [Paragraph("Tanggal Terbit", tbl_cell_bold), Paragraph("8 November 2026", tbl_cell)],
        [Paragraph("Penyusun", tbl_cell_bold), Paragraph("Tim Modul 3: Manajemen Partner & Onboarding Mitra", tbl_cell)],
        [Paragraph("Kelompok Terkait", tbl_cell_bold), Paragraph("Kel. A1 (User & Auth), Kel. A2 (Dashboard & Unit Usaha), Kel. A4 (Penjualan), Kel. A5 (Katalog Publik)", tbl_cell)],
        [Paragraph("Base URL", tbl_cell_bold), Paragraph("<code>http://127.0.0.1:8000/api/m3/v1/</code> (Lokal) | <code>https://[server-bersama]/api/m3/v1/</code> (Staging)", tbl_cell_code)],
        [Paragraph("OpenAPI Skema", tbl_cell_bold), Paragraph("<code>docs/openapi.yaml</code> & <code>flow/docs/03_openapi_modul3.yaml</code> | Swagger: <code>/api/m3/v1/docs/</code>", tbl_cell_code)],
    ]
    t_meta = Table(meta_data, colWidths=[110, 413])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Konvensi Umum & Ketentuan Arsitektur Bersama", h1_style))
    story.append(Paragraph(
        "Dokumen ini merupakan kontrak resmi API Modul 3 yang mengikat pengembang antarmuka internal (Frontend Melda), "
        "layanan backend, basis data (Akbar), pengujian QA, serta seluruh modul terintegrasi pada ekosistem Araya Business Hub "
        "(Modul 1 User/Auth, Modul 2 Dashboard/Unit Usaha, Modul 4 Penjualan/Produk, dan Modul 5 Katalog Publik). "
        "Seluruh implementasi wajib mematuhi aturan berikut:",
        body_style
    ))

    rules_data = [
        [Paragraph("Aspek", tbl_header), Paragraph("Aturan Standar Panduan API Bersama", tbl_header), Paragraph("Penerapan Khusus di Modul 3", tbl_header)],
        [Paragraph("Format Pertukaran Data", tbl_cell_bold), Paragraph("JSON untuk payload standar; Multipart untuk upload berkas dokumen.", tbl_cell), Paragraph("POST /partners/ mendukung multipart/form-data untuk upload foto KTP dan foto selfie KTP.", tbl_cell)],
        [Paragraph("Penamaan Kunci (Keys)", tbl_cell_bold), Paragraph("Wajib huruf kecil snake_case untuk seluruh field atribut JSON.", tbl_cell), Paragraph("Menggunakan nama baku: partner_id, unit_usaha_id, penanggung_jawab_nik, foto_ktp, dll.", tbl_cell)],
        [Paragraph("Format Waktu", tbl_cell_bold), Paragraph("ISO 8601 dengan offset WIB (+07:00), contoh YYYY-MM-DDTHH:mm:ss+07:00.", tbl_cell), Paragraph("created_at dan updated_at diserialisasi dalam zona waktu Jakarta (+07:00).", tbl_cell)],
        [Paragraph("Autentikasi Pengguna", tbl_cell_bold), Paragraph("Bearer token JWT dari Modul 1 (berlaku 8 jam).", tbl_cell), Paragraph("Header Authorization: Bearer <token_jwt_m1> untuk akses data profil mitra privat.", tbl_cell)],
        [Paragraph("Autentikasi Antarmodul", tbl_cell_bold), Paragraph("Kunci modul X-Service-Key untuk komunikasi server-to-server tanpa login.", tbl_cell), Paragraph("Header X-Service-Key: <kunci_modul_m3> untuk verifikasi antar-modul dan pengiriman event.", tbl_cell)],
        [Paragraph("Hak Akses Database", tbl_cell_bold), Paragraph("Dilarang keras mengakses tabel modul lain secara langsung via SQL query.", tbl_cell), Paragraph("Seluruh data dari/ke M1, M2, M4, dan M5 wajib melalui HTTP REST API atau Event Bus.", tbl_cell)],
    ]
    t_rules = Table(rules_data, colWidths=[100, 210, 213])
    t_rules.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_rules)

    # ==========================================
    # HALAMAN 2: DIAGRAM ANALISIS DFD LEVEL 0 & 1
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("2. Diagram Analisis Arsitektur & Aliran Data (Data Flow Diagram)", h1_style))
    story.append(Paragraph("<b>2.1 DFD Level 0 (Diagram Konteks Sistem Modul 3 Terhadap Entitas Luar)</b>", h2_style))
    dfd_0 = """+--------------------+          (Form Registrasi + KTP + Selfie)          +-----------------------+
|    CALON MITRA     | ==================================================> |                       |
| (Frontend Web M3)  | <================================================== |                       |
+--------------------+        (Kode PRT + Status Tracking Pendaftaran)     |                       |
                                                                           |                       |
+--------------------+            (Daftar Master Unit Usaha)               |                       |
|      MODUL 2       | --------------------------------------------------> |                       |
| (Master Unit Usaha)| <-------------------------------------------------- |                       |
+--------------------+         (Metrik Agregasi Partner per Kategori)      |                       |
                                                                           |        MODUL 3        |
+--------------------+            (Verifikasi Akun & Token JWT)            |  (MANAJEMEN PARTNER)  |
|      MODUL 1       | <=================================================> |                       |
| (User & Auth M1)   |         (Sync Kredensial Mitra saat Terverifikasi)  |                       |
+--------------------+                                                     |                       |
                                                                           |                       |
+--------------------+          (K-06: Verifikasi Status Hak Jual Mitra)   |                       |
|      MODUL 4       | <-------------------------------------------------- |                       |
| (Penjualan/Produk) | --------------------------------------------------> |                       |
+--------------------+            (Event Asinkron: partner.verified)       |                       |
                                                                           |                       |
+--------------------+        (K-06: Katalog Toko Mitra Terverifikasi)     |                       |
|      MODUL 5       | <-------------------------------------------------- |                       |
|  (Katalog Publik)  |            (Event Asinkron: partner.verified)       +-----------------------+
+--------------------+"""
    story.append(Preformatted(dfd_0, code_block))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>2.2 DFD Level 1 (Dekomposisi Proses Internal Modul 3)</b>", h2_style))
    dfd_1 = """[MODUL 2: Unit Usaha]           [CALON MITRA / FRONTEND M3]               [MODUL 1: User & Auth]
        |                                     |                                     |
   (GET Master Data)                 (Form Data & Berkas)                     (Validasi Token JWT)
        |                                     |                                     |
        v                                     v                                     v
+------------------+                 +------------------+                  +------------------+
| 1.0 FETCH MASTER |                 | 2.0 VALIDASI &   |                  | 4.0 SINKRONISASI |
|  UNIT USAHA (M2) |                 | PENDAFTARAN (M3) |                  |   AKUN MITRA M1  |
+------------------+                 +------------------+                  +------------------+
        |                                  |   |                                    ^
  (Dropdown Kategori)                      |   | (Simpan Partner & Akun)            | (Sync Kredensial)
        |                                  |   v                                    |
        +--------------------------------->| [D1: partners_partner]                 |
                                           | [D2: partner_documents]                |
                                           |                                        |
                                           v (Status: 'pending')                    |
                                     +------------------+                           |
[ADMINISTRATOR M3] =================>| 3.0 KEPUTUSAN    |---------------------------+
  (Review KTP, NIK & Selfie)         | VERIFIKASI ADMIN | (Ketika status 'terverifikasi')
                                     +------------------+
                                       |              |
                (Status: 'ditolak')    |              | (Status: 'terverifikasi')
                +----------------------+              +-----------------------------+
                |                                                                   |
                v                                                                   v
     [Catat Rejection Reason]                                            +--------------------+
     [Update Audit Log Trail]                                            | 5.0 PUBLIKASI DATA |
                |                                                        |   KATALOG (K-06)   |
                v                                                        +--------------------+
     [M3-US3: Status Ditampilkan]                                          |               |
     (Mitra Diizinkan Submit Ulang)                                        v               v
                                                                   [MODUL 5: Katalog] [MODUL 4: Penjualan]"""
    story.append(Preformatted(dfd_1, code_block))

    # ==========================================
    # HALAMAN 3: SIKLUS HIDUP STATUS & KONEKSI M1 & M2
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("3. Diagram Siklus Hidup Status Partner & Dampak Antarmodul", h1_style))
    story.append(Paragraph("Setiap transisi status pendaftaran partner di Modul 3 memiliki konsekuensi langsung pada hak akses antarmodul:", body_style))

    state_diag = """           +--------------------------------------------------------------+
           |                    CALON MITRA DAFTAR                        |
           |             (POST /api/m3/v1/partners/ multipart)            |
           +--------------------------------------------------------------+
                                          |
                                          v
                               +--------------------+
                               |   STATUS: PENDING  |
                               +--------------------+
                               | M1: Akun belum aktif
                               | M4: Dilarang posting produk
                               | M5: Belum tampil di etalase
                               +--------------------+
                                      /      \\
                      Admin Setuju   /        \\   Admin Tolak (rejection_reason)
                                    /          \\
                                   v            v
           +---------------------------+    +----------------------------+
           |   STATUS: TERVERIFIKASI   |    |       STATUS: DITOLAK      |
           +---------------------------+    +----------------------------+
           | M1: Akun aktif, login OK  |    | M1: Akun tidak aktif       |
           | M4: Boleh input produk    |    | M4: Dilarang transaksi     |
           | M5: Tampil di katalog     |    | M5: Tidak tampil di katalog|
           | EVT: partner.verified     |    | UI: Tampilkan alasan tolak |
           +---------------------------+    +----------------------------+
                     |         ^                           |
          Pelanggaran|         |Pulih                      | Mitra Perbaiki
          di Toko    |         |Sanksi                     | Dokumen
                     v         |                           v
           +---------------------------+             +-----------+
           |    STATUS: DITANGGUHKAN   |             | PERBAIKAN |
           +---------------------------+             | DOKUMEN   |
           | M1: Sesi login dibekukan  |             +-----------+
           | M4: Produk di-freeze      |                   |
           | M5: Toko di-hide          |                   +--------> (Kembali ke PENDING)
           +---------------------------+"""
    story.append(Preformatted(state_diag, code_block))
    story.append(Spacer(1, 3))

    story.append(Paragraph("4. Rincian Teknis Hubungan ke Modul 1 dan Modul 2", h1_style))
    story.append(Paragraph("<b>4.1 Koneksi ke Modul 1 (User, Akun, dan Autentikasi)</b>", h2_style))
    story.append(Paragraph(
        "Modul 1 memegang otoritas autentikasi pusat. Modul 3 berinteraksi dengan Modul 1 melalui 3 tahap teknis: "
        "(1) <b>Penerimaan Password</b>: Saat calon mitra mendaftar via <code>POST /api/m3/v1/partners/</code>, password di-hash secara aman menggunakan <code>make_password()</code> (PBKDF2 SHA-256) secara write-only; "
        "(2) <b>Sinkronisasi Akun saat Approval</b>: Saat admin menyetujui pendaftaran mitra di M3-US2, Modul 3 memanggil internal endpoint Modul 1 <code>POST /api/m1/v1/auth/register-partner</code> membawa <code>email_usaha</code>, <code>password_hash</code>, dan <code>partner_id</code> untuk mengaktifkan akun dan menerima <code>user_id</code>; "
        "(3) <b>Autentikasi Berbasis JWT</b>: Ketika mitra login melalui Modul 1, token JWT memuat payload <code>{ user_id, email, role: \"partner\", partner_id: \"PRT-...\" }</code>. Modul 3 memverifikasi token ini melalui header <code>Authorization: Bearer &lt;token&gt;</code> saat mitra mengakses endpoint privat toko.",
        body_style
    ))

    story.append(Paragraph("<b>4.2 Koneksi ke Modul 2 (Master Kategori Unit Usaha & Dashboard Agregasi)</b>", h2_style))
    story.append(Paragraph(
        "Modul 2 mengelola klasifikasi bisnis. Hubungan teknis dengan Modul 3: "
        "(1) <b>Inbound Dropdown Kategori Usaha</b>: Frontend/Backend Modul 3 memanggil <code>GET /api/m2/v1/unit-usaha/</code> untuk mempopulasikan pilihan kategori pada form pendaftaran mitra. Nilai yang dipilih disimpan di kolom <code>unit_usaha_id</code>. "
        "Bila service Modul 2 sedang luring, sistem Modul 3 menerapkan fallback aman ke kategori standar (<code>Produk</code> / <code>Jasa</code>); "
        "(2) <b>Outbound Dashboard Agregasi</b>: Dashboard Modul 2 memanggil Modul 3 via <code>GET /api/m3/v1/partners/?status=terverifikasi&unit_usaha_id={id}</code> untuk menampilkan jumlah dan sebaran mitra binaan aktif.",
        body_style
    ))

    # ==========================================
    # HALAMAN 4: ENDPOINT REGISTRASI MITRA (M3-US1)
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("5. Spesifikasi Detail Endpoint Modul 3", h1_style))
    story.append(Paragraph("<b>5.1 Pendaftaran Mandiri Calon Partner Baru (M3-US1 & T4.2 / T5.2)</b>", h2_style))
    story.append(Paragraph("Endpoint publik bagi pelaku usaha untuk mendaftarkan bisnis dan mengunggah dokumen identitas legalitas.", body_style))
    story.append(Paragraph("POST /api/m3/v1/partners/ | Content-Type: multipart/form-data | Autentikasi: Publik (Tanpa Token)", code_block))

    reg_params = [
        [Paragraph("Nama Field", tbl_header), Paragraph("Tipe", tbl_header), Paragraph("Wajib?", tbl_header), Paragraph("Aturan Validasi Ketat & Format", tbl_header)],
        [Paragraph("nama_usaha", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Nama merek/usaha partner. Maksimal 255 karakter.", tbl_cell)],
        [Paragraph("kategori_usaha", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Nilai: 'Produk' atau 'Jasa' (mengacu pada master unit usaha Modul 2).", tbl_cell)],
        [Paragraph("unit_usaha_id", tbl_cell_code), Paragraph("integer", tbl_cell), Paragraph("Opsional", tbl_cell), Paragraph("ID referensi unit usaha dari Modul 2 (misal: 1 = Pangan, 2 = Jasa).", tbl_cell)],
        [Paragraph("deskripsi", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Opsional", tbl_cell), Paragraph("Penjelasan profil atau deskripsi singkat produk/jasa yang ditawarkan.", tbl_cell)],
        [Paragraph("alamat_usaha", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Alamat operasional fisik/kantor usaha.", tbl_cell)],
        [Paragraph("email_usaha", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Email resmi usaha. Format email valid dan wajib unik di sistem.", tbl_cell)],
        [Paragraph("no_telepon", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Nomor telepon/WhatsApp aktif. 10-15 digit angka.", tbl_cell)],
        [Paragraph("penanggung_jawab_nama", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Nama lengkap penanggung jawab sesuai KTP.", tbl_cell)],
        [Paragraph("penanggung_jawab_nik", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Nomor Induk Kependudukan. Tepat 16 digit angka murni (regex ^\\d{16}$).", tbl_cell)],
        [Paragraph("foto_ktp", tbl_cell_code), Paragraph("file", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Unggahan foto KTP asli. Format: JPG, JPEG, PNG. Ukuran maksimal 5 MB.", tbl_cell)],
        [Paragraph("foto_memegang_ktp", tbl_cell_code), Paragraph("file", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Unggahan foto selfie memegang KTP. Format: JPG/PNG. Ukuran maks 5 MB.", tbl_cell)],
        [Paragraph("password", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Ya", tbl_cell_bold), Paragraph("Minimal 8 karakter, wajib kombinasi huruf dan angka. Write-only.", tbl_cell)],
    ]
    t_reg = Table(reg_params, colWidths=[105, 45, 45, 328])
    t_reg.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_reg)
    story.append(Spacer(1, 3))

    story.append(Paragraph("Contoh Respons Sukses (201 Created):", body_style))
    sample_reg_succ = """{
  "success": true,
  "status": "success",
  "message": "Pendaftaran partner berhasil dikirim dan menunggu verifikasi.",
  "data": {
    "id": 1,
    "partner_id": "PRT-20261108-A9F2",
    "unit_usaha_id": 1,
    "nama_usaha": "Toko Berkah Mandiri",
    "kategori_usaha": "Produk",
    "alamat_usaha": "Jl. Raya Araya No. 12, Malang",
    "email_usaha": "toko.berkah@example.com",
    "no_telepon": "081234567890",
    "status": "pending",
    "penanggung_jawab_nama": "Budi Santoso",
    "penanggung_jawab_nik": "3201234567890001",
    "foto_ktp": "/media/partner_documents/ktp/ktp.png",
    "foto_memegang_ktp": "/media/partner_documents/selfie/selfie.png",
    "rejection_reason": null,
    "created_at": "2026-11-08T09:15:00+07:00"
  }
}"""
    story.append(Preformatted(sample_reg_succ, code_block))

    # ==========================================
    # HALAMAN 5: STATUS & KATALOG K-06
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("5.2 Detail & Pelacakan Status Partner (M3-US3 & T10 / T11)", h1_style))
    story.append(Paragraph("Mendukung <b>Dual Lookup</b>: pemanggil dapat mencari berdasarkan ID numerik database (contoh: <code>1</code>) maupun string kode pendaftaran publik (contoh: <code>PRT-20261108-A9F2</code>).", body_style))
    story.append(Paragraph("GET /api/m3/v1/partners/{id}/ | Header: Opsional Bearer / X-Service-Key", code_block))

    story.append(Paragraph("Logika Respons Berdasarkan Status (Task T11):", body_style))
    story.append(Paragraph("• Jika status <code>pending</code>: <code>rejection_reason: null</code>. UI menampilkan lencana kuning 'Menunggu Verifikasi'. Tombol formulir terkunci.", body_style))
    story.append(Paragraph("• Jika status <code>terverifikasi</code>: <code>rejection_reason: null</code>. UI menampilkan lencana hijau 'Terverifikasi' dan tombol masuk akun Modul 1.", body_style))
    story.append(Paragraph("• Jika status <code>ditolak</code>: <code>rejection_reason</code> menyertakan alasan spesifik dari admin verifikator (M3-US2). UI menampilkan lencana merah dan tombol 'Daftar Ulang' untuk mengajukan perbaikan.", body_style))

    story.append(Paragraph("Contoh Respons Partner Ditolak (200 OK dengan rejection_reason):", body_style))
    sample_rej = """{
  "success": true,
  "status": "success",
  "message": "Data partner berhasil ditemukan",
  "data": {
    "id": 1,
    "partner_id": "PRT-20261108-A9F2",
    "nama_usaha": "Toko Berkah Mandiri",
    "status": "ditolak",
    "rejection_reason": "Foto KTP buram dan NIK tidak terbaca dengan jelas.",
    "created_at": "2026-11-08T09:15:00+07:00"
  }
}"""
    story.append(Preformatted(sample_rej, code_block))

    story.append(Paragraph("5.3 Katalog Partner Terverifikasi — Kontrak K-06 (M5 Katalog & M4 Penjualan)", h1_style))
    story.append(Paragraph("Endpoint resmi penyedia etalase mitra aktif untuk Modul 5 (Website Publik) dan validasi hak jual Modul 4. Dilengkapi pagination standar dan fitur filter pencarian.", body_style))
    story.append(Paragraph("GET /api/m3/v1/partners/?status=terverifikasi&page=1&per_page=10&q=berkah", code_block))

    story.append(Paragraph("Contoh Respons Katalog Lengkap dengan Objek Meta Pagination (200 OK):", body_style))
    sample_k06 = """{
  "success": true,
  "status": "success",
  "message": "Data partner berhasil ditemukan",
  "data": [
    {
      "id": 1,
      "partner_id": "PRT-20261108-A9F2",
      "unit_usaha_id": 1,
      "nama_usaha": "Toko Berkah Mandiri",
      "kategori_usaha": "Produk",
      "alamat_usaha": "Jl. Raya Araya No. 12, Malang",
      "email_usaha": "toko.berkah@example.com",
      "no_telepon": "081234567890",
      "status": "terverifikasi",
      "created_at": "2026-11-08T09:15:00+07:00"
    }
  ],
  "meta": {
    "page": 1,
    "per_page": 10,
    "total_data": 1,
    "total_pages": 1
  }
}"""
    story.append(Preformatted(sample_k06, code_block))

    # ==========================================
    # HALAMAN 6: KATALOG KODE GALAT & ROADMAP UNIFIKASI
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("6. Katalog Kode Galat Standar (Error Catalogue)", h1_style))
    story.append(Paragraph("Modul pemakai wajib melakukan parsing pada <code>error.code</code> (HURUF_BESAR_SNAKE_CASE) sesuai Panduan API Bersama:", body_style))

    err_catalog = [
        [Paragraph("HTTP Status", tbl_header), Paragraph("Kode Galat (error.code)", tbl_header), Paragraph("Kondisi Terjadinya Galat", tbl_header), Paragraph("Contoh Respons Message", tbl_header)],
        [Paragraph("400 Bad Request", tbl_cell_bold), Paragraph("BAD_REQUEST", tbl_cell_code), Paragraph("Payload JSON/Form tidak dapat diparsing atau format multipart rusak.", tbl_cell), Paragraph("Permintaan tidak dapat diproses. Periksa format data.", tbl_cell)],
        [Paragraph("401 Unauthorized", tbl_cell_bold), Paragraph("UNAUTHORIZED", tbl_cell_code), Paragraph("Header Authorization: Bearer tidak disertakan atau token kadaluarsa.", tbl_cell), Paragraph("Sesi tidak sah atau telah berakhir. Silakan login kembali.", tbl_cell)],
        [Paragraph("403 Forbidden", tbl_cell_bold), Paragraph("FORBIDDEN", tbl_cell_code), Paragraph("Pengguna tidak memiliki hak akses (role) terhadap sumber daya mitra.", tbl_cell), Paragraph("Anda tidak memiliki hak akses untuk tindakan ini.", tbl_cell)],
        [Paragraph("404 Not Found", tbl_cell_bold), Paragraph("NOT_FOUND", tbl_cell_code), Paragraph("ID partner numerik atau kode PRT tidak ditemukan di database Modul 3.", tbl_cell), Paragraph("Data partner tidak ditemukan.", tbl_cell)],
        [Paragraph("409 Conflict", tbl_cell_bold), Paragraph("EMAIL_DUPLICATE", tbl_cell_code), Paragraph("Email usaha yang didaftarkan sudah terdaftar pada partner lain.", tbl_cell), Paragraph("Email sudah terdaftar. Gunakan email lain atau login.", tbl_cell)],
        [Paragraph("422 Unprocessable", tbl_cell_bold), Paragraph("VALIDATION_ERROR", tbl_cell_code), Paragraph("Isian tidak lolos validasi ketat (NIK != 16 digit, file > 5 MB, password lemah).", tbl_cell), Paragraph("Isian tidak lolos validasi. Periksa rincian pada field error.", tbl_cell)],
        [Paragraph("500 Server Error", tbl_cell_bold), Paragraph("INTERNAL_SERVER_ERROR", tbl_cell_code), Paragraph("Gangguan internal server basis data atau kesalahan kode backend.", tbl_cell), Paragraph("Terjadi kesalahan pada server. Coba beberapa saat lagi.", tbl_cell)],
    ]
    t_err = Table(err_catalog, colWidths=[70, 115, 175, 163])
    t_err.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_err)
    story.append(Spacer(1, 3))

    story.append(Paragraph("7. Roadmap 7 Tahap Penyatuan Modul 3 dengan Modul 1, 2, 4, dan 5", h1_style))
    story.append(Paragraph("Tahapan resmi penyatuan sistem terintegrasi Araya Business Hub:", body_style))

    roadmap_stages = [
        [Paragraph("Tahap", tbl_header), Paragraph("Fokus Penyatuan", tbl_header), Paragraph("Langkah Kerja Teknis", tbl_header), Paragraph("Kriteria Selesai (DoD)", tbl_header)],
        [Paragraph("Tahap 1", tbl_cell_bold), Paragraph("Environment & Secrets", tbl_cell), Paragraph("Penyamaan konfigurasi .env: M1_BASE_URL, M2_BASE_URL, M4_BASE_URL, M5_BASE_URL, JWT_SECRET, X_SERVICE_KEY.", tbl_cell), Paragraph("Koneksi jaringan antar-service teruji via cURL.", tbl_cell)],
        [Paragraph("Tahap 2", tbl_cell_bold), Paragraph("Inbound Modul 2", tbl_cell), Paragraph("Binding dropdown form registrasi ke GET /api/m2/v1/unit-usaha/. Simpan unit_usaha_id dan sediakan graceful fallback.", tbl_cell), Paragraph("Dropdown kategori usaha dinamis dari database M2.", tbl_cell)],
        [Paragraph("Tahap 3", tbl_cell_bold), Paragraph("Inbound Modul 1", tbl_cell), Paragraph("Sinkronisasi akun saat persetujuan admin (M3-US2) via internal endpoint M1. Implementasi verifikasi Bearer JWT Token.", tbl_cell), Paragraph("Mitra yang disetujui dapat login di M1 dan dikenali M3.", tbl_cell)],
        [Paragraph("Tahap 4", tbl_cell_bold), Paragraph("Outbound Modul 4", tbl_cell), Paragraph("Penyediaan endpoint GET /api/m3/v1/partners/{id}/ untuk validasi status sebelum mitra memposting produk.", tbl_cell), Paragraph("M4 sukses menolak mitra pending/ditolak.", tbl_cell)],
        [Paragraph("Tahap 5", tbl_cell_bold), Paragraph("Outbound Modul 5", tbl_cell), Paragraph("Penyediaan endpoint Kontrak K-06 GET /api/m3/v1/partners/?status=terverifikasi lengkap pagination dan query q.", tbl_cell), Paragraph("Katalog toko publik M5 memuat mitra aktif secara dinamis.", tbl_cell)],
        [Paragraph("Tahap 6", tbl_cell_bold), Paragraph("Event Bus / PubSub", tbl_cell), Paragraph("Penerbitan event partner.registered dan partner.verified berformat amplop standar dan idempoten ke event broker.", tbl_cell), Paragraph("Event diproses sukses oleh Modul 4 dan Modul 5.", tbl_cell)],
        [Paragraph("Tahap 7", tbl_cell_bold), Paragraph("Joint Integration Test", tbl_cell), Paragraph("Eksekusi koleksi Postman bersama seluruh tim modul di lingkungan staging terintegrasi.", tbl_cell), Paragraph("100% skenario pengujian lintas modul lulus.", tbl_cell)],
    ]
    t_road = Table(roadmap_stages, colWidths=[40, 95, 250, 138])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_road)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Kontrak API Modul 3 berhasil diperbarui: {pdf_path}")


if __name__ == "__main__":
    build_pdf()

