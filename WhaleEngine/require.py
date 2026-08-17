def requirePlugin(plugin_name, current_plugin_or_class=None):
    from .engine import current_app
    if not plugin_name in current_app.plugins:
        raise Exception(f"{current_plugin_or_class} requires plugin '{plugin_name}' to be loaded first." if current_plugin_or_class else f"Plugin '{plugin_name}' is required to be loaded first.")

def incompatibleWithPlugin(plugin_name, current_plugin=None):
    from .engine import current_app
    if plugin_name in current_app.plugins:
        raise Exception(f"Plugin '{plugin_name}' is incompatible with '{current_plugin}'." if current_plugin else f"Plugin '{plugin_name}' is incompatible.")