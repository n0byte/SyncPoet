// ==================== Fehler-Konfiguration ==================== //
const errorConfig = {
    mode: {
      message: "Bitte wählen Sie einen Modus aus.",
      type: "warning"
    },
    singleMode: {
      message: "Bitte wählen Sie einen Single Mode aus.",
      type: "warning"
    },
    date: {
      message: "Bitte wählen Sie ein Datum aus.",
      type: "warning"
    },
    howMany: {
      message: "Bitte geben Sie einen gültigen Wert (mindestens 1) ein.",
      type: "warning"
    },
    howManySync: {
      message: "Bitte geben Sie einen gültigen Wert (mindestens 1) ein.",
      type: "warning"
    },
    generatedFields: {
      message: "Bitte füllen Sie mindestens eines der Felder (Email oder Name) aus.",
      type: "warning"
    },
    invalidEmail: {
      message: "Bitte geben Sie eine gültige E-Mail-Adresse ein.",
      type: "warning"
    },
    invalidName: {
      message: "Bitte geben Sie einen gültigen Namen ein (z. B. 'Melvin.-_').",
      type: "warning"
    }
  };  
  
  // ==================== Alert Funktion ==================== //
  function showAlert(message, type = 'warning', duration = 3000) {
    console.log("showAlert wird aufgerufen:", message);
    const alertsContainer = document.getElementById('alertsContainer');
    if (!alertsContainer) {
      console.error("Kein Container mit der ID 'alertsContainer' gefunden.");
      return;
    }
    const alertBox = document.createElement('div');
    alertBox.className = `alert ${type}`;
    alertBox.innerHTML = `
      <span class="closebtn">&times;</span>
      <strong>${type.charAt(0).toUpperCase() + type.slice(1)}!</strong> ${message}
    `;
    alertsContainer.appendChild(alertBox);
    console.log("Alert wurde zum Container hinzugefügt.", alertBox);
  
    // Close-Button Funktionalität
    attachCloseHandler(alertBox);
  
    // Automatisches Ausblenden nach der angegebenen Dauer
    const timeout = setTimeout(() => {
      alertBox.style.opacity = '0';
      setTimeout(() => alertBox.remove(), 600);
    }, duration);
  
    // Stoppe das automatische Ausblenden beim Hovern
    alertBox.addEventListener('mouseenter', () => {
      clearTimeout(timeout);
    });
    alertBox.addEventListener('mouseleave', () => {
      setTimeout(() => {
        alertBox.style.opacity = '0';
        setTimeout(() => alertBox.remove(), 600);
      }, duration);
    });
  }
  
  // Funktion, um den Close-Button (das "x") zu aktivieren
  function attachCloseHandler(alertBox) {
    const closeBtn = alertBox.querySelector('.closebtn');
    if (closeBtn) {
      closeBtn.onclick = function() {
        alertBox.style.opacity = '0';
        setTimeout(() => alertBox.remove(), 600);
      };
    }
  }
  
  // ==================== Formularvalidierung ==================== //
