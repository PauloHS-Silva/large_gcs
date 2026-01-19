"""Contact graph GCS extractor (from shaoyuancc/large_gcs repository)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

SHAO_LARGE_GCS_DIR = Path(__file__).parent

# Add to path if not already there
if str(SHAO_LARGE_GCS_DIR) not in sys.path:
    sys.path.insert(0, str(SHAO_LARGE_GCS_DIR))

from large_gcs.graph.contact_graph import ContactGraph
from large_gcs.graph_generators.contact_graph_generator import (
    ContactGraphGeneratorParams,
)


def make_contact_gcs(
    graph_name: str,
    use_l1_cost: bool = True,
):
    """
    Load a pre-generated contact graph and extract Drake's GraphOfConvexSets.
    
    This function loads a saved ContactGraph from file and extracts the underlying
    Drake GCS.
    
    Args:
        graph_name: Name of the pre-generated graph (e.g., "cg_simple_4", "cg_trichal4", "cg_maze_b1")
        use_l1_cost: If True, use L1 norm vertex cost; if False, use L2 norm
    
    Returns:
        drake_gcs: Drake's GraphOfConvexSets object
        drake_source: Source vertex from Drake GCS
        drake_target: Target vertex from Drake GCS
        env_info: Dictionary with environment information
    """
    # Set PROJECT_ROOT environment variable for graph loading
    if "PROJECT_ROOT" not in os.environ:
        os.environ["PROJECT_ROOT"] = str(SHAO_LARGE_GCS_DIR)
    
    # Get graph file path
    graph_file = ContactGraphGeneratorParams.graph_file_path_from_name(graph_name)
    
    # Load contact graph from file
    contact_graph = ContactGraph.load_from_file(
        graph_file,
        should_use_l1_norm_vertex_cost=use_l1_cost,
    )
    
    # Extract Drake GCS
    drake_gcs = contact_graph._gcs
    
    # Get source and target vertices
    source_vertex_name = contact_graph.source_name
    target_vertex_name = contact_graph.target_name
    
    drake_source = contact_graph.vertices[source_vertex_name].gcs_vertex
    drake_target = contact_graph.vertices[target_vertex_name].gcs_vertex
    
    # Create env_info dict
    env_info = {
        'graph_name': graph_name,
        'num_vertices': contact_graph.n_vertices,
        'num_edges': contact_graph.n_edges,
        'use_l1_cost': use_l1_cost,
    }
    
    return drake_gcs, drake_source, drake_target, env_info
