document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    const medicoRut = calendarEl.getAttribute('data-medico-rut');
    const horarioActions = document.getElementById('horario-actions');
    const saveBtn = document.getElementById('saveBtn');
    const deleteBtn = document.getElementById('deleteBtn');
    let selectedEventId = null; // Variable para guardar el ID del evento seleccionado

    // Obtener el token CSRF desde la cookie
    const csrfToken = document.cookie.split('csrftoken=')[1].split(';')[0];

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        locale: 'es',
        timeZone: 'local', // Usamos la zona horaria local del navegador
        slotMinTime: "08:00",
        slotMaxTime: "19:00",
        slotDuration: '00:30:00',
        slotLabelFormat: { hour: '2-digit', minute: '2-digit', omitZeroMinute: false, meridiem: false },
        slotLabelInterval: { minutes: 30 },
        allDaySlot: false,
        height: 'auto',
        buttonText: { today: 'Hoy' },
        events: `/api/horarios/?medico_rut=${medicoRut}`,
        editable: true,
        eventClick: function (info) {
            const event = info.event;
            selectedEventId = event.id;

            // Convertir la hora de UTC a la zona horaria local antes de mostrarla
            const fechaInicioLocal = new Date(event.start.getTime() - event.start.getTimezoneOffset() * 60000);
            const fechaFinLocal = new Date(event.end.getTime() - event.end.getTimezoneOffset() * 60000);

            // Asignar los valores al formulario de edición en el formato adecuado
            document.getElementById('fechainicio').value = fechaInicioLocal.toISOString().slice(0, 16);
            document.getElementById('fechafin').value = fechaFinLocal.toISOString().slice(0, 16);

            horarioActions.style.display = 'block';
        },
        eventDrop: function (info) {
            const event = info.event;
            // Convertir la nueva fecha de inicio y fin a la zona horaria local
            const fechaInicioLocal = new Date(event.start.getTime() - event.start.getTimezoneOffset() * 60000);
            const fechaFinLocal = new Date(event.end.getTime() - event.end.getTimezoneOffset() * 60000);

            // Actualizamos los campos del formulario con las nuevas fechas
            document.getElementById('fechainicio').value = fechaInicioLocal.toISOString().slice(0, 16);
            document.getElementById('fechafin').value = fechaFinLocal.toISOString().slice(0, 16);
        }
    });

    calendar.render();

    // Convertir las fechas a la zona horaria local antes de enviarlas al backend
    saveBtn.addEventListener('click', function () {
        const fechainicio = new Date(document.getElementById('fechainicio').value);
        const fechafin = new Date(document.getElementById('fechafin').value);
        
        // Convertir las fechas a la zona horaria local
        const localTimezoneOffset = fechainicio.getTimezoneOffset(); // Offset en minutos

        // Ajustar las fechas a la zona horaria local
        fechainicio.setMinutes(fechainicio.getMinutes() - localTimezoneOffset);
        fechafin.setMinutes(fechafin.getMinutes() - localTimezoneOffset);
        
        document.getElementById('fechainicio').value = fechainicio.toISOString().slice(0, 16);  // Convertir a formato ISO 8601 sin la zona horaria
        document.getElementById('fechafin').value = fechafin.toISOString().slice(0, 16);  // Convertir a formato ISO 8601 sin la zona horaria
        
        if (!selectedEventId) {
            alert("Por favor selecciona un evento para editar.");
            return;
        }
        
        fetch(`/api/horarios/${selectedEventId}/editar/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken // Incluir el token CSRF
            },
            body: JSON.stringify({ 
                fechainicio: fechainicio.toISOString(), 
                fechafin: fechafin.toISOString() 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Horario actualizado.');
                calendar.refetchEvents();
                horarioActions.style.display = 'none';
            } else {
                alert('Error al actualizar el horario: ' + data.message);
            }
        })
        .catch(err => {
            console.error('Error al hacer la solicitud:', err);
            alert('Hubo un error al intentar actualizar el horario.');
        });
    });

    // Eliminar horario
    deleteBtn.addEventListener('click', function () {
        if (!selectedEventId) {
            alert("Por favor selecciona un evento para eliminar.");
            return;
        }

        fetch(`/api/horarios/${selectedEventId}/eliminar/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken // Incluir el token CSRF
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Horario eliminado.');
                calendar.refetchEvents();
                horarioActions.style.display = 'none';
            } else {
                alert('Error al eliminar el horario: ' + data.message);
            }
        })
        .catch(err => {
            console.error('Error al hacer la solicitud:', err);
            alert('Hubo un error al intentar eliminar el horario.');
        });
    });
});

