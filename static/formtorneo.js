function mostrarAvisoTorneo(mensaje, tipo) {
    const aviso = document.getElementById("avisoFormTorneo");
    aviso.textContent = mensaje;
    aviso.className = `aviso-form ${tipo === "error" ? "aviso-form-error" : "aviso-form-exito"}`;
    aviso.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

document.addEventListener("DOMContentLoaded", () => {

    const fechaInicio = document.getElementById("fecha_inicio");
    const fechaFinal = document.getElementById("fecha_final");
    const formTorneo = document.getElementById("formTorneo");
    const maxParticipantes = document.querySelector('[name="max_participantes"]');

    const hoy = new Date().toISOString().split("T")[0];

    if (fechaInicio) {
        fechaInicio.min = hoy;

        fechaInicio.addEventListener("change", () => {
            fechaFinal.min = fechaInicio.value;
        });
    }

    if (formTorneo) {
        formTorneo.addEventListener("submit", function(e) {

            const fechaInicioValor = fechaInicio.value;
            const fechaFinalValor = fechaFinal.value;
            const max = parseInt(maxParticipantes.value);

            if (fechaInicioValor < hoy) {
                mostrarAvisoTorneo("La fecha de inicio no puede ser anterior a hoy", "error");
                e.preventDefault();
                return;
            }

            if (fechaFinalValor < fechaInicioValor) {
                mostrarAvisoTorneo("La fecha final no puede ser menor que la fecha de inicio", "error");
                e.preventDefault();
                return;
            }

            if (![4, 8, 16, 32, 64, 128].includes(max)) {
                mostrarAvisoTorneo("El número máximo de participantes no es válido", "error");
                e.preventDefault();
                return;
            }

        });
    }

});