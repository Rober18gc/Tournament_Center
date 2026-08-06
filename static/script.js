//INDEX.HTML
document.addEventListener("DOMContentLoaded", () => {

    let generoActivo = "";

    const btnMenu = document.getElementById('btnMenu');
    const sidebar = document.getElementById('sidebar');
    const btnLogin = document.getElementById('btnLogin');
    const loginBox = document.getElementById('loginBox');
    const registrarseBtn = document.getElementById('registrarseBtn');

    if(btnLogin && loginBox){
        btnLogin.addEventListener('click', (e) => {
            e.stopPropagation();
            loginBox.classList.toggle('show');
        });
    }

    if(btnMenu && sidebar){
        btnMenu.addEventListener('click', (e) => {
            e.stopPropagation();
            sidebar.classList.toggle('activo');
        });
    }

    document.addEventListener('click', () => {
        if(sidebar) sidebar.classList.remove('activo');
        if(loginBox) loginBox.classList.remove('show');
    });

    if(loginBox) loginBox.addEventListener('click', e => e.stopPropagation());
    if(sidebar) sidebar.addEventListener('click', e => e.stopPropagation());

    registrarseBtn?.addEventListener('click', () => {
        window.location.href = "formusuario";
    });

    // ===============================
    // 🔥 LIMPIAR VISTAS (IMPORTANTE)
    // ===============================

function limpiarSecciones() {

    const contenido = document.getElementById("contenido");
    if(!contenido) return;

    const ids = ["seccionPerfil", "seccionClasificacion"];

    ids.forEach(id => {
        const el = document.getElementById(id);
        if(el) el.style.display = "none";
    });
}

    // ===============================
    // MENÚS
    // ===============================
    window.toggleGeneros = function(){
        const submenu = document.getElementById("submenuGeneros");
        if(submenu) submenu.classList.toggle("show");
    };

    window.toggleTorneo = function(){
        const submenu = document.getElementById("submenuTorneo");
        if(submenu) submenu.classList.toggle("show");
    };

    window.toggleEquipos = function(){
        const submenu = document.getElementById("submenuEquipos");
        if(submenu) submenu.classList.toggle("show");
    };

    window.irACrearEquipo = function(){
        if (!window.usuarioLogueado) {
            abrirModalLoginCrearTorneo();
            return;
        }
        window.location.href = "/equipos/crear";
    };

    // ===============================
    // FILTRO JUEGOS (SEGURO)
    // ===============================
    window.mostrarJuegosGenero = function(genero){
        generoActivo = genero;

        const juegos = document.querySelectorAll(".juego");

        juegos.forEach(juego => {

            const g = juego.dataset.genero || "";

            // si no tiene género, no romper
            if(!juego.dataset.genero){
                juego.style.display = "block";
                return;
            }

            juego.style.display = (g === genero) ? "block" : "none";
        });

        const buscador = document.getElementById('buscador');
        if(buscador) buscador.value = "";
    };

    window.mostrarTodosJuegos = function(){
        const juegos = document.querySelectorAll(".juego");
        juegos.forEach(juego => juego.style.display="block");
    };

    window.buscarJuego = function(){

        const input = document.getElementById("buscador")?.value.toLowerCase() || "";
        const juegos = document.querySelectorAll(".juego");

        juegos.forEach(juego => {

            const nombre = (juego.dataset.nombre || "").toLowerCase();
            const genero = juego.dataset.genero || "";

            const coincideNombre = nombre.includes(input);
            const coincideGenero = (generoActivo === "" || genero === generoActivo);

            if(coincideNombre && coincideGenero){
                juego.style.display = "block";
            } else {
                juego.style.display = "none";
            }
        });
    };


// VOLVER INICIO

    window.volverInicio = function(){
        generoActivo = "";

        const buscador = document.getElementById('buscador');
        if(buscador) buscador.value = "";

        window.mostrarTodosJuegos();

        const inicio = document.getElementById("inicio");
        if(inicio) inicio.style.display = "block";

        const contenido = document.getElementById('contenido');

        if(contenido){
            Array.from(contenido.children).forEach(sec => {
                if(sec.id !== "inicio"){
                    sec.style.display = "none";
                }
            });
        }
    };


// CREAR TORNEO DESDE EL INDEX.HTML
    window.crearTorneo = function(tipo){
        if (!window.usuarioLogueado) {
            abrirModalLoginCrearTorneo();
            return;
        }
        window.location.href = `/seleccionar_juego`;
    };

    // ===============================
    // CLASIFICACION
    // ===============================
    window.verClasificacion = function(){
        limpiarSecciones();

        const contenido = document.getElementById('contenido');
        const inicio = document.getElementById("inicio");

        if(inicio) inicio.style.display = "none";

        let seccionClasificacion = document.getElementById("seccionClasificacion");

        if(!seccionClasificacion){
            seccionClasificacion = document.createElement("div");
            seccionClasificacion.id = "seccionClasificacion";
            contenido.appendChild(seccionClasificacion);
        }

        const juegos = [
            { id: 1, nombre: "Tekken 8" },
            { id: 2, nombre: "Street Fighter 6" },
            { id: 3, nombre: "Mortal Kombat 11" },
            { id: 4, nombre: "FIFA FC 26" },
            { id: 5, nombre: "NBA 2K26" },
            { id: 6, nombre: "Madden NFL 26" },
            { id: 7, nombre: "Battlefield 6" },
            { id: 8, nombre: "Call of Duty" },
            { id: 9, nombre: "Rainbow Six" }
        ];

        seccionClasificacion.innerHTML = `
            <h2 class="clasificacion-global-titulo">Clasificación Global</h2>
            <div class="clasificacion-global-grid" id="clasificacionGlobalGrid"></div>
        `;

        seccionClasificacion.style.display = "block";

        const grid = document.getElementById("clasificacionGlobalGrid");

        juegos.forEach(juego => {

            const seccionJuego = document.createElement("div");
            seccionJuego.className = "grupo-clasificacion-global";
            seccionJuego.innerHTML = `
                <h3>${juego.nombre}</h3>
                <div id="ranking-global-juego-${juego.id}">
                    <p class="cargando-ranking">Cargando...</p>
                </div>
            `;
            grid.appendChild(seccionJuego);

            cargarRankingEnContenedor(
                juego.id,
                document.getElementById(`ranking-global-juego-${juego.id}`)
            );
        });
    };


// PERFIL

    window.verPerfil = function() {
        if(!window.usuarioLogueado){
            _aviso("Acceso restringido", "Debes iniciar sesión para ver tu perfil", "info");
            return;
        }
        window.location.href = "/perfil";
    };

});

//------------------------------
//ZONA ADMINISTRADOR
//-----------------------------

const valoresOriginales = {};
const cambiosActuales = {};

// ===============================
// MODAL AVISO GENÉRICO
// ===============================

let _callbackAviso = null;
const _coloresAviso = { error: "#e53935", exito: "#28a745", info: "#00d4ff" };

function _aviso(titulo, mensaje, tipo = "info", callback = null) {
    const modal = document.getElementById("modalAviso");
    if (!modal) { alert(mensaje); if (callback) callback(); return; }
    document.getElementById("modalAvisoTitulo").textContent = titulo;
    document.getElementById("modalAvisoMensaje").textContent = mensaje;
    document.getElementById("modalAvisoTitulo").style.color = _coloresAviso[tipo] || _coloresAviso.info;
    _callbackAviso = callback;
    modal.classList.remove("oculto");
}

function _cerrarAviso() {
    document.getElementById("modalAviso")?.classList.add("oculto");
    if (_callbackAviso) { _callbackAviso(); _callbackAviso = null; }
}

// ===============================
// PAGINACIÓN GENÉRICA
// ===============================

const _estadoPagina = {};
const _ITEMS_PAGINA = 10;

function _actualizarPaginacion(idLista, selectorItems) {
    const lista = document.getElementById(idLista);
    const controles = document.getElementById(`paginacion-${idLista}`);
    if (!lista || !controles) return;

    const todos = Array.from(lista.querySelectorAll(`:scope > ${selectorItems}`));
    const visibles = todos.filter(el => !el.classList.contains("oculto"));

    todos.forEach(el => el.classList.remove("oculto-paginacion"));

    const total = visibles.length;
    const totalPaginas = Math.max(1, Math.ceil(total / _ITEMS_PAGINA));

    if (!_estadoPagina[idLista]) _estadoPagina[idLista] = 1;
    if (_estadoPagina[idLista] > totalPaginas) _estadoPagina[idLista] = totalPaginas;
    const pagina = _estadoPagina[idLista];

    const inicio = (pagina - 1) * _ITEMS_PAGINA;
    visibles.forEach((el, i) => {
        if (i < inicio || i >= inicio + _ITEMS_PAGINA) el.classList.add("oculto-paginacion");
    });

    if (total <= _ITEMS_PAGINA) {
        controles.classList.add("oculto");
    } else {
        controles.classList.remove("oculto");
        controles.querySelector(".pagina-actual-texto").textContent = `${pagina} / ${totalPaginas}`;
        controles.querySelectorAll(".btn-paginacion")[0].disabled = pagina <= 1;
        controles.querySelectorAll(".btn-paginacion")[1].disabled = pagina >= totalPaginas;
    }
}

function _cambiarPagina(idLista, selectorItems, delta) {
    if (!_estadoPagina[idLista]) _estadoPagina[idLista] = 1;
    _estadoPagina[idLista] += delta;
    _actualizarPaginacion(idLista, selectorItems);
}

function _resetPagina(idLista) {
    _estadoPagina[idLista] = 1;
}

function toggleDesplegable(cabecera) {
    const filaUsuario = cabecera.closest(".fila-usuario");
    const panelDesplegable = cabecera.nextElementSibling;
    const idUsuario = filaUsuario.dataset.id;
    const estaAbierto = !panelDesplegable.classList.contains("oculto");

    if (estaAbierto) {
        panelDesplegable.classList.add("oculto");
        cabecera.classList.remove("abierto");
    } else {
        panelDesplegable.classList.remove("oculto");
        cabecera.classList.add("abierto");
        capturarValoresOriginales(idUsuario, panelDesplegable);
    }
}

function capturarValoresOriginales(idUsuario, panelDesplegable) {
    if (valoresOriginales[idUsuario]) return;

    const snapshot = {};
    panelDesplegable.querySelectorAll(".dato-fila:not(.dato-solo-lectura)").forEach(filaDato => {
        const etiqueta = filaDato.querySelector(".etiqueta-dato")?.textContent;
        if (!etiqueta) return;
        const campo = mapaEtiquetasACampo[etiqueta];
        if (!campo) return;
        const spanValor = filaDato.querySelector(".valor-dato");
        snapshot[campo] = spanValor?.textContent.trim() ?? "";
    });

    valoresOriginales[idUsuario] = snapshot;
    cambiosActuales[idUsuario] = {};
}

function filtrarUsuarios(textoBuscado) {
    const textoEnMinusculas = textoBuscado.toLowerCase();
    document.querySelectorAll("#listaUsuarios .fila-usuario").forEach(filaUsuario => {
        const nombreVisible = filaUsuario.querySelector(".nombre-fila").textContent.toLowerCase();
        filaUsuario.classList.toggle("oculto", !nombreVisible.includes(textoEnMinusculas));
    });
    _resetPagina("listaUsuarios");
    _actualizarPaginacion("listaUsuarios", ".fila-usuario");
}

function ordenarUsuarios(criterioOrden) {
    const listaUsuarios = document.getElementById("listaUsuarios");
    const filasUsuario = Array.from(listaUsuarios.querySelectorAll(".fila-usuario"));

    filasUsuario.sort((filaA, filaB) => {
        switch (criterioOrden) {
            case "alfabetico":
                return filaA.dataset.nombre.localeCompare(filaB.dataset.nombre);
            case "edad":
                return new Date(filaA.dataset.fecha) - new Date(filaB.dataset.fecha);
            case "rol":
                return parseInt(filaA.dataset.rolOrden) - parseInt(filaB.dataset.rolOrden);
            case "torneos-participados":
                return parseInt(filaB.dataset.torneosParticipados) - parseInt(filaA.dataset.torneosParticipados);
            case "torneos-creados":
                return parseInt(filaB.dataset.torneosCreados) - parseInt(filaA.dataset.torneosCreados);
            case "torneos-ganados":
                return parseInt(filaB.dataset.torneosGanados) - parseInt(filaA.dataset.torneosGanados);
            default:
                return 0;
        }
    });

    filasUsuario.forEach(filaUsuario => listaUsuarios.appendChild(filaUsuario));
}

const mapaEtiquetasACampo = {
    "Nombre de usuario": "nombre_usuario",
    "Nombre": "nombre",
    "Apellidos": "apellidos",
    "Email": "email",
    "Rol": "rol"
};

function editarDato(evento, boton) {
    evento.stopPropagation();
    const filaDato = boton.closest(".dato-fila");
    const filaUsuario = boton.closest(".fila-usuario");
    const idUsuario = filaUsuario.dataset.id;
    const spanValor = filaDato.querySelector(".valor-dato");
    const etiquetaDato = filaDato.querySelector(".etiqueta-dato").textContent;

    if (spanValor.tagName === "INPUT" || spanValor.tagName === "SELECT") return;

    const textoActual = spanValor.textContent.trim();
    let campoEditable;

    if (etiquetaDato === "Rol") {
        campoEditable = document.createElement("select");
        campoEditable.className = "valor-dato input-edicion";
        ["Usuario", "Organizador", "Administrador"].forEach(opcionRol => {
            const elementoOpcion = document.createElement("option");
            elementoOpcion.value = opcionRol;
            elementoOpcion.textContent = opcionRol;
            if (opcionRol === textoActual) elementoOpcion.selected = true;
            campoEditable.appendChild(elementoOpcion);
        });
    } else {
        campoEditable = document.createElement("input");
        campoEditable.className = "valor-dato input-edicion";
        campoEditable.value = textoActual;
    }

    const eventoRastreo = campoEditable.tagName === "SELECT" ? "change" : "input";
    campoEditable.addEventListener(eventoRastreo, () => {
        const campo = mapaEtiquetasACampo[etiquetaDato];
        if (!campo) return;
        const valorOriginal = valoresOriginales[idUsuario]?.[campo] ?? "";
        const valorActual = campoEditable.tagName === "SELECT"
            ? campoEditable.options[campoEditable.selectedIndex].text
            : campoEditable.value.trim();
        if (!cambiosActuales[idUsuario]) cambiosActuales[idUsuario] = {};
        if (valorActual !== valorOriginal) {
            cambiosActuales[idUsuario][campo] = valorActual;
        } else {
            delete cambiosActuales[idUsuario][campo];
        }
        actualizarBotonAceptar(idUsuario);
    });

    spanValor.replaceWith(campoEditable);
    boton.textContent = "✅";
    boton.onclick = (evento) => confirmarEdicionDato(evento, boton, campoEditable);
    campoEditable.focus();
}

function confirmarEdicionDato(evento, boton, campoEditable) {
    evento.stopPropagation();

    const filaDato = boton.closest(".dato-fila");
    const filaUsuario = boton.closest(".fila-usuario");
    const idUsuario = filaUsuario.dataset.id;
    const etiquetaDato = filaDato.querySelector(".etiqueta-dato").textContent;
    const nombreCampo = mapaEtiquetasACampo[etiquetaDato];

    const nuevoValor = campoEditable.tagName === "SELECT"
        ? campoEditable.options[campoEditable.selectedIndex].text
        : campoEditable.value.trim();

    const spanValor = document.createElement("span");
    spanValor.className = "valor-dato";
    spanValor.textContent = nuevoValor;
    campoEditable.replaceWith(spanValor);
    boton.textContent = "✏️";
    boton.onclick = (evento) => editarDato(evento, boton);

    if (!nombreCampo) return;

    const valorOriginal = valoresOriginales[idUsuario]?.[nombreCampo] ?? "";
    if (!cambiosActuales[idUsuario]) cambiosActuales[idUsuario] = {};

    if (nuevoValor !== valorOriginal) {
        cambiosActuales[idUsuario][nombreCampo] = nuevoValor;
    } else {
        delete cambiosActuales[idUsuario][nombreCampo];
    }

    actualizarBotonAceptar(idUsuario);
}

function actualizarBotonAceptar(idUsuario) {
    const filaUsuario = document.querySelector(`.fila-usuario[data-id="${idUsuario}"]`);
    if (!filaUsuario) return;
    const btnAceptar = filaUsuario.querySelector(".btn-aceptar-cambios");
    if (!btnAceptar) return;
    const hayCambios = Object.keys(cambiosActuales[idUsuario] || {}).length > 0;
    btnAceptar.disabled = !hayCambios;
}

