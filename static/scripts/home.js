function updateFormAction() {
    var seasonSelect = document.getElementById('season');
    var form = document.getElementById('seasonSelect');
    form.action = '/season/' + seasonSelect.value;
    form.submit();
}

document.getElementById("load-leaderboards-button").addEventListener("click", function() {
    // Hide the load leaderboards button
    this.style.display = "none";

    // Show all loading elements
    [...document.getElementsByClassName("loading")].forEach(el => el.style.display = "block");

    // Fetch data and populate the container, then hide loading elements
    fetch("/load_leaderboards")
        .then(response => response.text())
        .then(data => {
            document.getElementById("leaderboards-container").innerHTML = data;

            // Hide all loading elements after data is loaded
            [...document.getElementsByClassName("loading")].forEach(el => el.style.display = "none");
        })
        .catch(error => {
            document.getElementById("leaderboards-container").innerHTML = `
                <p>Something went wrong. Try again later</p>
                <p>Error: ${error}</p>
            `;
        });
});