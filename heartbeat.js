console.log("Heartbeat script loaded.");

// Wait for DOM content to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
    console.log("Page loaded - Starting heartbeat fetch test");
    setInterval(fetchHeartbeat, 5000);  // Call fetchHeartbeat every 5 seconds
});

async function fetchHeartbeat() {
    console.log("Attempting to fetch heartbeat.json...");

    try {
        const response = await fetch('https://raw.githubusercontent.com/ZachRodgers/parallel/main/heartbeat.json?t=' + new Date().getTime(), { cache: 'no-store' });

        if (!response.ok) {
            console.error("Error fetching heartbeat.json: Response not ok");
            return;
        }

        const data = await response.json();

        // Log the response to the console
        console.log("Heartbeat fetched successfully: ", data);

        // Update the status box accordingly
        const statusBox = document.getElementById('status-box');
        if (data.status === 'online') {
            statusBox.classList.remove('offline');
            statusBox.classList.add('online');
            statusBox.textContent = `Online ${data.temperature}`;
        } else {
            statusBox.classList.remove('online');
            statusBox.classList.add('offline');
            statusBox.textContent = 'Offline --°C';
        }
    } catch (error) {
        console.error('Fetch heartbeat error:', error);
    }
}
