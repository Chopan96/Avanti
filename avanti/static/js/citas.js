document.addEventListener('DOMContentLoaded', function () {
    const fechasConHorarios = [...new Set(horarios.map(h => h.extendedProps.fecha))];
    const calendarEl = document.getElementById('calendar'); // El contenedor del calendario
    const modalEl = document.getElementById('modal'); // El modal para confirmar la cita
    const contactoForm = document.getElementById('contactoForm'); // Formulario de contacto
    const modalSubmitBtn = document.getElementById('modalSubmitBtn'); // Botón de confirmar
    const horariosListEl = document.getElementById('horariosList'); // Lista de horarios, si existe
    let calendar; // Variable para almacenar la instancia de FullCalendar

    // Inicializar FullCalendar
    calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es', // Idioma español
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: function (fetchInfo, successCallback, failureCallback) {
            const medicoRut = "{{ medico.rut.rut }}";  // Ajusta esto según cómo tengas el RUT del médico

            fetch(`/api/horarios/${medicoRut}/`)
                .then(response => response.json())
                .then(data => {
                    // Procesar los datos y agregar al calendario
                    horarios = data.map(item => ({
                        id: item.id,
                        title: `Sala: ${item.extendedProps.sala}`,
                        start: item.start,
                        end: item.end,
                        extendedProps: {
                            medico: item.extendedProps.medico,
                            sala: item.extendedProps.sala,
                            fecha: item.extendedProps.fecha,
                            hora: item.extendedProps.hora
                        }
                    }));

                    // Cargar los eventos al calendario
                    calendar.addEventSource(horarios);
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Hubo un problema al cargar los horarios.');
                });
        },
        eventClick: function (info) {
            const horario = info.event.extendedProps;
            const horarioIdInput = document.getElementById('horarioId');
            horarioIdInput.value = info.event.id; // Asignar ID del horario al input oculto
            modalEl.style.display = 'block'; // Mostrar modal
        }
    });

    // Renderizar el calendario
    calendar.render();

    // Capturar clic en el botón de "Confirmar"
    modalSubmitBtn.addEventListener('click', function () {
        const formData = new FormData(contactoForm);
        const horarioId = document.getElementById('horarioId').value;

        if (!horarioId) {
            alert("No se ha seleccionado un horario.");
            return;
        }

        formData.append('horario_id', horarioId);

        fetch("{% url 'administrativo:reservar_cita' %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Cita reservada con éxito');
                    modalEl.style.display = 'none';
                    calendar.refetchEvents(); // Actualizar eventos en el calendario
                } else {
                    alert(data.error || 'Error al reservar la cita.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un problema al procesar la solicitud.');
            });
    });

    // Configurar el ID del horario al abrir el modal (para listas de horarios)
    if (horariosListEl) {
        horariosListEl.addEventListener('click', function (e) {
            if (e.target.classList.contains('agendar-btn')) {
                const horarioId = e.target.dataset.horarioId;
                document.getElementById('horarioId').value = horarioId;
                modalEl.style.display = 'block';
            }
        });
    }
});
