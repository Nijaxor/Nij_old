import sys, threading, os, copy

def processLine(line, **ircStuff):
	if len(line) > 0:
		#print line.strip()
		linesplit = line.split()
		if linesplit[0] == "PING":
			ircStuff["writer"]("PONG " + linesplit[1])
		if len(linesplit) > 1:
			if linesplit[1] == "001":
				ircStuff["writer"]("PRIVMSG nickserv :identify " + ircStuff["connectionInfo"]["conLine"].split()[3])
				if not ircStuff["channels"] == False:
					for chan in ircStuff["channels"]:
						ircStuff["writer"]("JOIN " + chan)
			if linesplit[1] == "433":
				ircStuff["printQueue"].put("[E] Nickname in use '" + ircStuff["botNick"] + "' reattempting with an appended '_'.")
				ircStuff["botNick"] = ircStuff["botNick"] + "_"
				ircStuff["writer"]("NICK " + ircStuff["botNick"])
			if linesplit[1] == "PRIVMSG":
				if linesplit[3].startswith(ircStuff["prefix"]):
					linesplit[3] = linesplit[3].replace(ircStuff["prefix"], "%p", 1)
				if linesplit[3].replace(":", "", 1) in ircStuff["plugins"]:
					lowerNick = ircStuff["getNick"](line).lower()
					if not ircStuff["permissions"] == False:
						if lowerNick in ircStuff["permissions"]:
							if (linesplit[3].replace(":", "", 1) in ircStuff["permissions"][lowerNick]) or ("*" in ircStuff["permissions"][lowerNick]):
								plugins[linesplit[3].replace(":", "", 1)]["object"].ircFunction(line, **ircStuff)
				if linesplit[3] == ":\01VERSION\01":
					ircStuff["writer"]("NOTICE " + ircStuff["getNick"](line) + " :\01VERSION " + ircStuff["version"] + "\01")
