const cloud = document.getElementById("cloud");
const barraLateral = document.querySelector(".barra-lateral");
const spans = document.querySelectorAll("span");
const palanca = document.querySelector(".switch");
const circulo = document.querySelector(".circulo");
const menu = document.querySelector(".menu");
const main = document.querySelector("main");

// ===== MODO OSCURO PERSISTENTE =====
// Inicializar modo oscuro al cargar la página
function initDarkMode() {
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    const body = document.body;
    
    if (savedDarkMode) {
        body.classList.add('dark-mode');
        if (circulo) circulo.classList.add('prendido');
    } else {
        body.classList.remove('dark-mode');
        if (circulo) circulo.classList.remove('prendido');
    }
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', initDarkMode);

// También inicializar si el script se carga después del DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDarkMode);
} else {
    initDarkMode();
}

// Event listener para el menú (botón de hamburguesa)
if (menu) {
    menu.addEventListener("click", () => {
        barraLateral.classList.toggle("max-barra-lateral");
        if (barraLateral.classList.contains("max-barra-lateral")) {
            menu.children[0].style.display = "none";
            menu.children[1].style.display = "block";
        } else {
            menu.children[0].style.display = "block";
            menu.children[1].style.display = "none";
        }
        if (window.innerWidth <= 320) {
            barraLateral.classList.add("mini-barra-lateral");
            main.classList.add("min-main");
            spans.forEach((span) => {
                span.classList.add("oculto");
            })
        }
    });
}

// Event listener para el switch de modo oscuro
if (palanca) {
    palanca.addEventListener("click", () => {
        let body = document.body;
        const isDarkMode = body.classList.toggle("dark-mode");
        if (circulo) circulo.classList.toggle("prendido");
        
        // Guardar preferencia en localStorage
        localStorage.setItem('darkMode', isDarkMode.toString());
    });
}

// Event listener para el botón de nube (minimizar/expandir sidebar)
if (cloud) {
    cloud.addEventListener("click", () => {
        barraLateral.classList.toggle("mini-barra-lateral");
        main.classList.toggle("min-main");
        spans.forEach((span) => {
            span.classList.toggle("oculto");
        });
    });
}