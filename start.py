#!/usr/local/bin/python
nijversion = "NijBotv1 - Python 2.7.2 - Created by Nijaxor."
import threading, printer, Queue, sys
printer.Print("[I] Starting " + nijversion)

printQueue = Queue.Queue()

irc_connection = ""
try:
	irc_connection = __import__("connection")
	printer.Print("[I] Sucessfully loaded IRC connection module.")
except Exception as e:
	printer.Print("[E] Unable to load IRC connection module, Exiting.")
	printer.Print(e)
	sys.exit(0)
irc_pluginmanager = ""
try:
	irc_pluginmanager = __import__("pluginmanager")
	printer.Print("[I] Sucessfully loaded IRC pluginmanager module.")
	irc_pluginmanager.loadPlugins(printer.Print)
except Exception as e:
	printer.Print("[E] Unable to load IRC pluginmanager module, Exiting.")
	printer.Print(e)
	sys.exit(0)
irc_processline = ""
try:
	irc_processline = __import__("processline")
	printer.Print("[I] Sucessfully loaded IRC processline module.")
except Exception as e:
	printer.Print("[E] Unable to load IRC processline module, Exiting.")
	printer.Print(e)
	sys.exit(0)
irc_servers = ""
try:
	ircServers = open("servers/servers.txt").readlines()
	if len(ircServers) == 0:
		printer.Print("[E] servers/server.txt is empty, Exiting.")
		sys.exit(0)
	printer.Print("[I] Sucessfully loaded servers/servers.txt")
except Exception as e:
	printer.Print("[E] Unable to load servers/servers.txt, Exiting.")
	printer.Print(e)
	sys.exit(0)

ircConnections = {}

for line in ircServers:
	linesplit = line.split()
	if len(linesplit) >= 4:
		if ":" in linesplit[0]:
			ircConnections[linesplit[0].split(":")[0]] = {"address": linesplit[0]}
			chans = False
			if len(linesplit) > 4:
				chans = linesplit[4:]
			curCon = irc_connection.Connection
			threading.Thread(target=curCon, kwargs={"connectionInfo": {"conLine": line, "socket": False, "thread": False}, "channels": chans, "ircConnections": ircConnections, "connectModule": irc_connection, "processlineModule": irc_processline, "printQueue": printQueue, "version": nijversion, "pluginManager": irc_pluginmanager}).start()
		else:
			printer.Print("[E] Malformed server information for '" + linesplit[0] + "', skipping.")
	else:
		printer.Print("[E] Malformed server information for '" + linesplit[0] + "', skipping.")
printer.printerLoop(printQueue, ircConnections)
