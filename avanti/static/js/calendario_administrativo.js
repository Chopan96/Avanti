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
            document.getElementById('fechainicio').value = event.start.toISOString().slice(0, 16);
            document.getElementById('fechafin').value = event.end.toISOString().slice(0, 16);
            horarioActions.style.display = 'block';
        }
    });

    calendar.render();

    // Guardar cambios
    saveBtn.addEventListener('click', function () {
        const fechainicio = document.getElementById('fechainicio').value;
        const fechafin = document.getElementById('fechafin').value;
    
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
            body: JSON.stringify({ fechainicio, fechafin })
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