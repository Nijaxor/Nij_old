import sys, os, inspect
sys.path.append("plugins/")
plugins = {}

def loadPlugins(printMethod):
	if os.path.exists(os.getcwd() + "/plugins/"):
		pluginList = os.listdir("plugins/")
		for plugin in pluginList:
			if (plugin.startswith("irc_")) and (plugin.endswith(".py")):
				curPlugin = __import__(plugin.replace(".py", ""))
				if (hasattr(curPlugin, "ircFunction")) and (inspect.isfunction(getattr(curPlugin, "ircFunction"))):
					pluginName = plugin.replace("irc_", "", 1).replace(".py", "")
					plugins[pluginName] = {"object": curPlugin, "location": "plugins/" + plugin, "originalName": plugin}
					printMethod("[I] Loaded module \"" + pluginName + "\".")
				else:
					printMethod("[E] Module '" + pluginName + "' does not have an 'ircFunction' function.")
		return plugins
	else:
		return null
def reloadPlugins(printMethod):
	pluginList = os.listdir("plugins/")
	for plugin in plugins:
		matched = False
		for pluginA in pluginlist:
			if plugins[plugin]["originalName"] == pluginA:
				matched = True
		if matched == False:
			del sys.modules[plugins[plugin]["originalName"]]
			del plugins[plugin]
	for plugin in pluginList:
		if (plugin.startswith("irc_")) and (plugin.endswith(".py")):
			pluginName = plugin.replace("irc_", "", 1).replace(".py", "")
			if pluginName in plugins:
				reload(plugins[pluginName]["object"])
			else:
				curPlugin = __import__(plugin.replace(".py", ""))
				plugins[pluginName] = {"object": curPlugin, "location": "plugins/" + plugin, "originalName": plugin}
