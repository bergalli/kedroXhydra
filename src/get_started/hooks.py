"""Project hooks."""
import os
from typing import Any, Dict, Iterable, Optional
from typing import List

import hydra
from kedro.config import ConfigLoader
from kedro.framework.cli.hooks import cli_hook_impl
from kedro.framework.cli.hooks.specs import CLICommandSpecs
from kedro.framework.hooks import hook_impl
from kedro.framework.hooks.specs import PipelineSpecs
from kedro.framework.startup import ProjectMetadata
from kedro.io import DataCatalog
from kedro.pipeline import Pipeline
from kedro.versioning import Journal
from omegaconf import DictConfig


class HydraLoadConfigHook(CLICommandSpecs, PipelineSpecs):
    cfg: DictConfig

    @cli_hook_impl
    def before_command_run(
            self, project_metadata: ProjectMetadata, command_args: List[str]
    ) -> None:
        overrides = command_args
        config_name = command_args
        if overrides is None:
            overrides = []
        hydra.initialize(config_path=os.environ['CONF_ROOT'])
        self.cfg = hydra.compose(config_name=config_name, overrides=overrides)

    @hook_impl
    def before_pipeline_run(
            self, run_params: Dict[str, Any], pipeline: Pipeline, catalog: DataCatalog
    ) -> None:
        catalog.add_feed_dict({'cfg': self.cfg})


class ProjectHooks:
    @hook_impl
    def register_config_loader(
            self, conf_paths: Iterable[str], env: str, extra_params: Dict[str, Any]
    ) -> ConfigLoader:
        return ConfigLoader(conf_paths)

    @hook_impl
    def register_catalog(
            self,
            catalog: Optional[Dict[str, Dict[str, Any]]],
            credentials: Dict[str, Dict[str, Any]],
            load_versions: Dict[str, str],
            save_version: str,
            journal: Journal,
    ) -> DataCatalog:
        return DataCatalog.from_config(
            catalog, credentials, load_versions, save_version, journal
        )
