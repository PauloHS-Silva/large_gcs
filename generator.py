import os
import pathlib
import sys
from pathlib import Path

import hydra
import matplotlib.pyplot as plt
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf

# Add parent gcs_examples directory to path for imports
GCS_EXAMPLES_DIR = Path(__file__).parent.parent
if str(GCS_EXAMPLES_DIR) not in sys.path:
    sys.path.insert(0, str(GCS_EXAMPLES_DIR))

import dropbox
from gcs_examples import run_generators

# Register resolvers for config interpolation
OmegaConf.register_new_resolver(
    "dropbox_gcs_examples_path", lambda: dropbox.DROPBOX_GCS_EXAMPLES_PATH, replace=True
)


@hydra.main(version_base=None, config_path="conf", config_name="debug")
def main(cfg: DictConfig) -> None:
    # Get the hydra output directory (where .hydra config is automatically written)
    hydra_cfg = HydraConfig.get()
    output_dir = pathlib.Path(hydra_cfg.runtime.output_dir)
    gcs_path = output_dir / "gcs.pybin"
    if os.path.exists(gcs_path) and not cfg.force_remake:
        print(f"Example at {gcs_path} exists. Skipping")
        return

    # Generate the GCS from contact graph parameters
    params = cfg.contact_params

    # Import and call make_contact_gcs function
    from contact_graph import make_contact_gcs

    try:
        drake_gcs, drake_source, drake_target, env_info, contact_graph = make_contact_gcs(
            graph_name=params.graph_name,
            use_l1_cost=params.use_l1_cost,
        )

        # Plot contact graph and save
        contact_graph.plot(label_vertices_faces=False)
        fig = plt.gcf()
        fig.savefig(output_dir / "contact_graph.png", dpi=150, bbox_inches='tight')
        plt.close(fig)

        # Use run_generators.run_drake to solve and save
        run_generators.run_drake(
            drake_gcs, drake_source, drake_target, output_dir, num_trials=cfg.num_trials
        )
    except Exception as e:
        import traceback
        print(f"ERROR: Failed to generate GCS for graph_name={params.graph_name}, use_l1_cost={params.use_l1_cost}")
        print(f"Exception type: {type(e).__name__}: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
