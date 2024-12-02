const statusElem = document.getElementById("status");
const tempElem = document.getElementById("temperature");
const entriesElem = document.getElementById("entries");
const refreshBtn = document.getElementById("refresh");
const rebootBtn = document.getElementById("reboot");
const shutdownBtn = document.getElementById("shutdown");

// Function to fetch data from the server
async function fetchData() {
  try {
    const response = await fetch("http://your-server-address/api/data");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    
    // Update status
    statusElem.textContent = data.status ? "Online" : "Offline";
    
    // Update temperature
    tempElem.textContent = `${data.temperature}°C`;

    // Update entries
    entriesElem.innerHTML = data.entries.map(entry => `
      <tr>
        <td>${entry.lotID}</td>
        <td>${entry.plate}</td>
        <td>${entry.date}</td>
        <td>${entry.state}</td>
        <td><img src="${entry.plateImg}" alt="Plate Image"></td>
      </tr>
    `).join('');
  } catch (error) {
    console.error("Error fetching data:", error);
    statusElem.textContent = "Offline";
  }
}

// Event listeners for buttons
refreshBtn.addEventListener("click", fetchData);
rebootBtn.addEventListener("click", async () => {
  try {
    await fetch("http://your-server-address/api/reboot", { method: "POST" });
    alert("Reboot command sent");
  } catch (error) {
    console.error("Error sending reboot command:", error);
  }
});
shutdownBtn.addEventListener("click", async () => {
  try {
    await fetch("http://your-server-address/api/shutdown", { method: "POST" });
    alert("Shutdown command sent");
  } catch (error) {
    console.error("Error sending shutdown command:", error);
  }
});

// Poll server every 5 seconds to update data
setInterval(fetchData, 5000);

// Initial data fetch when the page loads
document.addEventListener("DOMContentLoaded", fetchData);
