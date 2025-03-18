// ==================== Selection Logic start ==================== //
document.addEventListener("DOMContentLoaded", function() {
    const modeSelect = document.getElementById("modeSelection");
    const singleModeSelect = document.getElementById("SinglemodeSelection");
    const dateSelect = document.getElementById("dateSelection");
    const howManyInput = document.getElementById("howMany");
    const howManySyncInput = document.getElementById("howManySynchronize");
  
    function updateVisibility() {
      const mode = modeSelect.value;
  
      // Zunächst alle optionalen Felder ausblenden
      singleModeSelect.style.display = "none";
      dateSelect.style.display = "none";
      howManyInput.style.display = "none";
      howManySyncInput.style.display = "none";
  
      // Wenn "select" gewählt ist, wird nur das modeSelect angezeigt
      if (mode === "select") {
        return;
      }
  
      // Bei Single Mode: Alle Felder anzeigen
      if (mode === "single") {
        singleModeSelect.style.display = "inline-block";
        dateSelect.style.display = "inline-block";
        howManyInput.style.display = "inline-block";
        howManySyncInput.style.display = "inline-block";
      }
  
      // Bei C2M, M2C oder ALL Mode: Nur dateSelect und ggf. howMany anzeigen
      if (mode === "c2m" || mode === "m2c" || mode === "all") {
        dateSelect.style.display = "inline-block";
        if (dateSelect.value !== "all") {
          howManyInput.style.display = "inline-block";
        }
      }
    }
  
    function updateHowManyVisibility() {
      if (dateSelect.value === "all") {
        howManyInput.style.display = "none";
      } else {
        const mode = modeSelect.value;
        if (mode === "single" || mode === "c2m" || mode === "m2c" || mode === "all") {
          howManyInput.style.display = "inline-block";
        }
      }
    }
  
    modeSelect.addEventListener("change", function() {
      updateVisibility();
    });
    
    dateSelect.addEventListener("change", function() {
      updateHowManyVisibility();
    });
  
    // Initiale Sichtbarkeit setzen
    updateVisibility();
  });
  // ==================== Selection Logic end ==================== //