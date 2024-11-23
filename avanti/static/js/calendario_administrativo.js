fetch(`/api/horarios/?medico_rut={{ medico.rut.rut }}`)
    .then(response => response.json())
    .then(data => console.log(data)); // Inspecciona los datos

document.addEventListener('DOMContentLoaded', function () {
    
        const calendarEl = document.getElementById('calendar');

        const calendar = new FullCalendar.Calendar(calendarEl, {
            
            initialView: 'timeGridWeek',
            locale: 'es',
            slotMinTime: "08:00",
            slotMaxTime: "19:00",
            slotDuration: '00:30:00',
            slotLabelFormat: {
                hour: '2-digit', 
                minute: '2-digit', 
                omitZeroMinute: false, 
                meridiem: false // Muestra las horas en formato 24 horas
            },
        
            slotLabelInterval: { minutes: 30 },
            allDaySlot: false,
            height: 'auto',
            buttonText: {
                today: 'Hoy' // Cambia "Today" a "Hoy"
            },
            events: `/api/horarios/?medico_rut={{ medico.rut.rut }}`, // URL para cargar eventos
            eventClick: function (info) {
                alert(`Horario:\nInicio: ${info.event.start}\nFin: ${info.event.end}`);
            }
        });

        calendar.render();
    });