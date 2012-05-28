import socket, ssl, threading, printer, os
def Connection(**ircStuff):
	conInfo = ircStuff["connectionInfo"]["conLine"].split()[0].split(":")
	prefix = ircStuff["connectionInfo"]["conLine"].split()[1]
	ircStuff["botNick"] = ircStuff["connectionInfo"]["conLine"].split()[2]
	ircStuff["prefix"] = prefix
	ircSocket = socket.socket()
	plugins = ircStuff["pluginManager"].plugins
	ircStuff["plugins"] = plugins
	ircStuff["statusChecks"] = {}
	permissions = {}
	try:
		perms = open("servers/" + conInfo[0] + "/permissions.txt").readlines()
		if len(perms) > 0:
			for line in perms:
				linesplit = line.split()
				if len(linesplit) > 1:
					permissions[linesplit[0].lower()] = ["[" + "] [".join(a for a in linesplit[1:]) + "]", linesplit[0]]
			ircStuff["printQueue"].put("[I] Sucessfully loaded permissions for '" + conInfo[0] + "'.")
		else:
			ircStuff["printQueue"].put("[E] Permissions file for '" + conInfo[0] + "' is empty.")
	except Exception as e:
		ircStuff["printQueue"].put("[E] Unable to open permissions file for '" + conInfo[0] + "', " + str(e))
		permissions = False
		os.mkdir("servers/" + conInfo[0])
		open("servers/" + conInfo[0] + "/permissions.txt", "w")
	ircStuff["permissions"] = permissions
	try:
		ircSocket.connect((conInfo[0], int(conInfo[1].replace("+", ""))))
		ircStuff["printQueue"].put("[I] Connected to " + conInfo[0])
	except:
		ircStuff["printQueue"].put("[E] Failed to connect to " + conInfo[0])
		del ircStuff["ircConnections"][conInfo[0]]
		ircStuff["printQueue"].put("[U]")
		return
	if conInfo[1].startswith("+"):
		ircSocket = ssl.wrap_socket(ircSocket)
	ircStuff["connectionInfo"]["socket"] = ircSocket
	ircStuff["connectionInfo"]["thread"] = threading.currentThread()
	ircStuff["ircConnections"][conInfo[0]]["socket"] = ircSocket
	ircStuff["ircConnections"][conInfo[0]]["thread"] = threading.currentThread()
	def chanOrPriv(line):
		if line.split()[2].startswith("#"):
			return [line.split()[2], "Chan"]
		else:
			nickname = ""
			try:
				nickname = line.split()[0].split("!")[0].replace(":", "", 1)
			except:
				nickname = line.split()[0].split(".")[0].replace(":", "", 1)
			return [nickname, "Priv"]
	ircStuff["chanOrPriv"] = chanOrPriv
	def getNick(line):
		nickname = ""
		try:
			nickname = line.split()[0].split("!")[0].replace(":", "", 1)
		except:
			nickname = line.split()[0].split(".")[0].replace(":", "", 1)
		return nickname
	ircStuff["getNick"] = getNick
	def writer(text):
		text = text.replace("\r", "").replace("\n", "").replace("\r\n", "")
		ircSocket.send(text + "\r\n")
		#ircStuff["printQueue"].put(printer.colorCodes["blue"] + "-> " + printer.colorCodes["reset"] + conInfo[0] + printer.colorCodes["blue"] + " -> " + printer.colorCodes["reset"] + text)
	ircStuff["writer"] = writer
	writer("USER " + ircStuff["connectionInfo"]["conLine"].split()[2] + " 0 0 :" + ircStuff["version"])
	writer("NICK " + ircStuff["connectionInfo"]["conLine"].split()[2])
	inputFile = ircSocket.makefile()
	while 1:
		line = inputFile.readline()
		if len(line) > 0:
			ircStuff["processlineModule"].processLine(line, False, **ircStuff)
			#threading.Thread(target=ircStuff["processlineModule"].processLine, args=(line, False), kwargs=ircStuff).start()
		else:
			ircStuff["printQueue"].put("[E] Disconnnected from '" + conInfo[0] + "'.")
			del ircStuff["ircConnections"][conInfo[0]]
			ircStuff["printQueue"].put("[U]")
			return