function aceptarCambiosUsuario(idUsuario) {
    const cambios = cambiosActuales[idUsuario];
    if (!cambios || Object.keys(cambios).length === 0) return;

    fetch(`/admin/editar_usuario/${idUsuario}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cambios)
    })
    .then(respuesta => respuesta.json())
    .then(datos => {
        if (datos.error) {
            mostrarModalErrorAdmin(datos.error);
        } else {
            mostrarAvisoAdmin("Cambios guardados", "exito");
            if (valoresOriginales[idUsuario]) {
                Object.assign(valoresOriginales[idUsuario], cambios);
            }
            cambiosActuales[idUsuario] = {};
            actualizarBotonAceptar(idUsuario);
            if (cambios.nombre_usuario) {
                const filaUsuario = document.querySelector(`.fila-usuario[data-id="${idUsuario}"]`);
                if (filaUsuario) {
                    filaUsuario.querySelector(".nombre-fila").textContent = cambios.nombre_usuario;
                    filaUsuario.dataset.nombre = cambios.nombre_usuario;
                }
            }
        }
    })
    .catch(() => mostrarAvisoAdmin("Error de red", "error"));
}

function restablecerCambiosUsuario(idUsuario) {
    const originales = valoresOriginales[idUsuario];
    if (!originales) return;

    const filaUsuario = document.querySelector(`.fila-usuario[data-id="${idUsuario}"]`);
    if (!filaUsuario) return;

    filaUsuario.querySelectorAll(".dato-fila:not(.dato-solo-lectura)").forEach(filaDato => {
        const etiqueta = filaDato.querySelector(".etiqueta-dato")?.textContent;
        if (!etiqueta) return;
        const campo = mapaEtiquetasACampo[etiqueta];
        if (!campo) return;

        const campoEditable = filaDato.querySelector(".input-edicion");
        const botonLapiz = filaDato.querySelector(".btn-lapiz-dato");

        if (campoEditable) {
            const spanValor = document.createElement("span");
            spanValor.className = "valor-dato";
            spanValor.textContent = originales[campo] ?? "";
            campoEditable.replaceWith(spanValor);
            if (botonLapiz) {
                botonLapiz.textContent = "✏️";
                botonLapiz.onclick = (evento) => editarDato(evento, botonLapiz);
            }
        } else {
            const spanValor = filaDato.querySelector(".valor-dato");
            if (spanValor) spanValor.textContent = originales[campo] ?? "";
        }
    });

    cambiosActuales[idUsuario] = {};
    actualizarBotonAceptar(idUsuario);

    const botonEditarTodo = filaUsuario.querySelector(".btn-lapiz[data-modo-edicion], .btn-lapiz");
    if (botonEditarTodo && botonEditarTodo.dataset.modoEdicion === "true") {
        botonEditarTodo.textContent = "✏️";
        botonEditarTodo.dataset.modoEdicion = "false";
    }
}

function toggleVerPassword(evento, idUsuario) {
    evento.stopPropagation();
    const filaUsuario = document.querySelector(`.fila-usuario[data-id="${idUsuario}"]`);
    if (!filaUsuario) return;
    const spanPassword = filaUsuario.querySelector(".span-password");
    const btnOjo = filaUsuario.querySelector(".btn-ojo");
    if (!spanPassword || !btnOjo) return;

    const passwordReal = filaUsuario.dataset.password;
    const estaVisible = spanPassword.dataset.visible === "true";

    if (estaVisible) {
        spanPassword.textContent = "••••••••";
        spanPassword.dataset.visible = "false";
        btnOjo.textContent = "👁️";
    } else {
        spanPassword.textContent = passwordReal;
        spanPassword.dataset.visible = "true";
        btnOjo.textContent = "🔒";
    }
}

function mostrarModalErrorAdmin(mensaje) {
    document.getElementById("textoModalErrorAdmin").textContent = mensaje;
    document.getElementById("modalErrorAdmin").classList.remove("oculto");
}

function cerrarModalErrorAdmin() {
    document.getElementById("modalErrorAdmin").classList.add("oculto");
}

function mostrarAvisoAdmin(mensaje, tipo) {
    let aviso = document.getElementById("avisoAdmin");
    if (!aviso) {
        aviso = document.createElement("div");
        aviso.id = "avisoAdmin";
        aviso.className = "aviso-admin";
        document.querySelector(".panel-admin").prepend(aviso);
    }
    aviso.textContent = mensaje;
    aviso.className = `aviso-admin aviso-${tipo}`;
    aviso.classList.remove("oculto");
    clearTimeout(aviso._temporizador);
    aviso._temporizador = setTimeout(() => aviso.classList.add("oculto"), 3000);
}

function editarTodo(evento, boton) {
    evento.stopPropagation();
    const filaUsuario = boton.closest(".fila-usuario");
    const panelDesplegable = filaUsuario.querySelector(".panel-desplegable");
    const idUsuario = filaUsuario.dataset.id;

    if (panelDesplegable.classList.contains("oculto")) {
        panelDesplegable.classList.remove("oculto");
        filaUsuario.querySelector(".cabecera-fila").classList.add("abierto");
        capturarValoresOriginales(idUsuario, panelDesplegable);
    }

    const enModoEdicion = boton.dataset.modoEdicion === "true";

    if (enModoEdicion) {
        panelDesplegable.querySelectorAll(".btn-lapiz-dato").forEach(lapiz => {
            const campoEditable = lapiz.closest(".dato-fila").querySelector(".input-edicion");
            if (campoEditable) confirmarEdicionDato(evento, lapiz, campoEditable);
        });
        boton.textContent = "✏️";
        boton.dataset.modoEdicion = "false";
    } else {
        panelDesplegable.querySelectorAll(".btn-lapiz-dato").forEach(lapiz => {
            const spanValor = lapiz.closest(".dato-fila").querySelector(".valor-dato");
            if (spanValor && spanValor.tagName !== "INPUT" && spanValor.tagName !== "SELECT") {
                editarDato(evento, lapiz);
            }
        });
        boton.textContent = "✅";
        boton.dataset.modoEdicion = "true";
    }
}

let idUsuarioABorrar = null;

function abrirModalBorrar(evento, idUsuario, nombreUsuario) {
    evento.stopPropagation();
    idUsuarioABorrar = idUsuario;
    document.getElementById("nombreUsuarioBorrar").textContent = nombreUsuario;
    document.getElementById("modalConfirmarBorrar").classList.remove("oculto");
}

function cerrarModalBorrar() {
    idUsuarioABorrar = null;
    document.getElementById("modalConfirmarBorrar").classList.add("oculto");
}

function confirmarBorrar() {
    if (!idUsuarioABorrar) return;

    fetch(`/admin/borrar_usuario/${idUsuarioABorrar}`, { method: "DELETE" })
        .then(respuesta => respuesta.json())
        .then(datos => {
            if (datos.error) {
                _aviso("Error", datos.error, "error");
            } else {
                const filaUsuario = document.querySelector(`.fila-usuario[data-id="${idUsuarioABorrar}"]`);
                if (filaUsuario) filaUsuario.remove();
                delete valoresOriginales[idUsuarioABorrar];
                delete cambiosActuales[idUsuarioABorrar];
                cerrarModalBorrar();
            }
        });
}

document.addEventListener("DOMContentLoaded", () => {
    const enlaceCerrarSesion = document.querySelector('a[href="/logout"]');
    if (!enlaceCerrarSesion) return;

    enlaceCerrarSesion.addEventListener("click", (evento) => {
        const usuariosConCambios = Object.entries(cambiosActuales).filter(
            ([idUsuario, cambios]) => Object.keys(cambios).length > 0
        );
        if (usuariosConCambios.length === 0) return;

        evento.preventDefault();
        mostrarModalCambiosPendientes(usuariosConCambios, enlaceCerrarSesion.href);
    });
});

function mostrarModalCambiosPendientes(usuariosConCambios, urlCerrarSesion) {
    const modal = document.getElementById("modalCambiosPendientes");
    const listaCambios = document.getElementById("listaCambiosPendientes");
    if (!modal || !listaCambios) return;

    listaCambios.innerHTML = "";
    usuariosConCambios.forEach(([idUsuario, cambios]) => {
        const filaUsuario = document.querySelector(`.fila-usuario[data-id="${idUsuario}"]`);
        const nombreUsuario = filaUsuario?.querySelector(".nombre-fila")?.textContent || `ID ${idUsuario}`;
        const camposModificados = Object.keys(cambios).join(", ");
        const elemento = document.createElement("li");
        elemento.textContent = `${nombreUsuario}: ${camposModificados}`;
        listaCambios.appendChild(elemento);
    });

    modal.dataset.urlSesion = urlCerrarSesion;
    modal.classList.remove("oculto");
}

function aceptarCambiosPendientesYSalir() {
    const modal = document.getElementById("modalCambiosPendientes");
    const urlCerrarSesion = modal.dataset.urlSesion;

    const promesas = Object.entries(cambiosActuales)
        .filter(([idUsuario, cambios]) => Object.keys(cambios).length > 0)
        .map(([idUsuario, cambios]) =>
            fetch(`/admin/editar_usuario/${idUsuario}`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(cambios)
            })
        );

    Promise.all(promesas).finally(() => {
        window.location.href = urlCerrarSesion;
    });
}

function rechazarCambiosPendientesYSalir() {
    const modal = document.getElementById("modalCambiosPendientes");
    const urlCerrarSesion = modal.dataset.urlSesion;
    window.location.href = urlCerrarSesion;
}

function revisarCambiosPendientes() {
    document.getElementById("modalCambiosPendientes").classList.add("oculto");
}

//------------------------------
//ZONA PERFIL
//-----------------------------

const mapaEtiquetasACampoPerfil = {
    "Nombre": "nombre",
    "Apellidos": "apellidos",
    "Nombre de usuario": "nombre_usuario",
    "Email": "email"
};

const valoresOriginalesPerfil = {};
const cambiosPerfil = {};

document.addEventListener("DOMContentLoaded", () => {
    const tarjetaPerfil = document.getElementById("tarjetaPerfil");
    if (!tarjetaPerfil) return;

    document.querySelectorAll(".info-item.info-editable").forEach(itemEditable => {
        const etiqueta = itemEditable.querySelector(".etiqueta-perfil")?.textContent;
        if (!etiqueta) return;
        const campo = mapaEtiquetasACampoPerfil[etiqueta];
        if (!campo) return;
        const valorActual = itemEditable.querySelector(".valor-perfil")?.textContent.trim() ?? "";
        valoresOriginalesPerfil[campo] = valorActual;
    });
});

function editarDatoPerfil(evento, boton) {
    evento.stopPropagation();
    const itemInfo = boton.closest(".info-item");
    const etiqueta = itemInfo.querySelector(".etiqueta-perfil")?.textContent;
    const parrafoValor = itemInfo.querySelector(".valor-perfil");

    if (parrafoValor.tagName === "INPUT") return;

    const textoActual = parrafoValor.textContent.trim();
    const campoEditable = document.createElement("input");
    campoEditable.className = "valor-perfil input-perfil-edicion";
    campoEditable.value = textoActual;

    campoEditable.addEventListener("input", () => {
        const campo = mapaEtiquetasACampoPerfil[etiqueta];
        if (!campo) return;
        const valorOriginal = valoresOriginalesPerfil[campo] ?? "";
        const valorActual = campoEditable.value.trim();
        if (valorActual !== valorOriginal) {
            cambiosPerfil[campo] = valorActual;
        } else {
            delete cambiosPerfil[campo];
        }
        actualizarBotonAceptarPerfil();
    });

    parrafoValor.replaceWith(campoEditable);
    boton.textContent = "✅";
    boton.onclick = (evento) => confirmarEdicionPerfil(evento, boton, campoEditable);
    campoEditable.focus();
}

function confirmarEdicionPerfil(evento, boton, campoEditable) {
    evento.stopPropagation();
    const itemInfo = boton.closest(".info-item");
    const etiqueta = itemInfo.querySelector(".etiqueta-perfil")?.textContent;
    const nombreCampo = mapaEtiquetasACampoPerfil[etiqueta];
    const nuevoValor = campoEditable.value.trim();

    const parrafoValor = document.createElement("p");
    parrafoValor.className = "valor-perfil";
    parrafoValor.textContent = nuevoValor;
    campoEditable.replaceWith(parrafoValor);
    boton.textContent = "✏️";
    boton.onclick = (evento) => editarDatoPerfil(evento, boton);

    if (!nombreCampo) return;

    const valorOriginal = valoresOriginalesPerfil[nombreCampo] ?? "";
    if (nuevoValor !== valorOriginal) {
        cambiosPerfil[nombreCampo] = nuevoValor;
    } else {
        delete cambiosPerfil[nombreCampo];
    }

    actualizarBotonAceptarPerfil();
}

function toggleVerPasswordPerfil(evento) {
    evento.stopPropagation();
    const itemPassword = document.getElementById("itemPassword");
    const spanPassword = itemPassword.querySelector(".span-password-perfil");
    const botonOjo = itemPassword.querySelector(".btn-perfil-ojo");
    const passwordReal = itemPassword.dataset.password;
    const estaVisible = spanPassword.dataset.visible === "true";

    if (estaVisible) {
        spanPassword.textContent = "••••••••";
        spanPassword.dataset.visible = "false";
        botonOjo.textContent = "👁️";
    } else {
        spanPassword.textContent = passwordReal;
        spanPassword.dataset.visible = "true";
        botonOjo.textContent = "🔒";
    }
}

function toggleEditarPasswordPerfil(evento, boton) {
    evento.stopPropagation();
    const contenedorNuevaPassword = document.getElementById("nuevaPasswordContenedor");
    const estaOculto = contenedorNuevaPassword.classList.contains("oculto");

    if (estaOculto) {
        contenedorNuevaPassword.classList.remove("oculto");
        const inputPassword = document.getElementById("inputNuevaPassword");
        inputPassword.focus();
        inputPassword.addEventListener("input", () => {
            if (inputPassword.value.trim()) {
                cambiosPerfil["password"] = inputPassword.value.trim();
            } else {
                delete cambiosPerfil["password"];
            }
            actualizarBotonAceptarPerfil();
        });
        boton.textContent = "✅";
        boton.onclick = (evento) => confirmarNuevaPassword(evento, boton);
    } else {
        contenedorNuevaPassword.classList.add("oculto");
        document.getElementById("inputNuevaPassword").value = "";
        delete cambiosPerfil["password"];
        boton.textContent = "✏️";
        boton.onclick = (evento) => toggleEditarPasswordPerfil(evento, boton);
        actualizarBotonAceptarPerfil();
    }
}

function confirmarNuevaPassword(evento, boton) {
    evento.stopPropagation();
    const inputNuevaPassword = document.getElementById("inputNuevaPassword");
    const nuevaPassword = inputNuevaPassword.value.trim();

    if (!nuevaPassword) return;

    cambiosPerfil["password"] = nuevaPassword;

    const botonLapizPassword = document.querySelector("#itemPassword .btn-perfil-lapiz:not(.btn-perfil-ojo)");
    document.getElementById("nuevaPasswordContenedor").classList.add("oculto");
    inputNuevaPassword.value = "";

    if (botonLapizPassword) {
        botonLapizPassword.textContent = "✏️";
        botonLapizPassword.onclick = (evento) => toggleEditarPasswordPerfil(evento, botonLapizPassword);
    }

    actualizarBotonAceptarPerfil();
}

function actualizarBotonAceptarPerfil() {
    const botonAceptar = document.getElementById("btnAceptarCambiosPerfil");
    if (!botonAceptar) return;
    botonAceptar.disabled = Object.keys(cambiosPerfil).length === 0;
}

function abrirModalConfirmarCambiosPerfil() {
    const mensajeError = document.getElementById("mensajeErrorPerfil");
    if (mensajeError) {
        mensajeError.textContent = "";
        mensajeError.style.display = "none";
    }
    document.getElementById("modalConfirmarCambiosPerfil").classList.remove("oculto");
}

function cerrarModalConfirmarCambiosPerfil() {
    document.getElementById("modalConfirmarCambiosPerfil").classList.add("oculto");
}

function confirmarCambiosPerfil() {
    if (Object.keys(cambiosPerfil).length === 0) return;

    fetch("/editar_mi_perfil", {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cambiosPerfil)
    })
    .then(respuesta => respuesta.json())
    .then(datos => {
        if (datos.error) {
            const mensajeError = document.getElementById("mensajeErrorPerfil");
            mensajeError.textContent = datos.error;
            mensajeError.style.display = "block";
            return;
        }

        cerrarModalConfirmarCambiosPerfil();

        if (cambiosPerfil.nombre || cambiosPerfil.apellidos) {
            const nombreActual = cambiosPerfil.nombre ?? valoresOriginalesPerfil.nombre;
            const apellidosActual = cambiosPerfil.apellidos ?? valoresOriginalesPerfil.apellidos;
            document.getElementById("headerNombreCompleto").textContent = `${nombreActual} ${apellidosActual}`;
        }

        if (cambiosPerfil.password) {
            const itemPassword = document.getElementById("itemPassword");
            itemPassword.dataset.password = cambiosPerfil.password;
            const spanPassword = itemPassword.querySelector(".span-password-perfil");
            if (spanPassword.dataset.visible === "true") {
                spanPassword.textContent = cambiosPerfil.password;
            }
        }

        Object.assign(valoresOriginalesPerfil, cambiosPerfil);
        Object.keys(cambiosPerfil).forEach(campo => delete cambiosPerfil[campo]);
        actualizarBotonAceptarPerfil();
    })
    .catch(() => {
        const mensajeError = document.getElementById("mensajeErrorPerfil");
        mensajeError.textContent = "Error de red, inténtalo de nuevo";
        mensajeError.style.display = "block";
    });
}

function abrirModalBorrarCuenta() {
    document.getElementById("modalBorrarCuenta").classList.remove("oculto");
}

function cerrarModalBorrarCuenta() {
    document.getElementById("modalBorrarCuenta").classList.add("oculto");
}

function confirmarBorrarCuenta() {
    fetch("/borrar_mi_cuenta", { method: "DELETE" })
        .then(respuesta => respuesta.json())
        .then(datos => {
            if (datos.error) {
                const mensajeError = document.getElementById("mensajeErrorBorrar");
                mensajeError.textContent = datos.error;
                mensajeError.style.display = "block";
            } else {
                window.location.href = "/";
            }
        });
}

//------------------------------
//JUEGO.HTML
//-----------------------------


//CARGAR TORNEOS EN JUEGOS.HTML

window.cargarTorneos = function () {

    const contenedor = document.getElementById("listaTorneosActivos");
    if (!contenedor) return;

    const id_juego = contenedor.dataset.juego;

    fetch(`/mostrar_torneo/${id_juego}`)
        .then(res => res.json())
        .then(data => {

            const contenedorActivos = document.getElementById("listaTorneosActivos");
            const contenedorFinalizados = document.getElementById("listaTorneosFinalizados");

            if (contenedorActivos) contenedorActivos.innerHTML = "";
            if (contenedorFinalizados) contenedorFinalizados.innerHTML = "";

            if (!data || data.length === 0) {
                if (contenedorActivos) contenedorActivos.innerHTML = "<p>No hay torneos disponibles</p>";
                return;
            }

            const activos = data.filter(t => t.estado !== "Finalizado");
            const finalizados = data.filter(t => t.estado === "Finalizado");

            if (activos.length === 0 && contenedorActivos) {
                contenedorActivos.innerHTML = "<p>No hay torneos activos</p>";
            }
            if (finalizados.length === 0 && contenedorFinalizados) {
                contenedorFinalizados.innerHTML = "<p>No hay torneos finalizados</p>";
            }

            [...activos, ...finalizados].forEach(torneo => {
                const destino = torneo.estado === "Finalizado" ? contenedorFinalizados : contenedorActivos;
                if (!destino) return;

                const imgSrc = torneo.portada && torneo.portada.startsWith("http")
                    ? torneo.portada
                    : `/static/imagenes/portadas/${torneo.portada || "Logo.png"}`;

            const torneoCerrado = torneo.estado === "Cerrado";
            const torneoLleno = torneo.participantes_totales >= torneo.max_participantes;

//solo organizador puede ver el botón
                const esOrganizador = torneo.es_creador;

                destino.innerHTML += `
                    <div class="torneo-card ${torneo.estado === 'Finalizado' ? 'torneo-finalizado' : ''}"
                        onclick="window.location.href='/torneo/${torneo.id_torneo}'"
                        style="cursor:pointer;">

                        <img src="${imgSrc}">

                        <div class="torneo-info-boton">

                            <div class="torneo-info">

                                <h3 onclick="event.stopPropagation(); window.location.href='/torneo/${torneo.id_torneo}'">
                                    ${torneo.nombre}
                                </h3>

                                <p>${torneo.descripcion}</p>

                                <p class="participantes">
                                    ${torneo.participantes_totales} / ${torneo.max_participantes} ${torneo.es_equipo ? 'equipos' : 'jugadores'}
                                </p>

                                <span class="fecha">
                                    ${torneo.fecha_inicio} - ${torneo.fecha_final}
                                </span>

                            </div>

                            <div class="botones-torneo">
                            ${torneo.estado === 'Finalizado' ? `
                            <button class="btn-participar btn-candado"
                            onclick="event.stopPropagation(); _aviso('Torneo finalizado', 'Ganador: ${torneo.ganador || 'Desconocido'}', 'exito');">
                            Finalizado
                            </button>

                            ` : torneo.ya_inscrito ? `
                            <button class="btn-participar btn-candado"
                            onclick="event.stopPropagation(); _aviso('Torneo', 'Ya estás inscrito en este torneo', 'info');">
                            Inscrito 🔒
                            <span class="tooltip-text">Ya estás inscrito en este torneo</span>
                            </button>

                            ` : torneoCerrado ? `
                            <button class="btn-participar btn-candado"
                            onclick="event.stopPropagation(); _aviso('Torneo cerrado', 'Este torneo ya no admite nuevos participantes', 'info');">
                            Cerrado 🔒
                            </button>

                            ` : torneoLleno ? `
                            <button class="btn-participar btn-candado"
                            onclick="event.stopPropagation(); _aviso('Torneo lleno', 'Este torneo ya ha alcanzado el máximo de participantes', 'info');">
                            Torneo lleno 🔒
                            </button>

                            ` : `
                            <button class="btn-participar"
                            onclick="event.stopPropagation();
                            if(!window.usuarioLogueado){
                            abrirModalLogin();
                            } else {
                            window.location.href='/participar_torneo/${torneo.id_torneo}';}">
                            Participar
                            </button>
                            `}

                            ${esOrganizador ? `
                            <button class="btn-cerrar-torneo"
                            onclick="event.stopPropagation(); cerrarTorneo(${torneo.id_torneo})">
                            Cerrar torneo
                            </button>
                            ` : ""}

                            </div>
                        </div>
                    </div>
                `;
            });

        })
        .catch(err => console.error(err));
};

window.abrirModalLogin = function () {
    const modal = document.getElementById("modalLoginTorneo");
    if(modal){
        modal.classList.remove("oculto");
    }
};

window.cerrarModalLogin = function () {
    const modal = document.getElementById("modalLoginTorneo");
    if(modal){
        modal.classList.add("oculto");
    }
};

window.abrirModalLoginCrearTorneo = function () {
    const modal = document.getElementById("modalLoginCrearTorneo");
    if(modal){
        modal.classList.remove("oculto");
    }
};

window.cerrarModalLoginCrearTorneo = function () {
    const modal = document.getElementById("modalLoginCrearTorneo");
    if(modal){
        modal.classList.add("oculto");
    }
};

window.mostrarLogin = function () {
    cerrarModalLogin();

    const loginBox = document.getElementById("loginBox");
    if(loginBox){
        loginBox.classList.add("show");
    }
};

// ===============================
document.addEventListener("DOMContentLoaded", () => {

    const contenedor = document.getElementById("listaTorneos");

    if(!contenedor) return;

    const id_juego = contenedor.dataset.juego;

    if(id_juego){
        cargarTorneos(id_juego);
    }
});


// JUGADORES ACTIVOS
window.cargarJugadoresActivos = function () {

    const contenedor = document.getElementById("jugadoresActivos");

    if (!contenedor) return;

    const idJuego = contenedor.dataset.juego;
    const esEquipo = contenedor.dataset.esEquipo === "true";

    fetch(`/juego/${idJuego}/jugadores_activos`)
        .then(res => {
            if (!res.ok) throw new Error("Error cargando activos");
            return res.json();
        })
        .then(data => {
            contenedor.innerHTML = "";

            if (!data || data.length === 0) {
                contenedor.innerHTML = `<p>${esEquipo ? 'No hay equipos activos' : 'No hay jugadores activos'}</p>`;
                return;
            }

            data.forEach(item => {
                contenedor.innerHTML += `
                    <div class="usuario-card" ${item.id_usuario ? `data-usuario-id="${item.id_usuario}"` : ''}>
                        ${item.usuario}
                    </div>
                `;
            });
        })
        .catch(err => {
            console.error("Error activos:", err);
            contenedor.innerHTML = `<p>Error cargando datos</p>`;
        });
};

document.addEventListener("DOMContentLoaded", () => {

    cargarJugadoresActivos();

});

// ===============================
// RANKING JUEGO
// ===============================

window.cargarRankingJuego = function(idJuego) {

    const contenedor = document.getElementById("rankingJuego");
    if (!contenedor) return;

    const esEquipo = contenedor.dataset.esEquipo === "true";

    fetch(`/juego/${idJuego}/ranking`)
        .then(respuesta => respuesta.json())
        .then(datos => {

            if (!datos || datos.length === 0) {
                contenedor.innerHTML = "<p>No hay datos de ranking aún</p>";
                return;
            }

            const colNombre = esEquipo ? "EQUIPO" : "JUGADOR";

            let html = `
                <table class="tabla-ranking">
                    <thead>
                        <tr>
                            <th>POS</th>
                            <th>${colNombre}</th>
                            <th>TP</th>
                            <th>TG</th>
                            <th>WT</th>
                            <th>PJ</th>
                            <th>PG</th>
                            <th>PP</th>
                            <th>PE</th>
                            <th>RG</th>
                            <th>RP</th>
                            <th>DR</th>
                            <th>PTS</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            datos.forEach(jugador => {
                const winrate = (jugador.wt * 100).toFixed(0) + "%";
                html += `
                    <tr>
                        <td>${jugador.pos}</td>
                        <td>${jugador.usuario}</td>
                        <td>${jugador.tp}</td>
                        <td>${jugador.tg}</td>
                        <td>${winrate}</td>
                        <td>${jugador.pj}</td>
                        <td>${jugador.pg}</td>
                        <td>${jugador.pp}</td>
                        <td>${jugador.pe}</td>
                        <td>${jugador.rg}</td>
                        <td>${jugador.rp}</td>
                        <td>${jugador.dr}</td>
                        <td>${jugador.pts}</td>
                    </tr>
                `;
            });

            html += `</tbody></table>`;
            contenedor.innerHTML = html;
        })
        .catch(error => {
            console.error("Error cargando ranking:", error);
            contenedor.innerHTML = "<p>Error cargando ranking</p>";
        });
};

