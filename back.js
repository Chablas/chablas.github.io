document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const contenido = urlParams.get('nombre');
    const api_key = urlParams.get('DEVELOPMENT_API_KEY');
    document.getElementById('contenido-enviado').textContent = contenido;

    let api_url = "https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-name/";
    api_url += contenido;
    api_url += '?api_key=' + api_key;
    fetch(api_url)
    .then(response => {
        if (!response.ok) {
            throw new Error('La solicitud no pudo completarse');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});