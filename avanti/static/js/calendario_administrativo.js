document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    const medicoRut = calendarEl.getAttribute('data-medico-rut');
    const horarioActions = document.getElementById('horario-actions');
    const saveBtn = document.getElementById('saveBtn');
    const deleteBtn = document.getElementById('deleteBtn');
    const modalMessage = document.getElementById('modalMessage');
    const messageModal = new bootstrap.Modal(document.getElementById('messageModal'));
    let selectedEventId = null;

    const csrfToken = document.cookie.split('csrftoken=')[1].split(';')[0];

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        locale: 'es',
        timeZone: 'local',
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

            const fechaInicioLocal = new Date(event.start.getTime() - event.start.getTimezoneOffset() * 60000);
            const fechaFinLocal = new Date(event.end.getTime() - event.end.getTimezoneOffset() * 60000);

            document.getElementById('fechainicio').value = fechaInicioLocal.toISOString().slice(0, 16);
            document.getElementById('fechafin').value = fechaFinLocal.toISOString().slice(0, 16);

            horarioActions.style.display = 'block';
        }
    });

    calendar.render();

    saveBtn.addEventListener('click', function () {
        const fechainicio = new Date(document.getElementById('fechainicio').value);
        const fechafin = new Date(document.getElementById('fechafin').value);

        fechainicio.setMinutes(fechainicio.getMinutes() - fechainicio.getTimezoneOffset());
        fechafin.setMinutes(fechafin.getMinutes() - fechafin.getTimezoneOffset());

        if (!selectedEventId) {
            showModalMessage("Por favor selecciona un evento para editar.");
            return;
        }

        fetch(`/api/horarios/${selectedEventId}/editar/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ 
                fechainicio: fechainicio.toISOString(), 
                fechafin: fechafin.toISOString() 
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showModalMessage('Horario actualizado correctamente.');
                calendar.refetchEvents();
                horarioActions.style.display = 'none';
            } else {
                showModalMessage('Error al actualizar el horario: ' + data.message);
            }
        })
        .catch(err => {
            console.error('Error:', err);
            showModalMessage('Hubo un error al intentar actualizar el horario.');
        });
    });

    deleteBtn.addEventListener('click', function () {
        if (!selectedEventId) {
            showModalMessage("Por favor selecciona un evento para eliminar.");
            return;
        }

        fetch(`/api/horarios/${selectedEventId}/eliminar/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showModalMessage('Horario eliminado correctamente.');
                calendar.refetchEvents();
                horarioActions.style.display = 'none';
            } else {
                showModalMessage('Error al eliminar el horario: ' + data.message);
            }
        })
        .catch(err => {
            console.error('Error:', err);
            showModalMessage('Hubo un error al intentar eliminar el horario.');
        });
    });

    function showModalMessage(message) {
        modalMessage.textContent = message;
        messageModal.show();
    }
});