document.addEventListener("DOMContentLoaded", () => {

    const contenedor = document.getElementById("rankingJuego");
    if (!contenedor) return;

    const idJuego = contenedor.dataset.juego;
    if (idJuego) cargarRankingJuego(idJuego);

});

function cargarRankingEnContenedor(idJuego, contenedor) {

    fetch(`/juego/${idJuego}/ranking`)
        .then(respuesta => respuesta.json())
        .then(datos => {

            if (!datos || datos.length === 0) {
                contenedor.innerHTML = "<p class='sin-datos-ranking'>Sin datos aún</p>";
                return;
            }

            let html = `
                <div class="scroll-ranking-global">
                <table class="tabla-ranking-global">
                    <thead>
                        <tr>
                            <th>POS</th>
                            <th>JUGADOR</th>
                            <th>TP</th>
                            <th>TG</th>
                            <th>WT</th>
                            <th>PJ</th>
                            <th>PG</th>
                            <th>PP</th>
                            <th>PE</th>
                            <th>RG</th>
                            <th>RP</th>
                            <th>DR</th>
                            <th>PTS</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            datos.forEach(jugador => {
                const winrate = (jugador.wt * 100).toFixed(0) + "%";
                html += `
                    <tr onclick="window.location.href='/juego/${idJuego}'" style="cursor:pointer;">
                        <td>${jugador.pos}</td>
                        <td>${jugador.usuario}</td>
                        <td>${jugador.tp}</td>
                        <td>${jugador.tg}</td>
                        <td>${winrate}</td>
                        <td>${jugador.pj}</td>
                        <td>${jugador.pg}</td>
                        <td>${jugador.pp}</td>
                        <td>${jugador.pe}</td>
                        <td>${jugador.rg}</td>
                        <td>${jugador.rp}</td>
                        <td>${jugador.dr}</td>
                        <td>${jugador.pts}</td>
                    </tr>
                `;
            });

            html += `</tbody></table></div>`;
            contenedor.innerHTML = html;
        })
        .catch(error => {
            console.error("Error cargando ranking:", error);
            contenedor.innerHTML = "<p class='sin-datos-ranking'>Error cargando ranking</p>";
        });
}

//----------------------
//TORNEO.HTML
//----------------------

document.addEventListener("DOMContentLoaded", () => {

    const usuarios = document.querySelectorAll(".usuario-card");

    const rivalBox = document.getElementById("rivalBox");
    const rivalNombre = document.getElementById("rivalNombre");
    const rivalExtra = document.getElementById("rivalExtra");
    const rivalVictorias = document.getElementById("rivalVictorias");
    const rivalDerrotas = document.getElementById("rivalDerrotas");
    const rivalEmpates = document.getElementById("rivalEmpates");

    //Seguridad DOM
   if (!rivalBox || !rivalNombre || !rivalExtra || !rivalVictorias || !rivalDerrotas || !rivalEmpates) {
    // simplemente salimos sin spamear consola
    return;
}

    usuarios.forEach(usuario => {

        usuario.addEventListener("click", () => {

            // quitar selección previa
            usuarios.forEach(u => u.classList.remove("seleccionado"));
            usuario.classList.add("seleccionado");

            const idUsuario = usuario.dataset.usuarioId;
            const idEquipo = usuario.dataset.equipoId;
            const idTorneo = window.location.pathname.split("/").pop();

            // 🔥 reset antes de cargar nuevo rival
            rivalBox.classList.remove("activo");

            rivalNombre.textContent = "Cargando...";
            rivalExtra.textContent = "";
            rivalVictorias.textContent = "";
            rivalDerrotas.textContent = "";
            rivalEmpates.textContent = "";

            if (idEquipo) {
                cargarRivalEquipo(idTorneo, idEquipo);
                return;
            }

            fetch(`/torneo/${idTorneo}/mostrar_participante/${idUsuario}`)
                .then(res => {
                    if (!res.ok) {
                        throw new Error("Error al obtener datos del rival");
                    }
                    return res.json();
                })
                .then(data => {

                    rivalNombre.textContent = data.usuario || "Sin nombre";

                    if (data.personaje) {
                        rivalExtra.textContent =  data.personaje;
                    } else if (data.club) {
                        rivalExtra.textContent = data.club;
                    } else {
                        rivalExtra.textContent = "";
                    }

                    rivalVictorias.textContent = "Victorias: " + (data.victorias ?? 0);
                    rivalDerrotas.textContent = "Derrotas: " + (data.derrotas ?? 0);
                    rivalEmpates.textContent = "Empates: " + (data.empates ?? 0);

                    // mostrar card
                    rivalBox.classList.add("activo");
                })
                .catch(err => {
                    console.error(err);

                    rivalNombre.textContent = "Error";
                    rivalExtra.textContent = "No se pudo cargar el rival";
                });

        });

    });

});

window.cerrarTorneo = function (id_torneo) {

    fetch(`/cerrar_torneo/${id_torneo}`, {
        method: "POST"
    })
    .then(async res => {

        const data = await res.json().catch(() => null);

        if (!res.ok) {
            _aviso("Error", data?.error || "Error al cerrar torneo", "error");
            return;
        }

        _aviso("Torneo cerrado", data.mensaje, "exito", () => location.reload());
    })
    .catch(err => {
        console.error(err);
        _aviso("Error de red", "No se pudo conectar con el servidor", "error");
    });
};

// ===============================
// 🔥 GRUPOS TORNEO
// ===============================
window.cargarGrupos = function(id_torneo) {

    const contenedor = document.getElementById("gruposTorneo");
    if (!contenedor) return;

    fetch(`/torneo/${id_torneo}/grupos`)
        .then(res => res.json())
        .then(data => {

            contenedor.innerHTML = "";

            if (!data || data.length === 0) {
                contenedor.innerHTML = "<p>No hay grupos generados</p>";
                return;
            }

            data.forEach(grupo => {

                let jugadoresHTML = "";

                grupo.participantes.forEach(p => {
                const dataAttr = p.id_equipo
                    ? `data-equipo-id="${p.id_equipo}"`
                    : `data-usuario-id="${p.id_usuario}"`;
                jugadoresHTML += `<li class="grupo-jugador" ${dataAttr}>
                ${p.usuario}
                </li>
                `;
                });

                contenedor.innerHTML += `
                    <div class="grupo-card">
                        <h3>Grupo ${grupo.grupo}</h3>
                        <ul>
                            ${jugadoresHTML}
                        </ul>
                    </div>
                `;
                const jugadoresGrupo = contenedor.querySelectorAll(".grupo-jugador");
                jugadoresGrupo.forEach(jugador => {
                jugador.addEventListener("click", () => {
                const idEquipoG = jugador.dataset.equipoId;
                const idUsuarioG = jugador.dataset.usuarioId;
                if (idEquipoG) {
                    cargarRivalEquipo(id_torneo, idEquipoG);
                } else {
                    cargarRival(id_torneo, idUsuarioG);
                }
                });
                });
            });

        })
        .catch(err => console.error(err));
};

window.cargarRival = function(idTorneo, idUsuario) {

    const rivalBox = document.getElementById("rivalBox");
    const rivalNombre = document.getElementById("rivalNombre");
    const rivalExtra = document.getElementById("rivalExtra");
    const rivalVictorias = document.getElementById("rivalVictorias");
    const rivalDerrotas = document.getElementById("rivalDerrotas");
    const rivalEmpates = document.getElementById("rivalEmpates");

    rivalBox.classList.remove("activo");

    rivalNombre.textContent = "Cargando...";
    rivalExtra.textContent = "";

    fetch(`/torneo/${idTorneo}/mostrar_participante/${idUsuario}`)
        .then(res => {

            if (!res.ok) {
                throw new Error("Error al obtener datos");
            }

            return res.json();
        })
        .then(data => {

            rivalNombre.textContent = data.usuario || "Sin nombre";

            if (data.personaje) {
                rivalExtra.textContent = data.personaje;
            }
            else if (data.club) {
                rivalExtra.textContent = data.club;
            }
            else {
                rivalExtra.textContent = "";
            }

            rivalVictorias.textContent = "Victorias: " + (data.victorias ?? 0);
            rivalDerrotas.textContent = "Derrotas: " + (data.derrotas ?? 0);
            rivalEmpates.textContent = "Empates: " + (data.empates ?? 0);

            rivalBox.classList.add("activo");

        })
        .catch(err => {

            console.error(err);

            rivalNombre.textContent = "Error";
            rivalExtra.textContent = "No se pudo cargar";

        });
};

window.cargarRivalEquipo = function(idTorneo, idEquipo) {

    const rivalBox = document.getElementById("rivalBox");
    const rivalPerfil = document.getElementById("rivalPerfil");

    rivalBox.classList.remove("activo");

    fetch(`/torneo/${idTorneo}/mostrar_equipo/${idEquipo}`)
        .then(res => {
            if (!res.ok) throw new Error("Error al obtener datos del equipo");
            return res.json();
        })
        .then(data => {
            const miembrosHTML = data.miembros && data.miembros.length
                ? `<ul class="lista-miembros-torneo">${data.miembros.map(m => `<li>${m}</li>`).join('')}</ul>`
                : '';

            rivalPerfil.innerHTML = `
                <div class="avatar">${data.usuario ? data.usuario.charAt(0).toUpperCase() : "?"}</div>
                <p class="nombre">${data.usuario || "Sin nombre"}</p>
                ${miembrosHTML}
                <div class="stats">
                    <span>Victorias: ${data.victorias ?? 0}</span>
                    <span>Derrotas: ${data.derrotas ?? 0}</span>
                    <span>Empates: ${data.empates ?? 0}</span>
                </div>
            `;

            rivalBox.classList.add("activo");
        })
        .catch(err => {
            console.error(err);
            rivalPerfil.innerHTML = `<p>Error al cargar el equipo</p>`;
        });
};

window.cargarDatosParticipante = function(id_torneo, id_usuario, destino) {

    fetch(`/torneo/${id_Torneo}/mostrar_participante/${id_Usuario}`)
        .then(res => res.json())
        .then(data => {

            if(data.error){
                destino.innerHTML = "<p>No disponible</p>";
                return;
            }

            destino.innerHTML = `
                <p><strong>${data.usuario}</strong></p>
                <div class="jugable">
                ${data.personaje ? `<div class="loadout-item"><span class="text"> ${data.personaje}</span></div>` : ""}
                ${data.club ? `<div class="loadout-item"><span class="text">${data.club}</span></div>` : ""}
                ${data.armas ? `<div class="loadout-item"><span class="text"> ${data.armas}</span></div>` : ""}
                </div>
                <p>Victorias: ${data.victorias}</p>
                <p>Derrotas: ${data.derrotas}</p>
                <p>Empates: ${data.empates}</p>
            `;
        });
};

window.cargarMiParticipante = function(idTorneo) {

    fetch(`/torneo/${idTorneo}/mi_participante`)
        .then(res => res.json())
        .then(data => {

            const box = document.getElementById("miParticipante");
            if (!box || data.error) return;

            if (data.es_equipo) {
                const miembrosHTML = data.miembros && data.miembros.length
                    ? `<ul class="lista-miembros-torneo">${data.miembros.map(m => `<li>${m}</li>`).join('')}</ul>`
                    : '';
                box.innerHTML = `
                    <div class="avatar">${data.usuario ? data.usuario.charAt(0).toUpperCase() : "?"}</div>
                    <p class="nombre">${data.usuario}</p>
                    ${miembrosHTML}
                    <div class="stats">
                        <span>Victorias: ${data.victorias}</span>
                        <span>Derrotas: ${data.derrotas}</span>
                        <span>Empates: ${data.empates}</span>
                    </div>
                `;
            } else {
                box.innerHTML = `
                    <div class="avatar">
                        ${data.usuario ? data.usuario.charAt(0).toUpperCase() : "?"}
                    </div>

                    <p class="nombre">${data.usuario}</p>

                    <div class="jugable">
                    ${data.personaje ? `<div class="loadout-item"><span class="text"> ${data.personaje}</span></div>` : ""}
                    ${data.club ? `<div class="loadout-item"><span class="text"> ${data.club}</span></div>` : ""}
                    ${data.armas ? `<div class="loadout-item"><span class="text"> ${data.armas}</span></div>` : ""}
                    </div>

                    <div class="stats">
                        <span>Victorias: ${data.victorias}</span>
                        <span>Derrotas: ${data.derrotas}</span>
                        <span>Empates: ${data.empates}</span>
                    </div>
                `;
            }
        });
};

function abrirModalResultado(idPartida) {
    document.getElementById("modalResultado").classList.remove("oculto");
    document.getElementById("partidaId").value = idPartida;
}

function cerrarModalResultado() {
    document.getElementById("modalResultado").classList.add("oculto");
}

document.addEventListener("DOMContentLoaded", () => {

    const formResultado = document.getElementById("formResultado");

    if (!formResultado) return;

    formResultado.addEventListener("submit", function (e) {
        e.preventDefault();

        const idPartida = document.getElementById("partidaId").value;

        const resultadoUsuario = document.getElementById("resultadoUsuario").value.trim();
        const resultadoRival = document.getElementById("resultadoRival").value.trim();

        const captura = document.getElementById("captura")?.files[0];

        // =========================
        // VALIDACIÓN SIMPLE (1 NÚMERO)
        // =========================

        if (resultadoUsuario === "" || resultadoRival === "") {
            _aviso("Campos vacíos", "Introduce ambos resultados para continuar", "error");
            return;
        }

        if (!/^\d+$/.test(resultadoUsuario) || !/^\d+$/.test(resultadoRival)) {
            _aviso("Formato incorrecto", "Solo se permiten números enteros", "error");
            return;
        }

        // =========================
        // FORM DATA
        // =========================

        const formData = new FormData();

        formData.append("resultado_usuario", resultadoUsuario);
        formData.append("resultado_rival", resultadoRival);

        if (captura) {
            formData.append("captura_resultado", captura);
        }

        // =========================
        // FETCH
        // =========================

        fetch(`/partida/${idPartida}/resultado`, {
            method: "POST",
            body: formData
        })
        .then(async res => {
            const data = await res.json();

            if (!res.ok) {
                throw new Error(data.error || "Error");
            }

            return data;
        })
        .then(data => {
            _aviso("Resultado enviado", data.mensaje || "Resultado enviado correctamente", "exito", () => { cerrarModalResultado(); location.reload(); });
        })
        .catch(err => {
            console.error(err);
            _aviso("Error", err.message, "error");
        });

    });

});

let partidaRevisionActual = null;

function abrirModalRevision(idPartida) {

    partidaRevisionActual = idPartida;

    fetch(`/conflicto/${idPartida}`)
    .then(async res => {

        // Intentar leer texto primero
        const text = await res.text();

        // Error servidor
        if (!res.ok) {
            console.error("Respuesta servidor:", text);
            throw new Error(`Error ${res.status} del servidor`);
        }

        // Intentar convertir a JSON
        try {
            return JSON.parse(text);
        } catch (e) {
            console.error("Respuesta NO JSON:", text);
            throw new Error("El servidor no devolvió JSON válido");
        }
    })
    .then(data => {

        const contenedor = document.getElementById("contenidoConflicto");

        if (!contenedor) {
            console.error("No existe #contenidoConflicto");
            return;
        }

        contenedor.innerHTML = "";

        // seguridad
        if (!Array.isArray(data)) {
            throw new Error("Formato inválido");
        }

        data.forEach(jugador => {

            contenedor.innerHTML += `
                <div class="conflicto-jugador">

                    <h3>${jugador.usuario || "Sin usuario"}</h3>

                    <p>
                        Su resultado:
                        ${jugador.resultado_usuario ?? "-"}
                    </p>

                    <p>
                        Resultado rival:
                        ${jugador.resultado_rival ?? "-"}
                    </p>

                    ${
                        jugador.captura
                        ?
                        `<a href="${jugador.captura}" target="_blank">
                            Ver captura
                        </a>`
                        :
                        `<p>Sin captura</p>`
                    }

                </div>
            `;
        });

        document
            .getElementById("modalRevision")
            ?.classList.remove("oculto");
    })
    .catch(err => {

        console.error(err);

        _aviso("Error", "Error al cargar el conflicto. Consulta la consola.", "error");
    });
}

function cerrarModalRevision() {

    document.getElementById("modalRevision")
        .classList.add("oculto");
}

function guardarResolucion() {

    const resultadoFinal = document
        .getElementById("resultadoFinalAdmin")
        .value.trim();

    if(resultadoFinal === ""){
        _aviso("Campo vacío", "Introduce el resultado final antes de continuar", "error");
        return;
    }

    if(!/^\d+-\d+$/.test(resultadoFinal)){
        _aviso("Formato incorrecto", "El resultado debe tener el formato x-x (ejemplo: 3-1), donde x representa un número", "error");
        return;
    }

    const formData = new FormData();

    formData.append("resultado_final", resultadoFinal);

    fetch(`/resolver_conflicto/${partidaRevisionActual}`, {
        method: "POST",
        body: formData
    })
    .then(async res => {
        const data = await res.json();
        if (!res.ok) {
            _aviso("No permitido", data.error || "No se puede guardar ese resultado", "error");
            return;
        }
        _aviso("Conflicto resuelto", data.mensaje, "exito", () => { cerrarModalRevision(); location.reload(); });
    })
    .catch(err => {
        console.error(err);
        _aviso("Error", "Error al resolver el conflicto", "error");
    });
}

async function cargarClasificacionGrupos(idTorneo, intento = 0) {

    const contenedor = document.getElementById("clasificacionGrupos");

    if (!contenedor) {
        console.warn("No existe contenedor clasificacionGrupos");
        return;
    }

    try {

        const res = await fetch(`/torneo/${idTorneo}/clasificacion_grupos`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        // 🔴 si el backend falla (500, 404, etc)
        if (!res.ok) {
            throw new Error("HTTP " + res.status);
        }

        const data = await res.json();

        // 🔴 si backend devuelve error controlado
        if (data.error) {
            throw new Error(data.error);
        }

        let html = "";

        data.forEach(grupo => {

            html += `
            <div class="grupo-clasificacion">
                <h3>Grupo ${grupo.grupo}</h3>

                <table class="tabla-ranking">
                    <thead>
                        <tr>
                            <th>POS</th>
                            <th>${window.esTorneoEquipo ? 'EQUIPO' : 'JUGADOR'}</th>
                            <th>PJ</th>
                            <th>PG</th>
                            <th>PE</th>
                            <th>PD</th>
                            <th>RG</th>
                            <th>RP</th>
                            <th>DR</th>
                            <th>PT</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            grupo.clasificacion.forEach(p => {

                html += `
                    <tr>
                        <td>${p.pos}</td>
                        <td>${p.usuario}</td>
                        <td>${p.pj}</td>
                        <td>${p.pg}</td>
                        <td>${p.pe}</td>
                        <td>${p.pd}</td>
                        <td>${p.rg}</td>
                        <td>${p.rp}</td>
                        <td>${p.dr}</td>
                        <td>${p.pt}</td>
                    </tr>
                `;
            });

            html += `
                    </tbody>
                </table>
            </div>
            `;
        });

        contenedor.innerHTML = html;

    } catch (err) {

        console.error("Error clasificación grupos:", err);

        // 🔁 RETRY automático (hasta 2 intentos)
        if (intento < 2) {
            setTimeout(() => {
                cargarClasificacionGrupos(idTorneo, intento + 1);
            }, 600);
        } else {
            contenedor.innerHTML = `
                <div class="error-clasificacion">
                    Error cargando clasificación. Intenta recargar la página.
                </div>
            `;
        }
    }
}



