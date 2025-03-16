import { Download } from "lucide-react";
import type { Build } from "../types";

interface SchematicDownloadProps {
  builds: Build[];
  selectedBuild: string;
  onBuildSelect: (folder: string) => void;
  onDownload: () => void;
}

export function SchematicDownload({
  builds,
  selectedBuild,
  onBuildSelect,
  onDownload,
}: SchematicDownloadProps) {
  return (
    <div className="panel">
      <h2 className="section-title">Build Selector</h2>
      <select
        value={selectedBuild}
        onChange={(e) => onBuildSelect(e.target.value)}
        className="select"
      >
        <option value="">Select a build</option>
        {builds.map((build) => (
          <option key={build.folder} value={build.folder}>
            {`${build.description} (${build.size}x${build.size})`}
          </option>
        ))}
      </select>

      <button
        onClick={onDownload}
        disabled={!selectedBuild}
        className="button button-primary"
      >
        <Download size={20} />
        Download Schematic
      </button>
    </div>
  );
}
