import Queue, sys
def Print(text):
	if str(text).startswith("[E]"):
		text = text.replace("[E]", "\033[91m[Error]\033[0m")
	if str(text).startswith("[I]"):
		text = text.replace("[I]", "\033[92m[Info]\033[0m")
	if str(text).startswith("[*]"):
		text = text.replace("[*]", "\033[94m")
	print text, "\033[0m"

def printerLoop(printQueue, ircConnections):
	while 1:
		line = printQueue.get(True)
		if str(line) == "[U]":
			pass
		elif str(line) == "[Q]":
			break
		else:
			Print(line)
		if len(ircConnections.keys()) == 0:
			break
colorCodes = {"black": "\033[90m", "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m", "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m", "white": "\033[97m", "reset": "\033[0m"}
