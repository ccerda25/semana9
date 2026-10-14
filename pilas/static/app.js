const video = document.getElementById("video");
const canvas = document.getElementById("canvas");

const iniciarCamara = document.getElementById("iniciarCamara");
const tomarFoto = document.getElementById("tomarFoto");

const mensajeCamara = document.getElementById("mensajeCamara");

let stream = null;


iniciarCamara.addEventListener("click", async function () {

    try {

        stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });

        video.srcObject = stream;

        tomarFoto.disabled = false;

        mensajeCamara.innerHTML = `
            <div class="alert alert-success">
                Cámara activada correctamente.
            </div>
        `;

    } catch (error) {

        mensajeCamara.innerHTML = `
            <div class="alert alert-danger">
                No se pudo acceder a la cámara.
                Verifique los permisos del navegador.
            </div>
        `;

        console.error(error);
    }

});


tomarFoto.addEventListener("click", function () {

    if (!stream) {
        return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const contexto = canvas.getContext("2d");

    contexto.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    const imagen = canvas.toDataURL("image/jpeg");

    guardarFoto(imagen);

});


async function guardarFoto(imagen) {

    try {

        const respuesta = await fetch("/guardar-foto", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                imagen: imagen
            })

        });

        const resultado = await respuesta.json();

        if (resultado.exito) {

            mensajeCamara.innerHTML = `
                <div class="alert alert-success">
                    Foto guardada correctamente.
                </div>
            `;

            setTimeout(function () {
                location.reload();
            }, 1000);

        } else {

            mensajeCamara.innerHTML = `
                <div class="alert alert-danger">
                    ${resultado.mensaje}
                </div>
            `;

        }

    } catch (error) {

        console.error(error);

        mensajeCamara.innerHTML = `
            <div class="alert alert-danger">
                Ocurrió un error al guardar la foto.
            </div>
        `;

    }

}