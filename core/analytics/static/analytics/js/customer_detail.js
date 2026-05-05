document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById("eventChart");

    if (!canvas) {
        console.error("eventChart canvas not found")
        return;
    }

    if (!window.eventData) {
        console.error("eventData not found")
        return;
    }

    const ctx = canvas.getContext("2d");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: window.eventData.labels,
            datasets: [{
                label: "Number of Events",
                data: window.eventData.counts,
                backgroundColor: "#c2910a"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRation: false
        }
    });
});