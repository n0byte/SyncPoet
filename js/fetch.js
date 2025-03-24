document.addEventListener("DOMContentLoaded", function() {
    const sendButton = document.getElementById("sendButton");
    if (sendButton) {
      sendButton.addEventListener("click", function(event) {
        event.preventDefault();
        console.log("Send Button wurde geklickt!");
  
        // Auslesen der statischen/Dropdown-Felder
        const mode = document.getElementById("modeSelection").value;
        const singleMode = document.getElementById("SinglemodeSelection").value;
        const date = document.getElementById("dateSelection").value;
        const howMany = document.getElementById("howMany").value;
        const howManySynchronize = document.getElementById("howManySynchronize").value;
        const CRMUrl = document.getElementById("CRMUrl").value;
        const CRMHeader = document.getElementById("CRMHeader").value;
        const MailPoetUrl = document.getElementById("MailPoetUrl").value;

        // Auslesen der dynamisch generierten Input-Felder über Klassen
        const emailInputs = document.querySelectorAll(".userInput-area .generated-email");
        const nameInputs = document.querySelectorAll(".userInput-area .generated-name");
        const emails = Array.from(emailInputs).map(input => input.value);
        const names = Array.from(nameInputs).map(input => input.value);
  
        const formData = {
          mode: mode,
          singleMode: singleMode,
          date: date,
          howMany: howMany,
          howManySynchronize: howManySynchronize,
          user: {
            emails: emails,   // Array von E-Mail-Adressen
            names: names      // Array von Namen
          },
          settings: {
            CRMUrl: CRMUrl,
            CRMHeader: CRMHeader,
            MailPoetUrl: MailPoetUrl
          }
        };
  
        console.log("Gesammelte Formulardaten:", formData);

        // Show processing alert
        showAlert("Verarbeitung läuft...", "info", 0); // Duration 0 means it stays until removed

        fetch('http://localhost:5000/api/GETmodeInfo', {
            method: 'POST',
            headers: {
          'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (response.status === 503) {
                // Process is busy
                return response.json().then(data => {
                    // Remove processing alert
                    removeExistingAlerts('info');
                    showAlert(data.message, "warning", 5000);
                    throw new Error('Process busy');
                });
            }
            if (!response.ok) {
          throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            // Remove processing alert
            removeExistingAlerts('info');
            
            if (data.status === "success") {
                showAlert(data.result.message, "success", 3000);
            } else if (data.error) {
                showAlert(data.error, "warning", 3000);
            }
        })
        .catch(error => {
            if (error.message !== 'Process busy') {
                console.error('Error:', error);
                // Remove processing alert
                removeExistingAlerts('info');
                showAlert("Ein Fehler ist aufgetreten: " + error.message, "warning", 3000);
            }
        });
      });
    } else {
      console.error("sendButton nicht gefunden!");
    }
  });

// Helper function to remove existing alerts of a specific type
function removeExistingAlerts(type) {
    const existingAlert = document.querySelector(`#alertsContainer .alert.${type}`);
    if (existingAlert) {
        existingAlert.remove();
    }
}