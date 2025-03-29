// ==================== Auto Save Settings Logic start ==================== //
function initializeSettingsModal() {
    // Stelle sicher, dass die Input-Felder im Settings-Modal vorhanden sind
    const crmUrlInput = document.getElementById("CRMUrl");
    const crmHeaderInput = document.getElementById("CRMHeader");
    const mailPoetUrlInput = document.getElementById("MailPoetUrl");
  
    // Definiere Standardwerte
    const defaults = {
      crmUrl: "https://erp.ketmarket.eu/api/index.php/thirdparties",
      crmHeader: '{"DOLAPIKEY": "31782J51I0s3ZFZZbpqZbCTWxcpPi8jv", "Accept": "application/json"}',
      mailPoetUrl: "https://ketmarket.eu/wp-json/artificialMailPoetAPI/v1"
    };  
  
    // Lade die gespeicherten Einstellungen aus localStorage
    let savedSettings;
    try {
      savedSettings = JSON.parse(localStorage.getItem("settings"));
    } catch (error) {
      savedSettings = null;
    }
    // Falls keine gültigen Einstellungen vorhanden sind, verwende die Standardwerte
    if (!savedSettings || typeof savedSettings !== "object") {
      savedSettings = defaults;
    } else {
      // Falls einzelne Werte fehlen oder undefined sind, Standardwerte setzen
      savedSettings.crmUrl = savedSettings.crmUrl || defaults.crmUrl;
      savedSettings.crmHeader = savedSettings.crmHeader || defaults.crmHeader;
      savedSettings.mailPoetUrl = savedSettings.mailPoetUrl || defaults.mailPoetUrl;
    }
  
    // Setze die Eingabefelder mit den gespeicherten bzw. Standardwerten
    if (crmUrlInput) {
      crmUrlInput.value = savedSettings.crmUrl;
    }
    if (crmHeaderInput) {
      crmHeaderInput.value = savedSettings.crmHeader;
    }
    if (mailPoetUrlInput) {
      mailPoetUrlInput.value = savedSettings.mailPoetUrl;
    }
  
    // Funktion zum automatischen Speichern der aktuellen Werte in localStorage
    function autoSaveSettings() {
      const currentSettings = {
        crmUrl: crmUrlInput ? crmUrlInput.value : "",
        crmHeader: crmHeaderInput ? crmHeaderInput.value : "",
        mailPoetUrl: mailPoetUrlInput ? mailPoetUrlInput.value : ""
      };
      localStorage.setItem("settings", JSON.stringify(currentSettings));
    }
  
    // Speichere automatisch bei jeder Änderung in den Input-Feldern
    if (crmUrlInput) {
      crmUrlInput.addEventListener("input", autoSaveSettings);
    }
    if (crmHeaderInput) {
      crmHeaderInput.addEventListener("input", autoSaveSettings);
    }
    if (mailPoetUrlInput) {
      mailPoetUrlInput.addEventListener("input", autoSaveSettings);
    }
  
    // Zusätzlich: Speichere in regelmäßigen Abständen (z. B. alle 100ms)
    setInterval(autoSaveSettings, 100);
  }
  
  document.addEventListener("DOMContentLoaded", initializeSettingsModal);
  // ==================== Auto Save Settings Logic end ==================== //