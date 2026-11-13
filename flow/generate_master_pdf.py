import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Group

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
        
        # Header (halaman > 1)
        if self._pageNumber > 1:
            self.drawString(36, 814, "Araya Hub - Panduan Resmi Alur Sistem, Skema Basis Data & Roadmap Task Modul 3")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 808, 559, 808)

        # Footer
        footer_text = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(559, 18, footer_text)
        self.drawString(36, 18, "Dokumen Acuan Tunggal Tim Modul 3 - Capstone Project PPL Kelas A")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 28, 559, 28)
        self.restoreState()


def draw_ecosystem_diagram():
    # Width 523, Height 95
    d = Drawing(523, 95)
    d.add(Rect(0, 0, 523, 95, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#E2E8F0"), strokeWidth=1, rx=4, ry=4))
    d.add(String(12, 82, "DIAGRAM 1: ARSITEKTUR EKOSISTEM MULTI-MODUL (MODUL 1 - 5)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#1E3A8A")))

    # Modul 2
    d.add(Rect(12, 20, 85, 48, fillColor=colors.HexColor("#EFF6FF"), strokeColor=colors.HexColor("#3B82F6"), strokeWidth=1.1, rx=3, ry=3))
    d.add(String(18, 54, "MODUL 2", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#1D4ED8")))
    d.add(String(18, 43, "Master Unit Usaha", fontName="Helvetica-Bold", fontSize=6.2, fillColor=colors.HexColor("#1E293B")))
    d.add(String(18, 33, "Kategori: Produk/Jasa", fontName="Helvetica", fontSize=5.5, fillColor=colors.HexColor("#475569")))
    d.add(String(18, 24, "(Kontrak K-01)", fontName="Helvetica-Bold", fontSize=5.5, fillColor=colors.HexColor("#2563EB")))

    # Arrow M2 -> M3
    d.add(Line(97, 44, 122, 44, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Polygon([122, 44, 117, 46, 117, 42], fillColor=colors.HexColor("#64748B"), strokeColor=None))

    # Modul 3 (Core)
    d.add(Rect(124, 10, 115, 68, fillColor=colors.HexColor("#FEF3C7"), strokeColor=colors.HexColor("#D97706"), strokeWidth=1.3, rx=4, ry=4))
    d.add(String(132, 65, "MODUL 3 (KITA)", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor("#B45309")))
    d.add(String(132, 54, "Manajemen Partner", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor("#92400E")))
    d.add(String(132, 43, "• Pendaftaran Partner", fontName="Helvetica", fontSize=5.8, fillColor=colors.HexColor("#78350F")))
    d.add(String(132, 33, "• Verifikasi Superadmin", fontName="Helvetica", fontSize=5.8, fillColor=colors.HexColor("#78350F")))
    d.add(String(132, 23, "• Cek Status (Kode PRT)", fontName="Helvetica", fontSize=5.8, fillColor=colors.HexColor("#78350F")))
    d.add(String(132, 13, "• Penangguhan Toko", fontName="Helvetica", fontSize=5.8, fillColor=colors.HexColor("#78350F")))

    # Arrow M3 -> M1
    d.add(Line(181, 10, 181, 4, strokeColor=colors.HexColor("#64748B"), strokeWidth=1))
    d.add(Line(181, 4, 265, 4, strokeColor=colors.HexColor("#64748B"), strokeWidth=1))
    d.add(Polygon([265, 4, 260, 6, 260, 2], fillColor=colors.HexColor("#64748B"), strokeColor=None))

    # Modul 1
    d.add(Rect(267, 3, 105, 38, fillColor=colors.HexColor("#F0FDF4"), strokeColor=colors.HexColor("#16A34A"), strokeWidth=1.1, rx=3, ry=3))
    d.add(String(273, 29, "MODUL 1: Auth & Divisi", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor("#15803D")))
    d.add(String(273, 19, "Akun Admin Partner Terverifikasi", fontName="Helvetica", fontSize=5.5, fillColor=colors.HexColor("#166534")))
    d.add(String(273, 10, "Kelola Struktur Divisi Organisasi", fontName="Helvetica", fontSize=5.5, fillColor=colors.HexColor("#14532D")))

    # Arrow M3 -> M5
    d.add(Line(239, 52, 275, 52, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Polygon([275, 52, 270, 54, 270, 50], fillColor=colors.HexColor("#64748B"), strokeColor=None))
    d.add(String(244, 57, "K-06", fontName="Helvetica-Bold", fontSize=5.8, fillColor=colors.HexColor("#B45309")))

    # Modul 5
    d.add(Rect(277, 42, 110, 44, fillColor=colors.HexColor("#FDF2F8"), strokeColor=colors.HexColor("#DB2777"), strokeWidth=1.1, rx=3, ry=3))
    d.add(String(284, 73, "MODUL 5: Marketplace", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor("#BE185D")))
    d.add(String(284, 63, "Toko Partner Terverifikasi", fontName="Helvetica", fontSize=5.8, fillColor=colors.HexColor("#9D174D")))
    d.add(String(284, 52, "Guest Checkout (No Login)", fontName="Helvetica-Bold", fontSize=5.8, fillColor=colors.HexColor("#831843")))

    # Arrow M5 -> M4
    d.add(Line(387, 52, 417, 52, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Polygon([417, 52, 412, 54, 412, 50], fillColor=colors.HexColor("#64748B"), strokeColor=None))
    d.add(String(392, 57, "K-04", fontName="Helvetica-Bold", fontSize=5.8, fillColor=colors.HexColor("#BE185D")))

    # Modul 4
    d.add(Rect(419, 12, 92, 74, fillColor=colors.HexColor("#F5F3FF"), strokeColor=colors.HexColor("#7C3AED"), strokeWidth=1.1, rx=3, ry=3))
    d.add(String(425, 74, "MODUL 4", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#6D28D9")))
    d.add(String(425, 63, "Katalog & Order", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#5B21B6")))
    d.add(String(425, 52, "• Produk / Jasa Toko", fontName="Helvetica", fontSize=5.8, fillColor=colors.HexColor("#4C1D95")))
    d.add(String(425, 42, "• Invoice Publik", fontName="Helvetica", fontSize=5.8, fillColor=colors.HexColor("#4C1D95")))
    d.add(String(425, 32, "• Tracking Guest", fontName="Helvetica-Bold", fontSize=5.8, fillColor=colors.HexColor("#4338CA")))
    d.add(String(425, 22, "• Update: Diproses/OK", fontName="Helvetica-Oblique", fontSize=5.2, fillColor=colors.HexColor("#3730A3")))

    return d


def draw_stepper_and_state_diagram():
    # Width 523, Height 120
    d = Drawing(523, 120)
    d.add(Rect(0, 0, 523, 120, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=1, rx=4, ry=4))
    d.add(String(12, 107, "DIAGRAM 2: ALUR PENDAFTARAN RESMI & ATURAN NAVIGASI STATUS (M3-US1 & US3)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#1E3A8A")))

    # 1. Landing
    d.add(Rect(12, 65, 75, 34, fillColor=colors.HexColor("#F1F5F9"), strokeColor=colors.HexColor("#64748B"), strokeWidth=1, rx=3, ry=3))
    d.add(String(16, 87, "1. Landing Page", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#1E293B")))
    d.add(String(16, 78, "Info Kemitraan (UI-01)", fontName="Helvetica", fontSize=5.2, fillColor=colors.HexColor("#475569")))
    d.add(String(16, 69, "Tombol 'Daftar'", fontName="Helvetica-Bold", fontSize=5.2, fillColor=colors.HexColor("#2563EB")))

    d.add(Line(87, 82, 102, 82, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Polygon([102, 82, 98, 84, 98, 80], fillColor=colors.HexColor("#64748B"), strokeColor=None))

    # 2. Info Usaha
    d.add(Rect(104, 65, 90, 34, fillColor=colors.HexColor("#EFF6FF"), strokeColor=colors.HexColor("#3B82F6"), strokeWidth=1, rx=3, ry=3))
    d.add(String(108, 87, "2. Info Usaha", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#1D4ED8")))
    d.add(String(108, 78, "Unit Usaha API M2", fontName="Helvetica-Bold", fontSize=5.2, fillColor=colors.HexColor("#2563EB")))
    d.add(String(108, 69, "Nama, Alamat, Telp, Logo", fontName="Helvetica", fontSize=5.2, fillColor=colors.HexColor("#475569")))

    d.add(Line(194, 82, 209, 82, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Polygon([209, 82, 205, 84, 205, 80], fillColor=colors.HexColor("#64748B"), strokeColor=None))

    # 3. Dokumen
    d.add(Rect(211, 65, 98, 34, fillColor=colors.HexColor("#FEF3C7"), strokeColor=colors.HexColor("#F59E0B"), strokeWidth=1, rx=3, ry=3))
    d.add(String(215, 87, "3. Form Dokumen", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#B45309")))
    d.add(String(215, 78, "NIK & Foto KTP", fontName="Helvetica", fontSize=5.2, fillColor=colors.HexColor("#78350F")))
    d.add(String(215, 69, "Foto Memegang KTP", fontName="Helvetica-Bold", fontSize=5.2, fillColor=colors.HexColor("#D97706")))

    d.add(Line(309, 82, 324, 82, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Polygon([324, 82, 320, 84, 320, 80], fillColor=colors.HexColor("#64748B"), strokeColor=None))

    # 4. Akun
    d.add(Rect(326, 65, 88, 34, fillColor=colors.HexColor("#F0FDF4"), strokeColor=colors.HexColor("#16A34A"), strokeWidth=1, rx=3, ry=3))
    d.add(String(330, 87, "4. Akun Aplikasi", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#15803D")))
    d.add(String(330, 78, "Email Akun Partner", fontName="Helvetica", fontSize=5.2, fillColor=colors.HexColor("#166534")))
    d.add(String(330, 69, "Password (Untuk M1)", fontName="Helvetica-Bold", fontSize=5.2, fillColor=colors.HexColor("#166534")))

    d.add(Line(414, 82, 429, 82, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Polygon([429, 82, 425, 84, 425, 80], fillColor=colors.HexColor("#64748B"), strokeColor=None))

    # 5. Konfirmasi
    d.add(Rect(431, 65, 80, 34, fillColor=colors.HexColor("#F5F3FF"), strokeColor=colors.HexColor("#7C3AED"), strokeWidth=1, rx=3, ry=3))
    d.add(String(435, 87, "5. Konfirmasi", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#6D28D9")))
    d.add(String(435, 78, "Review & Submit", fontName="Helvetica", fontSize=5.2, fillColor=colors.HexColor("#5B21B6")))
    d.add(String(435, 69, "Kirim ke Modul 3", fontName="Helvetica-Bold", fontSize=5.2, fillColor=colors.HexColor("#7C3AED")))

    # Arrow down to Status
    d.add(Line(471, 65, 471, 52, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Line(471, 52, 260, 52, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Line(260, 52, 260, 44, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Polygon([260, 44, 258, 48, 262, 48], fillColor=colors.HexColor("#64748B"), strokeColor=None))

    # Box Status PENDING
    d.add(Rect(180, 5, 160, 36, fillColor=colors.HexColor("#FEF3C7"), strokeColor=colors.HexColor("#D97706"), strokeWidth=1.2, rx=3, ry=3))
    d.add(String(186, 30, "HALAMAN STATUS (PENDING)", fontName="Helvetica-Bold", fontSize=6.8, fillColor=colors.HexColor("#B45309")))
    d.add(String(186, 21, "Terbit Kode PRT-YYYYMMDD-XXXX", fontName="Helvetica-Bold", fontSize=5.8, fillColor=colors.HexColor("#92400E")))
    d.add(String(186, 12, "DIKUNCI: Tidak bisa kembali ke form", fontName="Helvetica-Bold", fontSize=5.5, fillColor=colors.HexColor("#DC2626")))

    # Accept branch (Left)
    d.add(Line(180, 23, 140, 23, strokeColor=colors.HexColor("#16A34A"), strokeWidth=1.2))
    d.add(Polygon([140, 23, 144, 25, 144, 21], fillColor=colors.HexColor("#16A34A"), strokeColor=None))
    d.add(Rect(15, 5, 123, 36, fillColor=colors.HexColor("#DCFCE7"), strokeColor=colors.HexColor("#16A34A"), strokeWidth=1.1, rx=3, ry=3))
    d.add(String(20, 30, "STATUS: TERVERIFIKASI (ACC)", fontName="Helvetica-Bold", fontSize=6.2, fillColor=colors.HexColor("#15803D")))
    d.add(String(20, 21, "Tombol 'Login ke Akun'", fontName="Helvetica-Bold", fontSize=5.8, fillColor=colors.HexColor("#166534")))
    d.add(String(20, 12, "Diarahkan ke Login Modul 1 (M1)", fontName="Helvetica", fontSize=5.2, fillColor=colors.HexColor("#14532D")))

    # Reject branch (Right)
    d.add(Line(340, 23, 380, 23, strokeColor=colors.HexColor("#DC2626"), strokeWidth=1.2))
    d.add(Polygon([380, 23, 376, 25, 376, 21], fillColor=colors.HexColor("#DC2626"), strokeColor=None))
    d.add(Rect(382, 5, 129, 36, fillColor=colors.HexColor("#FEE2E2"), strokeColor=colors.HexColor("#DC2626"), strokeWidth=1.1, rx=3, ry=3))
    d.add(String(387, 30, "STATUS: DITOLAK (REJECT)", fontName="Helvetica-Bold", fontSize=6.2, fillColor=colors.HexColor("#B91C1C")))
    d.add(String(387, 21, "Alasan Tolak TETAP ADA (Permanen)", fontName="Helvetica-Bold", fontSize=5.2, fillColor=colors.HexColor("#991B1B")))
    d.add(String(387, 12, "Tombol 'Coba Mendaftar Lagi' (Form)", fontName="Helvetica-Bold", fontSize=5.2, fillColor=colors.HexColor("#DC2626")))

    return d


def draw_erd_diagram_detailed():
    # Width 523, Height 230
    d = Drawing(523, 230)
    d.add(Rect(0, 0, 523, 230, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=1, rx=4, ry=4))
    d.add(String(12, 216, "DIAGRAM 3: SKEMA BASIS DATA UTAMA - SELURUH ATRIBUT LIST VERTIKAL (AKBAR)", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor("#1E3A8A")))

    # Table 1: partners (Left) - Height 195, Width 248
    d.add(Rect(14, 10, 248, 195, fillColor=colors.HexColor("#FFFFFF"), strokeColor=colors.HexColor("#DB2777"), strokeWidth=1.2, rx=4, ry=4))
    d.add(Rect(14, 186, 248, 19, fillColor=colors.HexColor("#FDF2F8"), strokeColor=colors.HexColor("#DB2777"), strokeWidth=1, rx=4, ry=4))
    d.add(String(20, 192, "partners (Tabel Entitas Partner)", fontName="Helvetica-Bold", fontSize=7.2, fillColor=colors.HexColor("#9D174D")))

    fields_partners = [
        "1.  id : bigint [PRIMARY KEY, AUTO_INCREMENT]",
        "2.  partner_id : varchar(30) [UNIQUE, INDEX, KODE PRT]",
        "3.  nama_usaha : varchar(255) [NOT NULL]",
        "4.  kategori_usaha : varchar(50) ['Produk' | 'Jasa']",
        "5.  unit_usaha_id : int [FK Logic -> Modul 2]",
        "6.  deskripsi_usaha : text [NOT NULL]",
        "7.  alamat_usaha : text [NOT NULL]",
        "8.  nomor_telepon_usaha : varchar(30) [NOT NULL]",
        "9.  email : varchar(255) [UNIQUE, NOT NULL]",
        "10. password_hash : text [NOT NULL, BCRYPT]",
        "11. profil_usaha : text / file_path [NULLABLE]",
        "12. penanggung_jawab_nama : varchar(255) [NOT NULL]",
        "13. penanggung_jawab_nik : varchar(16) [NOT NULL]",
        "14. tempat_lahir : varchar(100) [NOT NULL]",
        "15. tanggal_lahir : date [NOT NULL]",
        "16. foto_ktp : text / file_path [NOT NULL]",
        "17. foto_memegang_ktp : text / file_path [NOT NULL]",
        "18. status : varchar(20) [pending/terverifikasi/ditolak/ditangguhkan]",
        "19. alasan_penolakan : text [NULLABLE]",
        "20. alasan_penangguhan : text [NULLABLE]",
        "21. created_at : timestamp [AUTO_NOW_ADD]",
        "22. updated_at : timestamp [AUTO_NOW]"
    ]

    y_p = 175
    for f in fields_partners:
        is_key = "PRIMARY KEY" in f or "UNIQUE" in f
        f_font = "Helvetica-Bold" if is_key else "Helvetica"
        f_color = colors.HexColor("#0F172A") if is_key else colors.HexColor("#1E293B")
        d.add(String(18, y_p, f, fontName=f_font, fontSize=5.3, fillColor=f_color))
        y_p -= 7.8

    # Relation line
    d.add(Line(262, 107, 288, 107, strokeColor=colors.HexColor("#64748B"), strokeWidth=1.2))
    d.add(Polygon([288, 107, 283, 109, 283, 105], fillColor=colors.HexColor("#64748B"), strokeColor=None))
    d.add(String(266, 112, "1 : N", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#475569")))

    # Table 2: partner_status_logs (Right) - Height 195, Width 218
    d.add(Rect(290, 10, 218, 195, fillColor=colors.HexColor("#FFFFFF"), strokeColor=colors.HexColor("#7C3AED"), strokeWidth=1.2, rx=4, ry=4))
    d.add(Rect(290, 186, 218, 19, fillColor=colors.HexColor("#F5F3FF"), strokeColor=colors.HexColor("#7C3AED"), strokeWidth=1, rx=4, ry=4))
    d.add(String(296, 192, "partner_status_logs (Audit Trail)", fontName="Helvetica-Bold", fontSize=7.2, fillColor=colors.HexColor("#5B21B6")))

    fields_logs = [
        "1. id : bigint [PRIMARY KEY, AUTO_INCREMENT]",
        "2. partner_id : bigint [FK -> partners.id, CASCADE]",
        "3. admin_id : bigint [Superadmin Eksekutor]",
        "4. status_sebelum : varchar(20) [NOT NULL]",
        "5. status_sesudah : varchar(20) [NOT NULL]",
        "6. aksi : varchar(50) ['APPROVE','REJECT','SUSPEND','ACTIVATE']",
        "7. alasan : text [Wajib saat REJECT & SUSPEND]",
        "8. created_at : timestamp [AUTO_NOW_ADD]"
    ]

    y_l = 175
    for f in fields_logs:
        is_key = "PRIMARY KEY" in f or "FK" in f
        f_font = "Helvetica-Bold" if is_key else "Helvetica"
        f_color = colors.HexColor("#0F172A") if is_key else colors.HexColor("#1E293B")
        d.add(String(294, y_l, f, fontName=f_font, fontSize=5.3, fillColor=f_color))
        y_l -= 7.8

    # Note below log table
    d.add(Rect(295, 20, 208, 55, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E1"), strokeWidth=0.8, rx=3, ry=3))
    d.add(String(300, 62, "Catatan Integritas Basis Data (Akbar):", fontName="Helvetica-Bold", fontSize=5.5, fillColor=colors.HexColor("#1E3A8A")))
    d.add(String(300, 52, "• Tabel partners berdiri mandiri tanpa dependensi", fontName="Helvetica", fontSize=5.2, fillColor=colors.HexColor("#334155")))
    d.add(String(300, 43, "  eksternal blocker dari modul lain.", fontName="Helvetica", fontSize=5.2, fillColor=colors.HexColor("#334155")))
    d.add(String(300, 33, "• Setiap aksi perubahan status mencatat 1 baris", fontName="Helvetica", fontSize=5.2, fillColor=colors.HexColor("#334155")))
    d.add(String(300, 24, "  audit log permanen ke partner_status_logs.", fontName="Helvetica", fontSize=5.2, fillColor=colors.HexColor("#334155")))

    return d


def build_master_pdf(filename="flow/Panduan_Resmi_Alur_dan_Roadmap_Modul_3.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13.5,
        leading=17,
        textColor=colors.HexColor('#0F172A')
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=11,
        textColor=colors.HexColor('#475569')
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    sub_h2_style = ParagraphStyle(
        'SubHeader2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=9.5,
        textColor=colors.HexColor('#1E293B')
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=5.9,
        leading=7.8,
        textColor=colors.HexColor('#1E293B')
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=5.9,
        leading=7.8,
        textColor=colors.HexColor('#0F172A')
    )

    tbl_header = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=9,
        textColor=colors.white
    )

    story = []

    # Title Banner
    story.append(Paragraph("ARAYA HUB: PANDUAN RESMI ALUR SISTEM & ROADMAP TASK MODUL 3", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Dokumen Acuan Tunggal Resmi: Arsitektur Ekosistem B2B2C, Skema Basis Data Rinci, Integrasi API, dan Roadmap Task 5 Role Tim", subtitle_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1E3A8A"), spaceBefore=2, spaceAfter=4))

    # Identitas 5 Role Tim
    team_data = [
        [Paragraph("Role Tim", tbl_header), Paragraph("Penanggung Jawab", tbl_header), Paragraph("Fokus Deliverable Utama", tbl_header)],
        [Paragraph("<b>Analis & Desain</b>", tbl_cell_bold), Paragraph("<b>Milda</b>", tbl_cell_bold), Paragraph("Use Case, Wireframe, Prototipe Figma (Landing Page, Stepper Form, Status, Dashboard Admin)", tbl_cell)],
        [Paragraph("<b>Frontend Developer</b>", tbl_cell_bold), Paragraph("<b>Melda</b>", tbl_cell_bold), Paragraph("Slicing UI HTML/CSS, Integrasi Form Stepper, Kunci Navigasi Status, Redirect Login Modul 1", tbl_cell)],
        [Paragraph("<b>Backend Developer</b>", tbl_cell_bold), Paragraph("<b>Moch Hary</b>", tbl_cell_bold), Paragraph("RESTful API, Validasi Serializer, Hashing Akun, Integrasi Lintas Modul, CI/CD Actions", tbl_cell)],
        [Paragraph("<b>QA / Acceptance Tester</b>", tbl_cell_bold), Paragraph("<b>Atha</b>", tbl_cell_bold), Paragraph("Test Cases, Automated Tests DRF, Pengujian Navigasi, Verifikasi Kepatuhan Respon", tbl_cell)],
        [Paragraph("<b>Database Specialist</b>", tbl_cell_bold), Paragraph("<b>Akbar</b>", tbl_cell_bold), Paragraph("Skema Tabel `partners` (22 Kolom) & `partner_status_logs`, Indexing `partner_id`, Fixtures", tbl_cell)]
    ]
    t_team = Table(team_data, colWidths=[110, 95, 318])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.8),
    ]))
    story.append(t_team)
    story.append(Spacer(1, 5))

    # SECTION 1: ARSITEKTUR & PENJELASAN PRT
    story.append(Paragraph("1. Arsitektur Ekosistem B2B2C & Arti Kode 'PRT'", h1_style))
    story.append(Paragraph(
        "• <b>Organisasi = Partner</b>: Pelaku usaha B2B penjual produk atau jasa. Modul 3 adalah gerbang legalitas platform.<br/>"
        "• <b>Customer = Guest</b>: Pelanggan akhir berbelanja di Modul 5 tanpa kewajiban login/register di Modul 1. Data identitas dasar ditangkap saat checkout dan dicatat di Modul 4. Pelacakan pesanan menggunakan nomor invoice publik.<br/>"
        "• <b>Aturan Kategori Usaha</b>: Satu partner <b>strictly hanya boleh bernilai 'Produk' ATAU 'Jasa'</b> (mutually exclusive) dan semuanya dijual online.<br/>"
        "• <b>Arti Kode 'PRT'</b>: Singkatan dari <b>Partner</b> (atau <i>Partner Registration Ticket</i>). Kode string acak unik berbasis tanggal (format: <code>PRT-YYYYMMDD-XXXX</code>) yang diterbitkan otomatis saat submit pendaftaran sebagai nomor pelacakan publik tanpa mengekspos ID auto-increment basis data.",
        body_style
    ))
    story.append(Spacer(1, 3))
    story.append(draw_ecosystem_diagram())
    story.append(Spacer(1, 4))

    # SECTION 2: ALUR RESMI PENDAFTARAN & ATURAN NAVIGASI
    story.append(Paragraph("2. Alur Resmi Pendaftaran Partner & Aturan Navigasi State (Milda & Melda)", h1_style))
    story.append(Paragraph(
        "Alur pendaftaran partner berlangsung secara berurutan melalui tahapan UI:<br/>"
        "1. <b>Landing Page Partner (UI-01)</b>: Halaman portal informasi awal kemitraan dengan tombol 'Daftar Sekarang'.<br/>"
        "2. <b>Form Info Usaha</b>: Mengisi identitas usaha, memilih unit usaha dari API Modul 2 (<code>GET /api/m2/v1/business-units</code>).<br/>"
        "3. <b>Form Dokumen (NPWP Dihapus)</b>: Mengisi NIK (16 digit), <b>Upload Foto KTP</b>, dan <b>Upload Foto Orang Memegang KTP (Selfie KTP)</b>.<br/>"
        "4. <b>Form Akun Aplikasi</b>: Input <b>Email dan Password Akun</b> yang dipersiapkan untuk login ke Modul 1 setelah di-approve.<br/>"
        "5. <b>Halaman Konfirmasi</b>: Meninjau seluruh ringkasan data sebelum submit multipart ke backend Modul 3.<br/>"
        "<b>Aturan Navigasi Halaman Status (Wajib Dipatuhi Milda & Melda)</b>:<br/>"
        "• <b>Saat Status Pending (Menunggu Verifikasi)</b>: Halaman <b>DIKUNCI</b>. Pendaftar tidak bisa kembali ke formulir sebelumnya untuk mencegah duplikasi data.<br/>"
        "• <b>Saat Status Terverifikasi (Accepted)</b>: Menampilkan ucapan selamat dan tombol aksi <b>'Login ke Akun'</b> yang langsung mengarahkan ke Halaman Login Modul 1.<br/>"
        "• <b>Saat Status Ditolak (Rejected)</b>: Menampilkan keterangan penolakan dan <b>Alasan Penolakan</b>, serta tombol <b>'Coba Mendaftar Lagi'</b> (kembali ke formulir awal). "
        "<b>Pesan penolakan dan alasannya TETAP ADA dan TIDAK BOLEH HILANG</b> kecuali jika pengajuan ulang tersebut nantinya sudah disetujui (di-acc).",
        body_style
    ))
    story.append(Spacer(1, 3))
    story.append(draw_stepper_and_state_diagram())
    story.append(Spacer(1, 6))

    # Page Break to Page 2 for Schema & API
    story.append(PageBreak())

    # SECTION 3: SKEMA BASIS DATA & PEMETAAN API
    story.append(Paragraph("3. Skema Basis Data Rinci (Akbar) & Pemetaan Integrasi API", h1_style))
    story.append(Paragraph(
        "Sesuai arahan teknis, seluruh kolom dan atribut model basis data di bawah ini diurutkan <b>satu per satu secara vertikal</b> tanpa dirangkum ke dalam satu baris guna menjamin kejelasan tipe data dan batas constraint:",
        body_style
    ))
    story.append(Spacer(1, 3))
    story.append(draw_erd_diagram_detailed())
    story.append(Spacer(1, 5))

    api_matrix = [
        [Paragraph("Langkah UI", tbl_header), Paragraph("Aksi Integrasi", tbl_header), Paragraph("Endpoint & Kontrak", tbl_header), Paragraph("Instruksi Frontend (Melda)", tbl_header)],
        [
            Paragraph("<b>Step 1: Info Usaha</b>", tbl_cell_bold),
            Paragraph("Tarik Unit Usaha dari <b>Modul 2</b>", tbl_cell),
            Paragraph("<code>GET /api/m2/v1/business-units</code><br/>(Kontrak K-01)", tbl_cell),
            Paragraph("Render opsi ke dropdown. Jika Modul 2 belum aktif, gunakan data fallback 'Produk' & 'Jasa'.", tbl_cell)
        ],
        [
            Paragraph("<b>Step 2-4: Submit</b>", tbl_cell_bold),
            Paragraph("Kirim Form & Berkas ke <b>Modul 3</b>", tbl_cell),
            Paragraph("<code>POST /api/m3/v1/partners/</code><br/>Content-Type: multipart/form-data", tbl_cell),
            Paragraph("Kirim data usaha, NIK, Foto KTP, Foto Selfie Pegang KTP, Email, Password. Tangkap kode <code>partner_id</code>.", tbl_cell)
        ],
        [
            Paragraph("<b>Halaman Status</b>", tbl_cell_bold),
            Paragraph("Cek Status ke <b>Modul 3</b>", tbl_cell),
            Paragraph("<code>GET /api/m3/v1/partners/{partner_id}/</code>", tbl_cell),
            Paragraph("Jika Pending: Kunci back.<br/>Jika Ditolak: Render alasan tolak permanen + tombol Daftar Ulang.<br/>Jika Terverifikasi: Tampilkan tombol Login M1.", tbl_cell)
        ],
        [
            Paragraph("<b>Login Mitra</b>", tbl_cell_bold),
            Paragraph("Redirect Pengguna ke <b>Modul 1</b>", tbl_cell),
            Paragraph("URL Halaman Login M1 (<code>/login</code>)", tbl_cell),
            Paragraph("Partner masuk menggunakan Email dan Password yang telah diinput pada formulir pendaftaran.", tbl_cell)
        ]
    ]
    t_api = Table(api_matrix, colWidths=[85, 120, 140, 178])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F766E')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0FDFA')]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.8),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 6))

    # Page Break to Page 3 for Sprint 1 Tasks (US1)
    story.append(PageBreak())

    # SECTION 4: DAFTAR LENGKAP TASK SPRINT 1 (US1 & US3)
    story.append(Paragraph("4. Daftar Lengkap Task Sprint 1 (M3-US1 & M3-US3 — 26 Task)", h1_style))
    story.append(Paragraph("4.1 User Story M3-US1: Pendaftaran Calon Partner Mandiri (18 Sub-Issues / Tasks)", sub_h2_style))

    sprint1_us1_tasks = [
        [Paragraph("Kode & Role", tbl_header), Paragraph("Judul Task Linear", tbl_header), Paragraph("Deskripsi & Kriteria Selesai (DoD)", tbl_header)],
        
        # Desain (Milda)
        [
            Paragraph("<b>T1</b><br/><font color='#DB2777'>Desain (Milda)</font>", tbl_cell_bold),
            Paragraph("Membuat Use Case", tbl_cell_bold),
            Paragraph("Merancang diagram use case pendaftaran calon partner mandiri (M3-US1), mengidentifikasi aktor calon partner, prekondisi, alur utama pendaftaran, serta skenario alternatif.", tbl_cell)
        ],
        [
            Paragraph("<b>T2</b><br/><font color='#DB2777'>Desain (Milda)</font>", tbl_cell_bold),
            Paragraph("Desain prototipe Figma Form Pendaftaran Partner", tbl_cell_bold),
            Paragraph("Merancang antarmuka awal formulir pendaftaran calon partner mandiri pada Figma dengan komponen input identitas usaha, informasi penanggung jawab, dan tata letak responsif.", tbl_cell)
        ],
        [
            Paragraph("<b>T2.1</b><br/><font color='#DB2777'>Desain (Milda)</font>", tbl_cell_bold),
            Paragraph("Revisi Figma: Foto KTP, Selfie Pegang KTP, dan Tambah Step Baru (data akun aplikasi)", tbl_cell_bold),
            Paragraph("Menghapus seluruh elemen NPWP dari Figma. Menambahkan komponen unggah berkas Foto KTP dan Foto Selfie Pegang KTP. Menambahkan tahapan (step) baru untuk input Akun Aplikasi (Email & Password).", tbl_cell)
        ],

        # Database (Akbar)
        [
            Paragraph("<b>T3</b><br/><font color='#D97706'>Database (Akbar)</font>", tbl_cell_bold),
            Paragraph("Perancangan skema tabel database partners & migrasi", tbl_cell_bold),
            Paragraph("Merancang skema relasional tabel database `partners` di PostgreSQL/SQLite, menentukan tipe data kolom awal, dan mengeksekusi file migrasi awal Django.", tbl_cell)
        ],
        [
            Paragraph("<b>T3.1</b><br/><font color='#D97706'>Database (Akbar)</font>", tbl_cell_bold),
            Paragraph("Pembaruan Skema Tabel partners (Hapus properti NPWP) (Tambah Foto KTP, Foto Selfie Pegang KTP, NIK, Password)", tbl_cell_bold),
            Paragraph("Migrasi pembaruan tabel `partners`: drop kolom npwp, tambah `foto_ktp`, `foto_memegang_ktp`, `nik` (16 digit), `tempat_lahir`, `tanggal_lahir`, `penanggung_jawab_nama`, `password_hash`, serta `partner_id` terindeks unik.", tbl_cell)
        ],
        [
            Paragraph("<b>T3.2</b><br/><font color='#D97706'>Database (Akbar)</font>", tbl_cell_bold),
            Paragraph("Pembuatan Skema Tabel Audit Log partner_status_logs & Migrasi", tbl_cell_bold),
            Paragraph("Membuat model Django `PartnerStatusLog` (kolom: `id`, `partner_id` FK, `admin_id`, `status_sebelum`, `status_sesudah`, `aksi`, `alasan`, `created_at`) dan mengeksekusi file migrasi Django.", tbl_cell)
        ],

        # Backend (Hari)
        [
            Paragraph("<b>T4</b><br/><font color='#2563EB'>Backend (Hari)</font>", tbl_cell_bold),
            Paragraph("Pembuatan API Endpoint POST pendaftaran partner", tbl_cell_bold),
            Paragraph("Membangun endpoint API dasar `POST /api/m3/v1/partners/` menggunakan Django REST Framework untuk menerima data registrasi calon partner.", tbl_cell)
        ],
        [
            Paragraph("<b>T4.1</b><br/><font color='#2563EB'>Backend (Hari)</font>", tbl_cell_bold),
            Paragraph("Penyesuaian API dengan dokumen bersama API", tbl_cell_bold),
            Paragraph("Menyelaraskan struktur request/response body endpoint registrasi, penamaan key snake_case, format JSON, dan status code sesuai dokumen kontrak bersama antarmodul.", tbl_cell)
        ],
        [
            Paragraph("<b>T4.2</b><br/><font color='#2563EB'>Backend (Hari)</font>", tbl_cell_bold),
            Paragraph("Endpoint POST Registrasi: Upload 2 Foto Dokumen, Akun Password & Auto Kode PRT", tbl_cell_bold),
            Paragraph("Endpoint POST menangani upload multipart `foto_ktp` dan `foto_memegang_ktp`, hashing password akun via `make_password`, auto-generate kode `PRT-YYYYMMDD-XXXX`, dan status awal `pending`.", tbl_cell)
        ],
        [
            Paragraph("<b>T5</b><br/><font color='#2563EB'>Backend (Hari)</font>", tbl_cell_bold),
            Paragraph("Implementasi validasi backend pendaftaran partner", tbl_cell_bold),
            Paragraph("Menerapkan validasi backend pada serializer Django REST Framework untuk memeriksa kelengkapan field wajib pada formulir pendaftaran partner.", tbl_cell)
        ],
        [
            Paragraph("<b>T5.1</b><br/><font color='#2563EB'>Backend (Hari)</font>", tbl_cell_bold),
            Paragraph("Penyesuaian implementasi validasi dengan dokumen bersama API", tbl_cell_bold),
            Paragraph("Menyesuaikan aturan validasi serializer agar mematuhi error handling kontrak bersama antarmodul (mengembalikan response HTTP 422 Unprocessable Entity saat payload invalid).", tbl_cell)
        ],
        [
            Paragraph("<b>T5.2</b><br/><font color='#2563EB'>Backend (Hari)</font>", tbl_cell_bold),
            Paragraph("Validasi Backend: NIK 16 Digit, Format Gambar (JPG/PNG), & password kuat", tbl_cell_bold),
            Paragraph("Validasi ketat: NIK wajib tepat 16 digit numerik, file `foto_ktp` & `foto_memegang_ktp` wajib bertipe gambar (JPG/JPEG/PNG) maks 5MB, serta password minimal 8 karakter kuat.", tbl_cell)
        ],
        [
            Paragraph("<b>T5.3</b><br/><font color='#2563EB'>Backend (Hari)</font>", tbl_cell_bold),
            Paragraph("Buat Dokumentasi API", tbl_cell_bold),
            Paragraph("Menyusun dokumentasi lengkap API Modul 3: spesifikasi OpenAPI 3.0 (`openapi_modul3.yaml`), Postman Collection v2.1, PDF panduan integrasi, dan README terstruktur untuk tim antarmodul.", tbl_cell)
        ],

        # Frontend (Melda)
        [
            Paragraph("<b>T6</b><br/><font color='#7C3AED'>Frontend (Melda)</font>", tbl_cell_bold),
            Paragraph("Slicing halaman & Form Pendaftaran Frontend", tbl_cell_bold),
            Paragraph("Slicing kode HTML/CSS awal untuk antarmuka formulir pendaftaran calon partner berdasarkan desain Figma.", tbl_cell)
        ],
        [
            Paragraph("<b>T6.1</b><br/><font color='#7C3AED'>Frontend (Melda)</font>", tbl_cell_bold),
            Paragraph("Slicing Landing Page Pendaftaran Partner (UI-01 Landing Partner)", tbl_cell_bold),
            Paragraph("Membangun antarmuka landing page resmi di Modul 3 (`UI-01 Landing Partner`) dengan tombol ajakan CTA 'Daftar Sekarang' yang mengarahkan partner ke form pendaftaran.", tbl_cell)
        ],
        [
            Paragraph("<b>T6.2</b><br/><font color='#7C3AED'>Frontend (Melda)</font>", tbl_cell_bold),
            Paragraph("Slicing Form Stepper: Info Usaha (untuk kategori unit usaha ambil dari dummy M2), Dokumen, Akun & Konfirmasi", tbl_cell_bold),
            Paragraph("Membangun stepper 4 tahap: Step 1 Info Usaha (kategori dari dummy API M2), Step 2 Unggah Dokumen (Foto KTP & Selfie KTP), Step 3 Akun Aplikasi (Email & Password), Step 4 Konfirmasi & submit multipart.", tbl_cell)
        ],

        # QA / Testing (Atha)
        [
            Paragraph("<b>T7</b><br/><font color='#DC2626'>Testing (Atha)</font>", tbl_cell_bold),
            Paragraph("Pengujian fungsional seluruh AC M3-US1 & code review", tbl_cell_bold),
            Paragraph("Menjalankan pengujian fungsional komprehensif terhadap seluruh Acceptance Criteria awal M3-US1 serta melakukan code review pada pull request tim.", tbl_cell)
        ],
        [
            Paragraph("<b>T7.1</b><br/><font color='#DC2626'>Testing (Atha)</font>", tbl_cell_bold),
            Paragraph("Automated Testing Registrasi: Foto KTP, Selfie Pegang KTP & Akun Aplikasi", tbl_cell_bold),
            Paragraph("Menulis test suite otomatis DRF untuk menguji alur registrasi baru: upload 2 berkas foto dokumen, validasi NIK 16 digit, pembuatan akun password, auto-generate kode `PRT-...`, dan status `pending`.", tbl_cell)
        ]
    ]

    t_s1_us1 = Table(sprint1_us1_tasks, colWidths=[85, 180, 258])
    t_s1_us1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.3),
    ]))
    story.append(t_s1_us1)
    story.append(Spacer(1, 4))

    # Page Break to Page 4 for M3-US3 and Sprint 2
    story.append(PageBreak())

    # SUBSECTION 4.2: USER STORY M3-US3
    story.append(Paragraph("4.2 User Story M3-US3: Melihat Status Pendaftaran oleh Partner (8 Sub-Issues / Tasks)", sub_h2_style))

    sprint1_us3_tasks = [
        [Paragraph("Kode & Role", tbl_header), Paragraph("Judul Task Linear", tbl_header), Paragraph("Deskripsi & Kriteria Selesai (DoD)", tbl_header)],
        
        # Desain (Milda)
        [
            Paragraph("<b>T8</b><br/><font color='#DB2777'>Desain (Milda)</font>", tbl_cell_bold),
            Paragraph("Desain prototipe Figma Halaman Cek Status Pendaftaran Partner", tbl_cell_bold),
            Paragraph("Merancang antarmuka awal di Figma untuk halaman pengecekan status pendaftaran calon partner mandiri.", tbl_cell)
        ],
        [
            Paragraph("<b>T8.1</b><br/><font color='#DB2777'>Desain (Milda)</font>", tbl_cell_bold),
            Paragraph("Desain Halaman Status: Kunci State Pending, Tombol Login dari M1 & Alasan Tolak", tbl_cell_bold),
            Paragraph("Desain detail 3 state: State Pending (navigasi dikunci tanpa opsi kembali ke form), State Terverifikasi (tombol link login ke M1), State Ditolak (box alasan tolak permanen & tombol daftar ulang).", tbl_cell)
        ],

        # Database (Akbar)
        [
            Paragraph("<b>T9</b><br/><font color='#D97706'>Database (Akbar)</font>", tbl_cell_bold),
            Paragraph("Penyesuaian query database status terkini & alasan tolak", tbl_cell_bold),
            Paragraph("Optimasi query pencarian data status partner dan alasan penolakan berdasarkan `partner_id` melalui index B-Tree aktif agar pencarian status publik instan (< 50ms).", tbl_cell)
        ],

        # Backend (Hari)
        [
            Paragraph("<b>T10</b><br/><font color='#2563EB'>Backend (Hari)</font>", tbl_cell_bold),
            Paragraph("Pembuatan API Endpoint GET status pendaftaran partner", tbl_cell_bold),
            Paragraph("Membangun endpoint API `GET /api/m3/v1/partners/{partner_id}/status/` untuk membaca status pendaftaran terkini (`pending`, `terverifikasi`, `ditolak`).", tbl_cell)
        ],
        [
            Paragraph("<b>T11</b><br/><font color='#2563EB'>Backend (Hari)</font>", tbl_cell_bold),
            Paragraph("Backend logic rejection_reason untuk status ditolak", tbl_cell_bold),
            Paragraph("Mengimplementasikan logika respons serializer backend: menyertakan kolom `alasan_penolakan` pada payload JSON ketika status registrasi partner adalah `ditolak`.", tbl_cell)
        ],

        # Frontend (Melda)
        [
            Paragraph("<b>T12</b><br/><font color='#7C3AED'>Frontend (Melda)</font>", tbl_cell_bold),
            Paragraph("Slicing Halaman Status Partner Frontend & integrasi API", tbl_cell_bold),
            Paragraph("Slicing antarmuka web halaman pengecekan status partner dan menghubungkannya dengan pemanggilan endpoint API status backend.", tbl_cell)
        ],
        [
            Paragraph("<b>T12.1</b><br/><font color='#7C3AED'>Frontend (Melda)</font>", tbl_cell_bold),
            Paragraph("Slicing Halaman Status: Kunci Navigasi Pending, Link Login dari M1 & Tombol Daftar Ulang", tbl_cell_bold),
            Paragraph("Slicing logika UI: navigasi dikunci saat `pending`, tombol redirect login ke M1 saat `terverifikasi`, serta box alasan penolakan permanen dan tombol 'Coba Mendaftar Lagi' saat `ditolak`.", tbl_cell)
        ],

        # QA / Testing (Atha)
        [
            Paragraph("<b>T13</b><br/><font color='#DC2626'>Testing (Atha)</font>", tbl_cell_bold),
            Paragraph("Pengujian fungsional AC M3-US3 & code review akhir Sprint 1", tbl_cell_bold),
            Paragraph("Pengujian fungsional komprehensif seluruh AC M3-US3 (validasi navigasi pending terkunci, tautan login M1 saat approved, dan alasan penolakan saat ditolak) serta code review akhir Sprint 1.", tbl_cell)
        ]
    ]

    t_s1_us3 = Table(sprint1_us3_tasks, colWidths=[85, 180, 258])
    t_s1_us3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.3),
    ]))
    story.append(t_s1_us3)
    story.append(Spacer(1, 6))

    # SECTION 5: TASK SPRINT 2 (US2 & US4)
    story.append(Paragraph("5. Daftar Task Sprint 2 (M3-US2: Verifikasi & M3-US4: Penangguhan — 12 Task)", h1_style))

    sprint2_tasks = [
        [Paragraph("Kode & Role", tbl_header), Paragraph("Judul Task Linear", tbl_header), Paragraph("Deskripsi & Kriteria Selesai (DoD)", tbl_header)],
        
        # Desain (Milda)
        [
            Paragraph("<b>T14</b><br/><font color='#DB2777'>Desain (Milda)</font>", tbl_cell_bold),
            Paragraph("Desain Figma Dashboard Verifikasi Superadmin (Pratinjau KTP & Selfie)", tbl_cell_bold),
            Paragraph("Merancang tabel antrean partner pending, modal pratinjau berkas Foto KTP dan Foto Selfie Pegang KTP, tombol Approve, dan modal penolakan (Reject wajib isi alasan).", tbl_cell)
        ],
        [
            Paragraph("<b>T15</b><br/><font color='#DB2777'>Desain (Milda)</font>", tbl_cell_bold),
            Paragraph("Desain Figma Manajemen Toko & Penangguhan Partner (M3-US4)", tbl_cell_bold),
            Paragraph("Merancang antarmuka pengelolaan partner terverifikasi, modal input alasan suspend, tombol re-aktivasi toko, dan halaman peringatan toko ditangguhkan.", tbl_cell)
        ],

        # Database (Akbar)
        [
            Paragraph("<b>T16</b><br/><font color='#D97706'>Database (Akbar)</font>", tbl_cell_bold),
            Paragraph("Trigger Otomatis Pencatatan Audit Perubahan Status ke `partner_status_logs`", tbl_cell_bold),
            Paragraph("Membangun servis model Django yang otomatis mencatat log setiap kali status berubah (admin_id, status lama, status baru, aksi APPROVE/REJECT/SUSPEND/ACTIVATE, alasan).", tbl_cell)
        ],
        [
            Paragraph("<b>T17</b><br/><font color='#D97706'>Database (Akbar)</font>", tbl_cell_bold),
            Paragraph("Seeding Fixtures Data Partner Multi-Status untuk Pengujian", tbl_cell_bold),
            Paragraph("Menyediakan file fixture JSON berisi sampel data partner dalam berbagai status (`pending`, `terverifikasi`, `ditolak`, `ditangguhkan`) untuk keperluan testing lokal FE & QA.", tbl_cell)
        ],

        # Backend (Hary)
        [
            Paragraph("<b>T18</b><br/><font color='#2563EB'>Backend (Hary)</font>", tbl_cell_bold),
            Paragraph("API List Antrean Partner Admin `GET /api/m3/v1/admin/partners/`", tbl_cell_bold),
            Paragraph("Menyediakan endpoint daftar partner untuk Superadmin dengan filter status (`pending`, `terverifikasi`, `ditolak`), pagination, dan URL berkas Foto KTP & Selfie KTP.", tbl_cell)
        ],
        [
            Paragraph("<b>T19</b><br/><font color='#2563EB'>Backend (Hary)</font>", tbl_cell_bold),
            Paragraph("API Approve (Sinkronisasi Akun ke M1) & API Reject (Wajib Alasan)", tbl_cell_bold),
            Paragraph("Endpoint POST `.../approve/`: ubah status ke `terverifikasi`, picu aktivasi akun di Modul 1 via API M1. Endpoint POST `.../reject/`: wajib `alasan_penolakan`, status -> `ditolak`. Catat log.", tbl_cell)
        ],
        [
            Paragraph("<b>T20</b><br/><font color='#2563EB'>Backend (Hary)</font>", tbl_cell_bold),
            Paragraph("API Penangguhan & Pengaktifan Kembali (`suspend/` & `activate/`)", tbl_cell_bold),
            Paragraph("Endpoint POST `.../suspend/`: wajib `alasan_penangguhan`, status -> `ditangguhkan`. Endpoint POST `.../activate/`: status kembali `terverifikasi`. Catat log audit.", tbl_cell)
        ],
        [
            Paragraph("<b>T21</b><br/><font color='#2563EB'>Backend (Hary)</font>", tbl_cell_bold),
            Paragraph("API Kontrak K-03 Ringkasan Dashboard Eksekutif untuk Modul 2", tbl_cell_bold),
            Paragraph("Endpoint `GET /api/m3/v1/dashboard-summary` mengembalikan agregat data: total partner, terverifikasi, pending, ditangguhkan, dan distribusi kategori (`Produk` vs `Jasa`).", tbl_cell)
        ],

        # Frontend (Melda)
        [
            Paragraph("<b>T22</b><br/><font color='#7C3AED'>Frontend (Melda)</font>", tbl_cell_bold),
            Paragraph("Slicing & Integrasi Dashboard Verifikasi Superadmin (Pratinjau KTP & Selfie)", tbl_cell_bold),
            Paragraph("Membangun antarmuka tabel antrean pendaftar, modal pratinjau dokumen (Foto KTP dan Foto Orang Memegang KTP), tombol Approve, dan modal penolakan ber-alasan.", tbl_cell)
        ],
        [
            Paragraph("<b>T23</b><br/><font color='#7C3AED'>Frontend (Melda)</font>", tbl_cell_bold),
            Paragraph("Slicing & Integrasi Pengelolaan Toko Partner Terverifikasi & Suspend", tbl_cell_bold),
            Paragraph("Membangun antarmuka pengelolaan partner aktif, modal input alasan penangguhan toko (Suspend), dan tombol Aktifkan Kembali terintegrasi ke API backend.", tbl_cell)
        ],

        # QA (Atha)
        [
            Paragraph("<b>T24</b><br/><font color='#DC2626'>Testing (Atha)</font>", tbl_cell_bold),
            Paragraph("Automated Test Suite M3-US2: Verifikasi Approval & Rejection", tbl_cell_bold),
            Paragraph("Menulis acceptance test: validasi transisi status pending -> terverifikasi, penolakan tanpa alasan wajib gagal (422), dan verifikasi pencatatan audit di `partner_status_logs`.", tbl_cell)
        ],
        [
            Paragraph("<b>T25</b><br/><font color='#DC2626'>Testing (Atha)</font>", tbl_cell_bold),
            Paragraph("Automated Test Suite M3-US4: Penangguhan, Re-aktivasi & Filter K-06 Modul 5", tbl_cell_bold),
            Paragraph("Menulis test suite: validasi penangguhan wajib alasan, re-aktivasi sukses, dan verifikasi ketat bahwa toko berstatus `ditangguhkan` **tidak muncul** pada API publik Modul 5.", tbl_cell)
        ]
    ]

    t_s2 = Table(sprint2_tasks, colWidths=[90, 175, 258])
    t_s2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F766E')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0FDFA')]),
        ('TOPPADDING', (0, 0), (-1, -1), 1.3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.3),
    ]))
    story.append(t_s2)
    story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master PDF resmi berhasil diperbarui: {filename}")

if __name__ == "__main__":
    output_dir = "flow"
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, "Panduan_Resmi_Alur_dan_Roadmap_Modul_3.pdf")
    build_master_pdf(pdf_path)
