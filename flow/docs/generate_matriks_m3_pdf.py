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
        fontSize=9.5,
        leading=13,
        textColor=c_body,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14.5,
        textColor=c_primary,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=c_accent,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=10,
        textColor=c_dark,
        spaceAfter=3
    )

    tbl_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=9,
        textColor=colors.white
    )

    tbl_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.5,
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
        fontSize=6,
        leading=8,
        textColor=colors.HexColor("#0F172A")
    )

    code_block = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6,
        leading=8,
        textColor=colors.HexColor("#1E293B"),
        backColor=c_light,
        borderColor=c_border,
        borderWidth=0.5,
        borderPadding=3,
        spaceAfter=4
    )

    story = []

    # ==========================================
    # HALAMAN 1: MATRIKS KETERGANTUNGAN LINTAS MODUL
    # ==========================================
    story.append(Paragraph("Matriks Event & Hubungan Antar-Modul (Modul 3)", title_style))
    story.append(Paragraph("Araya Business Hub Platform — Modul 3: Manajemen Partner (Partner Management)", subtitle_style))

    meta_data = [
        [Paragraph("Versi Dokumen", tbl_cell_bold), Paragraph("v2.0 (draf) — Matriks Komunikasi & Event Lintas Modul", tbl_cell)],
        [Paragraph("Tanggal", tbl_cell_bold), Paragraph("8 November 2026", tbl_cell)],
        [Paragraph("Cakupan Kontrak", tbl_cell_bold), Paragraph("K-06 (M5 & M4), K-01 (M1), M2-Ref (M2 Unit Usaha), M4-Prereq (M4), & Event Pub/Sub", tbl_cell)],
        [Paragraph("Dokumen Induk", tbl_cell_bold), Paragraph("<code>02_API_Contract_Modul_3.pdf</code>, <code>docs/openapi.yaml</code>, & <code>05_Postman_Collection_M3.json</code>", tbl_cell)],
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
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Matriks Ketergantungan Lintas Modul", h1_style))
    story.append(Paragraph(
        "Sesuai arsitektur Panduan API Bersama v1.0, <b>dilarang keras mengakses tabel basis data modul lain secara langsung</b>. "
        "Seluruh pertukaran data dan notifikasi antar-modul dengan Modul 3 dilakukan secara terstandardisasi melalui REST API Sinkron atau Event HTTP Asinkron:",
        body_style
    ))

    matrix_dep = [
        [Paragraph("ID", tbl_header), Paragraph("Arah Modul", tbl_header), Paragraph("Pola Komunikasi", tbl_header), Paragraph("Endpoint / Event", tbl_header), Paragraph("Autentikasi", tbl_header), Paragraph("User Story Terkait", tbl_header)],
        [Paragraph("K-06", tbl_cell_bold), Paragraph("M3 → M5, M4<br/>(M3 Penyedia)", tbl_cell), Paragraph("REST Sinkron", tbl_cell), Paragraph("GET /api/m3/v1/partners/?status=terverifikasi<br/>(Katalog Toko Mitra Aktif)", tbl_cell_code), Paragraph("Publik / Bearer /<br/>X-Service-Key", tbl_cell), Paragraph("M3-US2, M5-US1, M4-US1", tbl_cell)],
        [Paragraph("K-01", tbl_cell_bold), Paragraph("M1 ↔ M3<br/>(Akun & Auth)", tbl_cell), Paragraph("Token JWT /<br/>REST Sinkron", tbl_cell), Paragraph("POST /api/m3/v1/partners/ (Kredensial Mitra)<br/>Token JWT klaim user_id & role", tbl_cell_code), Paragraph("Bearer &lt;token&gt; /<br/>Write-only Hash", tbl_cell), Paragraph("M1-US1, M3-US1", tbl_cell)],
        [Paragraph("M2-Ref", tbl_cell_bold), Paragraph("M2 → M3<br/>(Master Usaha)", tbl_cell), Paragraph("REST Sinkron", tbl_cell), Paragraph("unit_usaha_id<br/>(Referensi Master Kategori Unit Usaha)", tbl_cell_code), Paragraph("Header X-Service-Key /<br/>Internal ID", tbl_cell), Paragraph("M2-US1, M3-US1", tbl_cell)],
        [Paragraph("M4-Prereq", tbl_cell_bold), Paragraph("M4 → M3<br/>(Cek Status)", tbl_cell), Paragraph("REST Sinkron", tbl_cell), Paragraph("GET /api/m3/v1/partners/{id}/<br/>(Validasi kelayakan mitra jual produk)", tbl_cell_code), Paragraph("X-Service-Key /<br/>Bearer Admin", tbl_cell), Paragraph("M4-US1, M3-US3", tbl_cell)],
        [Paragraph("EVT-01", tbl_cell_bold), Paragraph("M3 → Broker/M4/M5<br/>(M3 Pengirim)", tbl_cell), Paragraph("Event HTTP<br/>Asinkron", tbl_cell), Paragraph("POST /api/events/ (Event: partner.verified)<br/>Notifikasi persetujuan pendaftaran mitra", tbl_cell_code), Paragraph("X-Service-Key<br/>(Kunci Modul M3)", tbl_cell), Paragraph("M3-US2, M4-US1, M5-US1", tbl_cell)],
        [Paragraph("EVT-02", tbl_cell_bold), Paragraph("M3 → Notifikasi<br/>(M3 Pengirim)", tbl_cell), Paragraph("Event HTTP<br/>Asinkron", tbl_cell), Paragraph("POST /api/events/ (Event: partner.registered)<br/>Notifikasi pengajuan baru ke antrean admin", tbl_cell_code), Paragraph("X-Service-Key<br/>(Kunci Modul M3)", tbl_cell), Paragraph("M3-US1", tbl_cell)],
    ]
    t_matrix_dep = Table(matrix_dep, colWidths=[40, 85, 70, 185, 75, 68])
    t_matrix_dep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_matrix_dep)
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Rincian Hubungan Masuk ke Modul 3 (Inbound Contracts)", h1_style))
    story.append(Paragraph("<b>2.1 Calon Mitra / Frontend → Modul 3: Pendaftaran Mandiri Mitra (M3-US1)</b>", h2_style))
    story.append(Paragraph("• <b>Penyedia</b>: Modul 3 (<code>POST /api/m3/v1/partners/</code>) | <b>Pemanggil</b>: Frontend Web Modul 3 (Melda) saat calon mitra submit berkas.", body_style))
    story.append(Paragraph("• <b>Proses Bisnis Internal</b>: (1) Validasi NIK wajib tepat 16 digit angka (422 bila gagal); (2) Validasi berkas Foto KTP & Selfie KTP format JPG/PNG dan ukuran &le; 5 MB; (3) Validasi password &ge; 8 karakter kombinasi huruf & angka; (4) Deteksi email duplikat (409 EMAIL_DUPLICATE); (5) Enkripsi password menggunakan <code>make_password()</code>; (6) Auto-generate kode publik <code>partner_id</code> (<code>PRT-YYYYMMDD-XXXX</code>); (7) Set status awal <code>pending</code>.", body_style))

    story.append(Paragraph("<b>2.2 Administrator → Modul 3: Verifikasi Legalitas & Keputusan Status (M3-US2)</b>", h2_style))
    story.append(Paragraph("• <b>Penyedia</b>: Modul 3 | <b>Pemanggil</b>: Dashboard Admin Modul 3 / Modul 2.", body_style))
    story.append(Paragraph("• <b>Proses Bisnis Internal</b>: Admin memeriksa keaslian KTP, kesesuaian NIK, dan selfie. Admin menetapkan status menjadi <code>terverifikasi</code> (memicu event <code>partner.verified</code>) atau <code>ditolak</code> dengan menyertakan alasan penolakan wajib. Setiap perubahan status dicatat ke tabel audit trail <code>partner_status_logs</code>.", body_style))

    # ==========================================
    # HALAMAN 2: OUTBOUND CONTRACTS & EVENT KELUAR
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("3. Rincian Hubungan Keluar dari Modul 3 (Outbound Contracts)", h1_style))
    story.append(Paragraph("<b>3.1 Modul 3 → Modul 5 (Katalog Publik): Etalase Toko Mitra Aktif (Kontrak K-06)</b>", h2_style))
    story.append(Paragraph("• <b>Penyedia</b>: Modul 3 (<code>GET /api/m3/v1/partners/?status=terverifikasi</code>) | <b>Pemakai</b>: Modul 5 (Website & Katalog Publik).", body_style))
    story.append(Paragraph("• <b>Aturan Bisnis</b>: Modul 5 hanya menampilkan toko partner yang statusnya <code>terverifikasi</code>. Modul 3 menyajikan parameter pagination (<code>page</code>, <code>per_page</code>) dan pencarian (<code>q</code>) agar etalase dapat memuat ribuan mitra secara ringan tanpa beban memori.", body_style))

    story.append(Paragraph("<b>3.2 Modul 3 → Modul 4 (Penjualan): Otorisasi Posting Produk Mitra (Kontrak K-06 / M4-Prereq)</b>", h2_style))
    story.append(Paragraph("• <b>Penyedia</b>: Modul 3 (<code>GET /api/m3/v1/partners/{id}/</code>) | <b>Pemakai</b>: Modul 4 saat mitra mengakses form tambah produk.", body_style))
    story.append(Paragraph("• <b>Aturan Bisnis</b>: Modul 4 memverifikasi bahwa status mitra bernilai <code>terverifikasi</code>. Jika status bernilai <code>pending</code>, <code>ditolak</code>, atau <code>ditangguhkan</code>, Modul 4 menolak pembuatan produk/jasa.", body_style))

    story.append(Paragraph("4. Rincian Event Keluar dari Modul 3 (Outbound Events)", h1_style))
    story.append(Paragraph("Ketika status partner berubah krusial, Modul 3 mempublikasikan event asinkron ke antarmodul via endpoint event broker:", body_style))
    story.append(Paragraph("POST /api/events/ | Header: X-Service-Key: &lt;kunci_modul_m3&gt;", code_block))

    story.append(Paragraph("<b>4.1 Event partner.verified (Partner Disetujui Admin)</b>", h2_style))
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

    story.append(Paragraph("<b>4.2 Event partner.registered (Pendaftaran Baru Masuk)</b>", h2_style))
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
    # HALAMAN 3: SPESIFIKASI EVENT AMPLOP & MATRIKS TRANSISI STATUS
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("4.3 Spesifikasi Field Amplop Event & Kebijakan Retry", h1_style))
    event_fields = [
        [Paragraph("Field Event", tbl_header), Paragraph("Tipe Data", tbl_header), Paragraph("Aturan & Kewajiban Modul Penerima (M4, M5, Event Broker)", tbl_header)],
        [Paragraph("event_id", tbl_cell_code), Paragraph("string (UUID v4)", tbl_cell), Paragraph("ID unik per kejadian. <b>Wajib Idempoten</b>: Jika modul penerima mendapati event_id yang telah diproses, wajib mengabaikannya dan tetap menjawab 200 OK.", tbl_cell)],
        [Paragraph("event_type", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Format objek.kejadian bentuk lampau: <code>partner.registered</code>, <code>partner.verified</code>, <code>partner.rejected</code>, <code>partner.suspended</code>.", tbl_cell)],
        [Paragraph("source_module", tbl_cell_code), Paragraph("string", tbl_cell), Paragraph("Selalu bernilai <code>\"M3\"</code> untuk seluruh event yang diterbitkan oleh Modul 3.", tbl_cell)],
        [Paragraph("occurred_at", tbl_cell_code), Paragraph("string (ISO 8601)", tbl_cell), Paragraph("Waktu riil kejadian di Modul 3 dalam zona WIB (<code>+07:00</code>), bukan timestamp saat retry pengiriman jaringan.", tbl_cell)],
        [Paragraph("recipient_role", tbl_cell_code), Paragraph("string | null", tbl_cell), Paragraph("Bernilai <code>null</code> untuk sinkronisasi antar-sistem, atau peran target seperti <code>\"administrator\"</code>.", tbl_cell)],
        [Paragraph("payload", tbl_cell_code), Paragraph("object", tbl_cell), Paragraph("Memuat data esensial partner (<code>id</code>, <code>partner_id</code>, <code>nama_usaha</code>, <code>status</code>) agar penerima dapat bekerja tanpa memanggil balik API M3.", tbl_cell)],
    ]
    t_ev_fields = Table(event_fields, colWidths=[80, 80, 363])
    t_ev_fields.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_ev_fields)
    story.append(Spacer(1, 4))

    story.append(Paragraph("5. Matriks Pemetaan Transisi Status & Dampak Lintas Modul", h1_style))
    status_impact = [
        [Paragraph("Peristiwa Pemicu", tbl_header), Paragraph("Status Partner M3", tbl_header), Paragraph("Efek ke Modul 1 (Auth)", tbl_header), Paragraph("Efek ke Modul 4 (Jual)", tbl_header), Paragraph("Efek ke Modul 5 (Katalog)", tbl_header)],
        [Paragraph("Calon Mitra Submit Registrasi (POST /partners/)", tbl_cell), Paragraph("pending", tbl_cell_code), Paragraph("Akun terdaftar, namun belum aktif (menunggu verifikasi).", tbl_cell), Paragraph("Dilarang posting produk/jasa.", tbl_cell), Paragraph("Belum muncul di katalog toko publik.", tbl_cell)],
        [Paragraph("Admin Verifikasi & Setujui (M3-US2)", tbl_cell), Paragraph("terverifikasi", tbl_cell_code), Paragraph("Akun diaktifkan, mitra dapat login via email & password.", tbl_cell), Paragraph("Otorisasi dibuka: mitra boleh input produk & jasa.", tbl_cell), Paragraph("Toko otomatis terdaftar di katalog publik K-06.", tbl_cell)],
        [Paragraph("Admin Menolak Berkas (M3-US2)", tbl_cell), Paragraph("ditolak", tbl_cell_code), Paragraph("Akun ditolak; kirimkan email alasan penolakan.", tbl_cell), Paragraph("Ditolak (tidak bisa transaksi).", tbl_cell), Paragraph("Tidak muncul di katalog toko publik.", tbl_cell)],
        [Paragraph("Admin Menangguhkan Akun (M3-US4)", tbl_cell), Paragraph("ditangguhkan", tbl_cell_code), Paragraph("Sesi login dibekukan; token JWT ditolak.", tbl_cell), Paragraph("Produk mitra di-freeze (tidak dapat dibeli).", tbl_cell), Paragraph("Toko disembunyikan sementara dari etalase K-06.", tbl_cell)],
        [Paragraph("Mitra Submit Ulang Setelah Ditolak", tbl_cell), Paragraph("pending", tbl_cell_code), Paragraph("Data akun diperbarui; kembali ke antrean verifikasi.", tbl_cell), Paragraph("Dilarang posting produk.", tbl_cell), Paragraph("Belum muncul di katalog publik.", tbl_cell)],
    ]
    t_impact = Table(status_impact, colWidths=[105, 65, 115, 120, 118])
    t_impact.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_impact)

    # ==========================================
    # HALAMAN 4: DIAGRAM ALUR END-TO-END & INTEGRATION CHECKLIST
    # ==========================================
    story.append(PageBreak())
    story.append(Paragraph("6. Diagram Alur Komunikasi End-to-End", h1_style))
    story.append(Paragraph("Diagram di bawah menggambarkan alur komunikasi lengkap dari pendaftaran mandiri calon partner, verifikasi admin, hingga pemanfaatan data oleh Modul 5 & Modul 4:", body_style))

    e2e_flow = """Calon Mitra          Frontend M3            Backend M3             Database M3           Admin M3        Modul 5 (Katalog)       Modul 4 (Sales)
    |                     |                      |                      |                    |                    |                      |
    |-- 1. Input Form --->|                      |                      |                    |                    |                      |
    |      KTP & Selfie   |-- 2. POST multipart->|                      |                    |                    |                      |
    |                     |      /partners/      |-- 3. Validasi NIK, ->|                    |                    |                      |
    |                     |                      |      file, password  |                    |                    |                      |
    |                     |                      |-- 4. Auto PRT Code ->|                    |                    |                      |
    |                     |                      |      Status: pending |                    |                    |                      |
    |                     |                      |-- 5. INSERT Partner->|                    |                    |                      |
    |                     |<- 6. 201 Created ----|                      |                    |                    |                      |
    |                     |      {partner_id}    |                      |                    |                    |                      |
    |                     |                      |                      |                    |                    |                      |
    |                     |-- 7. GET status ---->|-- 8. SELECT ---------|                    |                    |                      |
    |                     |      /partners/{PRT} |<- 9. status: pending-|                    |                    |                      |
    |                     |                      |                      |                    |                    |                      |
    |                     |                      |                      |<-- 10. Verifikasi -|                    |                      |
    |                     |                      |                      |    KTP & NIK       |                    |                      |
    |                     |                      |                      |-- 11. UPDATE ----->|                    |                      |
    |                     |                      |                      |    'terverifikasi' |                    |                      |
    |                     |                      |-- 12. Event Hub ---->|                    |                    |                      |
    |                     |                      |   'partner.verified' |---------------------------------------->|                      |
    |                     |                      |                      |                    |                    |                      |
    |                     |                      |<- 13. GET K-06 ------------------------------------------------|                      |
    |                     |                      |       /partners/?status=terverifikasi     |                    |                      |
    |                     |                      |-- 14. 200 OK { data: [mitra_aktif], meta } ------------------->|                      |
    |                     |                      |                      |                    |                    |                      |
    |                     |                      |<- 15. GET Cek Status Otorisasi Mitra -------------------------------------------------|
    |                     |                      |-- 16. 200 OK { status: 'terverifikasi' } -------------------------------------------->|
    |                     |                      |                      |                    |                    |   (Mitra boleh input |
    |                     |                      |                      |                    |                    |    produk di M4)     |"""
    story.append(Preformatted(e2e_flow, code_block))
    story.append(Spacer(1, 4))

    story.append(Paragraph("7. Daftar Periksa Kesiapan Integrasi Antar-Kelompok", h1_style))
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

