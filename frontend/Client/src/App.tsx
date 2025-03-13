import { useState, useEffect } from "react";
import { BuildForm } from "./components/buildForm";
import { BuildSelector } from "./components/buildSelector";
import type { Build, GenerateBuildParams } from "./types";

function App() {
  const [builds, setBuilds] = useState<Build[]>([]);
  const [selectedBuild, setSelectedBuild] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    loadBuilds();
  }, []);

  const loadBuilds = async () => {
    try {
      const response = await fetch("/list-builds");
      const data = await response.json();
      setBuilds(data.builds);

      // Select the latest build if available
      if (data.builds.length > 0) {
        const latestBuild = data.builds[data.builds.length - 1];
        setSelectedBuild(latestBuild.folder);
      }
    } catch (error) {
      console.error("Error loading builds:", error);
    }
  };

  const handleBuildSubmit = async (params: GenerateBuildParams) => {
    try {
      setIsGenerating(true);
      alert("Build generation started! You will be notified when it's done.");

      await fetch("/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(params),
      });

      // Set up SSE for build completion notification
      const eventSource = new EventSource("/build-status");
      eventSource.onmessage = (event) => {
        const status = event.data.trim();
        if (status === "COMPLETE") {
          alert("Build generation complete! Loading the new build.");
          eventSource.close();
          setIsGenerating(false);
          loadBuilds(); // Refresh the builds list
        }
      };
    } catch (error) {
      console.error("Error:", error);
      setIsGenerating(false);
    }
  };

  const handleDownload = () => {
    if (selectedBuild) {
      window.location.href = `/download-schematic?folder=${selectedBuild}`;
    }
  };

  return (
    <div className="container">
      <div className="content">
        <h1 className="title">Minecraft AI Builder</h1>

        <BuildForm onSubmit={handleBuildSubmit} isGenerating={isGenerating} />

        <BuildSelector
          builds={builds}
          selectedBuild={selectedBuild}
          onBuildSelect={setSelectedBuild}
          onDownload={handleDownload}
        />
      </div>
    </div>
  );
}

export default App;
