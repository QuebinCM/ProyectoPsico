function validarFormulario() {
    var preguntasSinResponder = [];

    for (var i = 1; i <= 21; i++) {
        var groupName = "preg-" + i;
        var radios = document.getElementsByName(groupName);
        var algunaOpcionMarcada = false;

        for (var j = 0; j < radios.length; j++) {
            if (radios[j].checked) {
                algunaOpcionMarcada = true;
                break;
            }
        }

        if (!algunaOpcionMarcada) {
            preguntasSinResponder.push('<div class="number-preg-alert"><h2>' + i + "</h2></div>");
        }
    }

    if (preguntasSinResponder.length === 21) {
        Swal.fire({
            icon: "warning",
            title: "No marcaste ninguna pregunta",
            confirmButtonText: "Aceptar",
        });
        return false;
    } else if (preguntasSinResponder.length > 0) {
        var mensaje =
            '<h3>Falta marcar las siguientes preguntas:</h3><div class="preg-alert-container">' +
            preguntasSinResponder.join("") +
            "</div>";
        Swal.fire({
            icon: "warning",
            title: "Preguntas sin marcar",
            html: mensaje,
            confirmButtonText: "Aceptar",
        });
        return false;
    }
    Swal.fire({
        icon: "succes",
        title: "Procesando respuestas",
        text: "Esto puedo tomar algo de tiempo",
        allowOutsideClick: false,
        showConfirmButton: false,
        willOpen: () => {
            Swal.showLoading();
        },
    });
    return true;
}
