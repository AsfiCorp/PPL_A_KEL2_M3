from django import forms
from .models import Partner


class PartnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = [
            'nama_usaha',
            'kategori_usaha',
            'deskripsi_usaha',
            'alamat_usaha',
            'nomor_telepon_usaha',
            'email_usaha',
            'profil_usaha',
        ]
        labels = {
            'nama_usaha': 'Nama usaha',
            'kategori_usaha': 'Kategori usaha',
            'deskripsi_usaha': 'Deskripsi usaha',
            'alamat_usaha': 'Alamat usaha',
            'nomor_telepon_usaha': 'Nomor telepon usaha',
            'email_usaha': 'Email usaha',
            'profil_usaha': 'Profil usaha',
        }
        widgets = {
            'nama_usaha': forms.TextInput(attrs={
                'placeholder': 'Masukkan nama usaha',
                'autocomplete': 'organization',
            }),
            'kategori_usaha': forms.Select(),
            'deskripsi_usaha': forms.Textarea(attrs={
                'placeholder': 'Ceritakan usaha Anda',
                'rows': 4,
            }),
            'alamat_usaha': forms.TextInput(attrs={
                'placeholder': 'Masukkan alamat usaha',
                'autocomplete': 'street-address',
            }),
            'nomor_telepon_usaha': forms.TelInput(attrs={
                'placeholder': 'Contoh: 0812 3456 7890',
                'autocomplete': 'tel',
            }),
            'email_usaha': forms.EmailInput(attrs={
                'placeholder': 'Contoh: usaha@email.com',
                'autocomplete': 'email',
            }),
            'profil_usaha': forms.ClearableFileInput(attrs={
                'accept': '.png,.jpg,.jpeg',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
        self.fields['kategori_usaha'].choices = [
            ('', 'Pilih kategori usaha'),
            *Partner.KategoriUsaha.choices,
        ]
        self.fields['profil_usaha'].required = False
        self.fields['profil_usaha'].help_text = 'Pilih gambar PNG, JPG, atau JPEG. Maksimal 5 MB.'

    def clean_profil_usaha(self):
        image = self.cleaned_data.get('profil_usaha')
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Ukuran gambar melebihi 5 MB. Pilih gambar yang lebih kecil.')
        return image
