import React, { useState, useEffect } from "react";
import { BrainCircuit } from "lucide-react";
import { BuildForm } from "./components/buildForm";
import { BuildVisualization } from "./components/buildVisualization";
import { SchematicDownload } from "./components/buildSelector";
import type { Build, GenerateBuildParams } from "./types";

function App() {
  const [builds, setBuilds] = useState<Build[]>([]);
  const [selectedBuild, setSelectedBuild] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [size, setSize] = useState(20);
  const [description, setDescription] = useState("");

  useEffect(() => {
    loadBuilds();
  }, []);

  const loadBuilds = async () => {
    try {
      const response = await fetch("/list-builds");
      const data = await response.json();
      setBuilds(data.builds);
      if (data.builds.length > 0) {
        setSelectedBuild(data.builds[data.builds.length - 1].folder);
      }
    } catch (error) {
      console.error("Error loading builds:", error);
    }
  };

  const handleBuildSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const params: GenerateBuildParams = { size, description };

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

      const eventSource = new EventSource("/build-status");
      eventSource.onmessage = (event) => {
        const status = event.data.trim();
        if (status === "COMPLETE") {
          alert("Build generation complete! Loading the new build.");
          eventSource.close();
          setIsGenerating(false);
          loadBuilds();
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
    <>
      <header className="header">
        <BrainCircuit className="header-icon" />
        <h1 className="title">Cabin Crafter</h1>
      </header>
      <div className="container">
        <div className="content">
          <main className="main-content">
            <div className="panel">
              <BuildForm
                size={size}
                description={description}
                isGenerating={isGenerating}
                onSizeChange={setSize}
                onDescriptionChange={setDescription}
                onSubmit={handleBuildSubmit}
              />
            </div>

            <div>
              <BuildVisualization selectedBuild={selectedBuild} />
              <div style={{ marginTop: "1.5rem" }}>
                <SchematicDownload
                  builds={builds}
                  selectedBuild={selectedBuild}
                  onBuildSelect={setSelectedBuild}
                  onDownload={handleDownload}
                />
              </div>
            </div>
          </main>

          <footer className="footer">
            Powered by <a href="#">Gemini API</a> • Not affiliated with Mojang
          </footer>
        </div>
      </div>
    </>
  );
}

export default App;
