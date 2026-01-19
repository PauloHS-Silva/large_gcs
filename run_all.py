import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

# Add parent directory to path to import generate_contact_params
root = pathlib.Path(__file__).parent.resolve()

# Import from current directory
from generate_contact_params import main as generate_params

# Generate parameters to temporary folder
with tempfile.TemporaryDirectory(prefix="gcs_examples_temp_contact_config_") as temp_base_str:
    temp_base = pathlib.Path(temp_base_str)
    
    # Create temporary config structure: temp_base/conf/contact_params/
    temp_conf_dir = temp_base / "conf"
    temp_params_dir = temp_conf_dir / "contact_params"
    temp_params_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy the main config files to temp conf directory
    original_conf_dir = root / "conf"
    for config_file in ["config.yaml", "debug.yaml"]:
        src = original_conf_dir / config_file
        if src.exists():
            shutil.copy2(src, temp_conf_dir / config_file)
    
    # Generate parameter files
    generated_files = generate_params(output_dir=temp_params_dir)
    
    # Get just the filenames for Hydra
    names = [f.name for f in generated_files]
    
    # Run generator for each parameter file
    # Use --config-path to point to temporary config directory
    for n in names:
        subprocess.run(
            [
                "python",
                str(root / "generator.py"),
                f"--config-path={temp_conf_dir}",
                "--config-name=config",
                f"contact_params={n}",
                "force_remake=true",
            ],
            cwd=str(root),
        )
