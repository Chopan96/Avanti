document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    const calendarContainer = document.getElementById('calendario');
    const medicoForm = document.getElementById('medicoForm');

    medicoForm.addEventListener('submit', function (event) {
        event.preventDefault();  // Previene el envío del formulario
        console.log("Formulario enviado");
        const medicoRut = document.getElementById('medicoRut').value;

        if (!medicoRut) {
            alert("Por favor, ingresa un RUT válido.");
            return;
        }

        // Muestra el contenedor del calendario si estaba oculto
        calendarContainer.style.display = 'block';

        // Renderiza el calendario con los horarios del médico ingresado
        renderCalendar(medicoRut);
    });

    function renderCalendar(medicoRut) {
        console.log("Renderizando calendario para RUT:", medicoRut);
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'timeGridWeek',
            locale: 'es',
            slotMinTime: "09:00",
            slotMaxTime: "16:00",
            slotDuration: '00:30:00',
            allDaySlot: false,
            height: 'auto',
            buttonText: {
                today: 'Hoy' // Cambia "Today" a "Hoy"
            },
            events: `/api/horarios/?medico_rut=${medicoRut}`, // Pasar el RUT al backend
            eventDidMount: function(info) {
                // Si no hay eventos después de intentar cargar
                if (info.eventSources[0].internalEventSource.meta.hasEvents === false) {
                    alert("No hay horarios disponibles para el RUT ingresado.");
                    calendarContainer.style.display = 'none'; // Ocultar calendario
                }
            },
            eventClick: function (info) {
                const extendedProps = info.event.extendedProps;

                const eventDetails = `
                    <h4>Detalles del Horario</h4>
                    <p><strong>Médico:</strong> ${extendedProps.medico_rut}</p>
                    <p><strong>Sala:</strong> ${extendedProps.sala}</p>
                    <p><strong>Fecha:</strong> ${extendedProps.fecha}</p>
                `;

                document.getElementById('scheduleContent').innerHTML = eventDetails;
                document.getElementById('overlay').style.display = 'block';
                document.getElementById('modal').style.display = 'block';
            },
        });

        calendar.render();
    }
});