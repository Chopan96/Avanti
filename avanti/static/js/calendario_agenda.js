document.addEventListener('DOMContentLoaded', function () {
    const fechaInput = document.getElementById('fecha');
    const horariosList = document.getElementById('horarios-list');
    const horarios = Array.from(horariosList.children);

    fechaInput.addEventListener('change', function () {
        const fechaSeleccionada = this.value;

        horarios.forEach(horario => {
            const fechaHorario = horario.getAttribute('data-fecha');
            if (fechaHorario === fechaSeleccionada) {
                horario.style.display = '';
            } else {
                horario.style.display = 'none';
            }
        });
    });
});