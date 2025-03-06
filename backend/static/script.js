// script.js
let builds = {}; // Store builds in memory
let currentBuild = null; // Currently selected build

// Handle form submission
document
  .getElementById("buildForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const size = document.getElementById("size").value;
    const type = document.getElementById("type").value;

    // Show the progress bar
    const progressBarContainer = document.getElementById(
      "progressBarContainer"
    );
    const progressBar = document.getElementById("progressBar");
    const progressPercentage = document.getElementById("progressPercentage");
    progressBarContainer.style.display = "block";
    progressBar.value = 0;
    progressPercentage.textContent = "0%";

    fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ size: size, type: type }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(
          "Build generated successfully! Check the backend for the output files."
        );
        loadBuilds(); // Reload the list of builds
      })
      .catch((error) => {
        console.error("Error:", error);
      })
      .finally(() => {
        // Hide the progress bar after completion
        progressBarContainer.style.display = "none";
      });

    // Simulate progress updates (replace this with actual progress updates from the backend)
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      progressBar.value = progress;
      progressPercentage.textContent = `${progress}%`;
      if (progress >= 100) {
        clearInterval(interval);
      }
    }, 500);
  });

// Load the list of builds from the server
function loadBuilds() {
  fetch("/list-builds")
    .then((response) => response.json())
    .then((data) => {
      const buildSelect = document.getElementById("buildSelect");
      buildSelect.innerHTML = '<option value="">-- Select a Build --</option>';
      data.builds.forEach((build) => {
        const option = document.createElement("option");
        option.value = build.folder;
        option.textContent = `${build.type} (${build.size}x${build.size}) - ${build.timestamp}`;
        buildSelect.appendChild(option);
      });
    })
    .catch((error) => {
      console.error("Error loading builds:", error);
    });
}

// Handle build selection
document
  .getElementById("buildSelect")
  .addEventListener("change", function (event) {
    const selectedBuild = event.target.value;
    if (selectedBuild) {
      fetch(`/load-build?folder=${selectedBuild}`)
        .then((response) => response.json())
        .then((data) => {
          currentBuild = data.layers;
          updateLayerSlider(currentBuild.length);
          displayLayer(0); // Display the first layer
        })
        .catch((error) => {
          console.error("Error loading build:", error);
        });
    } else {
      currentBuild = null;
      document.getElementById("buildDisplay").textContent = "";
    }
  });

// Handle layer slider change
document
  .getElementById("layerSlider")
  .addEventListener("input", function (event) {
    const layerIndex = parseInt(event.target.value);
    displayLayer(layerIndex);
  });

// Update the layer slider based on the number of layers
function updateLayerSlider(numLayers) {
  const layerSlider = document.getElementById("layerSlider");
  layerSlider.max = numLayers - 1;
  layerSlider.value = 0;
  document.getElementById("currentLayer").textContent = "0";
}

// Display the selected layer
function displayLayer(layerIndex) {
  if (currentBuild && currentBuild[layerIndex]) {
    const layerContent = currentBuild[layerIndex]
      .map((row) => row.join(" "))
      .join("\n");
    document.getElementById("buildDisplay").textContent = layerContent;
    document.getElementById("currentLayer").textContent = layerIndex;
  } else {
    document.getElementById("buildDisplay").textContent =
      "No layer data available.";
  }
}

// Add download button functionality
document
  .getElementById("downloadButton")
  .addEventListener("click", function () {
    const selectedBuild = document.getElementById("buildSelect").value;
    if (selectedBuild) {
      window.location.href = `/download-schematic?folder=${selectedBuild}`;
    } else {
      alert("Please select a build to download.");
    }
  });

// Initial load of builds
loadBuilds();
