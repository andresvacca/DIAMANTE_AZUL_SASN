/* ════════════════════════════════════════════════
    SISTEMA DE NOTIFICACIONES GLOBAL
    Disponible para todas las apps (Artículos, Empeños, etc.)
    Uso: Toast.show("Mensaje", "success|error|info")
════════════════════════════════════════════════ */

const Toast = {
    show(mensaje, tipo = 'success') {
        const container = document.getElementById('toast-container');
        if (!container) {
            console.error("No se encontró el contenedor #toast-container");
            return;
        }

        const toast = document.createElement('div');
        // Usamos tus clases de auth.css: auth-alert-success, auth-alert-error, etc.
        toast.className = `auth-alert auth-alert-${tipo}`;
        
        toast.style.marginBottom = "10px";
        toast.style.boxShadow = "0 4px 15px rgba(0,0,0,0.2)";
        toast.style.minWidth = "280px";
        toast.style.transition = "all 0.5s ease";
        toast.style.cursor = "pointer";
        toast.textContent = mensaje;

        // Permitir cerrar al hacer clic
        toast.onclick = () => this.hide(toast);

        container.appendChild(toast);

        // Auto-eliminar después de 4 segundos
        setTimeout(() => this.hide(toast), 4000);
    },

    hide(toast) {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(30px)';
        setTimeout(() => {
            if (toast.parentNode) toast.remove();
        }, 500);
    }
};

/* ════════════════════════════════════════════════
    LÓGICA DE INTERFAZ (DOM)
════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {
    
    // 1. MODO OSCURO
    const btnModo = document.getElementById('btn-modo');
    const body    = document.body;

    // Verificar preferencia guardada (usando tu clave 'modo' para consistencia)
    if (localStorage.getItem('modo') === 'oscuro') {
        body.classList.add('dark');
    }

    if (btnModo) {
        btnModo.addEventListener('click', function () {
            body.classList.toggle('dark');
            localStorage.setItem('modo', body.classList.contains('dark') ? 'oscuro' : 'claro');
        });
    }

    // 2. NAVBAR MÓVIL (HAMBURGUESA)
    const hamburger   = document.getElementById('hamburger');
    const navbarLinks = document.getElementById('navbar-links');

    if (hamburger && navbarLinks) {
        hamburger.addEventListener('click', function () {
            navbarLinks.classList.toggle('abierto');
        });

        // Cerrar al hacer clic en un link
        navbarLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navbarLinks.classList.remove('abierto');
            });
        });
    }

    // 3. ANIMACIONES DE REVELAR (Intersection Observer)
    const elementos = document.querySelectorAll('.revelar');
    if (elementos.length > 0) {
        const observador = new IntersectionObserver(function (entradas) {
            entradas.forEach(function (entrada) {
                if (entrada.isIntersecting) {
                    entrada.target.classList.add('visible');
                    observador.unobserve(entrada.target);
                }
            });
        }, { threshold: 0.12 });

        elementos.forEach(el => observador.observe(el));
    }

    // 4. EFECTO SCROLL EN NAVBAR
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 40) {
                navbar.style.boxShadow = '0 4px 20px rgba(13, 27, 46, 0.12)';
            } else {
                navbar.style.boxShadow = 'none';
            }
        });
    }
});