# This is... Headache! One more very simple Brainfuck interpreter!
# by Sidnei Diniz - sidneidiniz@gmail.com - http://bitworm.com.br
# GitHub: http://github.com/scdiniz/headache
# Date: 29-12-2015
# How to use: py headache.py <file>
import sys
import getch # Class to read a key.  http://code.activestate.com/recipes/134892/

# Interpreter kernel
class Headache():
	# Constructor
	def __init__(self):
		self.cells = bytearray([0] * 30000)
		self.commands = []			
	
	# Load code file
	def load(self, file):
		try:
			with open(file, "r") as code:
				for line in code:
					for c in line:
						if c in ("<", ">", "+", "-", ".", ",", "[", "]"):
							self.commands.append(c)
			
			return True
		except FileNotFoundError:
			return False			
	
	# Verify loop for errors
	def validateLoop(self):
		countStart = 0
		countEnd = 0
		
		for cmd in self.commands:
			if cmd == "[":
				countStart += 1
			
			elif cmd == "]":
				countEnd += 1
				
		return countStart == countEnd
	
	# Make loop dictionary
	def setLoopDict(self):
		if self.validateLoop():
			self.loopDict = {}
			tmp = []
			i = 0
			
			while i < len(self.commands):
				if self.commands[i] == "[":			    
					tmp.append(i)
											
				if self.commands[i] == "]":
					if len(tmp) > 0:
						value = tmp.pop()
						
						self.loopDict[value] = i
						self.loopDict[i] = value
					else:
						return False
				
				i += 1
				
			return True
		else:
			return False
	
	# Run interpreter
	def run(self, file):
		# Load code file
		if self.load(file):
		
			# Make loop dictionary
			if self.setLoopDict():
				cell = 0
				i = 0
				
				# Execute command by command
				while i < len(self.commands):								
					if self.commands[i] == "<":
						cell -= 1
						
					elif self.commands[i] == ">":
						cell += 1
						
					elif self.commands[i] == "+":
						if self.cells[cell] < 255:
							self.cells[cell] += 1
						else:
							self.cells[cell] = 0
						
					elif self.commands[i] == "-":
						if self.cells[cell] > 0:
							self.cells[cell] -= 1
						else:
							self.cells[cell] = 255
						
					elif self.commands[i] == "]":	
						if self.cells[cell] > 0:
							i = self.loopDict[i]
						
					elif self.commands[i] == "[":	
						if self.cells[cell] == 0:
							i = self.loopDict[i]
						
					elif self.commands[i] == ",":
						self.cells[cell] = ord(getch.getch())					
						
					elif self.commands[i] == ".":
						try:
							print(chr(self.cells[cell]), end = "", flush = True)
						except:
							None
						
					i += 1
			else:
				# Error on loop dictionary
				print("My head hurts! Verify your loop instructions '[' ']'")
		else:
			# Error loading code file
			print("My head hurts! Come on, tell me a VALID brainfuck file name!")

# Start
count = 0
filename = ""

# Reading sys arguments
for arg in sys.argv:	
	count += 1
	if count == 2:
		filename = arg
		break

# Verify if file name was insert
if count < 2:
	print("My head hurts! Come on, tell me brainfuck file name!")
else:
	# Launch interpreter
	Headache().run(filename)
