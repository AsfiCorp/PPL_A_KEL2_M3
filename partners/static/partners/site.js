(() => {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.querySelector('.sidebar-backdrop');

    if (menuToggle && sidebar && backdrop) {
        const closeMenu = () => {
            document.body.classList.remove('nav-open');
            menuToggle.setAttribute('aria-expanded', 'false');
            backdrop.hidden = true;
        };

        menuToggle.addEventListener('click', () => {
            const isOpen = document.body.classList.toggle('nav-open');
            menuToggle.setAttribute('aria-expanded', String(isOpen));
            backdrop.hidden = !isOpen;
        });
        backdrop.addEventListener('click', closeMenu);
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') closeMenu();
        });
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

    const registrationForm = document.querySelector('.registration-form');
    if (registrationForm) {
        registrationForm.addEventListener('submit', () => {
            const submitButton = registrationForm.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Mengirim…';
            }
        });
    }
})();
