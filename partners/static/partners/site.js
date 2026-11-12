(() => {
    const profileTrigger = document.querySelector('.profile-trigger');
    const profileDrawer = document.querySelector('.profile-drawer');
    const profileBackdrop = document.querySelector('.profile-drawer-backdrop');

    if (profileTrigger && profileDrawer && profileBackdrop) {
        let closeTimer;

        const closeDrawer = () => {
            if (profileTrigger.getAttribute('aria-expanded') !== 'true') return;

            profileTrigger.setAttribute('aria-expanded', 'false');
            profileDrawer.setAttribute('aria-hidden', 'true');
            profileBackdrop.hidden = true;
            document.body.classList.remove('profile-open');
            window.clearTimeout(closeTimer);
            closeTimer = window.setTimeout(() => {
                if (profileTrigger.getAttribute('aria-expanded') !== 'true') {
                    profileDrawer.hidden = true;
                }
            }, 180);
            profileTrigger.focus();
        };

        profileTrigger.addEventListener('click', () => {
            if (profileTrigger.getAttribute('aria-expanded') === 'true') {
                closeDrawer();
                return;
            }

            window.clearTimeout(closeTimer);
            profileDrawer.hidden = false;
            profileBackdrop.hidden = false;
            profileDrawer.setAttribute('aria-hidden', 'false');
            profileTrigger.setAttribute('aria-expanded', 'true');
            document.body.classList.add('profile-open');
            const firstAction = profileDrawer.querySelector('a[href], button:not([disabled])');
            (firstAction || profileDrawer).focus();
        });

        profileBackdrop.addEventListener('click', closeDrawer);
        document.addEventListener('keydown', (event) => {
            if (profileTrigger.getAttribute('aria-expanded') !== 'true') return;

            if (event.key === 'Escape') {
                closeDrawer();
                return;
            }

            if (event.key === 'Tab') {
                const focusableItems = Array.from(
                    profileDrawer.querySelectorAll('a[href], button:not([disabled])'),
                );
                if (!focusableItems.length) {
                    event.preventDefault();
                    profileDrawer.focus();
                    return;
                }

                const firstItem = focusableItems[0];
                const lastItem = focusableItems[focusableItems.length - 1];
                if (event.shiftKey && document.activeElement === firstItem) {
                    event.preventDefault();
                    lastItem.focus();
                } else if (!event.shiftKey && document.activeElement === lastItem) {
                    event.preventDefault();
                    firstItem.focus();
                }
            }
        });
    }

    let navigateRegistrationStep = null;
    const registrationForm = document.querySelector('.registration-form');
    if (registrationForm) {
        const steps = Array.from(registrationForm.querySelectorAll('.registration-step'));
        const indicators = Array.from(registrationForm.querySelectorAll('.registration-steps li'));
        const backButton = registrationForm.querySelector('[data-step-back]');
        const nextButton = registrationForm.querySelector('[data-step-next]');
        const submitButton = registrationForm.querySelector('[data-step-submit]');
        const cancelLink = registrationForm.querySelector('.form-actions > a');
        let currentStep = 1;

        const showStep = (step) => {
            currentStep = step;
            steps.forEach((section) => {
                section.hidden = Number(section.dataset.step) !== step;
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
            backButton.hidden = step === 1;
            nextButton.hidden = step === steps.length;
            submitButton.hidden = step !== steps.length;
            cancelLink.hidden = step !== 1;
        };
        navigateRegistrationStep = showStep;

        const populateConfirmation = () => {
            const groups = {
                business: [
                    ['Nama Usaha', 'nama_usaha'],
                    ['Kategori', 'kategori_usaha', true],
                    ['Nomor Telepon Usaha', 'nomor_telepon_usaha'],
                    ['Email Usaha', 'email_usaha'],
                    ['Alamat Usaha', 'alamat_usaha'],
                    ['Deskripsi Usaha', 'deskripsi_usaha'],
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
                list.replaceChildren();
                entries.forEach(([label, name, useSelectedLabel, isFile]) => {
                    const field = registrationForm.elements.namedItem(name);
                    const value = isFile
                        ? field.files?.[0]?.name
                        : useSelectedLabel
                            ? field.options[field.selectedIndex]?.text
                            : field.value.trim();
                    const term = document.createElement('dt');
                    const description = document.createElement('dd');
                    term.textContent = label;
                    description.textContent = value || '—';
                    list.append(term, description);
                });
            });
        };

        nextButton.addEventListener('click', () => {
            const activeStep = steps[currentStep - 1];
            const password = registrationForm.elements.namedItem('password');
            const confirmPassword = registrationForm.elements.namedItem('confirm_password');
            if (currentStep === 3) {
                confirmPassword.setCustomValidity(
                    password.value === confirmPassword.value ? '' : 'Konfirmasi password tidak cocok.',
                );
            }

            const invalidField = Array.from(activeStep.querySelectorAll('input, select, textarea'))
                .find((field) => !field.checkValidity());
            if (invalidField) {
                invalidField.reportValidity();
                return;
            }

            const nextStep = currentStep + 1;
            if (nextStep === steps.length) populateConfirmation();
            showStep(nextStep);
        });

        backButton.addEventListener('click', () => showStep(currentStep - 1));
        registrationForm.elements.namedItem('confirm_password').addEventListener('input', (event) => {
            event.currentTarget.setCustomValidity('');
        });
        showStep(currentStep);
    }

    const imageInput = document.querySelector('#id_profil_usaha');
    const uploadLabel = document.querySelector('#upload-label');
    const uploadHint = document.querySelector('#upload-hint');
    if (imageInput && uploadLabel && uploadHint) {
        imageInput.addEventListener('change', () => {
            const file = imageInput.files && imageInput.files[0];
            uploadLabel.textContent = file ? file.name : 'Pilih gambar';
            uploadHint.textContent = file ? 'Pilih file lain untuk mengganti gambar' : 'Klik untuk memilih file PNG, JPG, atau JPEG';
        });
    }
    document.querySelectorAll('.registration-form input[name="ktp"], .registration-form input[name="foto_pemegang_ktp"]').forEach((input) => {
        input.addEventListener('change', () => {
            const file = input.files && input.files[0];
            const label = document.querySelector(`[data-upload-label="${input.name}"]`);
            const hint = document.querySelector(`[data-upload-hint="${input.name}"]`);
            if (label && hint) {
                label.textContent = file ? file.name : 'Unggah File';
                hint.textContent = file ? 'Pilih file lain untuk mengganti dokumen' : 'Klik untuk memilih file PNG, JPG, JPEG, atau PDF';
            }
        });
    });

    if (registrationForm) {
        const summary = registrationForm.querySelector('.form-summary');
        const summaryErrors = registrationForm.querySelector('.form-summary-errors');

        const clearErrors = () => {
            registrationForm.querySelectorAll('.field-errors').forEach((container) => {
                container.replaceChildren();
            });
            registrationForm.querySelectorAll('[aria-invalid="true"]').forEach((field) => {
                field.removeAttribute('aria-invalid');
                field.removeAttribute('aria-describedby');
            });
            summary.hidden = true;
            summaryErrors.replaceChildren();
        };

        const showErrors = (errors) => {
            const generalErrors = [];
            let firstErrorStep = null;
            Object.entries(errors).forEach(([fieldName, messages]) => {
                const container = registrationForm.querySelector(`[data-field-errors="${fieldName}"]`);
                const field = registrationForm.elements.namedItem(fieldName);
                const errorMessages = Array.isArray(messages) ? messages : [messages];

                if (!container || !field || typeof field === 'string') {
                    generalErrors.push(...errorMessages.map(String));
                    return;
                }

                field.setAttribute('aria-invalid', 'true');
                firstErrorStep = firstErrorStep || field.closest('.registration-step');
                const errorId = `${field.id}-api-error`;
                field.setAttribute('aria-describedby', errorId);
                errorMessages.forEach((message) => {
                    const error = document.createElement('p');
                    error.className = 'field-error';
                    error.id = errorId;
                    error.setAttribute('role', 'alert');
                    error.textContent = String(message);
                    container.append(error);
                });
            });

            if (generalErrors.length) {
                generalErrors.forEach((message) => {
                    const item = document.createElement('li');
                    item.textContent = message;
                    summaryErrors.append(item);
                });
                summary.hidden = false;
            }
            if (firstErrorStep) {
                const step = Number(firstErrorStep.dataset.step);
                if (step && navigateRegistrationStep) navigateRegistrationStep(step);
            }
        };

        registrationForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            clearErrors();
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Mengirim…';
            }

            let redirecting = false;
            try {
                const response = await fetch(registrationForm.dataset.apiUrl, {
                    method: 'POST',
                    headers: {
                        Accept: 'application/json',
                        'X-CSRFToken': registrationForm.elements.namedItem('csrfmiddlewaretoken').value,
                    },
                    body: new FormData(registrationForm),
                    credentials: 'same-origin',
                });
                const result = await response.json().catch(() => null);

                if (response.ok && result?.status === 'success' && result.data?.id) {
                    redirecting = true;
                    window.location.assign(registrationForm.dataset.statusUrl);
                    return;
                }

                if (result?.errors && typeof result.errors === 'object') {
                    showErrors(result.errors);
                } else {
                    showErrors({
                        __all__: [
                            result?.message || 'Server memberikan respons yang tidak dapat diproses. Silakan coba lagi.',
                        ],
                    });
                }
            } catch {
                showErrors({
                    __all__: ['Tidak dapat terhubung ke server. Periksa koneksi Anda, lalu coba lagi.'],
                });
            } finally {
                if (submitButton && !redirecting) {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Kirim Pendaftaran';
                }
            }
        });
    }
})();
