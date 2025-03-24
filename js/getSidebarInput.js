function getServerUrl() {
    const serverPort = 5000;
    return `http://localhost:${serverPort}`;
}

// Remove duplicate event listener and combine the functionality
document.addEventListener('DOMContentLoaded', () => {
    function simulateFetch() {
        const serverUrl = getServerUrl();
        
        return fetch(`${serverUrl}/api/GETsidebarInfo`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            mode: 'cors' // Add CORS mode
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data)) {
                console.warn('Received non-array data:', data);
                return [];
            }
            return data.map(item => ({
                filename: item.filename || 'Unknown',
                status: item.status || 'Unknown'
            }));
        })
        .catch(error => {
            console.error('Error fetching sidebar data:', error);
            return []; 
        });
    }

    function updateSidebar() {
        simulateFetch()
            .then(data => {
                if (data) {
                    clearSidebar();
                    addSidebarTitles();
                    data.forEach(item => addSidebarItem(item));
                }
            })
            .catch(error => {
                console.error('Sidebar update failed:', error);
            });
    }

    // Initial update
    updateSidebar();
    
    // Then update every second
    const intervalId = setInterval(updateSidebar, 1000);

    // Clean up interval when needed
    window.addEventListener('unload', () => {
        clearInterval(intervalId);
    });
});

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