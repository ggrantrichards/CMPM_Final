import type { Build } from "../types";

interface BuildSelectorProps {
  builds: Build[];
  selectedBuild: string;
  onBuildSelect: (folder: string) => void;
  onDownload: () => void;
}

export function BuildSelector({
  builds,
  selectedBuild,
  onBuildSelect,
  onDownload,
}: BuildSelectorProps) {
  return (
    <div className="build-selector">
      <div className="build-selector-content">
        <label htmlFor="buildSelect" className="label">
          Select Build:
        </label>
        <select
          id="buildSelect"
          value={selectedBuild}
          onChange={(e) => onBuildSelect(e.target.value)}
          className="select"
        >
          <option value="">-- Select a Build --</option>
          {builds.map((build) => (
            <option key={build.folder} value={build.folder}>
              {`${build.description} (${build.size}x${build.size}) - ${build.timestamp}`}
            </option>
          ))}
        </select>
      </div>
      <div className="build-selector-action">
        <div className="label">&nbsp;</div>
        <button
          onClick={onDownload}
          disabled={!selectedBuild}
          className="button button-success"
        >
          Download Schematic
        </button>
      </div>
    </div>
  );
}
