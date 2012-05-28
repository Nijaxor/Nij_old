import sys, threading, os, printer

def processLine(line, authed, **ircStuff):
	if len(line) > 0:
		#print line.strip()
		ircStuff["printQueue"].put(printer.colorCodes["blue"] + "<- " + printer.colorCodes["reset"] + ircStuff["connectionInfo"]["conLine"].split()[0].split(":")[0] + printer.colorCodes["blue"] + " <- " + printer.colorCodes["reset"] + line.strip())
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
				print "penis1"
				if linesplit[3].replace(":", "", 1).replace(ircStuff["prefix"], "", 1) in ircStuff["plugins"]:
					print "penis2"
					lowerNick = ircStuff["getNick"](line).lower()
					if "%p" in ircStuff["plugins"][linesplit[3].replace(":", "", 1).replace(ircStuff["prefix"], "", 1)]["flags"]:
						print "penis3"
						if linesplit[3].replace(":", "", 1).startswith(ircStuff["prefix"]):
							print "penis4"
							pass
						else:
							print "penis5"
							return
					if "%a" in ircStuff["plugins"][linesplit[3].replace(":", "", 1).replace(ircStuff["prefix"], "", 1)]["flags"]:
						print "penis6"
						if not ircStuff["permissions"] == False:
							if lowerNick in ircStuff["permissions"]:
								print "penis7"
								if ("[" + linesplit[3].replace(":", "", 1).replace(ircStuff["prefix"], "", 1) + "]" in ircStuff["permissions"][lowerNick][0]) or ("[*]" in ircStuff["permissions"][lowerNick][0]):
									print "penis8"
									if authed == True:
										print "penis9"
										ircStuff["plugins"][linesplit[3].replace(":", "", 1).replace(ircStuff["prefix"], "", 1)]["object"].ircFunction(line, **ircStuff)
									else:
										print "penis10"
										if not ircStuff["getNick"](line) in ircStuff["statusChecks"]:
											ircStuff["statusChecks"][ircStuff["getNick"](line)] = []
										ircStuff["statusChecks"][ircStuff["getNick"](line)].append(line)
										ircStuff["writer"]("PRIVMSG nickserv :status " + ircStuff["getNick"](line))
										ircStuff["writer"]("PRIVMSG nickserv :acc " + ircStuff["getNick"](line))
								else:
									ircStuff["writer"]("NOTICE " + ircStuff["getNick"](line) + " :You do not have sufficient permissions to do this.")
							else:
								ircStuff["writer"]("NOTICE " + ircStuff["getNick"](line) + " :You do not have sufficient permissions to do this.")
					else:
						ircStuff["plugins"][linesplit[3].replace(":", "", 1)]["object"].ircFunction(line, **ircStuff)
				if linesplit[3] == ":\01VERSION\01":
					ircStuff["writer"]("NOTICE " + ircStuff["getNick"](line) + " :\01VERSION " + ircStuff["version"] + "\01")
			if linesplit[1] == "NOTICE":
				if ircStuff["getNick"](line).lower() == "nickserv":
					if linesplit[3] == ":STATUS":
						if linesplit[4] in ircStuff["statusChecks"]:
							if linesplit[5] == "3":
								for command in ircStuff["statusChecks"][linesplit[4]]:
									ircStuff["processlineModule"].processLine(command, True, **ircStuff)
								del ircStuff["statusChecks"][linesplit[4]]
							else:
								ircStuff["writer"]("NOTICE " + linesplit[4] + " :You do not have sufficient permissions to do this.")
								del ircStuff["statusChecks"][linesplit[4]]
					if linesplit[4] == "ACC":
						if linesplit[3].replace(":", "", 1) in ircStuff["statusChecks"]:
							if linesplit[5] == "3":
								for command in ircStuff["statusChecks"][linesplit[3].replace(":", "", 1)]:
									ircStuff["processlineModule"].processLine(command, True, **ircStuff)
								del ircStuff["statusChecks"][linesplit[3].replace(":", "", 1)]
							else:
								ircStuff["writer"]("NOTICE " + linesplit[3].replace(":", "", 1) + " :You do not have sufficient permissions to do this.")
								del ircStuff["statusChecks"][linesplit[3].replace(":", "", 1)]