// =========================
// CARGA ELIMINATORIAS
// =========================

window.cargarEliminatorias = function(idTorneo) {

    fetch(`/torneo/${idTorneo}/eliminatorias_arbol`)
        .then(res => res.json())
        .then(data => {

            const container = document.querySelector("#bracket");
            container.innerHTML = "";

            const raiz = data.raiz;

            if (!raiz) {
                container.innerHTML = "<p>No hay eliminatorias aún</p>";
                return;
            }

            const hijos = raiz.hijos || [];
            const leftNodo  = hijos[0] || null;
            const rightNodo = hijos[1] || null;

            // rounds[0] = deepest (más partidas), rounds[last] = semi
            const leftRounds  = leftNodo  ? collectBracketRounds(leftNodo)  : [];
            const rightRounds = rightNodo ? collectBracketRounds(rightNodo) : [];

            const maxDepth = Math.max(leftRounds.length, rightRounds.length);
            const deepestCount = maxDepth > 0
                ? Math.max(
                    leftRounds.length  > 0 ? leftRounds[0].length  : 0,
                    rightRounds.length > 0 ? rightRounds[0].length : 0
                  )
                : 1;

            const SLOT_H = 110;

            const wrapper = document.createElement('div');
            wrapper.className = 'bracket-horizontal';

            // Columnas izquierda: ronda más profunda primero → semi último
            leftRounds.forEach((round, i) => {
                const slotsPerMatch = Math.pow(2, i);
                wrapper.appendChild(buildBracketCol(round, slotsPerMatch, SLOT_H, 'left'));
            });

            // Columna central: la final
            const finalSlot = document.createElement('div');
            finalSlot.className = 'bracket-slot';
            finalSlot.style.height = (deepestCount * SLOT_H) + 'px';
            finalSlot.appendChild(buildMatchCard(raiz));

            const finalCol = document.createElement('div');
            finalCol.className = 'bracket-col bracket-col-final';
            finalCol.appendChild(finalSlot);
            wrapper.appendChild(finalCol);

            // Columnas derecha: semi primero → ronda más profunda último
            [...rightRounds].reverse().forEach((round, j) => {
                const slotsPerMatch = Math.pow(2, rightRounds.length - 1 - j);
                wrapper.appendChild(buildBracketCol(round, slotsPerMatch, SLOT_H, 'right'));
            });

            container.appendChild(wrapper);
        })
        .catch(err => {
            console.error("Error cargando bracket:", err);
        });
};

// Devuelve rondas con deepest primero: [[octavos...], [cuartos...], [semi]]
function collectBracketRounds(nodo) {
    const rounds = [];
    let level = [nodo];

    while (level.length > 0) {
        rounds.push(level);
        const next = [];
        level.forEach(n => {
            if (n && n.hijos && n.hijos.length >= 2) {
                if (n.hijos[0]) next.push(n.hijos[0]);
                if (n.hijos[1]) next.push(n.hijos[1]);
            }
        });
        if (next.length === 0) break;
        level = next;
    }

    return rounds.reverse();
}

function buildBracketCol(matches, slotsPerMatch, slotH, side) {
    const col = document.createElement('div');
    col.className = `bracket-col bracket-col-${side}`;

    matches.forEach(match => {
        const slot = document.createElement('div');
        slot.className = 'bracket-slot';
        slot.style.height = (slotsPerMatch * slotH) + 'px';
        slot.appendChild(buildMatchCard(match));
        col.appendChild(slot);
    });

    return col;
}

// ===============================
// TIMER DE RESULTADO PENDIENTE
// ===============================

const DURACION_TIMER_MS = 60 * 1000;
const INTERVALO_SONDEO_MS = 5000;

function iniciarSondeoPartidas(idTorneo, esOrganizador) {

    const tarjetasEncuentro = document.querySelectorAll(".encuentro-card[id]");

    if (tarjetasEncuentro.length === 0) return;

    function sondarTodasLasPartidas() {
        tarjetasEncuentro.forEach(tarjeta => {
            const idPartida = tarjeta.id.replace("encuentro-", "");
            sondarEstadoPartida(idPartida, esOrganizador);
        });
    }

    sondarTodasLasPartidas();
    setInterval(sondarTodasLasPartidas, INTERVALO_SONDEO_MS);
}

function sondarEstadoPartida(idPartida, esOrganizador) {

    fetch(`/partida/${idPartida}/estado_resultado`)
        .then(respuesta => respuesta.json())
        .then(datos => {
            procesarEstadoPartida(idPartida, datos, esOrganizador);
        })
        .catch(error => console.error("Error sondeando partida:", error));
}

function procesarEstadoPartida(idPartida, datos, esOrganizador) {

    if (datos.estado === "Finalizado" || datos.estado === "Pendiente de revision") {
        limpiarTimerPartida(idPartida);
        return;
    }

    if (!datos.primer_resultado_enviado || datos.ambos_enviaron) {
        limpiarTimerPartida(idPartida);
        return;
    }

    gestionarTimerPartida(idPartida, esOrganizador);
}

function gestionarTimerPartida(idPartida, esOrganizador) {

    const claveStorage = `timer_partida_${idPartida}`;

    if (!localStorage.getItem(claveStorage)) {
        localStorage.setItem(claveStorage, Date.now().toString());
    }

    const momentoInicio = parseInt(localStorage.getItem(claveStorage));
    const tiempoTranscurrido = Date.now() - momentoInicio;
    const tiempoRestante = DURACION_TIMER_MS - tiempoTranscurrido;
    const elementoTimer = document.getElementById(`timer-${idPartida}`);

    if (tiempoRestante > 0) {

        if (elementoTimer) {
            const segundosRestantes = Math.ceil(tiempoRestante / 1000);
            elementoTimer.textContent = `Resolución en: ${segundosRestantes}s`;
            elementoTimer.classList.remove("oculto");
        }

        setTimeout(() => sondarEstadoPartida(idPartida, esOrganizador), 1000);

    } else {

        if (elementoTimer) {
            elementoTimer.classList.add("oculto");
        }

        if (esOrganizador) {
            mostrarBotonOrganizadorTimer(idPartida);
        }
    }
}

function mostrarBotonOrganizadorTimer(idPartida) {

    const botonTimer = document.getElementById(`btn-timer-organizador-${idPartida}`);

    if (botonTimer) {
        botonTimer.classList.remove("oculto");
    }
}

function limpiarTimerPartida(idPartida) {

    localStorage.removeItem(`timer_partida_${idPartida}`);

    const elementoTimer = document.getElementById(`timer-${idPartida}`);
    if (elementoTimer) {
        elementoTimer.classList.add("oculto");
    }

    const botonTimer = document.getElementById(`btn-timer-organizador-${idPartida}`);
    if (botonTimer) {
        botonTimer.classList.add("oculto");
    }
}

// ===============================
// ZONA CREACIÓN DE JUEGO (admin)
// ===============================

const arrayPersonajes = [];
const arrayEquipos = [];
const arrayArmas = [];
const arrayHabilidades = [];

function toggleNuevoGenero(valor) {
    const contenedor = document.getElementById("contenedorNuevoGenero");
    const inputNuevo = document.getElementById("inputNuevoGenero");
    if (valor === "nuevo") {
        contenedor.classList.remove("oculto");
    } else {
        contenedor.classList.add("oculto");
        inputNuevo.value = "";
    }
}

function previsualizarPortada(input) {
    const previa = document.getElementById("previstaPortada");
    if (input.files && input.files[0]) {
        previa.src = URL.createObjectURL(input.files[0]);
    }
}

function cambiarSeccionElementos(tipo) {
    document.querySelectorAll(".seccion-elementos").forEach(s => s.classList.add("oculto"));

    if (tipo === "Personajes" || tipo === "Personajes y Armas") {
        document.getElementById("seccionPersonajes").classList.remove("oculto");
    }
    if (tipo === "Equipos") {
        document.getElementById("seccionEquipos").classList.remove("oculto");
    }
    if (tipo === "Armas" || tipo === "Personajes y Armas") {
        document.getElementById("seccionArmas").classList.remove("oculto");
    }
    if (tipo === "Personajes y Armas") {
        document.getElementById("seccionHabilidades").classList.remove("oculto");
    }
}

