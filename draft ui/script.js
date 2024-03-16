document.getElementById("directoryInput").addEventListener("change", function (event) {
    const selectedDirectory = event.target.files[0].path;
    document.getElementById("selectedDirectory").textContent = "Selected Directory: " + selectedDirectory;
});

// Function to show the spinner
function showSpinner() {
   document.querySelector('.overlay').style.display = 'block';
}

// Function to hide the spinner
function hideSpinner() {
   document.querySelector('.overlay').style.display = 'none';
}

// Event listener for the button
document.getElementById("showSpinnerButton").addEventListener("click", function() {
   showSpinner(); // Show the spinner when the button is clicked

   // Simulate an asynchronous operation (e.g., AJAX request)
   setTimeout(function() {
     // Hide the spinner when the operation is complete
     hideSpinner();
   }, 3000); // Adjust the time as needed
});
