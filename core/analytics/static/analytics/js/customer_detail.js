let eventChartInstance = null;
let timeChartInstance = null;
let healthHistoryChartInstance = null;

document.addEventListener("DOMContentLoaded", function () {
    const customerId = window.location.pathname.split("/")[2];
    const rangeSelect = document.getElementById("range");
    loadCustomerDetail(customerId, rangeSelect.value);
    loadHealthHistory(customerId)
    rangeSelect.addEventListener("change", function() {
        loadCustomerDetail(customerId, rangeSelect.value)
    });

    setupTableToggle();
});

function loadCustomerDetail(customerId, selectedRange) {
    const loadingMessage = document.getElementById("loading-message");
    const errorMessage = document.getElementById("error-message");
    const pageContent = document.getElementById("page-content");
    fetch(`/api/customers/${customerId}/detail/?range=${selectedRange}`)
        .then(response => response.json())
        .then(data => {
            loadingMessage.classList.add("hidden");
            pageContent.classList.remove("hidden");
            renderCustomerInfo(data.customer);
            renderHealth(data.health);
            renderLists(data.risk_reasons, data.recommended_actions);
            renderCharts(data.event_distribution, data.events_over_time);
            renderEventsTable(data.events);
        })
        .catch(error => {
            console.error("Error loading customer detail:", error);
            loadingMessage.classList.add("hidden");
            errorMessage.classList.remove("hidden");
        });
}

function renderCustomerInfo(customer) {
    document.title = customer.company_name;

    document.getElementById("company-name").textContent = customer.company_name;
    document.getElementById("app-name").textContent = customer.app_name;
    document.getElementById("country").textContent = customer.country;
    document.getElementById("company-size").textContent = customer.company_size;
    document.getElementById("license-tier").textContent = customer.license_tier;
    document.getElementById("installed-at").textContent = customer.installed_at;
}

function renderHealth(health) {
    const healthStats = document.getElementById("health-stats");
    const noHealthMessage = document.getElementById("no-health-message");

    if (!health) {
        healthStats.classList.add("hidden");
        noHealthMessage.classList.remove("hidden");
        return;
    }

    healthStats.classList.remove("hidden");
    noHealthMessage.classList.add("hidden");

    document.getElementById("usage-score").textContent = health.usage_score;
    document.getElementById("feature-adoption-score").textContent = health.feature_adoption_score;
    document.getElementById("reliability-score").textContent = health.reliability_score;
    document.getElementById("support-score").textContent = health.support_score;
    document.getElementById("health-score").textContent = health.health_score;
    document.getElementById("churn-risk").textContent = health.churn_risk;
    document.getElementById("ml-churn-probability").textContent = health.ml_churn_probability;
    document.getElementById("risk-label").textContent = health.risk_label;
}

function renderCharts(eventDistribution, eventsOverTime) {
    const eventCanvas = document.getElementById("eventChart");
    const timeCanvas = document.getElementById("timeChart");

    if (eventCanvas) {
        if (eventChartInstance) {
            eventChartInstance.destroy();
        }

        eventChartInstance = new Chart(eventCanvas.getContext("2d"), {
            type: "bar",
            data: {
                labels: eventDistribution.labels,
                datasets: [{
                    label: "Number of Events",
                    data: eventDistribution.counts,
                    backgroundColor: "#a88a1e",
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: { enabled: true },
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                }
            }
        });
    }

    if (timeCanvas) {
        if (timeChartInstance) {
            timeChartInstance.destroy();
        }

        timeChartInstance = new Chart(timeCanvas.getContext("2d"), {
            type: "line",
            data: {
                labels: eventsOverTime.labels,
                datasets: [{
                    label: "Events Over Time",
                    data: eventsOverTime.counts,
                    tension: 0.3,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: { enabled: true }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                }
            }
        });
    }
}

function renderEventsTable(events) {
    const tableBody = document.getElementById("events-table-body");
    tableBody.innerHTML = "";

    if (events.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4">No events found</td>
            </tr>
        `;
        return;
    }

    events.forEach((event, index) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${event.event_type}</td>
            <td>${event.timestamp}</td>
            <td>${JSON.stringify(event.metadata)}</td>
        `;

        tableBody.appendChild(row);
    });
}

function setupTableToggle() {
    const table = document.getElementById("recentEventsTable");
    const btn = document.getElementById("toggleTableBtn");

    if (!table || !btn) {
        return;
    }

    btn.addEventListener("click", () => {
        table.classList.toggle("hidden");

        btn.textContent = table.classList.contains("hidden")
            ? "Show recent events table"
            : "Hide recent events table";
    });
}

function renderLists(riskReasons, recommendedActions) {
    const riskList = document.getElementById("risk-reasons-list");
    const actionList = document.getElementById("recommended-actions-list");

    riskList.innerHTML = "";
    actionList.innerHTML = "";

    riskReasons.forEach(reason => {
        const li = document.createElement("li");
        li.textContent = reason;
        riskList.appendChild(li);
    });

    recommendedActions.forEach(action => {
        const li = document.createElement("li");
        li.textContent = action;
        actionList.appendChild(li);
    });
}

function loadHealthHistory(customerId) {
    fetch(`/api/customers/${customerId}/health-history/`)
        .then(response => response.json())
        .then(data => {
            renderHealthHistoryChart(data);
        })
        .catch(error => {
            console.error("Error loading health history:", error);
        });
}

function renderHealthHistoryChart(data) {
    const canvas = document.getElementById("healthHistoryChart");

    if (!canvas) {
        return;
    }

    if (healthHistoryChartInstance) {
        healthHistoryChartInstance.destroy();
    }

    healthHistoryChartInstance = new Chart(canvas.getContext("2d"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [
                {
                label: "Health Score",
                data: data.health_scores,
                tension: 0.3,
                fill: false
            },
            {
                label: "Rule-based Churn Risk",
                data: data.churn_risks,
                tension: 0.3,
                fill: false,
            },
            {
                label: "ML Churn Probability",
                data: data.ml_churn_probabilities,
                tension: 0.3,
                fill: false,
            }
        ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
};