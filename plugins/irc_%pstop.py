def ircFunction(line, **ircStuff):
	for server in ircStuff["ircConnections"]:
		ircStuff["ircConnections"][server]["socket"].send("QUIT :Leaving.\r\n")
	ircStuff["printQueue"].put("[U]")