function renderizarLista(idLista, array, renderFila) {
    const lista = document.getElementById(idLista);
    lista.innerHTML = "";
    array.forEach((elemento, indice) => {
        const li = document.createElement("li");
        li.className = "elemento-lista";
        li.innerHTML = renderFila(elemento, indice);
        lista.appendChild(li);
    });
}

function actualizarSelectPersonajesHabilidad() {
    const select = document.getElementById("selectPersonajeHabilidad");
    if (!select) return;
    const valorActual = select.value;
    select.innerHTML = `<option value="">-- Personaje --</option>`;
    arrayPersonajes.forEach((nombre, indice) => {
        const opcion = document.createElement("option");
        opcion.value = indice;
        opcion.textContent = nombre;
        select.appendChild(opcion);
    });
    select.value = valorActual;
}

function actualizarSelectArmasHabilidad() {
    const select = document.getElementById("selectArmaHabilidad");
    if (!select) return;
    const valorActual = select.value;
    select.innerHTML = `<option value="">-- Arma --</option>`;
    arrayArmas.forEach((arma, indice) => {
        const opcion = document.createElement("option");
        opcion.value = indice;
        opcion.textContent = arma.nombre;
        select.appendChild(opcion);
    });
    select.value = valorActual;
}

function añadirPersonaje() {
    const input = document.getElementById("inputPersonaje");
    const nombre = input.value.trim();
    if (!nombre) return;
    arrayPersonajes.push(nombre);
    input.value = "";
    renderizarLista("listaPersonajes", arrayPersonajes, (nombre, i) =>
        `<span>${nombre}</span><button type="button" class="btn-eliminar-elemento" onclick="eliminarPersonaje(${i})">✕</button>`
    );
    document.getElementById("hiddenPersonajes").value = JSON.stringify(arrayPersonajes);
    actualizarSelectPersonajesHabilidad();
}

function eliminarPersonaje(indice) {
    arrayPersonajes.splice(indice, 1);
    renderizarLista("listaPersonajes", arrayPersonajes, (nombre, i) =>
        `<span>${nombre}</span><button type="button" class="btn-eliminar-elemento" onclick="eliminarPersonaje(${i})">✕</button>`
    );
    document.getElementById("hiddenPersonajes").value = JSON.stringify(arrayPersonajes);
    actualizarSelectPersonajesHabilidad();
}

function añadirEquipo() {
    const input = document.getElementById("inputEquipo");
    const nombre = input.value.trim();
    if (!nombre) return;
    arrayEquipos.push(nombre);
    input.value = "";
    renderizarLista("listaEquipos", arrayEquipos, (nombre, i) =>
        `<span>${nombre}</span><button type="button" class="btn-eliminar-elemento" onclick="eliminarEquipo(${i})">✕</button>`
    );
    document.getElementById("hiddenEquipos").value = JSON.stringify(arrayEquipos);
}

function eliminarEquipo(indice) {
    arrayEquipos.splice(indice, 1);
    renderizarLista("listaEquipos", arrayEquipos, (nombre, i) =>
        `<span>${nombre}</span><button type="button" class="btn-eliminar-elemento" onclick="eliminarEquipo(${i})">✕</button>`
    );
    document.getElementById("hiddenEquipos").value = JSON.stringify(arrayEquipos);
}

function añadirArma() {
    const inputNombre = document.getElementById("inputNombreArma");
    const inputTipo = document.getElementById("inputTipoArma");
    const nombre = inputNombre.value.trim();
    const tipo = inputTipo.value.trim();
    if (!nombre || !tipo) return;
    arrayArmas.push({ nombre, tipo_arma: tipo });
    inputNombre.value = "";
    inputTipo.value = "";
    renderizarLista("listaArmas", arrayArmas, (arma, i) =>
        `<span>${arma.nombre} <em>(${arma.tipo_arma})</em></span><button type="button" class="btn-eliminar-elemento" onclick="eliminarArma(${i})">✕</button>`
    );
    document.getElementById("hiddenArmas").value = JSON.stringify(arrayArmas);
    actualizarSelectArmasHabilidad();
}

function eliminarArma(indice) {
    arrayArmas.splice(indice, 1);
    renderizarLista("listaArmas", arrayArmas, (arma, i) =>
        `<span>${arma.nombre} <em>(${arma.tipo_arma})</em></span><button type="button" class="btn-eliminar-elemento" onclick="eliminarArma(${i})">✕</button>`
    );
    document.getElementById("hiddenArmas").value = JSON.stringify(arrayArmas);
    actualizarSelectArmasHabilidad();
}

function añadirHabilidad() {
    const selectPersonaje = document.getElementById("selectPersonajeHabilidad");
    const selectArma = document.getElementById("selectArmaHabilidad");
    const inputHabilidad = document.getElementById("inputHabilidad");

    const personajeIdx = selectPersonaje.value;
    const armaIdx = selectArma.value;
    const habilidad = inputHabilidad.value.trim();

    if (personajeIdx === "" || armaIdx === "" || !habilidad) return;

    arrayHabilidades.push({
        personaje_idx: parseInt(personajeIdx),
        arma_idx: parseInt(armaIdx),
        habilidad
    });

    selectPersonaje.value = "";
    selectArma.value = "";
    inputHabilidad.value = "";

    renderizarLista("listaHabilidades", arrayHabilidades, (hab, i) => {
        const nombreP = arrayPersonajes[hab.personaje_idx] || "?";
        const nombreA = arrayArmas[hab.arma_idx]?.nombre || "?";
        return `<span>${nombreP} → ${nombreA}: <em>${hab.habilidad}</em></span>
                <button type="button" class="btn-eliminar-elemento" onclick="eliminarHabilidad(${i})">✕</button>`;
    });

    document.getElementById("hiddenHabilidades").value = JSON.stringify(arrayHabilidades);
}

function eliminarHabilidad(indice) {
    arrayHabilidades.splice(indice, 1);
    renderizarLista("listaHabilidades", arrayHabilidades, (hab, i) => {
        const nombreP = arrayPersonajes[hab.personaje_idx] || "?";
        const nombreA = arrayArmas[hab.arma_idx]?.nombre || "?";
        return `<span>${nombreP} → ${nombreA}: <em>${hab.habilidad}</em></span>
                <button type="button" class="btn-eliminar-elemento" onclick="eliminarHabilidad(${i})">✕</button>`;
    });
    document.getElementById("hiddenHabilidades").value = JSON.stringify(arrayHabilidades);
}

function mostrarAvisoCreacion(mensaje, tipo) {
    const aviso = document.getElementById("avisoCreacion");
    aviso.textContent = mensaje;
    aviso.className = `aviso-admin ${tipo === "error" ? "aviso-error" : "aviso-exito"}`;
    aviso.scrollIntoView({ behavior: "smooth" });
}

async function enviarFormularioJuego() {
    const formulario = document.getElementById("formCrearJuego");
    const nombreJuego = formulario.querySelector("[name='nombre_juego']").value.trim();
    const selectGenero = document.getElementById("selectGenero");
    const tipoElemento = formulario.querySelector("[name='tipo_elemento']").value;
    const nuevoGenero = document.getElementById("inputNuevoGenero")?.value.trim();

    if (nombreJuego.length < 3) {
        mostrarAvisoCreacion("El nombre del juego debe tener al menos 3 caracteres", "error");
        return;
    }

    const generoSeleccionado = selectGenero.value;
    if (!generoSeleccionado) {
        mostrarAvisoCreacion("Debes seleccionar un género", "error");
        return;
    }
    if (generoSeleccionado === "nuevo" && !nuevoGenero) {
        mostrarAvisoCreacion("Escribe el nombre del nuevo género", "error");
        return;
    }

    if (!tipoElemento) {
        mostrarAvisoCreacion("Debes seleccionar el tipo de elemento", "error");
        return;
    }

    if (generoSeleccionado === "nuevo") {
        selectGenero.value = "";
    }

    const formData = new FormData(formulario);

    const inputPortada = document.getElementById("inputPortada");
    if (inputPortada && inputPortada.files[0]) {
        formData.append("portada", inputPortada.files[0]);
    }

    try {
        const respuesta = await fetch("/admin/juegos/crear", {
            method: "POST",
            body: formData
        });
        const datos = await respuesta.json();

        if (!respuesta.ok) {
            mostrarAvisoCreacion(datos.error || "Error al crear el juego", "error");
            return;
        }

        arrayPersonajes.length = 0;
        arrayEquipos.length = 0;
        arrayArmas.length = 0;
        arrayHabilidades.length = 0;

        document.getElementById("formCrearJuego").reset();
        document.getElementById("previstaPortada").src = "/static/imagenes/Logo.png";
        document.querySelectorAll(".seccion-elementos").forEach(s => s.classList.add("oculto"));
        document.getElementById("contenedorNuevoGenero").classList.add("oculto");
        ["listaPersonajes","listaEquipos","listaArmas","listaHabilidades"].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.innerHTML = "";
        });
        ["hiddenPersonajes","hiddenEquipos","hiddenArmas","hiddenHabilidades"].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = "[]";
        });

        mostrarAvisoCreacion("Juego creado correctamente", "exito");

    } catch (error) {
        mostrarAvisoCreacion("Error de conexión al crear el juego", "error");
    }
}

// ===============================
// ===============================
// INIT PAGINACIÓN PANELES ADMIN
// ===============================

document.addEventListener("DOMContentLoaded", () => {
    [
        ["listaUsuarios", ".fila-usuario"],
        ["listaJuegos", ".fila-usuario"],
        ["listaTorneosAdmin", ".seccion-juego-torneos"],
        ["listaGestionTorneos", ".seccion-gestion-juego"],
    ].forEach(([idLista, selector]) => {
        if (document.getElementById(idLista)) _actualizarPaginacion(idLista, selector);
    });
});

// ===============================
// GESTIÓN TORNEOS (administracion_torneo.html)
// ===============================

const cambiosTorneo = {};
let idTorneoParaBorrar = null;
let idTorneoConfirmandoCambios = null;
let _filtroBusquedaGestionTorneo = "";
let _filtroEstadoGestionTorneo = "";

function toggleDesplegableGestionTorneo(cabecera) {
    const panel = cabecera.nextElementSibling;
    panel.classList.toggle("oculto");
}

function toggleDetalleTorneoGestion(cabecera) {
    const detalle = cabecera.nextElementSibling;
    detalle.classList.toggle("oculto");
}

function abrirInfoTorneoGestion(evento, idTorneo) {
    evento.stopPropagation();
    const boton = evento.currentTarget;
    const fila = document.querySelector(`.fila-torneo-gestion[data-id="${idTorneo}"]`);
    if (!fila) return;
    const detalle = fila.querySelector(".detalle-torneo-gestion");
    if (detalle) detalle.classList.remove("oculto");

    const enModoEdicion = boton.dataset.modoEdicion === "true";

    if (enModoEdicion) {
        detalle.querySelectorAll(".dato-fila:not(.dato-solo-lectura)").forEach(filaDato => {
            const btnConfirmar = Array.from(filaDato.querySelectorAll(".btn-lapiz-dato")).find(b => b.textContent === "✅");
            if (btnConfirmar) btnConfirmar.click();
        });
        boton.textContent = "✏️";
        boton.dataset.modoEdicion = "false";
    } else {
        detalle.querySelectorAll(".dato-fila:not(.dato-solo-lectura)").forEach(filaDato => {
            const btnLapiz = Array.from(filaDato.querySelectorAll(".btn-lapiz-dato")).find(b => b.textContent === "✏️");
            if (btnLapiz) btnLapiz.click();
        });
        boton.textContent = "✅";
        boton.dataset.modoEdicion = "true";
    }
}

function editarDatoTorneoGestion(evento, boton) {
    evento.stopPropagation();
    const filaDato = boton.closest(".dato-fila");
    const campo = filaDato.dataset.campo;
    const valorOriginal = filaDato.dataset.valorOriginal;
    const spanValor = filaDato.querySelector(".valor-dato");
    const idTorneo = parseInt(filaDato.closest(".fila-torneo-gestion").dataset.id);

    if (filaDato.querySelector("input, select, textarea")) return;

    boton.style.display = "none";
    spanValor.style.display = "none";

    let control;

    if (campo === "estado") {
        control = document.createElement("select");
        control.className = "input-edicion";
        ["Activo", "Cerrado", "Finalizado"].forEach(op => {
            const opt = document.createElement("option");
            opt.value = op;
            opt.textContent = op;
            if (op === valorOriginal) opt.selected = true;
            control.appendChild(opt);
        });
    } else if (campo === "fecha_inicio" || campo === "fecha_final") {
        control = document.createElement("input");
        control.type = "date";
        control.className = "input-edicion";
        control.value = valorOriginal;
    } else if (campo === "descripcion") {
        control = document.createElement("textarea");
        control.className = "input-edicion input-descripcion-torneo";
        control.value = valorOriginal;
        control.rows = 3;
    } else if (campo === "max_participantes") {
        control = document.createElement("select");
        control.className = "input-edicion";
        [8, 16, 32, 64, 128].forEach(n => {
            const opt = document.createElement("option");
            opt.value = n;
            opt.textContent = n;
            if (String(n) === String(valorOriginal)) opt.selected = true;
            control.appendChild(opt);
        });
    } else {
        control = document.createElement("input");
        control.type = "text";
        control.className = "input-edicion";
        control.value = valorOriginal;
    }

    control.addEventListener("input", () => _rastrearCambioTorneo(idTorneo, campo, filaDato, control.value));
    control.addEventListener("change", () => _rastrearCambioTorneo(idTorneo, campo, filaDato, control.value));

    filaDato.insertBefore(control, boton);

    const btnConfirmar = document.createElement("button");
    btnConfirmar.textContent = "✅";
    btnConfirmar.className = "btn-lapiz-dato";
    btnConfirmar.onclick = (e) => {
        e.stopPropagation();
        const nuevoValor = control.value;

        if (campo === "fecha_inicio" || campo === "fecha_final") {
            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);
            const fechaValor = new Date(nuevoValor);
            const detalle = filaDato.closest(".detalle-torneo-gestion");

            if (campo === "fecha_inicio" && fechaValor < hoy) {
                _mostrarErrorTorneo("La fecha de inicio debe ser igual o posterior a hoy.");
                return;
            }
            if (campo === "fecha_final") {
                const filaInicio = detalle ? detalle.querySelector(".dato-fila[data-campo='fecha_inicio']") : null;
                const valorInicio = filaInicio ? (filaInicio.querySelector("input")?.value || filaInicio.dataset.valorOriginal) : null;
                if (valorInicio && fechaValor < new Date(valorInicio)) {
                    _mostrarErrorTorneo("La fecha final debe ser igual o posterior a la fecha de inicio.");
                    return;
                }
            }
        }

        _rastrearCambioTorneo(idTorneo, campo, filaDato, nuevoValor);
        spanValor.textContent = nuevoValor;
        spanValor.style.display = "";
        control.remove();
        btnConfirmar.remove();
        boton.style.display = "";
    };
    filaDato.insertBefore(btnConfirmar, boton);
}

function _rastrearCambioTorneo(idTorneo, campo, filaDato, nuevoValor) {
    const original = filaDato.dataset.valorOriginal;
    if (!cambiosTorneo[idTorneo]) cambiosTorneo[idTorneo] = {};
    if (nuevoValor !== original) {
        cambiosTorneo[idTorneo][campo] = nuevoValor;
    } else {
        delete cambiosTorneo[idTorneo][campo];
    }
    actualizarBotonAceptarTorneo(idTorneo);
}

function _mostrarErrorTorneo(mensaje) {
    document.getElementById("textoModalErrorTorneoGestion").textContent = mensaje;
    document.getElementById("modalErrorTorneoGestion").classList.remove("oculto");
}

function actualizarBotonAceptarTorneo(idTorneo) {
    const btn = document.getElementById(`btnAceptarTorneo-${idTorneo}`);
    if (!btn) return;
    const hayCambios = cambiosTorneo[idTorneo] && Object.keys(cambiosTorneo[idTorneo]).length > 0;
    btn.disabled = !hayCambios;
}

function abrirModalConfirmarCambiosTorneo(idTorneo) {
    idTorneoConfirmandoCambios = idTorneo;
    const fila = document.querySelector(`.fila-torneo-gestion[data-id="${idTorneo}"]`);
    const nombre = fila ? fila.dataset.nombre : "";
    document.getElementById("nombreTorneoCambios").textContent = nombre;
    document.getElementById("modalConfirmarCambiosTorneoGestion").classList.remove("oculto");
}

function cerrarModalConfirmarCambiosTorneoGestion() {
    document.getElementById("modalConfirmarCambiosTorneoGestion").classList.add("oculto");
    idTorneoConfirmandoCambios = null;
}

function confirmarGuardarCambiosTorneoGestion() {
    const idTorneo = idTorneoConfirmandoCambios;
    cerrarModalConfirmarCambiosTorneoGestion();
    if (!idTorneo || !cambiosTorneo[idTorneo]) return;

    fetch(`/admin/torneo/${idTorneo}/info`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cambiosTorneo[idTorneo])
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            document.getElementById("textoModalErrorTorneoGestion").textContent = data.error;
            document.getElementById("modalErrorTorneoGestion").classList.remove("oculto");
            return;
        }
        const fila = document.querySelector(`.fila-torneo-gestion[data-id="${idTorneo}"]`);
        fila.querySelectorAll(".dato-fila[data-campo]").forEach(filaDato => {
            const campo = filaDato.dataset.campo;
            if (cambiosTorneo[idTorneo][campo] !== undefined) {
                filaDato.dataset.valorOriginal = cambiosTorneo[idTorneo][campo];
                const span = filaDato.querySelector(".valor-dato");
                if (span) span.textContent = cambiosTorneo[idTorneo][campo];
            }
        });
        if (cambiosTorneo[idTorneo]["estado"]) {
            const nuevoEstado = cambiosTorneo[idTorneo]["estado"];
            fila.dataset.estado = nuevoEstado;
            const badge = fila.querySelector(".estado-torneo-badge");
            if (badge) {
                badge.textContent = nuevoEstado;
                badge.className = `estado-torneo-badge estado-${nuevoEstado.toLowerCase()}`;
            }
        }
        if (cambiosTorneo[idTorneo]["nombre"]) {
            const nuevoNombre = cambiosTorneo[idTorneo]["nombre"];
            fila.dataset.nombre = nuevoNombre.toLowerCase();
            const spanNombre = fila.querySelector(".nombre-torneo-admin");
            if (spanNombre) spanNombre.textContent = nuevoNombre;
        }
        cambiosTorneo[idTorneo] = {};
        actualizarBotonAceptarTorneo(idTorneo);
    })
    .catch(() => {
        document.getElementById("textoModalErrorTorneoGestion").textContent = "Error al guardar los cambios.";
        document.getElementById("modalErrorTorneoGestion").classList.remove("oculto");
    });
}

