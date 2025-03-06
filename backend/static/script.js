let currentBuild = null; // Currently selected build

// Handle form submission: now using free-text description.
document.getElementById("buildForm").addEventListener("submit", function (event) {
  event.preventDefault();
  const size = document.getElementById("size").value;
  const description = document.getElementById("description").value;
  
  fetch("/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ size: size, description: description }),
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById("message").textContent = data.message;
  })
  .catch(error => {
    console.error("Error:", error);
    document.getElementById("message").textContent = "Error generating build.";
  });
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
        option.textContent = `${build.description} (${build.size}x${build.size}) - ${build.timestamp}`;
        buildSelect.appendChild(option);
      });
    })
    .catch((error) => {
      console.error("Error loading builds:", error);
    });
}

// Handle build selection from the dropdown
document.getElementById("buildSelect").addEventListener("change", function (event) {
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
document.getElementById("layerSlider").addEventListener("input", function (event) {
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
    document.getElementById("buildDisplay").textContent = "No layer data available.";
  }
}

// Initial load of builds
loadBuilds();
