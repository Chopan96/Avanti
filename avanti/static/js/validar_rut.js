// Referencia al campo de RUT y al mensaje de retroalimentación
const rutInput = document.getElementById('rutMedico');
const rutFeedback = document.getElementById('rutFeedback');

// Evento de validación en tiempo real (al escribir en el campo)
rutInput.addEventListener('input', function () {
    const rut = rutInput.value.trim();
    if (validarRut(rut)) {
        // Si el RUT es válido, muestra un mensaje de éxito (opcional) o limpia errores
        rutInput.classList.remove('is-invalid');
        rutInput.classList.add('is-valid');
        rutFeedback.textContent = '';
    } else {
        // Si el RUT es inválido, muestra un mensaje de error
        rutInput.classList.remove('is-valid');
        rutInput.classList.add('is-invalid');
        rutFeedback.textContent = 'El RUT ingresado no es válido.';
    }
});

// Función para validar el RUT
function validarRut(rut) {
    // Elimina puntos y guiones
    rut = rut.replace(/[^0-9kK]/g, '');
    if (rut.length < 8) return false;

    const cuerpo = rut.slice(0, -1);
    const dv = rut.slice(-1).toUpperCase();

    // Valida que solo tenga números en el cuerpo
    if (!/^\d+$/.test(cuerpo)) return false;

    // Calcula el dígito verificador
    let suma = 0;
    let multiplo = 2;

    for (let i = cuerpo.length - 1; i >= 0; i--) {
        suma += parseInt(cuerpo[i]) * multiplo;
        multiplo = multiplo === 7 ? 2 : multiplo + 1;
    }

    const resto = suma % 11;
    const dvEsperado = resto === 0 ? '0' : resto === 1 ? 'K' : String(11 - resto);

    return dv === dvEsperado;
}
