export interface Build {
  folder: string;
  description: string;
  size: string;
  timestamp: string;
}

export interface BuildLayer {
  layer: string[][];
}

export interface GenerateBuildParams {
  size: number;
  description: string;
}