function restablecerCambiosTorneo(idTorneo) {
    const fila = document.querySelector(`.fila-torneo-gestion[data-id="${idTorneo}"]`);
    if (!fila) return;
    fila.querySelectorAll(".dato-fila[data-campo]").forEach(filaDato => {
        const original = filaDato.dataset.valorOriginal;
        const control = filaDato.querySelector("input, select, textarea");
        const spanValor = filaDato.querySelector(".valor-dato");
        const btnLapiz = filaDato.querySelector(".btn-lapiz-dato:not(.btn-confirmar-inline)");
        const btnConfirmar = filaDato.querySelectorAll(".btn-lapiz-dato")[1];
        if (control) {
            spanValor.textContent = original;
            spanValor.style.display = "";
            control.remove();
            if (btnConfirmar) btnConfirmar.remove();
            if (btnLapiz) btnLapiz.style.display = "";
        }
    });
    cambiosTorneo[idTorneo] = {};
    actualizarBotonAceptarTorneo(idTorneo);
}

function abrirModalBorrarTorneo(evento, idTorneo, nombre) {
    evento.stopPropagation();
    idTorneoParaBorrar = idTorneo;
    document.getElementById("nombreTorneoBorrar").textContent = nombre;
    document.getElementById("modalBorrarTorneoGestion").classList.remove("oculto");
}

function cerrarModalBorrarTorneoGestion() {
    document.getElementById("modalBorrarTorneoGestion").classList.add("oculto");
    idTorneoParaBorrar = null;
}

function confirmarBorrarTorneoGestion() {
    const id = idTorneoParaBorrar;
    cerrarModalBorrarTorneoGestion();
    fetch(`/admin/torneo/${id}`, { method: "DELETE" })
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                document.getElementById("textoModalErrorTorneoGestion").textContent = data.error;
                document.getElementById("modalErrorTorneoGestion").classList.remove("oculto");
                return;
            }
            const fila = document.querySelector(`.fila-torneo-gestion[data-id="${id}"]`);
            if (fila) fila.remove();
        });
}

function abrirModalBorrarFinalizados() {
    document.getElementById("modalBorrarFinalizados").classList.remove("oculto");
}

function cerrarModalBorrarFinalizados() {
    document.getElementById("modalBorrarFinalizados").classList.add("oculto");
}

function confirmarBorrarFinalizados() {
    cerrarModalBorrarFinalizados();
    fetch("/admin/torneos/finalizados", { method: "DELETE" })
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                document.getElementById("textoModalErrorTorneoGestion").textContent = data.error;
                document.getElementById("modalErrorTorneoGestion").classList.remove("oculto");
                return;
            }
            document.querySelectorAll(".fila-torneo-gestion[data-estado='Finalizado']").forEach(f => f.remove());
        })
        .catch(err => {
            document.getElementById("textoModalErrorTorneoGestion").textContent = "Error inesperado al borrar: " + err;
            document.getElementById("modalErrorTorneoGestion").classList.remove("oculto");
        });
}

function cambiarRolParticipanteGestion(idTorneo, idUsuario, select) {
    const nuevoRol = select.value;
    const rolAnterior = select.dataset.rolAnterior || select.value;
    fetch(`/admin/torneo/${idTorneo}/participante/${idUsuario}/rol`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rol: nuevoRol })
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            document.getElementById("textoModalErrorTorneoGestion").textContent = data.error;
            document.getElementById("modalErrorTorneoGestion").classList.remove("oculto");
            select.value = rolAnterior;
            return;
        }
        if (nuevoRol === "Organizador") {
            // bajar el anterior organizador a Participante en la UI
            const lista = document.getElementById(`listaParticipantes-${idTorneo}`);
            if (lista) {
                lista.querySelectorAll(".elemento-participante").forEach(li => {
                    const idU = parseInt(li.dataset.idUsuario);
                    if (idU !== idUsuario) {
                        const sel = li.querySelector(".select-rol-participante");
                        const lbl = li.querySelector(".rol-participante");
                        if (sel && sel.value === "Organizador") {
                            sel.value = "Participante";
                            sel.dataset.rolAnterior = "Participante";
                            if (lbl) lbl.textContent = "(Participante)";
                        }
                    }
                });
            }
        }
        const label = document.getElementById(`rolLabel-${idTorneo}-${idUsuario}`);
        if (label) label.textContent = `(${nuevoRol})`;
        select.dataset.rolAnterior = nuevoRol;
    });
}

function filtrarGestionTorneos(texto) {
    _filtroBusquedaGestionTorneo = texto.toLowerCase().trim();
    _aplicarFiltrosGestionTorneos();
}

function filtrarGestionTorneosPorEstado(estado) {
    _filtroEstadoGestionTorneo = estado;
    _aplicarFiltrosGestionTorneos();
}

function _aplicarFiltrosGestionTorneos() {
    document.querySelectorAll(".seccion-gestion-juego").forEach(seccion => {
        const nombreJuego = seccion.dataset.juego || "";
        let algunoVisible = false;

        seccion.querySelectorAll(".fila-torneo-gestion").forEach(fila => {
            const nombre = fila.dataset.nombre || "";
            const juego = fila.dataset.juego || "";
            const estado = fila.dataset.estado || "";

            const coincideBusqueda = !_filtroBusquedaGestionTorneo ||
                nombre.includes(_filtroBusquedaGestionTorneo) ||
                juego.includes(_filtroBusquedaGestionTorneo) ||
                nombreJuego.includes(_filtroBusquedaGestionTorneo);

            const coincideEstado = !_filtroEstadoGestionTorneo || estado === _filtroEstadoGestionTorneo;

            const visible = coincideBusqueda && coincideEstado;
            fila.classList.toggle("oculto", !visible);
            if (visible) algunoVisible = true;
        });

        seccion.classList.toggle("oculto", !algunoVisible);
        if (algunoVisible && (_filtroBusquedaGestionTorneo || _filtroEstadoGestionTorneo)) {
            const panel = seccion.querySelector(".panel-desplegable");
            if (panel) panel.classList.remove("oculto");
        }
    });
    _resetPagina("listaGestionTorneos");
    _actualizarPaginacion("listaGestionTorneos", ".seccion-gestion-juego");
}

function ordenarGestionTorneos(criterio) {
    const lista = document.getElementById("listaGestionTorneos");
    if (!lista) return;
    const secciones = Array.from(lista.querySelectorAll(".seccion-gestion-juego"));
    secciones.sort((a, b) => {
        if (criterio === "alfabetico")  return (a.dataset.juego || "").localeCompare(b.dataset.juego || "");
        if (criterio === "max-torneos") return parseInt(b.dataset.numTorneos || 0) - parseInt(a.dataset.numTorneos || 0);
        if (criterio === "min-torneos") return parseInt(a.dataset.numTorneos || 0) - parseInt(b.dataset.numTorneos || 0);
        return 0;
    });
    secciones.forEach(s => lista.appendChild(s));
}

// TORNEO ADMIN (torneo_admin.html)
// ===============================

let _filtroBusquedaTorneoAdmin = "";
let _filtroEstadoTorneoAdmin = "";

function toggleDesplegableTorneoAdmin(cabecera) {
    const panel = cabecera.nextElementSibling;
    panel.classList.toggle("oculto");
}

function toggleDetalleTorneoAdmin(cabecera) {
    const detalle = cabecera.nextElementSibling;
    detalle.classList.toggle("oculto");
}

function filtrarTorneosAdmin(texto) {
    _filtroBusquedaTorneoAdmin = texto.toLowerCase().trim();
    _aplicarFiltrosTorneosAdmin();
}

function filtrarTorneosAdminPorEstado(estado) {
    _filtroEstadoTorneoAdmin = estado;
    _aplicarFiltrosTorneosAdmin();
}

function _aplicarFiltrosTorneosAdmin() {
    document.querySelectorAll(".seccion-juego-torneos").forEach(seccion => {
        const nombreJuego = seccion.dataset.juego || "";
        let algunoVisible = false;

        seccion.querySelectorAll(".fila-torneo-admin").forEach(fila => {
            const nombre = fila.dataset.nombre || "";
            const juego = fila.dataset.juego || "";
            const estado = fila.dataset.estado || "";

            const coincideBusqueda = !_filtroBusquedaTorneoAdmin ||
                nombre.includes(_filtroBusquedaTorneoAdmin) ||
                juego.includes(_filtroBusquedaTorneoAdmin) ||
                nombreJuego.includes(_filtroBusquedaTorneoAdmin);

            const coincideEstado = !_filtroEstadoTorneoAdmin || estado === _filtroEstadoTorneoAdmin;

            const visible = coincideBusqueda && coincideEstado;
            fila.classList.toggle("oculto", !visible);
            if (visible) algunoVisible = true;
        });

        seccion.classList.toggle("oculto", !algunoVisible);

        if (algunoVisible && (_filtroBusquedaTorneoAdmin || _filtroEstadoTorneoAdmin)) {
            const panel = seccion.querySelector(".panel-desplegable");
            if (panel) panel.classList.remove("oculto");
        }
    });
    _resetPagina("listaTorneosAdmin");
    _actualizarPaginacion("listaTorneosAdmin", ".seccion-juego-torneos");
}

function ordenarSeccionesJuegoAdmin(criterio) {
    const lista = document.getElementById("listaTorneosAdmin");
    if (!lista) return;
    const secciones = Array.from(lista.querySelectorAll(".seccion-juego-torneos"));

    secciones.sort((a, b) => {
        if (criterio === "alfabetico")  return (a.dataset.juego || "").localeCompare(b.dataset.juego || "");
        if (criterio === "max-torneos") return parseInt(b.dataset.numTorneos || 0) - parseInt(a.dataset.numTorneos || 0);
        if (criterio === "min-torneos") return parseInt(a.dataset.numTorneos || 0) - parseInt(b.dataset.numTorneos || 0);
        return 0;
    });

    secciones.forEach(s => lista.appendChild(s));
}

function cerrarTorneoAdmin(idTorneo, boton) {
    fetch(`/cerrar_torneo/${idTorneo}`, { method: "POST" })
        .then(r => r.json())
        .then(data => {
            if (data.error) {
                _aviso("Error", data.error, "error");
                return;
            }
            const fila = boton.closest(".fila-torneo-admin");
            fila.dataset.estado = "Cerrado";
            const badge = fila.querySelector(".estado-torneo-badge");
            if (badge) {
                badge.textContent = "Cerrado";
                badge.className = "estado-torneo-badge estado-cerrado";
            }
            boton.remove();
        })
        .catch(() => _aviso("Error", "Error al cerrar el torneo", "error"));
}

// ===============================
// GESTIÓN EQUIPOS ADMIN
// ===============================

const _cambiosEquipoAdmin = {};
const _valoresOriginalesEquipoAdmin = {};

const _mapaEtiquetasEquipo = {
    "Nombre": "nombre",
    "Descripción": "descripcion",
    "Máx. miembros": "max_miembros"
};

function _capturarValoresEquipoAdmin(idEquipo, panel) {
    if (_valoresOriginalesEquipoAdmin[idEquipo]) return;
    const snapshot = {};
    panel.querySelectorAll(".dato-fila:not(.dato-solo-lectura)").forEach(filaDato => {
        const etiqueta = filaDato.querySelector(".etiqueta-dato")?.textContent;
        const campo = _mapaEtiquetasEquipo[etiqueta];
        if (!campo) return;
        snapshot[campo] = filaDato.querySelector(".valor-dato")?.textContent.trim() ?? "";
    });
    _valoresOriginalesEquipoAdmin[idEquipo] = snapshot;
    _cambiosEquipoAdmin[idEquipo] = {};
}

function _actualizarBotonAceptarEquipo(idEquipo) {
    const btn = document.getElementById(`btnAceptarEquipo-${idEquipo}`);
    if (btn) btn.disabled = Object.keys(_cambiosEquipoAdmin[idEquipo] || {}).length === 0;
}

function editarDatoEquipoAdmin(evento, boton) {
    evento.stopPropagation();
    const filaDato = boton.closest(".dato-fila");
    const idEquipo = boton.closest(".fila-usuario").dataset.id;
    const etiqueta = filaDato.querySelector(".etiqueta-dato").textContent;
    const campo = _mapaEtiquetasEquipo[etiqueta];
    const spanValor = filaDato.querySelector(".valor-dato");

    if (spanValor.classList.contains("input-edicion")) return;

    const valorActual = spanValor.textContent.trim();
    let control;

    if (etiqueta === "Máx. miembros") {
        control = document.createElement("select");
        control.className = "valor-dato input-edicion";
        [5, 10, 15, 20, 50, 100].forEach(v => {
            const opt = document.createElement("option");
            opt.value = v;
            opt.textContent = v;
            if (String(v) === valorActual) opt.selected = true;
            control.appendChild(opt);
        });
    } else if (etiqueta === "Descripción") {
        control = document.createElement("textarea");
        control.className = "valor-dato input-edicion";
        control.rows = 2;
        control.value = valorActual;
    } else {
        control = document.createElement("input");
        control.type = "text";
        control.className = "valor-dato input-edicion";
        control.value = valorActual;
    }

    const eventoRastreo = control.tagName === "SELECT" ? "change" : "input";
    control.addEventListener(eventoRastreo, () => {
        if (!campo) return;
        const valorOriginal = _valoresOriginalesEquipoAdmin[idEquipo]?.[campo] ?? "";
        const valorNuevo = control.tagName === "SELECT"
            ? control.options[control.selectedIndex].value
            : control.value.trim();
        if (!_cambiosEquipoAdmin[idEquipo]) _cambiosEquipoAdmin[idEquipo] = {};
        if (valorNuevo !== valorOriginal) {
            _cambiosEquipoAdmin[idEquipo][campo] = valorNuevo;
        } else {
            delete _cambiosEquipoAdmin[idEquipo][campo];
        }
        _actualizarBotonAceptarEquipo(idEquipo);
    });

    spanValor.replaceWith(control);
    boton.textContent = "✅";
    boton.onclick = (e) => confirmarEdicionDatoEquipoAdmin(e, boton, control);
    control.focus();
}

function confirmarEdicionDatoEquipoAdmin(evento, boton, control) {
    evento.stopPropagation();
    const filaDato = boton.closest(".dato-fila");
    const idEquipo = boton.closest(".fila-usuario").dataset.id;
    const etiqueta = filaDato.querySelector(".etiqueta-dato").textContent;
    const campo = _mapaEtiquetasEquipo[etiqueta];

    const nuevoValor = control.tagName === "SELECT"
        ? control.options[control.selectedIndex].value
        : control.value.trim();

    const spanValor = document.createElement("span");
    spanValor.className = "valor-dato";
    spanValor.textContent = nuevoValor;
    control.replaceWith(spanValor);

    boton.textContent = "✏️";
    boton.onclick = (e) => editarDatoEquipoAdmin(e, boton);

    if (campo) {
        const valorOriginal = _valoresOriginalesEquipoAdmin[idEquipo]?.[campo] ?? "";
        if (!_cambiosEquipoAdmin[idEquipo]) _cambiosEquipoAdmin[idEquipo] = {};
        if (nuevoValor !== valorOriginal) {
            _cambiosEquipoAdmin[idEquipo][campo] = nuevoValor;
        } else {
            delete _cambiosEquipoAdmin[idEquipo][campo];
        }
        _actualizarBotonAceptarEquipo(idEquipo);
    }

    // Si no quedan campos abiertos, resetear botón global
    const panel = boton.closest(".panel-desplegable");
    if (panel && !panel.querySelector(".input-edicion")) {
        const btnGlobal = panel.closest(".fila-usuario")?.querySelector(".btn-lapiz");
        if (btnGlobal) { btnGlobal.textContent = "✏️"; btnGlobal.dataset.modoEdicion = "false"; }
    }
}

function editarTodoEquipoAdmin(evento, boton) {
    evento.stopPropagation();
    const fila = boton.closest(".fila-usuario");
    const panel = fila.querySelector(".panel-desplegable");
    const idEquipo = fila.dataset.id;

    if (panel.classList.contains("oculto")) {
        panel.classList.remove("oculto");
        fila.querySelector(".cabecera-fila").classList.add("abierto");
    }
    _capturarValoresEquipoAdmin(idEquipo, panel);

    const enModoEdicion = boton.dataset.modoEdicion === "true";
    if (enModoEdicion) {
        panel.querySelectorAll(".btn-lapiz-dato").forEach(lapiz => {
            const campoEditable = lapiz.closest(".dato-fila").querySelector(".input-edicion");
            if (campoEditable) confirmarEdicionDatoEquipoAdmin(evento, lapiz, campoEditable);
        });
        boton.textContent = "✏️";
        boton.dataset.modoEdicion = "false";
    } else {
        panel.querySelectorAll(".btn-lapiz-dato").forEach(lapiz => {
            const spanValor = lapiz.closest(".dato-fila").querySelector(".valor-dato");
            if (spanValor && !spanValor.classList.contains("input-edicion")) editarDatoEquipoAdmin(evento, lapiz);
        });
        boton.textContent = "✅";
        boton.dataset.modoEdicion = "true";
    }
}

