  // ==================== Input Field Generation Logic start ==================== //
  const modeSelection = document.getElementById("modeSelection");
  const userInputArea = document.querySelector(".userInput-area");
  const howManySynchronize = document.getElementById("howManySynchronize");
  const howMany = document.getElementById("howMany");
  const dateSelection = document.getElementById("dateSelection");
  
  const generateInputs = (count) => {
    // Aktuelle Inhalte der Felder sichern
    const currentEmails = Array.from(document.querySelectorAll('.generated-email')).map(input => input.value);
    const currentNames = Array.from(document.querySelectorAll('.generated-name')).map(input => input.value);
  
    userInputArea.innerHTML = "";
    
    // Grid-Container erstellen und zentriert ausrichten
    let container = document.createElement("div");
    container.style.display = "grid";
    container.style.gap = "10px";
    container.style.width = "100%";
    container.style.margin = "0 auto";
    container.style.justifyItems = "center";
    container.style.alignItems = "center";
  
    // Bei wenigen Feldern (<= 5) wird eine Spalte genutzt, sonst 2 Spalten
    if (count <= 5) {
      container.style.gridTemplateColumns = "1fr";
      container.style.maxWidth = "650px";
    } else {
      container.style.gridTemplateColumns = "repeat(2, minmax(300px, 1fr))";
      container.style.maxWidth = "1200px";
    }
  
    for (let i = 0; i < count; i++) {
      let fieldContainer = document.createElement("div");
      fieldContainer.style.display = "flex";
      fieldContainer.style.flexDirection = "column";
      fieldContainer.style.gap = "5px";
      fieldContainer.style.width = "100%";
      fieldContainer.style.maxWidth = "500px";
      fieldContainer.style.margin = "0 auto";
  
      let emailInput = document.createElement("input");
      emailInput.type = "text";
      emailInput.placeholder = `Email ${i + 1}`;
      emailInput.classList.add("generated-email");
      // Falls vorhanden, den gespeicherten Wert setzen
      if (i < currentEmails.length) {
        emailInput.value = currentEmails[i];
      }
  
      let nameInput = document.createElement("input");
      nameInput.type = "text";
      nameInput.placeholder = `Name ${i + 1}`;
      nameInput.classList.add("generated-name");
      if (i < currentNames.length) {
        nameInput.value = currentNames[i];
      }
  
      fieldContainer.appendChild(emailInput);
      fieldContainer.appendChild(nameInput);
  
      // Sonderfall: Bei 7 bzw. 9 Feldern spannt das letzte Element beide Spalten
      if ((count === 7 && i === 6) || (count === 9 && i === 8)) {
        fieldContainer.style.gridColumn = "span 2";
        fieldContainer.style.width = "40%";
        fieldContainer.style.maxWidth = "500px";
      }
  
      container.appendChild(fieldContainer);
    }
  
    userInputArea.appendChild(container);
  };
  
  
  howManySynchronize.addEventListener("input", function () {
    let value = parseInt(this.value);
    if (!isNaN(value) && value >= 1 && value <= 10) {
      generateInputs(value);
    }
  });
  
  document.addEventListener("DOMContentLoaded", function () {
    generateInputs(parseInt(howManySynchronize.value));
  });
  // ==================== Input Field Generation Logic end ==================== //