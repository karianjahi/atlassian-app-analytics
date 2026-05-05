let eventChartInstance = null;
let timeChartInstance = null;

document.addEventListener("DOMContentLoaded", function () {

    const eventLabels = JSON.parse(document.getElementById("event-labels").textContent);
    const eventCounts = JSON.parse(document.getElementById("event-counts").textContent);
    const timeLabels = JSON.parse(document.getElementById("time-labels").textContent);
    const timeCounts = JSON.parse(document.getElementById("time-counts").textContent);

    const eventCanvas = document.getElementById("eventChart");

    if (eventCanvas) {
        if (eventChartInstance) {
            eventChartInstance.destroy(); // otherwise it plots on top in a loop
        }
        eventChartInstance = new Chart(eventCanvas, {
            type: "bar",
            data: {
                labels: eventLabels,
                datasets: [{
                    label: "Number of Events",
                    data: eventCounts
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
    const timeCanvas = document.getElementById("timeChart");

    if (timeCanvas) {
        if (timeChartInstance) {
            timeChartInstance.destroy();
        }
        timeChartInstance = new Chart(timeCanvas, {
            type: "line",
            data: {
                labels: timeLabels,
                datasets: [{
                    label: "Events Over Time",
                    data: timeCounts,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        })
    }
});