function mostrarAvisoUsuario(mensaje, tipo) {
    const aviso = document.getElementById("avisoFormUsuario");
    aviso.textContent = mensaje;
    aviso.className = `aviso-form ${tipo === "error" ? "aviso-form-error" : "aviso-form-exito"}`;
    aviso.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

document.getElementById("formRegistro").addEventListener("submit", async function (e) {
    e.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const apellidos = document.getElementById("apellidos").value.trim();
    const fecha_nacimiento = document.getElementById("fecha_nacimiento").value;
    const email = document.getElementById("email").value.trim();
    const nombre_usuario = document.getElementById("nombre_usuario").value.trim();
    const password = document.getElementById("password").value;

    const soloLetras = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (nombre.length < 2 || !soloLetras.test(nombre)) {
        mostrarAvisoUsuario("El nombre solo puede contener letras y debe tener al menos 2 caracteres", "error");
        return;
    }

    if (apellidos.length < 2 || !soloLetras.test(apellidos)) {
        mostrarAvisoUsuario("Los apellidos solo pueden contener letras y deben tener al menos 2 caracteres", "error");
        return;
    }

    const hoy = new Date().toISOString().split("T")[0];
    if (fecha_nacimiento > hoy) {
        mostrarAvisoUsuario("La fecha de nacimiento no puede ser futura", "error");
        return;
    }

    if (!emailRegex.test(email)) {
        mostrarAvisoUsuario("El email introducido no es válido", "error");
        return;
    }

    if (nombre_usuario.length < 3) {
        mostrarAvisoUsuario("El nombre de usuario debe tener al menos 3 caracteres", "error");
        return;
    }

    const data = { nombre, apellidos, fecha_nacimiento, email, nombre_usuario, password };

    try {
        const response = await fetch("/crear_usuario", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = "/";
        } else {
            mostrarAvisoUsuario(result.error || "Error al crear el usuario", "error");
        }

    } catch (error) {
        mostrarAvisoUsuario("Error de conexión, inténtalo de nuevo", "error");
    }
});

function volver() {
    window.location.href = "/";
}