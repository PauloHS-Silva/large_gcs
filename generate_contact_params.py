import random
import sys
import tempfile
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import numpy as np


def _fmt(v: Any) -> str:
    """Format values so filenames are readable and stable."""
    if v is None:
        return "None"
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, float):
        return f"{v:.3f}".rstrip("0").rstrip(".")
    return str(v)


def generate_filename(config: Dict[str, Any], existing_files: Set[str]) -> str:
    """
    Generate YAML filename with actual values.
    Format:
    {graph_name}_{use_l1_cost}_{seed}.yaml
    """

    parts = [
        _fmt(config["graph_name"]),
        _fmt(config["use_l1_cost"]),
        _fmt(config["seed"]),
    ]

    filename = "_".join(parts) + ".yaml"
    original_seed = config["seed"]

    # Ensure uniqueness by bumping seed if needed
    attempt = 0
    max_attempts = 100
    while filename in existing_files and attempt < max_attempts:
        attempt += 1
        config["seed"] = original_seed + attempt
        parts[2] = _fmt(config["seed"])
        filename = "_".join(parts) + ".yaml"

    if attempt >= max_attempts:
        import time
        config["seed"] = int(time.time())
        parts[2] = _fmt(config["seed"])
        filename = "_".join(parts) + ".yaml"

    return filename


def main(output_dir: Optional[Path] = None) -> List[Path]:
    """
    Generate contact graph parameter YAML files.
    
    Args:
        output_dir: Directory to write parameter files to. If None, uses system temp.
    
    Returns:
        List of paths to generated YAML files
    """
    COUNT = 150
    SEED = 0
    
    random.seed(SEED)
    np.random.seed(SEED)
    
    # Set output directory, use temp directory if not specified
    if output_dir is None:
        output_dir = Path(tempfile.gettempdir()) / "gcs_examples_temp_contact_params"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get existing files to avoid duplicates
    existing_files = set(f.name for f in output_dir.glob("*.yaml") if f.is_file())
    
    # Generate config files
    generated_files = []
    
    # Available graph names
    # graph_names = ["cg_simple_4", "cg_trichal4", "cg_maze_b1"]
    graph_names = ["cg_simple_4"]
    
    for _ in range(COUNT):
        # Graph selection
        graph_name = random.choice(graph_names)
        
        # Cost type (L1 or L2)
        use_l1_cost = random.choice([True, False])
        
        # Random seed
        seed = random.randint(0, 100)
        
        config = {
            'graph_name': graph_name,
            'use_l1_cost': use_l1_cost,
            'seed': seed,
        }
        
        # Generate filename based on all parameter values
        filename = generate_filename(config, existing_files)
        filepath = output_dir / filename
        existing_files.add(filename)  # Add to set to avoid duplicates
        
        # Write config file
        with open(filepath, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=True, allow_unicode=True)
        
        generated_files.append(filepath)
    
    return generated_files


if __name__ == "__main__":
    main()
