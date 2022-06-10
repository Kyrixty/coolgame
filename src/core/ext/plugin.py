from typing import List
from pydantic import BaseModel
from ...utils.string_utils import get_shortest_str


class PluginObject(BaseModel):
    """A `PluginObject` is the base object for all plugins.
    Each Plugin, no matter how customized, must have the
    following attributes:

    :param authors: A list of the authors of the plugin.
    :param title: The plugin's title.
    :param config: The plugin's config
    """

    authors: List[str]
    title: str
    description: str

    def get_shortest_description(self) -> str:
        """Returns the plugin's description, either with trailing periods (<short description>...)
        or the entire description if it is 64 characters in length or less."""
        return get_shortest_str(
            self.description,
            f"{self.description[:61]}...",
        )

    def Start(self) -> None:
        """Called once as the game starts."""
        ...

    def Update(self) -> None:
        """Called once per frame."""
        ...

    def Exit(self) -> None:
        """Called before game exit."""
        ...
