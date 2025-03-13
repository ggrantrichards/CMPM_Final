import React, { useState } from "react";
import type { GenerateBuildParams } from "../types";

interface BuildFormProps {
  onSubmit: (params: GenerateBuildParams) => void;
  isGenerating: boolean;
}

export function BuildForm({ onSubmit }: BuildFormProps) {
  const [size, setSize] = useState<number>(10);
  const [description, setDescription] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ size, description });
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <div className="form-group">
        <label htmlFor="size" className="label">
          Size (10-30):
        </label>
        <input
          type="number"
          id="size"
          value={size}
          onChange={(e) => setSize(parseInt(e.target.value))}
          min={10}
          max={30}
          required
          className="input"
        />
      </div>

      <div className="form-group">
        <label htmlFor="description" className="label">
          Describe the build in a short sentence:
        </label>
        <input
          type="text"
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="e.g. Japanese house, Medieval castle, small store"
          required
          className="input"
        />
      </div>

      <button type="submit" className="button button-primary">
        Generate Build
      </button>
    </form>
  );
}
