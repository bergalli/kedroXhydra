"""Project pipelines."""
from typing import Dict

import hydra
from get_started.pipelines import data_engineering as de
from get_started.pipelines import data_science as ds
from kedro.pipeline import Pipeline


# both decorators not working
# @hydra.main(config_path="../../conf", config_name="config")
@hydra.main(config_path="conf", config_name="config")
def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.

    """
    # hydra workaround
    # hydra.initialize(config_path="../../conf")
    # cfg = hydra.compose(config_name="config")

    data_engineering_pipeline = de.create_pipeline()
    data_science_pipeline = ds.create_pipeline()

    return {
        "de": data_engineering_pipeline,
        "ds": data_science_pipeline,
        "__default__": data_engineering_pipeline + data_science_pipeline,
    }