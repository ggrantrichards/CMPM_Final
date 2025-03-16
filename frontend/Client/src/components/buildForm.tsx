import React from "react";
import { Wand2 } from "lucide-react";
// import type { GenerateBuildParams } from "../types";

interface BuildFormProps {
  size: number;
  description: string;
  isGenerating: boolean;
  onSizeChange: (size: number) => void;
  onDescriptionChange: (description: string) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export function BuildForm({
  size,
  description,
  isGenerating,
  onSizeChange,
  onDescriptionChange,
  onSubmit,
}: BuildFormProps) {
  return (
    <form onSubmit={onSubmit}>
      <div className="range-container">
        <div className="range-header">
          <h2 className="section-title">Build Size (5-20 blocks)</h2>
          <span className="range-value">
            {size}x{size}
          </span>
        </div>
        <input
          type="range"
          min="5"
          max="20"
          value={size}
          onChange={(e) => onSizeChange(parseInt(e.target.value))}
          className="range-input"
          disabled={isGenerating}
        />
        <div className="range-labels">
          <span>5</span>
          <span>20</span>
        </div>
      </div>
      <h2 className="section-title">Build Description</h2>
      <div className="prompt-container">
        <textarea
          value={description}
          onChange={(e) => onDescriptionChange(e.target.value)}
          placeholder="Describe your Minecraft build..."
          className="textarea"
          disabled={isGenerating}
          required
        />
      </div>

      <button
        type="submit"
        className="button button-primary"
        disabled={isGenerating}
      >
        <Wand2 size={20} />
        Generate Build
      </button>
    </form>
  );
}
