# This is... Headache! One more very simple Brainfuck interpreter! #
# by Sidnei Diniz - sidneidiniz@gmail.com - http://bitworm.com.br #
# GitHub: http://github.com/scdiniz/headache
# Date: 29-12-2015 #
import sys

# Interpreter kernel
class Headache():
	# Constructor
	def __init__(self):
		self.cells = bytearray([0] * 30000)
		self.commands = []			
	
	# Load code file
	def load(self, file):
		code = open(file, "r")
		
		for line in code:
			for c in line:
				if c in ("<", ">", "+", "-", ".", ",", "[", "]"):
					self.commands.append(c)
		
		code.close()
	
	# Verify loop for errors
	def validateLoop(self):
		countStart = 0
		countEnd = 0
		
		for cmd in self.commands:
			if cmd == "[":
				countStart += 1
			
			if cmd == "]":
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
		self.load(file)		
		
		# Make loop dictionary
		if self.setLoopDict():
			cell = 0
			i = 0
			
			# Execute command by command
			while i < len(self.commands):								
				if self.commands[i] == "<":
					cell -= 1
					
				if self.commands[i] == ">":
					cell += 1
					
				if self.commands[i] == "+":
					if self.cells[cell] < 255:
						self.cells[cell] += 1
					else:
						self.cells[cell] = 0
					
				if self.commands[i] == "-":
					if self.cells[cell] > 0:
						self.cells[cell] -= 1
					else:
						self.cells[cell] = 255
					
				if self.commands[i] == "]":	
					if self.cells[cell] > 0:
						i = self.loopDict[i]
					
				if self.commands[i] == "[":	
					if self.cells[cell] == 0:
						i = self.loopDict[i]
					
				if self.commands[i] == ",":
					self.cells[cell] = ord(input()[0])#ord(input()[0])
					
				if self.commands[i] == ".":
					try:
						print(chr(self.cells[cell]), end = "", flush = True)
					except:
						None
					
				i += 1
		else:
			# Error on loop dictionary
			print("My head hurts! Verify your loop instructions '[' ']'")

# Start
count = 0
file = ""

# Reading sys arguments
for arg in sys.argv:	
	count += 1
	if count == 2:
		file = arg
		break

# Verify if file name was insert
if count < 2:
	print("My head hurts! Come on, tell me brainfuck file name!")
else:
	# Launch interpreter
	Headache().run(file)
