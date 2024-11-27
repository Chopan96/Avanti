document.addEventListener('DOMContentLoaded', function() {
    // Capturamos el JSON que pasamos desde Django
    const horarios = JSON.parse(document.getElementById('horarios-data').textContent);
    
    // Depuración: Verifica los datos que se están pasando a JavaScript
    console.log("Eventos cargados:", horarios);

    var calendarEl = document.getElementById('calendar');
    
    // Depuración: Verifica si el contenedor del calendario se está encontrando correctamente
    if (calendarEl) {
        console.log("Contenedor del calendario encontrado:", calendarEl);
    } else {
        console.error("No se encontró el contenedor del calendario.");
    }

    // Inicializar FullCalendar
    var calendar = new FullCalendar.Calendar(calendarEl, {
        selectable: true,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: horarios,  // Los eventos cargados desde Django
        dateClick: function(info) {
            // Al hacer clic en una fecha, filtramos los horarios
            var fechaSeleccionada = info.dateStr;
            console.log('Fecha seleccionada:', fechaSeleccionada);  // Verifica la fecha seleccionada

            // Filtrar los horarios en la lista según la fecha seleccionada
            const horariosList = document.getElementById('horarios-list');
            const horariosDias = Array.from(horariosList.children);

            // Depuración: Verifica la cantidad de días en la lista de horarios
            console.log("Número de días en la lista de horarios:", horariosDias.length);

            horariosDias.forEach(dia => {
                const diaFecha = dia.getAttribute('data-fecha');
                console.log('Fecha del horario:', diaFecha);  // Verifica las fechas de los horarios

                if (diaFecha === fechaSeleccionada) {
                    dia.style.display = '';
                } else {
                    dia.style.display = 'none';
                }
            });
        }
    });

    // Depuración: Verifica si el calendario se está renderizando
    try {
        calendar.render();
        console.log("Calendario renderizado correctamente.");
    } catch (error) {
        console.error("Error al renderizar el calendario:", error);
    }
});