function verifyForm() {
    console.log("verifyForm aufgerufen");
    let valid = true;
    let errors = [];
  
    // Felder abrufen
    const modeSelect = document.getElementById("modeSelection");
    const singleModeSelect = document.getElementById("SinglemodeSelection");
    const dateSelect = document.getElementById("dateSelection");
    const howManyInput = document.getElementById("howMany");
    const howManySyncInput = document.getElementById("howManySynchronize");
  
    // Vorherige Fehlerrahmen entfernen
    [modeSelect, singleModeSelect, dateSelect, howManyInput, howManySyncInput].forEach(elem => {
      if (elem) {
        elem.style.border = "";
      }
    });
  
    const defaultOption = "select";
  
    if (modeSelect && modeSelect.style.display !== "none") {
      if (modeSelect.value === defaultOption || modeSelect.value === "0") {
        modeSelect.style.border = "2px solid orange";
        errors.push("mode");
        valid = false;
        console.log("Fehler: mode");
      }
    }
  
    if (singleModeSelect && singleModeSelect.style.display !== "none") {
      if (singleModeSelect.value === defaultOption || singleModeSelect.value === "0") {
        singleModeSelect.style.border = "2px solid orange";
        errors.push("singleMode");
        valid = false;
        console.log("Fehler: singleMode");
      }
    }
  
    if (dateSelect && dateSelect.style.display !== "none") {
      if (dateSelect.value === defaultOption || dateSelect.value === "0") {
        dateSelect.style.border = "2px solid orange";
        errors.push("date");
        valid = false;
        console.log("Fehler: date");
      }
    }
  
    if (howManyInput && howManyInput.style.display !== "none") {
      if (isNaN(howManyInput.value) || Number(howManyInput.value) < 1) {
        howManyInput.style.border = "2px solid orange";
        errors.push("howMany");
        valid = false;
        console.log("Fehler: howMany");
      }
    }
  
    if (howManySyncInput && howManySyncInput.style.display !== "none") {
      if (isNaN(howManySyncInput.value) || Number(howManySyncInput.value) < 1) {
        howManySyncInput.style.border = "2px solid orange";
        errors.push("howManySync");
        valid = false;
        console.log("Fehler: howManySync");
      }
    }
  
    // Neue Validierung für die generierten Felder (Email und Name)
    const generatedEmails = document.querySelectorAll(".generated-email");
    const generatedNames = document.querySelectorAll(".generated-name");
  
    generatedEmails.forEach((emailInput, index) => {
      const nameInput = generatedNames[index];
      let emailValue = emailInput.value.trim();
      let nameValue = nameInput.value.trim();
  
      // Überprüfen, ob mindestens eines der Felder ausgefüllt wurde
      if (emailValue === "" && nameValue === "") {
        emailInput.style.border = "2px solid orange";
        nameInput.style.border = "2px solid orange";
        errors.push("generatedFields");
        valid = false;
        console.log("Fehler: generatedFields in Gruppe " + (index + 1));
      }
  
      // Wenn Email ausgefüllt, dann Format überprüfen (gängiges Email-Regex)
      if (emailValue !== "") {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailValue)) {
          emailInput.style.border = "2px solid orange";
          errors.push("invalidEmail");
          valid = false;
          console.log("Fehler: invalidEmail in Gruppe " + (index + 1));
        }
      }
  
      // Wenn Name ausgefüllt, dann Format überprüfen
      if (nameValue !== "") {
        // Name muss mit einem Buchstaben beginnen und darf nur Buchstaben, Punkt, Bindestrich und Unterstrich enthalten
        const nameRegex = /^[A-Za-zÄäÖöÜüß][A-Za-zÄäÖöÜüß.\-_]*$/;
        if (!nameRegex.test(nameValue)) {
          nameInput.style.border = "2px solid orange";
          errors.push("invalidName");
          valid = false;
          console.log("Fehler: invalidName in Gruppe " + (index + 1));
        }
      }
    });
  
    // Wenn Fehler vorhanden sind, alle Fehlermeldungen zusammenfassen
    if (!valid) {
      // Einzigartige Fehlermeldungen sammeln
      const uniqueMessages = [...new Set(errors.map(err => errorConfig[err].message))];
      const combinedMessage = uniqueMessages.join("<br>");
  
      // Prüfen, ob bereits ein Fehler-Alert (Warning) existiert
      let existingAlert = document.querySelector("#alertsContainer .alert.warning");
      if (existingAlert) {
        // Inhalt des bestehenden Alerts aktualisieren und Close-Handler erneut anhängen
        existingAlert.innerHTML = `<span class="closebtn">&times;</span>
          <strong>Warning!</strong> ${combinedMessage}`;
        attachCloseHandler(existingAlert);
        console.log("Bestehender Fehler-Alert aktualisiert.");
      } else {
        showAlert(combinedMessage, "warning", 3000);
      }
      return false;
    } else {
      // Falls keine Fehler vorhanden sind, vorhandene Fehler-Alerts entfernen
      let existingAlert = document.querySelector("#alertsContainer .alert.warning");
      if (existingAlert) {
        existingAlert.remove();
      }
      return true;
    }
  }  
  
  // ==================== Event-Listener ==================== //
  document.getElementById("check").addEventListener("click", function(event) {
    console.log("Checkbox wurde geklickt");
    if (!verifyForm()) {
      event.preventDefault();
      this.checked = false;
      console.log("Checkbox zurückgesetzt");
    } else {
      // Bei erfolgreicher Validierung: Zeige einen Success-Alert, falls noch keiner existiert
      let existingSuccessAlert = document.querySelector("#alertsContainer .alert.success");
      if (!existingSuccessAlert) {
        showAlert("You can now Send!", "success", 3000);
      }
    }
  });  

// ==================== Lock and delock Send and Checkbox start ==================== //
const checkBox = document.getElementById("check");
const sendButton = document.getElementById("sendButton");

// Initial state: disable send button
sendButton.disabled = true;

// Event listener for checkbox
checkBox.addEventListener("change", function() {
    if (this.checked && verifyForm()) {
        sendButton.disabled = false;
    } else {
        sendButton.disabled = true;
    }
});

// Event listener for send button
sendButton.addEventListener("click", function() {
    if (!sendButton.disabled) {
        // Simulate sending action
        console.log("Send button clicked");

        // Disable send button and checkbox
        sendButton.disabled = true;
        checkBox.disabled = true;

        // Simulate API call to check for a specific key
        setTimeout(() => {
            const data = { key: "ProcessDoneReadyToContinue" };
            if (data.key === "ProcessDoneReadyToContinue") {
                // Re-enable checkbox and send button
                checkBox.disabled = false;
                checkBox.checked = false;
                sendButton.disabled = true;
            }
        }, 3000);
    }
});
// ==================== Lock and delock Send and Checkbox end ==================== //
