import json
import os

from .core.game import Game
from .models.config import AppConfig
from .models.plugin import PluginConfig

if __name__ == "__main__":
    if not os.path.isfile("config.json"):
        config = AppConfig()
        config.export_config("config.json")
    else:
        with open("config.json", mode="r") as f:
            config = AppConfig(**json.load(f))
    config.add_plugin(PluginConfig(
        plugin_path="C:/Users/ShirtyDiamond33/Desktop/coolstuff/coolgame/src/plugins/MyPlugin",
        description="Sample description",
        hasRequirements=True
    ))
    config.export_config("config.json")
    game = Game(config=config)
    game.setup()
    game.start()