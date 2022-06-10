# CoolGame
I need a name..

## Plugin Architecture
Each plugin MUST have the following directory structure:
```bash
MyPlugin/
    src/
        main.py
    authors
    description
    requirements.txt
    version
```
Additionally, there must be a class in your plugin's `main.py` file that has the same title as the project which also inherits from `PluginObject`. This class should serve as the "entry point" to your plugin. Using the architecture above, `MyPlugin/src/main.py` would have a class titled `MyPlugin` which inherits from the `PluginObject` class found in `coolgame/src/core/ext/plugin.py`.

For example, assuming we have the plugin structered the same way as the above example:
```python
from coolgame.core.ext.plugin import PluginObject


class MyPlugin(PluginObject):
    def Start(self) -> None:
        #Start logic here
        ...
        
    def Update(self) -> None:
        #Update logic here
        ...
        
    def Exit(self) -> None:
        #Exit logic here
        ...
```
