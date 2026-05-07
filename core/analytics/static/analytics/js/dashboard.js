document.addEventListener("DOMContentLoaded", function () {
    const chartCanvas = document.getElementById("mychart");
    const tableBody = document.getElementById("health-records-body");

    fetch("/api/dashboard/")
        .then(response => response.json())
        .then(data => {
            const summary = data.summary;
            const customers = data.customers;

            document.getElementById("total-customers").textContent = summary.total_customers;
            document.getElementById("average-health-score").textContent = summary.average_health_score;
            document.getElementById("healthy-count").textContent = summary.healthy;
            document.getElementById("watch-count").textContent = summary.watch;
            document.getElementById("high-risk-count").textContent = summary.high_risk;

            new Chart(chartCanvas, {
                type: "doughnut",
                data: {
                    labels: ["Healthy", "Watch", "High Risk"],
                    datasets: [{
                        data: [summary.healthy, summary.watch, summary.high_risk],
                        backgroundColor: ["#2ecc71", "#f1c40f", "#e74c3c"],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function (context) {
                                    const value = context.raw;
                                    const chartData = context.dataset.data;
                                    const total = chartData.reduce((sum, val) => sum + val, 0);
                                    const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;

                                    return `${context.label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });

            tableBody.innerHTML = "";

            customers.forEach((customer, index) => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>
                        <a href="/customers/${customer.id}/">
                            ${customer.company_name}
                        </a>
                    </td>
                    <td>${customer.app_name}</td>
                    <td>${customer.health_score}</td>
                    <td>${customer.churn_risk}</td>
                    <td>${customer.ml_churn_probability}</td>
                    <td>${customer.risk_label}</td>
                `;

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error loading dashboard data:", error);
        });

    fetch("/api/ml/metrics")
        .then(response => response.json())
        .then(metrics => {
            document.getElementById("ml-accuracy").textContent = `${metrics.accuracy}%`
        })
        .catch(error => {
            console.error("Error loading ML metrics:", error);
            document.getElementById("ml-accuracy").textContent = "N/A";
        });

    fetch("/api/ml/feature-importance/")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("feature-importance-body");
            tableBody.innerHTML = "";

            data.feature_importance.forEach(item => {
                const featureLabels = {
                    usage_score: "Usage Score",
                    feature_adoption_score: "Feature Adoption Score",
                    reliability_score: "Reliability Score",
                    support_score: "Support Score",
                    company_size: "Company Size"
                };

                const row = document.createElement("tr");

                const interpretation = item.coefficient > 0
                    ? "Increases churn risk"
                    : "Decreases churn risk";

                row.innerHTML = `
                <td>${featureLabels[item.feature] || item.feature}</td>
                <td>${item.coefficient}</td>
                <td>${interpretation}</td>
            `;

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error loading feature importance:", error);
        });
});