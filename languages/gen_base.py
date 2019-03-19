################################################################################                                                     
## 
## Register map generation tool
##
## Copyright (C) 2018 Ondrej Ille <ondrej.ille@gmail.com>
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this SW component and associated documentation files (the "Component"),
## to deal in the Component without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Component, and to permit persons to whom the
## Component is furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Component.
##
## THE COMPONENT IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHTHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE COMPONENT OR THE USE OR OTHER DEALINGS
## IN THE COMPONENT.
##
###############################################################################

###############################################################################
##
##   Base generator class. Universal Class for generation of different
##   types of source codes.
##
##	Revision history:
##		25.01.2018	First implementation
##
################################################################################

from abc import ABCMeta, abstractmethod

class BaseGenerator(metaclass=ABCMeta):
	
	# Generator output
	out = None
	
	# Comment sign for particular language generator
	commentSign = None
	
	# Simple stack implementation for adding language constructs which require
	# ending parts such as structures, entities, HTML tags ...
	# Reffered to as append_stack
	appendText = None
	
	def __init__(self):
		self.out = []
		self.appendText = []
		self.commentSign = "#"

	
	def wr_line(self, line):
		"""
		Write single line to the generator output.
		Arguments:
			line		 Line to write into the output source code
		"""
		self.out.append(line)


	def append_line(self, line):
		"""
		Push the line to the generator stack.
		Arguments:
			line		 Line to write into the output source code
		"""
		self.appendText.insert(0, line)
	
	
	def wr_nl(self):
		"""
		Write new line into the generator output.
		"""
		self.wr_line("\n")
		
	
	def commit_append_line(self, count):
		"""
		Pop number of elements from the generator stack and write it to the 
		generator output.
		Arguments:
			count		 Number of items to pop
		"""
		for i in range(0, min(count, len(self.appendText))):
			self.wr_line(self.appendText[0])
			self.appendText.pop(0)
	
	
	def commit_append_lines_all(self):
		"""
		Pop all elements from the generator stack and write them to the output.
		Arguments:
			line		 Line to write into the output source code
		"""
		self.commit_append_line(len(self.appendText))
		
	
	@abstractmethod
	def write_comm_line(self, gap=2):
		"""
		Write full comment line to the generator output.
		Arguments:
			gap		 Number of tabs before the comment line
		"""
		pass


	@abstractmethod
	def write_comment(self, input, gap, caption=None, small=False):
		"""
		Write comment in the language specific format into the generator
		output.
		Arguments:
			input		Text of the comment to write
			gap			Number of tabs before the comment
			caption 	Caption of the comment
			small		Small comment is as compact as possible, Big comment
						takes more lines. Depends on particular language
						implemnetation
		"""
		pass
