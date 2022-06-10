from typing import List
from pydantic import BaseModel
from ..models.config import PluginConfig
from ..models.plugin import PluginObject


class PluginHandler(BaseModel):
    plugin_pool: List[PluginObject] = []

    def start_plugins(self):
        for plugin in self.plugin_pool:
            plugin.Start()

    def update_plugins(self):
        for plugin in self.plugin_pool:
            plugin.Update()

    def kill_plugins(self):
        for plugin in self.plugin_pool:
            plugin.Exit()
            self.plugin_pool.remove(plugin)
