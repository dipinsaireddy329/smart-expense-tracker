const sidebarToggle = document.getElementById("sidebarToggle");
const sidebar = document.querySelector(".sidebar");

if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener("click", () => sidebar.classList.toggle("open"));
}

function parseDataset(element, key, fallback = []) {
    if (!element || !element.dataset[key]) return fallback;
    try {
        return JSON.parse(element.dataset[key]);
    } catch {
        return fallback;
    }
}

function renderCategoryPie() {
    const canvas = document.getElementById("categoryPie");
    if (!canvas || typeof Chart === "undefined") return;

    const labels = parseDataset(canvas, "labels");
    const values = parseDataset(canvas, "values");
    const colors = parseDataset(canvas, "colors", ["#2563eb", "#0f766e", "#f59e0b", "#dc2626", "#7c3aed", "#0891b2"]);

    new Chart(canvas, {
        type: "doughnut",
        data: {
            labels: labels.length ? labels : ["No expenses"],
            datasets: [{
                data: values.length ? values : [1],
                backgroundColor: values.length ? colors : ["#e5e7eb"],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "bottom" }
            },
            cutout: "62%"
        }
    });
}

function renderMonthlyBar() {
    const canvas = document.getElementById("monthlyBar");
    if (!canvas || typeof Chart === "undefined") return;

    const labels = parseDataset(canvas, "labels");
    const values = parseDataset(canvas, "values");

    new Chart(canvas, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label: "Expenses",
                data: values,
                backgroundColor: "#2563eb",
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, grid: { color: "#edf2f7" } },
                x: { grid: { display: false } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

renderCategoryPie();
renderMonthlyBar();

// Auto-activate sidebar links based on location
document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".sidebar-nav .nav-link");
    navLinks.forEach(link => {
        const href = link.getAttribute("href");
        if (currentPath === href || (href !== "/" && currentPath.startsWith(href))) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
});
