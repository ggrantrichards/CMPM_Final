import { useState, useEffect } from "react";
import { Cuboid as Cube } from "lucide-react";
import SchematicViewer from "@mcjeffr/react-schematicwebviewer";

interface Props {
  selectedBuild: string;
}

export function BuildVisualization({ selectedBuild }: Props) {
  const [schematicBase64, setSchematicBase64] = useState<string | null>(null);

  useEffect(() => {
    if (selectedBuild) {
      fetch(`/schematic-base64?folder=${selectedBuild}`)
        .then((res) => res.json())
        .then((data) => {
          if (data.error) {
            console.error("Error fetching base64 schematic:", data.error);
            setSchematicBase64(null);
          } else {
            setSchematicBase64(data.schematic);
          }
        })
        .catch((error) => {
          console.error("Error fetching base64 schematic:", error);
          setSchematicBase64(null);
        });
    }
  }, [selectedBuild]);

  // Provide a Minecraft jar or texture pack URL
  // e.g. "http://localhost:8080/assets/1.16.5.jar"
  // or a texture pack you have hosted somewhere
  const jarUrl = "client.jar";

  if (!selectedBuild) {
    return (
      <>
        <div className="panel">
          <h2 className="section-title">Build Visualization</h2>
          <div className="visualization">
            <div>Select a build</div>
          </div>
        </div>
      </>
    );
  }

  // If we haven't fetched the schematic yet
  if (!schematicBase64) {
    return (
      <>
        <div className="panel">
          <h2 className="section-title">Build Visualization</h2>
          <div className="visualization">
            <Cube className="visualization-icon" />
          </div>
        </div>
      </>
    );
  }
  return (
    <div className="panel">
      <h2 className="section-title">Build Visualization</h2>
      <div className="visualization">
        <div style={{ width: "600px", height: "600px" }}>
          <SchematicViewer
            schematic={schematicBase64}
            jarUrl={jarUrl}
            loader={
              <div style={{ textAlign: "center", paddingTop: "50px" }}>
                Loading your schematic...
              </div>
            }
            // You can pass other props as well:
            // orbit, renderArrow, renderBars, backgroundColor, etc.
            orbit
            renderBars
          />
        </div>
      </div>
    </div>
  );
}