function restablecerCambiosEquipoAdmin(idEquipo) {
    const originales = _valoresOriginalesEquipoAdmin[idEquipo];
    if (!originales) return;
    const fila = document.querySelector(`.fila-usuario[data-id="${idEquipo}"]`);
    if (!fila) return;

    fila.querySelectorAll(".dato-fila:not(.dato-solo-lectura)").forEach(filaDato => {
        const etiqueta = filaDato.querySelector(".etiqueta-dato")?.textContent;
        const campo = _mapaEtiquetasEquipo[etiqueta];
        if (!campo) return;
        const control = filaDato.querySelector(".input-edicion");
        const botonLapiz = filaDato.querySelector(".btn-lapiz-dato");
        if (control) {
            const span = document.createElement("span");
            span.className = "valor-dato";
            span.textContent = originales[campo] ?? "";
            control.replaceWith(span);
            if (botonLapiz) {
                botonLapiz.textContent = "✏️";
                botonLapiz.onclick = (e) => editarDatoEquipoAdmin(e, botonLapiz);
            }
        } else {
            const span = filaDato.querySelector(".valor-dato");
            if (span) span.textContent = originales[campo] ?? "";
        }
    });

    _cambiosEquipoAdmin[idEquipo] = {};
    _actualizarBotonAceptarEquipo(idEquipo);

    const btnGlobal = fila.querySelector(".btn-lapiz");
    if (btnGlobal && btnGlobal.dataset.modoEdicion === "true") {
        btnGlobal.textContent = "✏️";
        btnGlobal.dataset.modoEdicion = "false";
    }
}

function aceptarCambiosEquipoAdmin(idEquipo) {
    const cambios = _cambiosEquipoAdmin[idEquipo];
    if (!cambios || Object.keys(cambios).length === 0) return;

    const promesas = Object.entries(cambios).map(([campo, valor]) => {
        return fetch(`/admin/equipo/${idEquipo}/info`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ campo, valor })
        }).then(async r => {
            const data = await r.json();
            if (!r.ok) throw new Error(data.error || "Error al guardar");
            return data;
        });
    });

    Promise.all(promesas)
        .then(() => {
            if (_valoresOriginalesEquipoAdmin[idEquipo]) {
                Object.assign(_valoresOriginalesEquipoAdmin[idEquipo], cambios);
            }
            _cambiosEquipoAdmin[idEquipo] = {};
            _actualizarBotonAceptarEquipo(idEquipo);

            const fila = document.querySelector(`.fila-usuario[data-id="${idEquipo}"]`);
            if (fila && cambios.nombre) {
                fila.querySelector(".cabecera-fila .nombre-fila").textContent = cambios.nombre;
                fila.dataset.nombre = cambios.nombre;
            }
            const btnGlobal = fila?.querySelector(".btn-lapiz");
            if (btnGlobal) { btnGlobal.textContent = "✏️"; btnGlobal.dataset.modoEdicion = "false"; }

            mostrarAvisoAdmin("Cambios guardados", "exito");
        })
        .catch(err => _mostrarErrorEquipoAdmin(err.message));
}

function _mostrarErrorEquipoAdmin(mensaje) {
    document.getElementById("mensajeErrorEquipoAdmin").textContent = mensaje;
    document.getElementById("modalErrorEquipoAdmin").classList.remove("oculto");
}

let _idEquipoParaBorrar = null;

function abrirModalBorrarEquipo(evento, idEquipo, nombre) {
    evento.stopPropagation();
    _idEquipoParaBorrar = idEquipo;
    document.getElementById("nombreEquipoBorrar").textContent = nombre;
    document.getElementById("modalBorrarEquipoAdmin").classList.remove("oculto");
}

function cerrarModalBorrarEquipoAdmin() {
    _idEquipoParaBorrar = null;
    document.getElementById("modalBorrarEquipoAdmin").classList.add("oculto");
}

function confirmarBorrarEquipoAdmin() {
    if (!_idEquipoParaBorrar) return;
    fetch(`/admin/equipo/${_idEquipoParaBorrar}`, { method: "DELETE" })
        .then(r => r.json())
        .then(data => {
            if (data.error) { _mostrarErrorEquipoAdmin(data.error); return; }
            document.querySelector(`.fila-usuario[data-id="${_idEquipoParaBorrar}"]`)?.remove();
            _actualizarPaginacion("listaEquiposAdmin", ".fila-usuario");
            cerrarModalBorrarEquipoAdmin();
        })
        .catch(() => _mostrarErrorEquipoAdmin("Error de red al borrar el equipo"));
}

function expulsarMiembroEquipoAdmin(idEquipo, idUsuario, boton) {
    fetch(`/admin/equipo/${idEquipo}/miembro/${idUsuario}`, { method: "DELETE" })
        .then(r => r.json())
        .then(data => {
            if (data.error) { _mostrarErrorEquipoAdmin(data.error); return; }
            boton.closest(".elemento-participante")?.remove();
            const fila = document.querySelector(`.fila-usuario[data-id="${idEquipo}"]`);
            if (fila) {
                const actuales = fila.querySelectorAll(".elemento-participante").length;
                const max = fila.querySelector(".panel-desplegable .dato-fila:nth-child(3) .valor-dato")?.textContent || "?";
                fila.querySelector(".contador-torneos-badge").textContent = `${actuales} / ${max} miembros`;
            }
        })
        .catch(() => _mostrarErrorEquipoAdmin("Error de red al expulsar miembro"));
}

function toggleCapitanEquipoAdmin(idEquipo, idUsuario, boton) {
    fetch(`/admin/equipo/${idEquipo}/capitan/${idUsuario}`, { method: "PATCH" })
        .then(r => r.json())
        .then(data => {
            if (data.error) { _mostrarErrorEquipoAdmin(data.error); return; }
            const li = boton.closest(".elemento-participante");
            const esCapitanAhora = data.rol === "capitan";
            li.dataset.esCapitan = esCapitanAhora ? "true" : "false";

            const badge = li.querySelector(".rol-capitan");
            const nombreSpan = li.querySelector(".nombre-participante");

            if (esCapitanAhora) {
                if (!badge) {
                    const nuevosBadge = document.createElement("span");
                    nuevosBadge.className = "rol-participante rol-capitan";
                    nuevosBadge.textContent = "Capitán";
                    nombreSpan.appendChild(nuevosBadge);
                }
                boton.className = "btn-quitar-capitan";
                boton.textContent = "Quitar capitán";
            } else {
                if (badge) badge.remove();
                boton.className = "btn-hacer-capitan";
                boton.textContent = "Hacer capitán";
            }
        })
        .catch(() => _mostrarErrorEquipoAdmin("Error de red al cambiar capitán"));
}

function filtrarEquiposAdmin(texto) {
    const q = texto.toLowerCase();
    document.querySelectorAll("#listaEquiposAdmin .fila-usuario").forEach(fila => {
        fila.classList.toggle("oculto", !fila.dataset.nombre.toLowerCase().includes(q));
    });
    _resetPagina("listaEquiposAdmin");
    _actualizarPaginacion("listaEquiposAdmin", ".fila-usuario");
}

function ordenarEquiposAdmin(criterio) {
    const lista = document.getElementById("listaEquiposAdmin");
    if (!lista) return;
    const filas = Array.from(lista.querySelectorAll(":scope > .fila-usuario"));
    filas.sort((a, b) => {
        if (criterio === "miembros") return parseInt(b.dataset.miembros) - parseInt(a.dataset.miembros);
        return (a.dataset.nombre || "").localeCompare(b.dataset.nombre || "");
    });
    filas.forEach(f => lista.appendChild(f));
    _resetPagina("listaEquiposAdmin");
    _actualizarPaginacion("listaEquiposAdmin", ".fila-usuario");
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("listaEquiposAdmin")) {
        _actualizarPaginacion("listaEquiposAdmin", ".fila-usuario");
        document.querySelectorAll("#listaEquiposAdmin .fila-usuario").forEach(fila => {
            _capturarValoresEquipoAdmin(fila.dataset.id, fila.querySelector(".panel-desplegable"));
        });
    }
});

// ===============================
// ZONA ADMINISTRADOR JUEGOS
// ===============================

const cambiosJuego = {};
let idJuegoParaBorrar = null;
let idJuegoConfirmandoCambios = null;

let _filtroBusquedaJuego = "";
let _filtroTipoJuego = "";

function filtrarJuegos(textoBuscado) {
    _filtroBusquedaJuego = textoBuscado.toLowerCase();
    _aplicarFiltrosJuegos();
}

function filtrarJuegosPorTipo(tipo) {
    _filtroTipoJuego = tipo;
    _aplicarFiltrosJuegos();
}

function _aplicarFiltrosJuegos() {
    document.querySelectorAll("#listaJuegos .fila-usuario").forEach(fila => {
        const nombre = fila.dataset.nombre || "";
        const tipo = fila.dataset.tipoElemento || "";
        const coincideBusqueda = nombre.includes(_filtroBusquedaJuego);
        const coincideTipo = !_filtroTipoJuego || tipo === _filtroTipoJuego;
        fila.classList.toggle("oculto", !(coincideBusqueda && coincideTipo));
    });
    _resetPagina("listaJuegos");
    _actualizarPaginacion("listaJuegos", ".fila-usuario");
}

function ordenarJuegos(criterio) {
    const lista = document.getElementById("listaJuegos");
    const filas = Array.from(lista.querySelectorAll(".fila-usuario"));
    filas.sort((a, b) => {
        switch (criterio) {
            case "alfabetico":
                return (a.dataset.nombre || "").localeCompare(b.dataset.nombre || "");
            case "genero":
                return (a.dataset.genero || "").localeCompare(b.dataset.genero || "");
            case "tipo":
                return (a.dataset.tipoElemento || "").localeCompare(b.dataset.tipoElemento || "");
            default:
                return 0;
        }
    });
    filas.forEach(fila => lista.appendChild(fila));
}

function toggleDesplegableJuego(cabecera) {
    const panel = cabecera.nextElementSibling;
    const estaAbierto = !panel.classList.contains("oculto");
    panel.classList.toggle("oculto", estaAbierto);
    cabecera.classList.toggle("abierto", !estaAbierto);
}

function toggleSeccionAnadir(evento, idJuego) {
    evento.stopPropagation();
    const filaJuego = document.querySelector(`.fila-usuario[data-id="${idJuego}"]`);
    const panel = filaJuego.querySelector(".panel-desplegable");
    const seccion = document.getElementById(`anadir-${idJuego}`);
    panel.classList.remove("oculto");
    filaJuego.querySelector(".cabecera-fila").classList.add("abierto");
    seccion.classList.toggle("oculto");
}

function mostrarModalErrorJuego(mensaje) {
    document.getElementById("textoModalErrorJuego").textContent = mensaje;
    document.getElementById("modalErrorJuego").classList.remove("oculto");
}

function cerrarModalErrorJuego() {
    document.getElementById("modalErrorJuego").classList.add("oculto");
}

// ---- ABRIR DROPDOWN + FOCO EN INFO ----

function abrirInfoJuego(evento, idJuego) {
    evento.stopPropagation();
    const boton = evento.currentTarget;
    const fila = document.querySelector(`.fila-usuario[data-id="${idJuego}"]`);
    const panel = fila.querySelector(".panel-desplegable");
    const cabecera = fila.querySelector(".cabecera-fila");
    panel.classList.remove("oculto");
    cabecera.classList.add("abierto");

    const enModoEdicion = boton.dataset.modoEdicion === "true";

    if (enModoEdicion) {
        panel.querySelectorAll(".seccion-info-juego .dato-fila:not(.dato-solo-lectura)").forEach(filaDato => {
            const btnConfirmar = Array.from(filaDato.querySelectorAll(".btn-lapiz-dato")).find(b => b.textContent === "✅");
            if (btnConfirmar) btnConfirmar.click();
        });
        boton.textContent = "✏️";
        boton.dataset.modoEdicion = "false";
    } else {
        panel.querySelectorAll(".seccion-info-juego .dato-fila:not(.dato-solo-lectura)").forEach(filaDato => {
            const btnLapiz = Array.from(filaDato.querySelectorAll(".btn-lapiz-dato")).find(b => b.textContent === "✏️");
            if (btnLapiz) btnLapiz.click();
        });
        boton.textContent = "✅";
        boton.dataset.modoEdicion = "true";
    }
}

// ---- EDITAR CAMPOS DE INFO DEL JUEGO ----

function _rastrearCambioJuego(idJuego, campo, filaDato, nuevoValor, cuerpoExtra) {
    if (!cambiosJuego[idJuego]) cambiosJuego[idJuego] = {};
    const valorOriginal = filaDato.dataset.valorOriginal;
    if (nuevoValor !== valorOriginal && nuevoValor !== "") {
        cambiosJuego[idJuego][campo] = { valor: nuevoValor, extra: cuerpoExtra || {} };
    } else {
        delete cambiosJuego[idJuego][campo];
    }
    actualizarBotonAceptarJuego(idJuego);
}

function editarDatoJuego(evento, boton) {
    evento.stopPropagation();
    const filaDato = boton.closest(".dato-fila");
    const idJuego = boton.closest(".fila-usuario").dataset.id;
    const campo = filaDato.dataset.campo;
    const spanValor = filaDato.querySelector(".valor-dato");

    if (boton.dataset.editando === "true") {
        let nuevoValor, cuerpoExtra = {};

        if (campo === "genero") {
            const select = filaDato.querySelector(".input-edicion");
            const inputNuevo = filaDato.querySelector(".input-nuevo-genero");
            if (select.value === "nuevo") {
                const nombreNuevo = inputNuevo ? inputNuevo.value.trim() : "";
                if (!nombreNuevo) { mostrarModalErrorJuego("Escribe el nombre del nuevo género"); return; }
                nuevoValor = nombreNuevo;
                cuerpoExtra = { _tipo: "nuevo_genero", valor: nombreNuevo };
            } else if (select.value) {
                nuevoValor = select.options[select.selectedIndex].text;
                cuerpoExtra = { _tipo: "id_genero", idGenero: parseInt(select.value) };
                filaDato.dataset.idGenero = select.value;
            } else {
                mostrarModalErrorJuego("Selecciona un género"); return;
            }
        } else if (campo === "tipo") {
            const select = filaDato.querySelector(".input-edicion");
            nuevoValor = select.value;
            if (!nuevoValor) { mostrarModalErrorJuego("Selecciona un tipo de elemento"); return; }
        } else {
            const input = filaDato.querySelector(".input-edicion");
            nuevoValor = input.value.trim();
            if (nuevoValor.length < 3) { mostrarModalErrorJuego("El nombre debe tener al menos 3 caracteres"); return; }
        }

        filaDato.querySelectorAll(".input-edicion, .input-nuevo-genero").forEach(el => el.remove());
        spanValor.textContent = nuevoValor;
        spanValor.style.display = "";
        boton.textContent = "✏️";
        boton.dataset.editando = "false";
        _rastrearCambioJuego(idJuego, campo, filaDato, nuevoValor, cuerpoExtra);

    } else {
        boton.dataset.editando = "true";
        boton.textContent = "✅";
        spanValor.style.display = "none";
        const textoActual = spanValor.textContent.trim();

        if (campo === "nombre") {
            const input = document.createElement("input");
            input.type = "text";
            input.className = "valor-dato input-edicion";
            input.value = textoActual;
            input.addEventListener("input", () => {
                _rastrearCambioJuego(idJuego, campo, filaDato, input.value.trim(), {});
            });
            filaDato.insertBefore(input, boton);

        } else if (campo === "genero") {
            const listaGeneros = window.generosDisponibles || (typeof generosDisponibles !== "undefined" ? generosDisponibles : []);
            const select = document.createElement("select");
            select.className = "valor-dato input-edicion";
            select.innerHTML = `<option value="">-- Selecciona género --</option>`;
            listaGeneros.forEach(g => {
                const opt = document.createElement("option");
                opt.value = g.id;
                opt.textContent = g.nombre;
                if (g.nombre === textoActual) opt.selected = true;
                select.appendChild(opt);
            });
            const optNuevo = document.createElement("option");
            optNuevo.value = "nuevo";
            optNuevo.textContent = "+ Nuevo género...";
            select.appendChild(optNuevo);

            const inputNuevo = document.createElement("input");
            inputNuevo.type = "text";
            inputNuevo.className = "valor-dato input-nuevo-genero oculto";
            inputNuevo.placeholder = "Nombre del nuevo género";

            const actualizarGenero = () => {
                if (select.value === "nuevo") {
                    inputNuevo.classList.remove("oculto");
                    const nombreNuevo = inputNuevo.value.trim();
                    if (nombreNuevo) _rastrearCambioJuego(idJuego, campo, filaDato, nombreNuevo,
                        { _tipo: "nuevo_genero", valor: nombreNuevo });
                } else if (select.value) {
                    inputNuevo.classList.add("oculto");
                    const texto = select.options[select.selectedIndex].text;
                    _rastrearCambioJuego(idJuego, campo, filaDato, texto,
                        { _tipo: "id_genero", idGenero: parseInt(select.value) });
                } else {
                    inputNuevo.classList.add("oculto");
                    _rastrearCambioJuego(idJuego, campo, filaDato, "", {});
                }
            };
            select.addEventListener("change", actualizarGenero);
            inputNuevo.addEventListener("input", actualizarGenero);

            filaDato.insertBefore(select, boton);
            filaDato.insertBefore(inputNuevo, boton);

        } else if (campo === "tipo") {
            const select = document.createElement("select");
            select.className = "valor-dato input-edicion";
            select.innerHTML = `<option value="">-- Selecciona tipo --</option>`;
            ["Personajes", "Equipos", "Armas", "Personajes y Armas"].forEach(op => {
                const opt = document.createElement("option");
                opt.value = op;
                opt.textContent = op;
                if (op === textoActual) opt.selected = true;
                select.appendChild(opt);
            });
            select.addEventListener("change", () => {
                _rastrearCambioJuego(idJuego, campo, filaDato, select.value, {});
            });
            filaDato.insertBefore(select, boton);
        }
    }
}

