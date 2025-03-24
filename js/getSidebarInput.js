document.addEventListener('DOMContentLoaded', () => {
  // Rufe die Funktion regelmäßig auf, um die Sidebar zu aktualisieren
  setInterval(() => {
    simulateFetch().then(data => {
      // Leere den aktuellen Inhalt der Sidebar
      clearSidebar();
      // Füge die Titel hinzu
      addSidebarTitles();
      // Füge die neuen Daten hinzu
      data.forEach(item => addSidebarItem(item));
    });
  }, 1000); // Aktualisiere alle 1 Sekunden
});

// Funktion, die einen simulierten Fetch mit mindestens 10 Testdaten zurückgibt
function simulateFetch() {
  return new Promise((resolve) => {
    fetch('http://localhost:5000/api/GETsidebarInfo') // Replace with your actual API endpoint
      .then(response => response.json())
      .then(data => {
        // Ensure data is in correct format regardless of input
        let formattedData = [];
        
        if (typeof data === 'string') {
          // If data is a string, try to parse it
          try {
            data = JSON.parse(data);
          } catch (e) {
            data = [{ filename: data, status: 'Unknown' }];
          }
        }
        
        // Handle array of strings or objects
        formattedData = Array.isArray(data) ? data.map(item => {
          if (typeof item === 'string') {
            return { filename: item, status: 'Unknown' };
          }
          return {
            filename: item.filename || item.name || 'Unknown',
            status: item.status || 'Unknown'
          };
        }) : [];

        resolve(formattedData);
      })
      .catch(() => {
        // Return empty array in case of error
        resolve([]);
      });
  });
}

// Funktion, die die Titel für die Sidebar hinzufügt
function addSidebarTitles() {
  const sidebarContent = document.createElement('div');
  sidebarContent.className = 'sidebarContent';

  const leftSide = document.createElement('div');
  leftSide.className = 'leftSide';
  const leftTitle = document.createElement('span');
  leftTitle.className = 'itemTitle';
  leftTitle.textContent = 'Dateiname';
  leftSide.appendChild(leftTitle);

  const rightSide = document.createElement('div');
  rightSide.className = 'rightSide';
  const rightTitle = document.createElement('span');
  rightTitle.className = 'itemTitle';
  rightTitle.textContent = 'Status';
  rightSide.appendChild(rightTitle);

  sidebarContent.appendChild(leftSide);
  sidebarContent.appendChild(rightSide);

  document.querySelector('aside').appendChild(sidebarContent);
}

// Funktion, die ein neues Sidebar-Item erstellt und in den <aside> Container einfügt
function addSidebarItem(data) {
  const leftItem = document.createElement('div');
  leftItem.className = 'item';
  leftItem.textContent = data.filename;

  const rightItem = document.createElement('span');
  rightItem.className = 'item';
  rightItem.textContent = data.status;

  const leftSide = document.querySelector('aside .leftSide');
  const rightSide = document.querySelector('aside .rightSide');

  leftSide.appendChild(leftItem);
  rightSide.appendChild(rightItem);
}

// Funktion, die den Inhalt der Sidebar leert
function clearSidebar() {
  const sidebar = document.querySelector('aside');
  while (sidebar.firstChild) {
    sidebar.removeChild(sidebar.firstChild);
  }
}