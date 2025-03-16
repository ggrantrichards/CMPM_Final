import { useState, useEffect } from "react";
import { Cuboid as Cube, ChevronUp, ChevronDown } from "lucide-react";
import rawBlockAbbreviations from "../assets/block_abbreviations.json";

const blockAbbreviations = rawBlockAbbreviations as Record<string, string>;

function getBlockImage(abbr: string): string {
  // Look up the block name from the JSON; default to "minecraft:air" if missing
  const blockName = blockAbbreviations[abbr] || "minecraft:air";
  // Remove the "minecraft:" part
  const shortName = blockName.replace("minecraft:", "");
  // Build the final path
  return `./blockRepresentations/${shortName}.webp`;
}

function getBlockName(abbr: string): string {
  const blockName = blockAbbreviations[abbr] || "minecraft:air";
  const shortName = blockName.replace("minecraft:", "");
  return shortName;
}

function getCellDimension(buildSize: number): string {
  if (!buildSize) return "1rem";
  const dimension = 30 / buildSize;
  return `${dimension}rem`;
}

function getBuildSize(folderName: string): number {
  const parts = folderName.split("_");
  if (parts.length < 2) return 0;

  const sizeString = parts[1];
  const sizeParts = sizeString.split("x");
  if (sizeParts.length < 2) return 0;

  return parseInt(sizeParts[0], 10);
}

interface BuildVisualizationProps {
  doSpin: boolean;
  selectedBuild: string;
}

export function BuildVisualization({
  doSpin,
  selectedBuild,
}: BuildVisualizationProps) {
  const [layers, setLayers] = useState<string[][][]>([]);
  const [currentLayer, setCurrentLayer] = useState(0);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const buildSize = selectedBuild ? getBuildSize(selectedBuild) : 0;
  const cellDimension = getCellDimension(buildSize);

  useEffect(() => {
    if (selectedBuild) {
      loadLayers();
    } else {
      setErrorMessage(null);
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
      if (data.error) {
        console.error("No layers found:", data.error);
        setErrorMessage(data.error);
        setLayers([]);
      } else {
        setErrorMessage(null);
        setLayers(data.layers);
        setCurrentLayer(0); // Reset to first layer when loading new build
      }
    } catch (error) {
      console.error("Error loading layers:", error);
      setErrorMessage("Unexpected error loading layers");
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
          <Cube className="visualization-icon" />
        ) : layers.length > 0 && !doSpin ? (
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
              <div className="layer-content">
                {layers[currentLayer]?.map((row, i) => (
                  <div key={i} className="layer-row">
                    {row.map((cell, j) => {
                      // 1) Get the block name
                      const blockName = getBlockName(cell);

                      // 2) If it's air, show text. Otherwise, show an image
                      if (blockName === "air") {
                        return (
                          <div
                            key={j}
                            className="layer-cell air-cell"
                            style={{
                              width: cellDimension,
                              height: cellDimension,
                            }}
                          >
                            Air
                          </div>
                        );
                      } else {
                        // Normal block
                        return (
                          <div
                            key={j}
                            className="layer-cell"
                            style={{
                              width: cellDimension,
                              height: cellDimension,
                            }}
                          >
                            <img
                              src={getBlockImage(cell)}
                              title={blockName}
                              alt={cell}
                              className="block-image"
                            />
                          </div>
                        );
                      }
                    })}
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : doSpin ? (
          <div className="empty-state">
            <Cube className="visualization-icon-spin" />
            <p>Generating your build....</p>
          </div>
        ) : errorMessage ? (
          <div className="empty-state">
            <Cube className="visualization-icon" />
            <p>
              Build Failed try making a smaller build or use a different prompt
            </p>
            <div> Layer Length: {layers.length} </div>
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
