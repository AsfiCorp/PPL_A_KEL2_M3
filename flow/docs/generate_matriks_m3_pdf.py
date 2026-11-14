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
        footer_text = f"Matriks Event & Hubungan Antar-Modul (Modul 3) | v2.0 (draf) | Halaman {self._pageNumber} dari {page_count}"
        self.drawString(36, 18, footer_text)
        self.drawRightString(559, 18, "Dokumen Acuan Resmi Lintas Modul")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 28, 559, 28)
        self.restoreState()


def build_pdf():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(output_dir, "04_Matriks_Event_&_Hubungan_Antarmodul.pdf")

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
    # HALAMAN 1: IDENTITAS & MATRIKS KETERGANTUNGAN
    # ==========================================
    story.append(Paragraph("Matriks Event & Hubungan Antar-Modul (Modul 3)", title_style))
    story.append(Paragraph("Araya Business Hub Platform — Modul 3: Manajemen Partner (Partner Management)", subtitle_style))

    meta_data = [
        [Paragraph("Versi Dokumen", tbl_cell_bold), Paragraph("v2.0 (draf) — Matriks Komunikasi & Event Lintas Modul Lengkap", tbl_cell)],
        [Paragraph("Tanggal", tbl_cell_bold), Paragraph("8 November 2026", tbl_cell)],
        [Paragraph("Cakupan Kontrak", tbl_cell_bold), Paragraph("K-06 (M5 & M4), K-01 (M1 Auth & Akun), M2-Ref (M2 Master Usaha), M4-Prereq (M4), & Event Pub/Sub", tbl_cell)],
        [Paragraph("Dokumen Terkait", tbl_cell_bold), Paragraph("<code>01_Ringkasan_Integrasi_M3_README.pdf</code>, <code>02_API_Contract_Modul_3.pdf</code>, <code>03_openapi_modul3.yaml</code>, & <code>05_Postman_Collection_M3.json</code>", tbl_cell)],
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
    story.append(Spacer(1, 3))

    story.append(Paragraph("1. Matriks Ketergantungan Lintas Modul", h1_style))
    story.append(Paragraph(
        "Sesuai arsitektur Panduan API Bersama v1.0, <b>dilarang keras mengakses tabel basis data modul lain secara langsung</b>. "
        "Seluruh pertukaran data, sinkronisasi akun, dan notifikasi antar-modul dengan Modul 3 dilakukan secara terstandardisasi melalui REST API Sinkron atau Event HTTP Asinkron:",
        body_style
    ))

    matrix_dep = [
        [Paragraph("ID", tbl_header), Paragraph("Arah Modul", tbl_header), Paragraph("Pola Komunikasi", tbl_header), Paragraph("Endpoint / Event", tbl_header), Paragraph("Autentikasi", tbl_header), Paragraph("User Story Terkait", tbl_header)],
        [Paragraph("K-06", tbl_cell_bold), Paragraph("M3 → M5, M4<br/>(M3 Penyedia)", tbl_cell), Paragraph("REST Sinkron", tbl_cell), Paragraph("GET /api/m3/v1/partners/?status=terverifikasi<br/>(Katalog Toko Mitra Aktif)", tbl_cell_code), Paragraph("Publik / Bearer /<br/>X-Service-Key", tbl_cell), Paragraph("M3-US2, M5-US1, M4-US1", tbl_cell)],
        [Paragraph("K-01", tbl_cell_bold), Paragraph("M1 ↔ M3<br/>(Akun & Auth)", tbl_cell), Paragraph("Token JWT /<br/>REST Sinkron", tbl_cell), Paragraph("POST /api/m3/v1/partners/ (Kredensial Mitra)<br/>Sinkronisasi registrasi akun & klaim JWT", tbl_cell_code), Paragraph("Bearer &lt;token&gt; /<br/>Write-only Hash", tbl_cell), Paragraph("M1-US1, M3-US1", tbl_cell)],
        [Paragraph("M2-Ref", tbl_cell_bold), Paragraph("M2 → M3<br/>(Master Usaha)", tbl_cell), Paragraph("REST Sinkron", tbl_cell), Paragraph("GET /api/m2/v1/unit-usaha/<br/>unit_usaha_id (Dropdown kategori usaha)", tbl_cell_code), Paragraph("Header X-Service-Key /<br/>Internal ID", tbl_cell), Paragraph("M2-US1, M3-US1", tbl_cell)],
        [Paragraph("M4-Prereq", tbl_cell_bold), Paragraph("M4 → M3<br/>(Cek Status)", tbl_cell), Paragraph("REST Sinkron", tbl_cell), Paragraph("GET /api/m3/v1/partners/{id}/<br/>(Validasi kelayakan mitra jual produk)", tbl_cell_code), Paragraph("X-Service-Key /<br/>Bearer Admin", tbl_cell), Paragraph("M4-US1, M3-US3", tbl_cell)],
        [Paragraph("EVT-01", tbl_cell_bold), Paragraph("M3 → Broker/M4/M5<br/>(M3 Pengirim)", tbl_cell), Paragraph("Event HTTP<br/>Asinkron", tbl_cell), Paragraph("POST /api/events/ (Event: partner.verified)<br/>Notifikasi persetujuan pendaftaran mitra", tbl_cell_code), Paragraph("X-Service-Key<br/>(Kunci Modul M3)", tbl_cell), Paragraph("M3-US2, M4-US1, M5-US1", tbl_cell)],
        [Paragraph("EVT-02", tbl_cell_bold), Paragraph("M3 → Notifikasi<br/>(M3 Pengirim)", tbl_cell), Paragraph("Event HTTP<br/>Asinkron", tbl_cell), Paragraph("POST /api/events/ (Event: partner.registered)<br/>Notifikasi pengajuan baru ke antrean admin", tbl_cell_code), Paragraph("X-Service-Key<br/>(Kunci Modul M3)", tbl_cell), Paragraph("M3-US1", tbl_cell)],
    ]
    t_matrix_dep = Table(matrix_dep, colWidths=[38, 85, 68, 188, 76, 68])
    t_matrix_dep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_matrix_dep)
    story.append(Spacer(1, 3))

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

    # ==========================================
    # HALAMAN 2: DFD LEVEL 1 & SIKLUS HIDUP STATUS
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("2.2 DFD Level 1 (Dekomposisi Proses Internal & Pertukaran Data Lintas Modul)", h1_style))
    story.append(Paragraph("Dekomposisi proses bisnis Modul 3 memperlihatkan batas tanggung jawab antara Modul 1, Modul 2, Modul 3, Modul 4, dan Modul 5:", body_style))

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
    story.append(Spacer(1, 3))

    story.append(Paragraph("3. Diagram Siklus Hidup Status Partner & Dampak Antarmodul", h1_style))
    story.append(Paragraph("Setiap transisi status pendaftaran partner di Modul 3 memiliki dampak langsung terhadap hak akses pada Modul 1, Modul 4, dan Modul 5:", body_style))

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

    # ==========================================
    # HALAMAN 3: RINCIAN KONEKSI MODUL 1 & MODUL 2
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("4. Rincian Teknis Hubungan ke Modul 1 dan Modul 2", h1_style))
    story.append(Paragraph("Bagian ini menjelaskan secara rinci dan mendalam kontrak interaksi teknis Modul 3 dengan Modul 1 (User & Auth) dan Modul 2 (Master Unit Usaha):", body_style))

    story.append(Paragraph("<b>4.1 Koneksi ke Modul 1 (User, Akun, dan Autentikasi)</b>", h2_style))
    story.append(Paragraph(
        "Modul 1 memegang otoritas autentikasi pusat pada ekosistem Araya Business Hub. Interaksi teknis antara Modul 3 dan Modul 1 mencakup tiga tahap integrasi:",
        body_style
    ))
    story.append(Paragraph("• <b>Tahap 1: Pengambilan Kredensial Saat Registrasi Mitra (M3-US1)</b>: Calon mitra mendaftarkan <code>email_usaha</code> dan <code>password</code> di formulir Modul 3. Backend Modul 3 memvalidasi ketat password (minimal 8 karakter kombinasi huruf dan angka), mengenkripsinya secara satu arah menggunakan <code>make_password()</code> (PBKDF2 SHA-256), dan menyimpannya secara <i>write-only</i>. Password plaintext tidak pernah dicatat di log atau dikembalikan pada respons JSON.", body_style))
    story.append(Paragraph("• <b>Tahap 2: Aktivasi & Sinkronisasi Akun saat Verifikasi Admin (M3-US2)</b>: Ketika admin menyetujui pendaftaran partner (status menjadi <code>terverifikasi</code>), Modul 3 menyinkronkan data akun ke Modul 1 via internal API: <code>POST /api/m1/v1/auth/register-partner</code> (membawa <code>email_usaha</code>, <code>password_hash</code>, <code>nama_usaha</code>, dan <code>partner_id</code>). Modul 1 mengembalikan <code>user_id</code> yang kemudian disimpan di tabel partner Modul 3.", body_style))
    story.append(Paragraph("• <b>Tahap 3: Autentikasi Berbasis Token JWT pada Akses Mitra</b>: Ketika mitra login melalui portal Modul 1 (<code>POST /api/m1/v1/auth/login</code>), Modul 1 menerbitkan JWT token yang memuat payload standar:", body_style))

    jwt_payload = """{
  "user_id": 42,
  "email": "toko.berkah@example.com",
  "role": "partner",
  "partner_id": "PRT-20261108-A9F2",
  "exp": 1794172800,
  "iss": "araya-modul-1-auth"
}"""
    story.append(Preformatted(jwt_payload, code_block))
    story.append(Paragraph("Ketika mitra mengakses endpoint internal Modul 3 (misalnya memperbarui profil usaha atau mengecek status privat), Modul 3 memverifikasi token pada header <code>Authorization: Bearer &lt;token&gt;</code> dan memastikan kecocokan <code>role: \"partner\"</code> serta <code>partner_id</code>.", body_style))

    story.append(Paragraph("<b>4.2 Koneksi ke Modul 2 (Master Kategori Unit Usaha & Dashboard Agregasi)</b>", h2_style))
    story.append(Paragraph(
        "Modul 2 mengelola klasifikasi bisnis dan hierarki unit usaha. Hubungan teknis dengan Modul 3 mencakup dua arah komunikasi:",
        body_style
    ))
    story.append(Paragraph("• <b>Arah Masuk (M2 → M3): Pengambilan Data Master Kategori Unit Usaha</b>: Saat formulir pendaftaran mitra dibuka, Frontend/Backend Modul 3 memanggil endpoint Modul 2: <code>GET /api/m2/v1/unit-usaha/</code> (dengan header <code>X-Service-Key</code> atau akses publik). Daftar unit usaha aktif (misal: ID 1: Produk Olahan Pangan, ID 2: Jasa Kreatif & Kerajinan) di-binding ke dropdown formulir pendaftaran.", body_style))
    story.append(Paragraph("• <b>Penyimpanan Foreign Key & Fallback Graceful</b>: Nilai yang dipilih calon mitra disimpan di Modul 3 pada kolom <code>unit_usaha_id</code> (integer). Jika service Modul 2 mengalami downtime atau belum siap pada lingkungan pengujian lokal, sistem Modul 3 menerapkan fallback aman ke pilihan teks standar (<code>Produk</code> atau <code>Jasa</code>) tanpa memblokir proses pendaftaran.", body_style))
    story.append(Paragraph("• <b>Arah Keluar (M3 → M2): Metrik Agregasi Partner untuk Dashboard Eksekutif M2</b>: Dashboard Modul 2 menampilkan ringkasan jumlah mitra UMKM binaan yang aktif. Modul 2 memanggil Modul 3: <code>GET /api/m3/v1/partners/?status=terverifikasi&unit_usaha_id={id}</code> untuk menampilkan jumlah dan sebaran mitra UMKM yang terverifikasi.", body_style))

    # ==========================================
    # HALAMAN 4: OUTBOUND CONTRACTS & EVENT PAYLOAD
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("5. Rincian Hubungan Keluar ke Modul 4 dan Modul 5", h1_style))
    story.append(Paragraph("<b>5.1 Modul 3 → Modul 5 (Katalog Publik): Etalase Toko Mitra Aktif (Kontrak K-06)</b>", h2_style))
    story.append(Paragraph("• <b>Penyedia</b>: Modul 3 (<code>GET /api/m3/v1/partners/?status=terverifikasi</code>) | <b>Pemakai</b>: Modul 5 (Website & Katalog Publik).", body_style))
    story.append(Paragraph("• <b>Aturan Bisnis</b>: Modul 5 hanya menampilkan toko partner yang statusnya <code>terverifikasi</code>. Modul 3 menyajikan parameter pagination (<code>page</code>, <code>per_page</code>) dan pencarian (<code>q</code>) agar etalase dapat memuat ribuan mitra secara ringan tanpa beban memori.", body_style))

    story.append(Paragraph("<b>5.2 Modul 3 → Modul 4 (Penjualan): Otorisasi Posting Produk Mitra (Kontrak K-06 / M4-Prereq)</b>", h2_style))
    story.append(Paragraph("• <b>Penyedia</b>: Modul 3 (<code>GET /api/m3/v1/partners/{id}/</code>) | <b>Pemakai</b>: Modul 4 saat mitra mengakses form tambah produk.", body_style))
    story.append(Paragraph("• <b>Aturan Bisnis</b>: Modul 4 memverifikasi bahwa status mitra bernilai <code>terverifikasi</code>. Jika status bernilai <code>pending</code>, <code>ditolak</code>, atau <code>ditangguhkan</code>, Modul 4 menolak pembuatan produk/jasa mitra.", body_style))

    story.append(Paragraph("6. Rincian Event Asinkron Keluar dari Modul 3 (Outbound Events)", h1_style))
    story.append(Paragraph("Ketika status partner berubah krusial, Modul 3 mempublikasikan event asinkron ke antarmodul via endpoint event broker:", body_style))
    story.append(Paragraph("POST /api/events/ | Header: X-Service-Key: &lt;kunci_modul_m3&gt;", code_block))

    story.append(Paragraph("<b>6.1 Event partner.verified (Partner Disetujui Admin)</b>", h2_style))
    story.append(Paragraph("• <b>Pemicu</b>: Admin menyetujui pendaftaran partner di M3-US2, status berubah dari <code>pending</code> menjadi <code>terverifikasi</code>.", body_style))
    event_verified = """{
  "event_id": "8f3a1b2c-4d5e-6f7a-8b9c-0d1e2f3a4b5c",
  "event_type": "partner.verified",
  "source_module": "M3",
  "occurred_at": "2026-11-08T10:30:00+07:00",
  "recipient_role": null,
  "payload": {
    "id": 1,
    "partner_id": "PRT-20261108-A9F2",
    "unit_usaha_id": 1,
    "nama_usaha": "Toko Berkah Sejahtera",
    "kategori_usaha": "Produk",
    "email_usaha": "toko.berkah@example.com",
    "status": "terverifikasi"
  }
}"""
    story.append(Preformatted(event_verified, code_block))
    story.append(Paragraph("• <b>Tindakan Modul Pemakai</b>: Modul 5 memperbarui cache etalase toko; Modul 4 membuka hak akses penginputan katalog produk/jasa bagi mitra tersebut.", body_style))

    story.append(Paragraph("<b>6.2 Event partner.registered (Pendaftaran Baru Masuk)</b>", h2_style))
    story.append(Paragraph("• <b>Pemicu</b>: Calon mitra berhasil melakukan submit formulir pendaftaran multipart di M3-US1.", body_style))
    event_registered = """{
  "event_id": "7e2a0b1c-3d4e-5f6a-7b8c-9d0e1f2a3b4c",
  "event_type": "partner.registered",
  "source_module": "M3",
  "occurred_at": "2026-11-08T09:15:00+07:00",
  "recipient_role": "administrator",
  "payload": {
    "id": 1,
    "partner_id": "PRT-20261108-A9F2",
    "nama_usaha": "Toko Berkah Sejahtera",
    "penanggung_jawab_nama": "Budi Santoso",
    "penanggung_jawab_nik": "3201234567890001",
    "email_usaha": "toko.berkah@example.com",
    "status": "pending"
  }
}"""
    story.append(Preformatted(event_registered, code_block))
    story.append(Paragraph("• <b>Tindakan Modul Pemakai</b>: Modul Notifikasi mengirimkan email tanda terima berkas pendaftaran ke calon mitra dan menaruh tiket ke antrean verifikasi admin.", body_style))

    # ==========================================
    # HALAMAN 5: ALUR SEQUENCE & ROADMAP PENYATUAN MODUL
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("7. Diagram Alur Komunikasi End-to-End (Sequence Flow)", h1_style))
    story.append(Paragraph("Diagram sequence di bawah mendemonstrasikan interaksi lengkap seluruh modul dari awal pendaftaran hingga konsumsi data publik:", body_style))

    e2e_flow = """Calon Mitra      Modul 2 (Master)    Modul 3 (Backend)    Admin (Review)     Modul 1 (Auth)     Modul 5 (Katalog)   Modul 4 (Sales)
    |                    |                    |                 |                  |                   |                  |
    |-- 1. Buka Form --->|                    |                 |                  |                   |                  |
    |   Registrasi       |<- 2. GET Unit Usaha|                 |                  |                   |                  |
    |                    |-- 3. Daftar Kategori                |                  |                   |                  |
    |-- 4. Submit Data & Berkas Foto -------->|                 |                  |                   |                  |
    |   (KTP, Selfie, Password, NIK)          |-- 5. Validasi & Hashing            |                   |                  |
    |                                         |-- 6. Generate PRT Code             |                   |                  |
    |<- 7. 201 Created {partner_id: PRT-...}-|-- 8. Event: partner.registered ---->| (Notifikasi)      |                  |
    |                                         |                 |                  |                   |                  |
    |-- 9. Pantau Status (GET PRT Code) ----->|                 |                  |                   |                  |
    |<- 10. 200 OK {status: 'pending'} -------|                 |                  |                   |                  |
    |                                         |                 |<-- 11. Review ---|                   |                  |
    |                                         |                 |    KTP & Selfie  |                   |                  |
    |                                         |<-- 12. Keputusan: 'terverifikasi' -|                   |                  |
    |                                         |-- 13. Sync Akun Mitra ------------>|                   |                  |
    |                                         |<- 14. 201 User Created (user_id)---|                   |                  |
    |                                         |-- 15. Event: partner.verified ------------------------>|                  |
    |                                         |                                                        |                  |
    |                                         |<- 16. GET /partners/?status=terverifikasi (K-06)-------|                  |
    |                                         |-- 17. 200 OK { data: [mitra_terverifikasi] } ---------->|                  |
    |                                         |                                                                           |
    |                                         |<- 18. GET /partners/{id}/ (Cek Status Hak Jual Mitra)---------------------|
    |                                         |-- 19. 200 OK { status: 'terverifikasi' } --------------------------------->|
    |                                         |                                                       (Mitra boleh input  |
    |                                         |                                                        produk di Modul 4) |"""
    story.append(Preformatted(e2e_flow, code_block))
    story.append(Spacer(1, 3))

    story.append(Paragraph("8. Roadmap & Panduan Langkah Penyatuan dengan Modul 1, 2, 4, dan 5", h1_style))
    story.append(Paragraph("Untuk menyatukan Modul 3 ke dalam platform bersama Araya Business Hub, tim wajib mengikuti 7 tahapan unifikasi teknis berikut:", body_style))

    roadmap_stages = [
        [Paragraph("Tahap", tbl_header), Paragraph("Fokus Penyatuan", tbl_header), Paragraph("Langkah Kerja Teknis & Konfigurasi", tbl_header), Paragraph("Kriteria Selesai (DoD)", tbl_header)],
        [Paragraph("Tahap 1", tbl_cell_bold), Paragraph("Environment & Secret Bersama", tbl_cell), Paragraph("Konfigurasi <code>.env</code> seragam: <code>M1_BASE_URL</code>, <code>M2_BASE_URL</code>, <code>M4_BASE_URL</code>, <code>M5_BASE_URL</code>, <code>JWT_SECRET</code>, dan <code>X_SERVICE_KEY</code>.", tbl_cell), Paragraph("Koneksi jaringan antar-service berhasil diuji via cURL.", tbl_cell)],
        [Paragraph("Tahap 2", tbl_cell_bold), Paragraph("Unifikasi Inbound Modul 2", tbl_cell), Paragraph("Binding dropdown form registrasi ke <code>GET /api/m2/v1/unit-usaha/</code>. Simpan <code>unit_usaha_id</code> dan pastikan fallback aman bila M2 offline.", tbl_cell), Paragraph("Data kategori di formulir pendaftaran dinamis dari database M2.", tbl_cell)],
        [Paragraph("Tahap 3", tbl_cell_bold), Paragraph("Unifikasi Inbound Modul 1", tbl_cell), Paragraph("Sinkronisasi akun saat approval (M3-US2) via internal endpoint M1. Implementasi middleware verifikasi Bearer JWT Token dari M1 pada endpoint mitra.", tbl_cell), Paragraph("Mitra yang disetujui dapat login di portal M1 dan token JWT dikenali M3.", tbl_cell)],
        [Paragraph("Tahap 4", tbl_cell_bold), Paragraph("Unifikasi Outbound Modul 4", tbl_cell), Paragraph("Penyediaan endpoint <code>GET /api/m3/v1/partners/{id}/</code> untuk validasi hak akses posting produk oleh Modul 4.", tbl_cell), Paragraph("Modul 4 sukses menolak mitra pending/ditolak dan mengizinkan mitra terverifikasi.", tbl_cell)],
        [Paragraph("Tahap 5", tbl_cell_bold), Paragraph("Unifikasi Outbound Modul 5", tbl_cell), Paragraph("Penyediaan endpoint Kontrak K-06 <code>GET /api/m3/v1/partners/?status=terverifikasi</code> dengan pagination dan search query <code>q</code>.", tbl_cell), Paragraph("Katalog toko publik Modul 5 menampilkan seluruh toko mitra aktif secara dinamis.", tbl_cell)],
        [Paragraph("Tahap 6", tbl_cell_bold), Paragraph("Unifikasi Event Bus / Webhook", tbl_cell), Paragraph("Pengiriman payload <code>partner.registered</code> dan <code>partner.verified</code> ke endpoint event broker pusat ber-header <code>X-Service-Key</code>.", tbl_cell), Paragraph("Event idempoten diterima dan diproses oleh Modul 5 dan Modul 4.", tbl_cell)],
        [Paragraph("Tahap 7", tbl_cell_bold), Paragraph("Pengujian Bersama (Joint Test)", tbl_cell), Paragraph("Menjalankan <code>05_Postman_Collection_M3.json</code> secara menyeluruh di lingkungan staging bersama dengan mock dan live service antarmodul.", tbl_cell), Paragraph("100% skenario pengujian lintas modul lulus tanpa regresi.", tbl_cell)],
    ]
    t_roadmap = Table(roadmap_stages, colWidths=[40, 85, 263, 136])
    t_roadmap.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_roadmap)

    # ==========================================
    # HALAMAN 6: CHECKLIST INTEGRASI LINTAS KELOMPOK
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("9. Daftar Periksa Kesiapan Integrasi Antar-Kelompok (Integration Checklist)", h1_style))
    checklist_inter = [
        [Paragraph("Pasangan Modul", tbl_header), Paragraph("Kontrak", tbl_header), Paragraph("Hal yang Wajib Diverifikasi Saat Integration Test", tbl_header), Paragraph("Skenario di Postman M3", tbl_header)],
        [Paragraph("M3 ↔ M1<br/>(User & Auth)", tbl_cell_bold), Paragraph("K-01", tbl_cell_bold), Paragraph("Password terenkripsi dengan make_password(), format email dinormalisasi lowercase, dan user_id terasosiasi dengan benar saat login.", tbl_cell), Paragraph("Folder 01 (Skenario 01.1 & 01.2)", tbl_cell)],
        [Paragraph("M3 ↔ M2<br/>(Master Usaha)", tbl_cell_bold), Paragraph("M2-Ref", tbl_cell_bold), Paragraph("unit_usaha_id tersimpan dan valid mengacu pada master unit usaha Modul 2. Bila Modul 2 belum aktif, fallback 'Produk' & 'Jasa' tetap berjalan aman.", tbl_cell), Paragraph("Folder 01 (Skenario 01.1 & 01.2)", tbl_cell)],
        [Paragraph("M3 ↔ M5<br/>(Katalog Web)", tbl_cell_bold), Paragraph("K-06", tbl_cell_bold), Paragraph("GET /api/m3/v1/partners/?status=terverifikasi mengembalikan daftar partner terverifikasi lengkap dengan struktur meta pagination dan respons filter pencarian.", tbl_cell), Paragraph("Folder 03. Kontrak K-06 (Skenario 03.1 & 03.2)", tbl_cell)],
        [Paragraph("M3 ↔ M4<br/>(Penjualan)", tbl_cell_bold), Paragraph("K-06 /<br/>M4-Prereq", tbl_cell_bold), Paragraph("GET /api/m3/v1/partners/{id}/ menjawab status akurat: menolak partner pending/ditolak untuk input produk, dan mengizinkan hanya saat terverifikasi.", tbl_cell), Paragraph("Folder 02. Pelacakan Status (Skenario 02.1 & 02.2)", tbl_cell)],
        [Paragraph("Frontend M3<br/>↔ Backend M3", tbl_cell_bold), Paragraph("UI-Flow", tbl_cell_bold), Paragraph("Multipart form berkas KTP & selfie KTP berhasil dikirim, validasi error 422 muncul spesifik di field, dan kode PRT tersimpan di session untuk halaman status.", tbl_cell), Paragraph("Folder 01 & Folder 02 (Seluruh skenario)", tbl_cell)],
    ]
    t_chk_inter = Table(checklist_inter, colWidths=[70, 45, 273, 135])
    t_chk_inter.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_chk_inter)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Matriks Event & Hubungan Antarmodul Modul 3 berhasil dibuat: {pdf_path}")


if __name__ == "__main__":
    build_pdf()

