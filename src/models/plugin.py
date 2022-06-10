import inspect
import importlib
import subprocess

from typing import Callable, List, Tuple
from pydantic import BaseModel
from ..core.ext.plugin import PluginObject
from ..utils.string_utils import get_shortest_str
from ..exceptions.plugin import InvalidPluginError


class PluginConfig(BaseModel):
    """
    Configuration settings for a plugin. Exported to the app's
    `config.json` file upon installation & modifications.
    :param plugin_path: The path on the user's system pointing towards the plugin.
    :param icon_url: The URL pointing to the plugin's icon. Leave blank for default icon.
    :param version: A tuple of 3 integers, (MAJOR, MINOR, BRANCH) e.g. (1, 0, 0).
    :param description: The plugin's description. Will get shortened in overviews (unless expanded) to 64 characters (including 3 trailing spaces)
    :param activated: Activation status for the plugin. If deactivated, the plugin will not be loaded on game startup.
    """

    plugin_path: str
    icon_url: str = ""
    version: Tuple[int, int, int] = (0, 0, 1)  # Major, Minor, Branch
    description: str
    activated: bool = True
    hasRequirements: bool = False
    installedRequirements: bool = False

    def load_plugin(
        self, export_config_callback: Callable, path_to_config: str
    ) -> PluginObject:
        """Loads a plugin."""
        plugin_title = self.get_plugin_title()
        if self.hasRequirements and not self.installedRequirements:
            self._prompt_plugin_dependency_install()
            if not self.installedRequirements:
                print(
                    f"{plugin_title} will not be loaded since it's dependencies have not been installed."
                )
                return
            export_config_callback(path_to_config)
        plugin_main_file_path = f"{self.plugin_path}/main.py"
        plugin_name = inspect.getmodulename(plugin_main_file_path)
        plugin_module = importlib.import_module(
            f"src.plugins.{plugin_title}.src.{plugin_name}"
        )
        plugin_members = inspect.getmembers(plugin_module, inspect.isclass)
        plugin_main_class = None
        for member in plugin_members:
            if member[0] == plugin_title:
                plugin_main_class = member[1]
        if plugin_main_class is None:
            raise InvalidPluginError(
                f"Plugin {plugin_title} has no class with the name {plugin_title}!"
            )
        authors, version, description = self.get_plugin_metadata()
        return plugin_main_class(
            authors=authors,
            title=plugin_title,
            description=description,
        )

    def get_plugin_title(self):
        return self.plugin_path.split("/")[-1]

    def get_plugin_metadata(self):
        authors_path = f"{self.plugin_path}/authors"
        version_path = f"{self.plugin_path}/version"
        desc_path = f"{self.plugin_path}/description"
        with open(authors_path, mode="r") as f:
            authors = f.readlines()
        with open(version_path, mode="r") as f:
            version = f.read()
        with open(desc_path, mode="r") as f:
            description = f.read()
        return authors, version, description

    def _prompt_plugin_dependency_install(self) -> None:
        """Prompts the user to install the plugin's additional dependencies.
        If installation is successful, `plugin_config.installedRequirements`
        will be set to `True`."""
        title = self.get_plugin_title()
        install = input(
            f"{title} has additional dependencies. Would you like to install them now (y/n)? "
        )
        if install in ("y", "Y"):
            print(f"Installing dependencies for {title}..")
            subprocess.run(
                [
                    "py",
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    f"{self.plugin_path}/requirements.txt",
                ]
            )
            self.installedRequirements = True
