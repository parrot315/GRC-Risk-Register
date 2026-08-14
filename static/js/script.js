/* =========================================================
   GRC Risk Register — script.js
   Handles: live risk score calculation, delete confirmation,
   and small UI enhancements.
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

  // ---------------------------------------------------------
  // Live inherent / residual risk score calculation
  // ---------------------------------------------------------
  function levelFromScore(score) {
    if (score <= 4) return "Low";
    if (score <= 9) return "Medium";
    if (score <= 16) return "High";
    return "Critical";
  }

  function wireCalculator(likelihoodId, impactId, scoreOutId, levelOutId) {
    const likeEl = document.getElementById(likelihoodId);
    const impactEl = document.getElementById(impactId);
    const scoreOut = document.getElementById(scoreOutId);
    const levelOut = document.getElementById(levelOutId);

    if (!likeEl || !impactEl || !scoreOut || !levelOut) return;

    function update() {
      const l = parseInt(likeEl.value, 10);
      const i = parseInt(impactEl.value, 10);
      if (!l || !i || l < 1 || l > 5 || i < 1 || i > 5) {
        scoreOut.textContent = "--";
        levelOut.textContent = "--";
        levelOut.className = "badge-risk";
        return;
      }
      const score = l * i;
      const level = levelFromScore(score);
      scoreOut.textContent = score;
      levelOut.textContent = level;
      levelOut.className = "badge-risk " + level;
    }

    likeEl.addEventListener("change", update);
    impactEl.addEventListener("change", update);
    update();
  }

  wireCalculator("likelihood", "impact", "inherent-score-out", "inherent-level-out");
  wireCalculator("residual_likelihood", "residual_impact", "residual-score-out", "residual-level-out");

  // ---------------------------------------------------------
  // Delete confirmation modals (fallback to confirm() if no modal present)
  // ---------------------------------------------------------
  document.querySelectorAll("form.delete-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      const label = form.getAttribute("data-risk-label") || "this risk";
      if (!window.confirm("Are you sure you want to delete " + label + "? This action cannot be undone.")) {
        e.preventDefault();
      }
    });
  });

  // ---------------------------------------------------------
  // Auto-dismiss alerts after 6 seconds
  // ---------------------------------------------------------
  document.querySelectorAll(".alert").forEach(function (alertEl) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      if (bsAlert) bsAlert.close();
    }, 6000);
  });

});
