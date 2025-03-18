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
        fetch('http://localhost:5000/api/getInformation', {
            method: 'POST',
            headers: {
          'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
          throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
      });
    } else {
      console.error("sendButton nicht gefunden!");
    }
  });  