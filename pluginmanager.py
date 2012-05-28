import sys, os, inspect
sys.path.append("plugins/")
plugins = {}

def loadPlugins(printMethod):
	if os.path.exists(os.getcwd() + "/plugins/"):
		pluginList = os.listdir("plugins/")
		for plugin in pluginList:
			if (plugin.startswith("irc_")) and (plugin.endswith(".py")):
				pluginName = plugin.replace("irc_", "", 1).replace(".py", "")
				flags = ""
				if (pluginName.startswith("%a")) or (pluginName.startswith("%p")):
					flags = flags + pluginName[:2]
					pluginName = pluginName.replace(pluginName[:2], "", 1)
				if (pluginName.startswith("%a")) or (pluginName.startswith("%p")):
					flags = flags + pluginName[:2]
					pluginName = pluginName.replace(pluginName[:2], "", 1)
				try:
					curPlugin = __import__(plugin.replace(".py", ""))
					if (hasattr(curPlugin, "ircFunction")) and (inspect.isfunction(getattr(curPlugin, "ircFunction"))):
						plugins[pluginName] = {"object": curPlugin, "location": "plugins/" + plugin, "originalName": plugin, "flags": flags}
						printMethod("[I] Loaded module \"" + pluginName + "\".")
					else:
						printMethod("[E] Module '" + pluginName + "' does not have an 'ircFunction' function.")
						del curPlugin
						del sys.modules[plugin.replace(".py", "")]
				except Exception as e:
					printMethod("[E] Module '" + plugin + "' failed to load: " + str(e) + ".")
def reloadPlugins(printMethod):
	pluginList = os.listdir("plugins/")
	errors = []
	reloaded = []
	for plugin in plugins:
		matched = False
		for pluginA in pluginList:
			if plugins[plugin]["originalName"] == pluginA:
				matched = True
		if matched == False:
			del sys.modules[plugins[plugin]["originalName"]]
			del plugins[plugin]
		else:
			try:
				reload(plugins[plugin]["object"])
				if (hasattr(plugins[pluginName]["object"], "ircFunction")) and (inspect.isfunction(plugins[pluginName]["object"].ircFunction)):
					reloaded.append(plugin)
				else:
					errors.append(["reload", plugin, "Does not have an 'ircFunction' function."])
					printMethod("[E] Module '" + pluginName + "' does not have an 'ircFunction' function.")
			except Exception as e:
				printMethod("[E] Module '" + pluginName + "' failed to load: " + str(e) + ".")
				errors.append(["reload", plugin, str(e)])
	pluginlist = "[" + "][".join(a for a in pluginList) + "]"
	for plugin in reloaded:
		pluginlist.replace("[" + plugin + "]", "")
	pluginList = pluginlist[1:-1].split("][")
	print pluginList
	for plugin in pluginList:
		if (plugin.startswith("irc_")) and (plugin.endswith(".py")):
			pluginName = plugin.replace("irc_", "", 1).replace(".py", "")
			flags = ""
			if (pluginName.startswith("%a")) or (pluginName.startswith("%p")):
				flags = flags + pluginName[:2]
				pluginName = plugin.replace(plugin[:2], "", 1)
			if (pluginName.startswith("%a")) or (pluginName.startswith("%p")):
				flags = flags + pluginName[:2]
				pluginName = pluginName.replace(plugin[:2], "", 1)
			try:
				curPlugin = __import__(plugin.replace(".py", ""))
				if (hasattr(curPlugin, "ircFunction")) and (inspect.isfunction(getattr(curPlugin, "ircFunction"))):
					plugins[pluginName] = {"object": curPlugin, "location": "plugins/" + plugin, "originalName": plugin, "flags": flags}
					printMethod("[I] Loaded module \"" + pluginName + "\".")
				else:
					printMethod("[E] Module '" + pluginName + "' does not have an 'ircFunction' function.")
					del curPlugin
					del sys.modules[plugin.replace(".py", "")]
			except Exception as e:
				printMethod("[E] Module '" + pluginName + "' failed to load: " + str(e) + ".")
				errors.append(["load", pluginName, str(e)])
	return errors
			