function actualizarBotonAceptarJuego(idJuego) {
    const fila = document.querySelector(`.fila-usuario[data-id="${idJuego}"]`);
    if (!fila) return;
    const btn = fila.querySelector(".btn-aceptar-cambios");
    if (!btn) return;
    btn.disabled = Object.keys(cambiosJuego[idJuego] || {}).length === 0;
}

function abrirModalConfirmarCambiosJuego(idJuego) {
    idJuegoConfirmandoCambios = idJuego;
    const fila = document.querySelector(`.fila-usuario[data-id="${idJuego}"]`);
    const nombre = fila?.querySelector(".nombre-fila")?.textContent || "";
    document.getElementById("nombreJuegoCambios").textContent = nombre;
    document.getElementById("modalConfirmarCambiosJuego").classList.remove("oculto");
}

function cancelarModalConfirmarCambiosJuego() {
    document.getElementById("modalConfirmarCambiosJuego").classList.add("oculto");
    idJuegoConfirmandoCambios = null;
}

function confirmarGuardarCambiosJuego() {
    const idJuego = idJuegoConfirmandoCambios;
    document.getElementById("modalConfirmarCambiosJuego").classList.add("oculto");
    idJuegoConfirmandoCambios = null;

    const cambios = cambiosJuego[idJuego];
    if (!cambios || Object.keys(cambios).length === 0) return;

    const cuerpo = {};
    if (cambios.nombre) cuerpo.nombre = cambios.nombre.valor;
    if (cambios.tipo) cuerpo.tipo_elemento = cambios.tipo.valor;
    if (cambios.genero) {
        const extra = cambios.genero.extra;
        if (extra._tipo === "nuevo_genero") cuerpo.nuevo_genero = extra.valor;
        else cuerpo.id_genero = extra.idGenero;
    }

    fetch(`/admin/juegos/${idJuego}/info`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cuerpo)
    }).then(res => res.json()).then(datos => {
        if (datos.error) { mostrarModalErrorJuego(datos.error); return; }

        const fila = document.querySelector(`.fila-usuario[data-id="${idJuego}"]`);
        if (datos.nombre) {
            fila.querySelector(".nombre-fila").textContent = datos.nombre;
            fila.querySelector(`[data-campo="nombre"]`).dataset.valorOriginal = datos.nombre;
        }
        if (datos.nombre_genero) {
            const filaDatoGenero = fila.querySelector(`[data-campo="genero"]`);
            filaDatoGenero.dataset.valorOriginal = datos.nombre_genero;
            if (datos.id_genero) filaDatoGenero.dataset.idGenero = datos.id_genero;
        }
        if (datos.tipo_elemento) {
            fila.querySelector(`[data-campo="tipo"]`).dataset.valorOriginal = datos.tipo_elemento;
        }

        cambiosJuego[idJuego] = {};
        actualizarBotonAceptarJuego(idJuego);
    });
}

function restablecerCambiosJuego(idJuego) {
    const fila = document.querySelector(`.fila-usuario[data-id="${idJuego}"]`);
    if (!fila) return;

    fila.querySelectorAll(".dato-fila:not(.dato-solo-lectura)").forEach(filaDato => {
        const campo = filaDato.dataset.campo;
        if (!campo) return;
        const valorOriginal = filaDato.dataset.valorOriginal || "";

        const editables = filaDato.querySelectorAll(".input-edicion, .input-nuevo-genero");
        const boton = filaDato.querySelector(".btn-lapiz-dato");
        if (editables.length > 0) {
            editables.forEach(el => el.remove());
            const span = filaDato.querySelector(".valor-dato");
            if (span) { span.textContent = valorOriginal; span.style.display = ""; }
            if (boton) { boton.textContent = "✏️"; boton.dataset.editando = "false"; }
        } else {
            const span = filaDato.querySelector(".valor-dato");
            if (span) span.textContent = valorOriginal;
        }
    });

    cambiosJuego[idJuego] = {};
    actualizarBotonAceptarJuego(idJuego);
}

// ---- BORRAR JUEGO ----

function abrirModalBorrarJuego(evento, idJuego, nombreJuego) {
    evento.stopPropagation();
    idJuegoParaBorrar = idJuego;
    document.getElementById("nombreJuegoBorrar").textContent = nombreJuego;
    document.getElementById("modalBorrarJuego").classList.remove("oculto");
}

function cerrarModalBorrarJuego() {
    document.getElementById("modalBorrarJuego").classList.add("oculto");
}

function confirmarBorrarJuego() {
    if (!idJuegoParaBorrar) return;
    const idGuardado = idJuegoParaBorrar;
    document.getElementById("modalBorrarJuego").classList.add("oculto");

    const fila = document.querySelector(`.fila-usuario[data-id="${idGuardado}"]`);
    const torneosActivos = parseInt(fila?.dataset.torneosActivos || "0");

    if (torneosActivos > 0) {
        document.getElementById("nombreJuegoBorrarTorneos").textContent =
            fila.querySelector(".nombre-fila").textContent;
        document.getElementById("cantidadTorneosActivos").textContent = torneosActivos;
        document.getElementById("modalBorrarJuegoConTorneos").classList.remove("oculto");
    } else {
        idJuegoParaBorrar = null;
        _ejecutarBorrarJuego(idGuardado);
    }
}

function cerrarModalBorrarJuegoConTorneos() {
    document.getElementById("modalBorrarJuegoConTorneos").classList.add("oculto");
    idJuegoParaBorrar = null;
}

function confirmarBorrarJuegoConTorneos() {
    const idGuardado = idJuegoParaBorrar;
    idJuegoParaBorrar = null;
    document.getElementById("modalBorrarJuegoConTorneos").classList.add("oculto");
    _ejecutarBorrarJuego(idGuardado);
}

function _ejecutarBorrarJuego(id) {
    fetch(`/admin/juegos/${id}`, { method: "DELETE" })
        .then(res => res.json())
        .then(datos => {
            if (datos.error) { mostrarModalErrorJuego(datos.error); return; }
            document.querySelector(`.fila-usuario[data-id="${id}"]`)?.remove();
        });
}

// ---- EDITAR / BORRAR ELEMENTOS ----

function editarElementoJuego(evento, tipo, id, boton) {
    evento.stopPropagation();
    const li = boton.closest(".elemento-juego");
    const span = li.querySelector(".valor-elemento");

    if (boton.dataset.editando === "true") {
        const inputs = li.querySelectorAll(".input-edicion-elemento");
        const nombre = inputs[0]?.value.trim();
        const tipoArma = inputs[1]?.value.trim();

        if (!nombre) { mostrarModalErrorJuego("El nombre es obligatorio"); return; }

        const cuerpo = { nombre };
        if (tipo === "arma" && tipoArma) cuerpo.tipo_arma = tipoArma;

        fetch(`/admin/${tipo}/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(cuerpo)
        }).then(res => res.json()).then(datos => {
            if (datos.error) { mostrarModalErrorJuego(datos.error); return; }
            inputs.forEach(inp => inp.remove());
            span.style.display = "";
            if (tipo === "arma" && tipoArma) {
                span.innerHTML = `${nombre} <em>(${tipoArma})</em>`;
            } else {
                span.textContent = nombre;
            }
            boton.textContent = "✏️";
            boton.dataset.editando = "false";
        });
    } else {
        const textoActual = span.textContent.trim();
        span.style.display = "none";

        const inputNombre = document.createElement("input");
        inputNombre.type = "text";
        inputNombre.className = "input-edicion input-edicion-elemento";
        inputNombre.value = tipo === "arma" ? span.childNodes[0]?.textContent.trim() : textoActual;

        li.insertBefore(inputNombre, li.querySelector(".botones-elemento"));

        if (tipo === "arma") {
            const inputTipo = document.createElement("input");
            inputTipo.type = "text";
            inputTipo.className = "input-edicion input-edicion-elemento";
            inputTipo.value = span.querySelector("em")?.textContent || "";
            li.insertBefore(inputTipo, li.querySelector(".botones-elemento"));
        }

        boton.textContent = "✅";
        boton.dataset.editando = "true";
    }
}

function borrarElementoJuego(tipo, id, boton) {
    fetch(`/admin/${tipo}/${id}`, { method: "DELETE" })
        .then(res => res.json())
        .then(datos => {
            if (datos.error) { mostrarModalErrorJuego(datos.error); return; }
            boton.closest(".elemento-juego").remove();
        });
}

// ---- EDITAR / BORRAR HABILIDADES ----

function editarHabilidadJuego(evento, idJuego, idPersonaje, idArma, boton) {
    evento.stopPropagation();
    const li = boton.closest(".elemento-juego");
    const span = li.querySelector(".valor-elemento");

    if (boton.dataset.editando === "true") {
        const input = li.querySelector(".input-edicion-elemento");
        const habilidad = input?.value.trim();
        if (!habilidad) { mostrarModalErrorJuego("La habilidad es obligatoria"); return; }

        fetch(`/admin/habilidad/${idJuego}/${idPersonaje}/${idArma}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ habilidad })
        }).then(res => res.json()).then(datos => {
            if (datos.error) { mostrarModalErrorJuego(datos.error); return; }
            const textoBase = span.textContent.split(":")[0];
            span.innerHTML = `${textoBase}: <em>${habilidad}</em>`;
            input.remove();
            span.style.display = "";
            boton.textContent = "✏️";
            boton.dataset.editando = "false";
        });
    } else {
        const emActual = span.querySelector("em")?.textContent || "";
        span.style.display = "none";
        const input = document.createElement("input");
        input.type = "text";
        input.className = "input-edicion input-edicion-elemento";
        input.value = emActual;
        li.insertBefore(input, li.querySelector(".botones-elemento"));
        boton.textContent = "✅";
        boton.dataset.editando = "true";
    }
}

function borrarHabilidadJuego(idJuego, idPersonaje, idArma, boton) {
    fetch(`/admin/habilidad/${idJuego}/${idPersonaje}/${idArma}`, { method: "DELETE" })
        .then(res => res.json())
        .then(datos => {
            if (datos.error) { mostrarModalErrorJuego(datos.error); return; }
            boton.closest(".elemento-juego").remove();
        });
}

// ---- AÑADIR ELEMENTOS ----

function anadirPersonajeJuego(idJuego) {
    const input = document.getElementById(`inputAnadirPersonaje-${idJuego}`);
    const nombre = input.value.trim();
    if (nombre.length < 3) { mostrarModalErrorJuego("El nombre debe tener al menos 3 caracteres"); return; }
    fetch(`/admin/juegos/${idJuego}/personaje`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre })
    }).then(res => res.json()).then(datos => {
        if (datos.error) { mostrarModalErrorJuego(datos.error); return; }
        input.value = "";
        const lista = document.getElementById(`listaPersonajesJuego-${idJuego}`);
        const li = crearLiElemento("personaje", datos.id, datos.nombre);
        lista.appendChild(li);
        const selectPersonaje = document.getElementById(`selectAnadirPersonaje-${idJuego}`);
        if (selectPersonaje) {
            const opcion = document.createElement("option");
            opcion.value = datos.id;
            opcion.textContent = datos.nombre;
            selectPersonaje.appendChild(opcion);
        }
    });
}

function anadirEquipoJuego(idJuego) {
    const input = document.getElementById(`inputAnadirEquipo-${idJuego}`);
    const nombre = input.value.trim();
    if (nombre.length < 3) { mostrarModalErrorJuego("El nombre debe tener al menos 3 caracteres"); return; }
    fetch(`/admin/juegos/${idJuego}/club`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre })
    }).then(res => res.json()).then(datos => {
        if (datos.error) { mostrarModalErrorJuego(datos.error); return; }
        input.value = "";
        const lista = document.getElementById(`listaEquiposJuego-${idJuego}`);
        const li = crearLiElemento("club", datos.id, datos.nombre);
        lista.appendChild(li);
    });
}

function anadirArmaJuego(idJuego) {
    const inputNombre = document.getElementById(`inputAnadirNombreArma-${idJuego}`);
    const inputTipo = document.getElementById(`inputAnadirTipoArma-${idJuego}`);
    const nombre = inputNombre.value.trim();
    const tipoArma = inputTipo.value.trim();
    if (nombre.length < 3 || tipoArma.length < 3) {
        mostrarModalErrorJuego("Nombre y tipo deben tener al menos 3 caracteres");
        return;
    }
    fetch(`/admin/juegos/${idJuego}/arma`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, tipo_arma: tipoArma })
    }).then(res => res.json()).then(datos => {
        if (datos.error) { mostrarModalErrorJuego(datos.error); return; }
        inputNombre.value = "";
        inputTipo.value = "";
        const lista = document.getElementById(`listaArmasJuego-${idJuego}`);
        const li = crearLiElemento("arma", datos.id, `${datos.nombre} <em>(${datos.tipo_arma})</em>`);
        lista.appendChild(li);
        const selectArma = document.getElementById(`selectAnadirArma-${idJuego}`);
        if (selectArma) {
            const opcion = document.createElement("option");
            opcion.value = datos.id;
            opcion.textContent = datos.nombre;
            selectArma.appendChild(opcion);
        }
    });
}

function anadirHabilidadJuego(idJuego) {
    const selectPersonaje = document.getElementById(`selectAnadirPersonaje-${idJuego}`);
    const selectArma = document.getElementById(`selectAnadirArma-${idJuego}`);
    const inputHabilidad = document.getElementById(`inputAnadirHabilidad-${idJuego}`);
    const idPersonaje = parseInt(selectPersonaje.value);
    const idArma = parseInt(selectArma.value);
    const habilidad = inputHabilidad.value.trim();
    if (!idPersonaje || !idArma || habilidad.length < 3) {
        mostrarModalErrorJuego("Selecciona personaje y arma, y escribe una habilidad (mínimo 3 caracteres)");
        return;
    }
    fetch(`/admin/juegos/${idJuego}/habilidad`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_personaje: idPersonaje, id_arma: idArma, habilidad })
    }).then(res => res.json()).then(datos => {
        if (datos.error) { mostrarModalErrorJuego(datos.error); return; }
        selectPersonaje.value = "";
        selectArma.value = "";
        inputHabilidad.value = "";
        const lista = document.getElementById(`listaHabilidadesJuego-${idJuego}`);
        const nombreP = selectPersonaje.options[selectPersonaje.selectedIndex]?.text || "";
        const nombreA = selectArma.options[selectArma.selectedIndex]?.text || "";
        const li = document.createElement("li");
        li.className = "elemento-juego";
        li.dataset.idPersonaje = idPersonaje;
        li.dataset.idArma = idArma;
        li.innerHTML = `
            <span class="valor-elemento">${nombreP} → ${nombreA}: <em>${habilidad}</em></span>
            <div class="botones-elemento">
                <button class="btn-lapiz-dato" onclick="editarHabilidadJuego(event,${idJuego},${idPersonaje},${idArma},this)">✏️</button>
                <button class="btn-papelera" onclick="borrarHabilidadJuego(${idJuego},${idPersonaje},${idArma},this)">🗑️</button>
            </div>`;
        lista.appendChild(li);
    });
}

function crearLiElemento(tipo, id, htmlContenido) {
    const li = document.createElement("li");
    li.className = "elemento-juego";
    li.dataset.id = id;
    li.innerHTML = `
        <span class="valor-elemento">${htmlContenido}</span>
        <div class="botones-elemento">
            <button class="btn-lapiz-dato" onclick="editarElementoJuego(event,'${tipo}',${id},this)">✏️</button>
            <button class="btn-papelera" onclick="borrarElementoJuego('${tipo}',${id},this)">🗑️</button>
        </div>`;
    return li;
}


function cambiarPortadaJuego(idJuego, input) {
    if (!input.files[0]) return;
    const formData = new FormData();
    formData.append("portada", input.files[0]);
    fetch(`/admin/juegos/${idJuego}/portada`, { method: "PATCH", body: formData })
        .then(res => res.json())
        .then(datos => {
            if (datos.error) { mostrarModalErrorJuego(datos.error); return; }
            const img = document.getElementById(`infoPortada-${idJuego}`);
            if (img) img.src = datos.portada.startsWith("http")
                ? `${datos.portada}?t=${Date.now()}`
                : `/static/imagenes/portadas/${datos.portada}?t=${Date.now()}`;
        });
}

function buildMatchCard(nodo) {
    const j1 = nodo?.jugadores?.[0] || "---";
    const j2 = nodo?.jugadores?.[1] || "---";
    const estado    = nodo?.estado    || "";
    const resultado = nodo?.resultado || "";

    let middleHTML = "";

    if (resultado) {
        const partes = resultado.split("-");
        const s1 = parseInt(partes[0]) || 0;
        const s2 = parseInt(partes[1]) || 0;
        const clase1 = s1 > s2 ? "score-win" : s1 < s2 ? "score-lose" : "score-draw";
        const clase2 = s2 > s1 ? "score-win" : s2 < s1 ? "score-lose" : "score-draw";
        middleHTML = `
            <div class="score-row">
                <span class="score-num ${clase1}">${s1}</span>
                <span class="vs-inline">VS</span>
                <span class="score-num ${clase2}">${s2}</span>
            </div>
        `;
    } else {
        middleHTML = `<div class="vs-separator">VS</div>`;
    }

    const card = document.createElement('div');
    card.className = `match-card compact${estado === "Finalizado" ? " finished" : ""}`;

    card.innerHTML = `
        <div class="player-row">${j1}</div>
        ${middleHTML}
        <div class="player-row">${j2}</div>
    `;

    return card;
}