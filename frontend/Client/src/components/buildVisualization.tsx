import { useState, useEffect } from "react";
import { Cuboid as Cube, ChevronUp, ChevronDown } from "lucide-react";

// interface Layer {
//   content: string[][];
// }

export function BuildVisualization({
  selectedBuild,
}: {
  selectedBuild: string;
}) {
  const [layers, setLayers] = useState<string[][][]>([]);
  const [currentLayer, setCurrentLayer] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedBuild) {
      loadLayers();
    } else {
      setLayers([]);
    }
  }, [selectedBuild]);

  const loadLayers = async () => {
    if (!selectedBuild) return;

    setLoading(true);
    try {
      const response = await fetch(
        `/load-build?folder=${encodeURIComponent(selectedBuild)}`
      );
      const data = await response.json();
      setLayers(data.layers);
      setCurrentLayer(0); // Reset to first layer when loading new build
    } catch (error) {
      console.error("Error loading layers:", error);
    } finally {
      setLoading(false);
    }
  };

  const navigateLayer = (direction: "up" | "down") => {
    if (direction === "up" && currentLayer < layers.length - 1) {
      setCurrentLayer((prev) => prev + 1);
    } else if (direction === "down" && currentLayer > 0) {
      setCurrentLayer((prev) => prev - 1);
    }
  };

  return (
    <div className="panel">
      <h2 className="section-title">Build Visualization</h2>
      <div className="visualization">
        {loading ? (
          <Cube className="visualization-icon animate-pulse" />
        ) : layers.length > 0 ? (
          <div className="layer-viewer">
            <div className="layer-navigation">
              <button
                onClick={() => navigateLayer("up")}
                disabled={currentLayer >= layers.length - 1}
                className="nav-button"
              >
                <ChevronUp size={24} />
              </button>
              <div className="layer-indicator">
                Layer {currentLayer + 1} of {layers.length}
              </div>
              <button
                onClick={() => navigateLayer("down")}
                disabled={currentLayer <= 0}
                className="nav-button"
              >
                <ChevronDown size={24} />
              </button>
            </div>
            <div className="layer-display">
              <pre className="layer-content">
                {layers[currentLayer]?.map((row, i) => (
                  <div key={i} className="layer-row">
                    {row.map((cell, j) => (
                      <span key={j} className="layer-cell">
                        {cell}
                      </span>
                    ))}
                  </div>
                ))}
              </pre>
            </div>
          </div>
        ) : (
          <div className="empty-state">
            <Cube className="visualization-icon" />
            <p>Select a build below to view</p>
          </div>
        )}
      </div>
    </div>
  );
}
