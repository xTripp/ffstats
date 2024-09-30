// Handle the season select dropdown page reload
document.addEventListener("change", function(event) {
    if (event.target && event.target.id === 'season-select') {
        // Disable the dropdown box while loading and remove old season data
        document.getElementById("season-select").disabled = true;
        document.getElementById("season-info").innerHTML = '';

        // Show all loading elements
        document.getElementById("loading-season").textContent = `Loading ${event.target.value} Season... This may take a minute`;
        document.getElementById("season-loading-container").style.display = "flex";

        // Fetch data and populate the page, then hide loading elements
        fetch(`/${event.target.value}`)
            .then(response => response.text())
            .then(data => {
                // Re-enable season select dropdown
                document.getElementById("season-select").disabled = false;

                // Reload page data
                document.documentElement.innerHTML = data;

                // Hide all loading elements after data is loaded
                document.getElementById("season-loading-container").style.display = "none";
            })
            .catch(error => {
                document.documentElement.innerHTML = `
                    <p>Something went wrong. Try again later</p>
                    <p>Error: ${error}</p>
                `;
            });
    }
});

// Handle the load leaderboards button's load sequence
document.addEventListener("click", function(event) {
    if (event.target && event.target.id === 'load-leaderboards-button') {
        // Hide the load leaderboards button and show loading elements
        event.target.parentNode.style.display = "none";
        document.getElementById("leaderboards-loading-container").style.display = "flex";

        // Get current selected season for leaderboards
        const season = document.getElementById("season-select").value

        // Fetch data and populate the container, then hide loading elements
        fetch(`/load_leaderboards?year=${season}`)
            .then(response => response.text())
            .then(data => {
                // Load leaderboards data into page
                document.getElementById("leaderboards-container").innerHTML = data;

                // Hide loading elements after data is loaded
                document.getElementById("leaderboards-loading-container").style.display = "none";
            })
            .catch(error => {
                document.getElementById("leaderboards-container").innerHTML = `
                    <p>Something went wrong. Try again later</p>
                    <p>Error: ${error}</p>
                `;
            });
    }
});

// Translate trade time from UTC to the user's local time
document.querySelectorAll(".trade").forEach(tradeElement => {
    const epochTime = parseInt(tradeElement.getAttribute("data-epoch"));
    const date = new Date(epochTime);  // Convert epoch to a Date object
    const options = {
        month: 'long',     // Full month name
        day: '2-digit',    // 2-digit day
        year: 'numeric',   // Full year
        hour: 'numeric',   // Hour
        minute: '2-digit', // Minute with leading zero
        hour12: true       // AM/PM format
    };

    const localTime = date.toLocaleString('en-US', options);  // Convert to local time with format
    tradeElement.querySelector(".trade-time").innerHTML = localTime
});