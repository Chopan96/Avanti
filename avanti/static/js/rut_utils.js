// Normaliza un RUT chileno (12.345.678-K)
function normalizarRut(rut) {
    if (!rut) return '';
    rut = rut.replace(/[^\dkK]/g, '').toUpperCase();
    let cuerpo = rut.slice(0, -1);
    let dv = rut.slice(-1);
    let cuerpoFormateado = parseInt(cuerpo, 10).toLocaleString('es-CL');
    return `${cuerpoFormateado}-${dv}`;
}
