ircSyntax = "QUIT (Optional: server address)"
def ircFunction(line, **ircStuff):
	linesplit = line.split()
	if len(linesplit) > 4:
		if linesplit[4] in ircStuff["ircConnections"]:
			ircStuff["ircConnections"][linesplit[4]]["socket"].send("QUIT :Leaving.\r\n")
		else:
			ircStuff["writer"]("NOTICE " + ircStuff["getNick"](line) + " :Not connected to server '" + linesplit[4] + "'.")
	else:
		for server in ircStuff["ircConnections"]:
			ircStuff["ircConnections"][server]["socket"].send("QUIT :Leaving.\r\n")
