function mostrarAvisoParticipar(mensaje, tipo) {
    const aviso = document.getElementById("avisoFormParticipar");
    aviso.textContent = mensaje;
    aviso.className = `aviso-form ${tipo === "error" ? "aviso-form-error" : "aviso-form-exito"}`;
    aviso.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function mostrarMiembros(idEquipo) {
    document.querySelectorAll(".zona-miembros").forEach(div => {
        div.style.display = "none";
        div.querySelectorAll("input[type=checkbox]").forEach(cb => cb.checked = false);
    });
    if (idEquipo) {
        const div = document.getElementById("miembros-" + idEquipo);
        if (div) div.style.display = "block";
    }
}

function seleccionarMaximos(idZona, max) {
    const zona = document.getElementById(idZona);
    if (!zona) return;
    const checkboxes = zona.querySelectorAll("input[type=checkbox]");
    checkboxes.forEach(cb => cb.checked = false);
    let seleccionados = 0;
    checkboxes.forEach(cb => {
        if (seleccionados < max) {
            cb.checked = true;
            seleccionados++;
        }
    });
}

function limitarCheckboxes(checkbox, max) {
    const zona = checkbox.closest(".zona-miembros");
    if (!zona) return;
    const marcados = zona.querySelectorAll("input[type=checkbox]:checked");
    if (marcados.length > max) {
        checkbox.checked = false;
        mostrarAvisoParticipar(`Solo puedes seleccionar un máximo de ${max} miembros`, "error");
    }
}

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("formParticipar");
    if (!form) return;

    const esEquipo = form.dataset.equipo === "true";

    form.addEventListener("submit", function (e) {

        if (esEquipo) {
            const selectEquipo = form.querySelector("[name='id_equipo']");
            if (selectEquipo && !selectEquipo.value) {
                e.preventDefault();
                mostrarAvisoParticipar("Debes seleccionar un equipo", "error");
                return;
            }

            const zonaVisible = form.querySelector(".zona-miembros[style*='block']");
            if (zonaVisible) {
                const marcados = zonaVisible.querySelectorAll("input[type=checkbox]:checked");
                if (marcados.length === 0) {
                    e.preventDefault();
                    mostrarAvisoParticipar("Debes seleccionar al menos un miembro participante", "error");
                }
            }
            return;
        }

        const selects = form.querySelectorAll("select");
        let hayError = false;

        selects.forEach(select => {
            if (select.offsetParent !== null) {
                if (!select.value || select.value.trim() === "") {
                    hayError = true;
                }
            }
        });

        if (hayError) {
            e.preventDefault();
            mostrarAvisoParticipar("Debes seleccionar todas las opciones para participar en el torneo", "error");
        }

    });

});
