document.addEventListener("DOMContentLoaded", function() { // wait for html content to load
    const ctx = document.getElementById("mychart"); // find canvas with id mychart

    if (!ctx) {
        console.error("healthChart canvas not found"); // error if no canvas found in html
        return;
    }

    // if (!window.healthData) {
    //     console.error("healthData not found"); // error if no health data found
    //     return;
    // }

    // const healthy = JSON.parse(document.getElementById("healthy-count").textContent);
    // const watch = JSON.parse(document.getElementById("watch-count").textContent);
    // const highRisk = JSON.parse(document.getElementById("high-risk-count").textContent);

    fetch("/api/summary/")
        .then(response => response.json())
        .then(data => {

            const healthy = data.healthy;
            const watch = data.watch;
            const highRisk = data.high_risk;

            new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: ["Healthy", "Watch", "High Risk"],
                    datasets: [{
                        data: [healthy, watch, highRisk],
                        backgroundColor: [
                            "#2ecc71",
                            "#f1c40f",
                            "#e74c3c"
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.raw;
                                    const data = context.dataset.data;
                                    const total = data.reduce((sum, val) => sum + val, 0);

                                    const percentage = total > 0
                                        ? ((value / total) * 100).toFixed(1)
                                        : 0;

                                    return `${context.label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });

        })
        .catch(error => {
            console.error("Error loading summary data:", error);
        });
});