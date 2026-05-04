document.addEventListener("DOMContentLoaded", function() { // wait for html content to load
    const ctx = document.getElementById("mychart"); // find canvas with id mychart

    if (!ctx) {
        console.error("healthChart canvas not found"); // error if no canvas found in html
        return;
    }

    if (!window.healthData) {
        console.error("healthData not found"); // error if no health data found
        return;
    }

    new Chart(ctx, { // plot the chart
        type: "doughnut",
        data: {
            labels: ["Healthy", "Watch", "High Risk"],
            datasets: [{
                data: [
                    window.healthData.healthy,
                    window.healthData.watch,
                    window.healthData.high_risk
                ],
                backgroundColor: [
                    "#2ecc71",  // green
                    "#f1c40f",  // yellow
                    "#e74c3c"   // red
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
});