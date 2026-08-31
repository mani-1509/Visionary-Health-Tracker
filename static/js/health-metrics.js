document.addEventListener("DOMContentLoaded", function () {
  const healthMetricForm = document.getElementById("health-metric-form");
  const healthTipsContainer = document.getElementById("health-tips");

  if (!healthMetricForm) return;

  // Handle form submission
  healthMetricForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(healthMetricForm);
    const rawData = Object.fromEntries(formData.entries());
    
    // Filter out empty fields
    const data = {};
    for (const [key, value] of Object.entries(rawData)) {
      if (value !== "" && value !== null && value !== undefined) {
        data[key] = parseInt(value, 10);
      }
    }

    if (Object.keys(data).length === 0) {
      alert("Please enter at least one health metric before submitting.");
      return;
    }

    try {
      const response = await fetch("/api/health-metrics", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const resData = await response.json();

      if (!response.ok) {
        throw new Error(resData.error || "Failed to submit metrics");
      }

      // Clear form
      healthMetricForm.reset();

      // Load health tips after submission
      loadHealthTips();

      alert("Health metrics submitted successfully!");
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to submit health metrics: " + error.message);
    }
  });

  // Load health tips
  async function loadHealthTips() {
    if (!healthTipsContainer) return;

    try {
      const response = await fetch("/api/health-tips");
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || errorData.error || "Failed to fetch health tips");
      }

      const data = await response.json();
      const rawTips = data.health_tips || "";
      const renderedHtml = typeof marked !== "undefined" ? marked.parse(rawTips) : rawTips.replace(/\n/g, "<br>");

      const hrDisplay = data.metrics.heart_rate !== "N/A" ? `${data.metrics.heart_rate} BPM` : 'N/A';
      const calDisplay = data.metrics.calorie_count !== "N/A" ? `${data.metrics.calorie_count} kcal` : 'N/A';

      healthTipsContainer.innerHTML = `
        <div class="tips-content">
          <div id="markdown-tips">${renderedHtml}</div>
          <div class="current-metrics" style="margin-top: 20px; padding: 15px; background: rgba(139, 92, 246, 0.1); border-radius: 10px;">
            <h3>Current Metrics:</h3>
            <p>Heart Rate: ${hrDisplay}</p>
            <p>Blood Pressure: ${data.metrics.blood_pressure} mmHg</p>
            <p>Calorie Count: ${calDisplay}</p>
          </div>
        </div>
      `;
    } catch (error) {
      console.error("Error loading health tips:", error);
      healthTipsContainer.innerHTML = `
        <p>Submit your metrics to receive personalized health tips.</p>
      `;
    }
  }

  // Load tips on page load
  loadHealthTips();
});
