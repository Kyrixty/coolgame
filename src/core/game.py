from typing import List
from pydantic import BaseModel
from ..models.plugin import PluginConfig, PluginObject
from ..models.config import AppConfig
from ..exceptions.game import NotSetupError
from .plugin_handler import PluginHandler


class Game(BaseModel):
    config: AppConfig
    isSetup: bool = False
    running: bool = False
    plugin_handler: PluginHandler | None = None

    def setup(self) -> None:
        plugin_configs = self.get_activated_plugin_configs()
        plugin_pool: List[PluginObject] = [
            plugin
            for plugin in [
                plugin_config.load_plugin(self.config.export_config, "config.json") for plugin_config in plugin_configs
            ]
            if plugin is not None
        ]
        self.plugin_handler = PluginHandler(plugin_pool=plugin_pool)
        self.isSetup = True

    def start(self) -> None:
        """Starts the game."""
        if not self.isSetup:
            raise NotSetupError("The game has not been setup!")
        self.plugin_handler.start_plugins()
        self.running = True
        while self.running:
            self.plugin_handler.update_plugins()
        self.plugin_handler.kill_plugins()

    def stop(self) -> None:
        """Stops the game."""
        self.running = False

    def get_activated_plugin_configs(self) -> List[PluginConfig]:
        """Loads all *activated* plugins on game startup."""
        return [plugin for plugin in list(self.config.plugins.values()) if plugin.activated]
