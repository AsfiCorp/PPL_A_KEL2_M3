(() => {
    // =========================================================================
    // Microservices Client-Side API Consumer - Modul 3 (Araya Business Hub)
    // Langsung memanggil REST API backend:
    // - POST /api/m3/v1/partners/ (Pendaftaran Partner M3-US1)
    // - GET  /api/m3/v1/partners/{partner_id}/ (Cek Status Pendaftaran M3-US3)
    // =========================================================================

    const getCsrfToken = () => {
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input) return input.value;
        const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    };

    // Helper untuk menampilkan error pada field
    const setFieldError = (fieldElement, errorContainer, message) => {
        if (fieldElement) {
            fieldElement.classList.add('is-invalid');
        }
        if (errorContainer) {
            errorContainer.textContent = message;
        }
    };

    const clearFieldErrors = (form) => {
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        form.querySelectorAll('.field-errors').forEach(el => el.textContent = '');
        const summary = form.querySelector('.form-summary');
        if (summary) summary.hidden = true;
    };

    // -------------------------------------------------------------------------
    // Logika Stepper & Form Pendaftaran
    // -------------------------------------------------------------------------
    const registrationForm = document.querySelector('.registration-form');
    if (registrationForm) {
        const steps = Array.from(registrationForm.querySelectorAll('.registration-step'));
        const indicators = Array.from(registrationForm.querySelectorAll('.registration-steps li'));
        const nextButtons = Array.from(registrationForm.querySelectorAll('[data-step-next]'));
        const backButtons = Array.from(registrationForm.querySelectorAll('[data-step-back]'));
        const submitButton = registrationForm.querySelector('[data-step-submit]');
        let currentStep = 1;

        const showStep = (step) => {
            currentStep = step;
            steps.forEach((section) => {
                const isCurrent = Number(section.dataset.step) === step;
                section.hidden = !isCurrent;
                if (isCurrent) {
                    section.removeAttribute('hidden');
                } else {
                    section.setAttribute('hidden', '');
                }
            });
            indicators.forEach((indicator, index) => {
                const indicatorStep = index + 1;
                indicator.classList.toggle('is-active', indicatorStep === step);
                indicator.classList.toggle('is-complete', indicatorStep < step);
                if (indicatorStep === step) {
                    indicator.setAttribute('aria-current', 'step');
                } else {
                    indicator.removeAttribute('aria-current');
                }
            });
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };

        const validateStep = (stepNumber) => {
            let isValid = true;
            clearFieldErrors(registrationForm);

            if (stepNumber === 1) {
                const requiredFields = [
                    ['nama_usaha', 'Masukan Nama Usaha'],
                    ['kategori_usaha', 'Pilih Kategori Usaha'],
                    ['deskripsi_usaha', 'Deskripsi usaha wajib diisi'],
                    ['alamat_usaha', 'Alamat usaha wajib diisi'],
                    ['nomor_telepon_usaha', 'Nomor telepon usaha wajib diisi'],
                    ['email_usaha', 'Email usaha wajib diisi']
                ];
                requiredFields.forEach(([name, errMsg]) => {
                    const field = registrationForm.elements.namedItem(name);
                    const errorBox = registrationForm.querySelector(`[data-field-errors="${name}"]`);
                    if (!field || !field.value.trim()) {
                        setFieldError(field, errorBox, errMsg);
                        isValid = false;
                    }
                });
            } else if (stepNumber === 2) {
                const requiredFields = [
                    ['nama_lengkap', 'Nama lengkap penanggung jawab wajib diisi'],
                    ['nik', 'NIK wajib diisi (16 digit angka)'],
                    ['tempat_lahir', 'Tempat lahir wajib diisi'],
                    ['tanggal_lahir', 'Tanggal lahir wajib diisi']
                ];
                requiredFields.forEach(([name, errMsg]) => {
                    const field = registrationForm.elements.namedItem(name);
                    const errorBox = registrationForm.querySelector(`[data-field-errors="${name}"]`);
                    if (!field || !field.value.trim()) {
                        setFieldError(field, errorBox, errMsg);
                        isValid = false;
                    }
                });

                const nikField = registrationForm.elements.namedItem('nik');
                if (nikField && nikField.value.trim() && !/^\d{16}$/.test(nikField.value.trim())) {
                    setFieldError(nikField, registrationForm.querySelector('[data-field-errors="nik"]'), 'NIK harus tepat 16 digit angka.');
                    isValid = false;
                }

                // Cek unggah dokumen KTP & Foto memegang KTP
                const ktpInput = registrationForm.elements.namedItem('ktp');
                const fotoPemegangInput = registrationForm.elements.namedItem('foto_pemegang_ktp');
                if (ktpInput && (!ktpInput.files || ktpInput.files.length === 0)) {
                    setFieldError(null, registrationForm.querySelector('[data-field-errors="ktp"]'), 'Unggah foto KTP wajib disertakan.');
                    isValid = false;
                }
                if (fotoPemegangInput && (!fotoPemegangInput.files || fotoPemegangInput.files.length === 0)) {
                    setFieldError(null, registrationForm.querySelector('[data-field-errors="foto_pemegang_ktp"]'), 'Unggah swafoto memegang KTP wajib disertakan.');
                    isValid = false;
                }
            } else if (stepNumber === 3) {
                const emailField = registrationForm.elements.namedItem('account_email');
                const passField = registrationForm.elements.namedItem('password');
                const confirmField = registrationForm.elements.namedItem('confirm_password');

                if (!emailField || !emailField.value.trim()) {
                    setFieldError(emailField, registrationForm.querySelector('[data-field-errors="account_email"]'), 'Email akun wajib diisi');
                    isValid = false;
                }
                if (!passField || passField.value.length < 8) {
                    setFieldError(passField, registrationForm.querySelector('[data-field-errors="password"]'), 'Password minimal 8 karakter');
                    isValid = false;
                }
                if (!confirmField || confirmField.value !== (passField ? passField.value : '')) {
                    setFieldError(confirmField, registrationForm.querySelector('[data-field-errors="confirm_password"]'), 'Konfirmasi password tidak cocok.');
                    isValid = false;
                }
            }

            return isValid;
        };

        const populateConfirmation = () => {
            const groups = {
                business: [
                    ['Nama Usaha', 'nama_usaha'],
                    ['Kategori', 'kategori_usaha', true],
                    ['Nomor Telepon Usaha', 'nomor_telepon_usaha'],
                    ['Email Usaha', 'email_usaha'],
                    ['Alamat Usaha', 'alamat_usaha'],
                    ['Deskripsi Usaha', 'deskripsi_usaha'],
                    ['Profil Usaha', 'profil_usaha', false, true],
                ],
                responsible: [
                    ['Nama Lengkap', 'nama_lengkap'],
                    ['Nomor Induk Penduduk (NIK)', 'nik'],
                    ['Tempat Lahir', 'tempat_lahir'],
                    ['Tanggal Lahir', 'tanggal_lahir'],
                    ['Kartu Tanda Penduduk', 'ktp', false, true],
                    ['Foto Orang Memegang KTP', 'foto_pemegang_ktp', false, true],
                ],
                account: [['Email', 'account_email']],
            };

            Object.entries(groups).forEach(([group, entries]) => {
                const list = registrationForm.querySelector(`[data-confirmation="${group}"]`);
                if (!list) return;
                list.replaceChildren();
                entries.forEach(([label, name, useSelectedLabel, isFile]) => {
                    const field = registrationForm.elements.namedItem(name);
                    let value = '—';
                    if (field) {
                        if (isFile) {
                            value = field.files?.[0]?.name || 'Berkas terpilih';
                        } else if (useSelectedLabel) {
                            value = field.options[field.selectedIndex]?.text || field.value;
                        } else {
                            value = field.value.trim() || '—';
                        }
                    }
                    const term = document.createElement('dt');
                    const description = document.createElement('dd');
                    term.textContent = label;
                    description.textContent = value;
                    list.append(term, description);
                });
            });
        };

        nextButtons.forEach((btn) => {
            btn.addEventListener('click', () => {
                if (!validateStep(currentStep)) return;
                const nextStep = currentStep + 1;
                if (nextStep === steps.length) {
                    populateConfirmation();
                }
                showStep(nextStep);
            });
        });

        backButtons.forEach((btn) => {
            btn.addEventListener('click', () => {
                clearFieldErrors(registrationForm);
                showStep(currentStep - 1);
            });
        });

        // ---------------------------------------------------------------------
        // HIT BACKEND REST API LANGSUNG (POST /api/m3/v1/partners/)
        // ---------------------------------------------------------------------
        registrationForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Kumpulkan data multipart form
            const formData = new FormData(registrationForm);
            formData.set('complete_registration', 'true');

            // Handle file inputs secara eksplisit
            const profilInput = registrationForm.elements.namedItem('profil_usaha');
            const ktpInput = registrationForm.elements.namedItem('ktp');
            const selfieInput = registrationForm.elements.namedItem('foto_pemegang_ktp');

            const profilFile = profilInput?.files?.[0];
            const ktpFile = ktpInput?.files?.[0];
            const selfieFile = selfieInput?.files?.[0];

            if (profilFile && profilFile.size > 0) {
                formData.set('profil_usaha', profilFile);
            } else {
                formData.delete('profil_usaha');
            }

            if (ktpFile && ktpFile.size > 0) {
                formData.set('ktp', ktpFile);
                formData.set('foto_ktp', ktpFile);
            }

            if (selfieFile && selfieFile.size > 0) {
                formData.set('foto_pemegang_ktp', selfieFile);
                formData.set('foto_memegang_ktp', selfieFile);
            }

            // UI loading state
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Mengirim pendaftaran...';
            }

            try {
                const response = await fetch('/api/m3/v1/partners/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Accept': 'application/json'
                    },
                    body: formData
                });

                const json = await response.json();

                if (response.ok && json.success) {
                    const partnerId = json.data?.partner_id || json.data?.id;
                    if (partnerId) {
                        sessionStorage.setItem('current_partner_id', partnerId);
                        window.location.href = `/pendaftaran-partner/status/?partner_id=${encodeURIComponent(partnerId)}`;
                    } else {
                        window.location.href = '/pendaftaran-partner/status/';
                    }
                } else {
                    // Penanganan galat validasi dari REST API (422 / 409)
                    if (submitButton) {
                        submitButton.disabled = false;
                        submitButton.textContent = 'Kirim Pendaftaran';
                    }

                    const errors = json.error?.fields || json.errors || {};
                    let firstErrorStep = null;

                    Object.entries(errors).forEach(([field, msg]) => {
                        const fieldEl = registrationForm.elements.namedItem(field);
                        const errBox = registrationForm.querySelector(`[data-field-errors="${field}"]`);
                        setFieldError(fieldEl, errBox, msg);

                        if (!firstErrorStep) {
                            if (['nama_usaha', 'kategori_usaha', 'deskripsi_usaha', 'alamat_usaha', 'nomor_telepon_usaha', 'email_usaha'].includes(field)) {
                                firstErrorStep = 1;
                            } else if (['nama_lengkap', 'nik', 'tempat_lahir', 'tanggal_lahir', 'ktp', 'foto_pemegang_ktp', 'foto_ktp', 'foto_memegang_ktp'].includes(field)) {
                                firstErrorStep = 2;
                            } else if (['account_email', 'password', 'confirm_password'].includes(field)) {
                                firstErrorStep = 3;
                            }
                        }
                    });

                    const summary = registrationForm.querySelector('.form-summary');
                    if (summary) {
                        summary.hidden = false;
                        const errorList = summary.querySelector('.form-summary-errors');
                        if (errorList) {
                            errorList.replaceChildren();
                            Object.entries(errors).forEach(([f, m]) => {
                                const li = document.createElement('li');
                                li.textContent = `${f}: ${m}`;
                                errorList.appendChild(li);
                            });
                        }
                    }

                    if (firstErrorStep) {
                        showStep(firstErrorStep);
                    }
                }
            } catch (err) {
                console.error('Fetch error:', err);
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Kirim Pendaftaran';
                }
                // Fallback: submit form secara tradisional bila koneksi fetch mengalami isu jaringan
                registrationForm.submit();
            }
        });

        // Tampilkan langkah awal
        showStep(1);
    }

    // -------------------------------------------------------------------------
    // Interactive Upload Controls (Drag & Drop, Visual Preview, Accessible Click)
    // -------------------------------------------------------------------------
    const uploadControls = document.querySelectorAll('.upload-control');

    uploadControls.forEach((control) => {
        const input = control.querySelector('input[type="file"]');
        if (!input) return;

        const fieldName = input.name;
        const labelEl = control.querySelector('strong');
        const hintEl = control.querySelector('span:not(.upload-icon)');
        const previewEl = control.querySelector('.upload-preview');

        const updateDisplay = (file) => {
            if (file) {
                control.classList.add('has-file');
                if (labelEl) {
                    labelEl.textContent = file.name;
                }
                const sizeKB = (file.size / 1024).toFixed(1);
                const sizeStr = file.size > 1024 * 1024
                    ? `${(file.size / (1024 * 1024)).toFixed(2)} MB`
                    : `${sizeKB} KB`;
                if (hintEl) {
                    hintEl.textContent = `Berkas dipilih (${sizeStr}). Klik untuk mengganti.`;
                }

                if (previewEl && file.type && file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        previewEl.innerHTML = `<img src="${e.target.result}" alt="Preview ${file.name}" class="preview-thumbnail">`;
                        previewEl.hidden = false;
                        previewEl.removeAttribute('hidden');
                    };
                    reader.readAsDataURL(file);
                } else if (previewEl) {
                    previewEl.innerHTML = `<span class="preview-badge">Berkas: ${file.name}</span>`;
                    previewEl.hidden = false;
                    previewEl.removeAttribute('hidden');
                }

                // Bersihkan pesan error jika ada
                const errBox = control.parentElement?.querySelector(`[data-field-errors="${fieldName}"]`);
                if (errBox) errBox.textContent = '';
                control.classList.remove('is-invalid');
            } else {
                control.classList.remove('has-file');
                if (labelEl) {
                    labelEl.textContent = fieldName === 'profil_usaha' ? 'Pilih gambar' : 'Unggah File';
                }
                if (hintEl) {
                    hintEl.textContent = fieldName === 'profil_usaha'
                        ? 'Klik untuk memilih file PNG, JPG, atau SVG'
                        : 'Klik untuk memilih file PNG, JPG atau PDF';
                }
                if (previewEl) {
                    previewEl.innerHTML = '';
                    previewEl.hidden = true;
                    previewEl.setAttribute('hidden', '');
                }
            }
        };

        // Buka dialog pemilihan file saat kotak diklik
        control.addEventListener('click', (e) => {
            if (e.target !== input) {
                e.preventDefault();
                input.click();
            }
        });

        // Dukungan aksesibilitas keyboard (Enter atau Spasi)
        control.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                input.click();
            }
        });

        // Event change dari native input
        input.addEventListener('change', () => {
            const file = input.files?.[0];
            updateDisplay(file);
        });

        // Drag & drop support
        ['dragenter', 'dragover'].forEach((eventName) => {
            control.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                control.classList.add('is-dragover');
            });
        });

        ['dragleave', 'drop'].forEach((eventName) => {
            control.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                control.classList.remove('is-dragover');
            });
        });

        control.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files && files.length > 0) {
                input.files = files;
                updateDisplay(files[0]);
            }
        });
    });

    // -------------------------------------------------------------------------
    // HIT BACKEND REST API LANGSUNG PADA HALAMAN STATUS (M3-US3)
    // -------------------------------------------------------------------------
    const statusContainer = document.querySelector('.status-card');
    if (statusContainer) {
        const urlParams = new URLSearchParams(window.location.search);
        const partnerId = urlParams.get('partner_id') || sessionStorage.getItem('current_partner_id');

        if (partnerId) {
            fetch(`/api/m3/v1/partners/${encodeURIComponent(partnerId)}/`, {
                headers: { 'Accept': 'application/json' }
            })
            .then(res => res.json())
            .then(json => {
                if (json.success && json.data) {
                    const data = json.data;
                    const statusVal = data.status; // pending, ditolak, terverifikasi
                    statusContainer.setAttribute('data-registration-status', statusVal);

                    // Perbarui info detail jika berubah
                    const statusTextEl = statusContainer.querySelector('.detail-row dd .status-badge');
                    if (statusTextEl) {
                        const isSuccess = ['terverifikasi', 'approve', 'active'].includes(statusVal);
                        const isDanger = ['ditolak', 'reject'].includes(statusVal);
                        const badgeClass = isDanger ? 'danger' : isSuccess ? 'success' : 'pending';
                        statusTextEl.className = `status-badge status-${badgeClass}`;
                        const labelMap = {
                            'pending': 'Menunggu Persetujuan',
                            'terverifikasi': 'Terverifikasi',
                            'approve': 'Disetujui',
                            'active': 'Aktif',
                            'ditolak': 'Ditolak',
                            'reject': 'Ditolak',
                            'ditangguhkan': 'Ditangguhkan',
                            'suspend': 'Ditangguhkan'
                        };
                        statusTextEl.innerHTML = `<span class="status-dot"></span>${labelMap[statusVal] || statusVal}`;
                    }
                }
            })
            .catch(err => console.debug('Status API fetch background:', err));
        }
    }
})();
