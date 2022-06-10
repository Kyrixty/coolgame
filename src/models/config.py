import json
import subprocess

from os import PathLike
from typing import Dict
from pydantic import BaseModel
from .plugin import PluginConfig


class AppConfig(BaseModel):
    plugins: Dict[str, PluginConfig] = {}

    def export_config(self, path_to_config_file: PathLike) -> None:
        """Loads the app's config."""
        with open(path_to_config_file, mode="w") as f:
            f.write(self.json(indent=4, sort_keys=True))

    def load_config(path_to_config_file: PathLike):
        """Loads the app's config."""
        with open(path_to_config_file, mode="r") as f:
            return AppConfig(**json.load(f))

    def add_plugin(self, plugin_config: PluginConfig) -> None:
        plugin_title = plugin_config.get_plugin_title()
        if plugin_title in self.plugins:
            return
        self.plugins[plugin_title] = plugin_config

    def rmv_plugin(self, plugin_title: str) -> None:
        del self.plugins[plugin_title]
