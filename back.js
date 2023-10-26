document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const contenido = urlParams.get('contenido');
    document.getElementById('contenido-enviado').textContent = contenido;
});