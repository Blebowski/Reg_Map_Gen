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
##   Class for language declaration of variable, constant, etc...
##
##	Revision history:
##		25.01.2018	First implementation
##
################################################################################

from abc import ABCMeta, abstractmethod

class LanDeclaration(metaclass=ABCMeta):
	
	# Declaration specifier: const, volatile ...
	specifier = None
	
	# Declaration type: uint32_t, std_logic ...
	type = None
	
	# Declaration bit (width of std_logic_vector or bitfield)
	bitWidth = 0
	
	# Declaration bit index for bitfield element declaration
	bitIndex = None
	
	# Declaration value
	value = None
	
	# Declaration name
	name = None
	
	# Declaration alignment
	aligLen = 50
	
	# Number of tabs before the declaration
	gap = 0

	# Ports of VHDL entity (Dictionary of Declarations)
	ports = {}

	# Generics of VHDL entity (Dictionary of Declarations)
	generics = {}

	# Alignment of generated declaration to the Right
	alignRight = True

	# Alignment of generated declaration to the Right
	alignLeft = False

	# Indent between name and type specifiers
	doIndent = False
	
	# Wrap declaration if it is longer than 80 characters
	wrap = True

	# Comment before the declaration
	comment =   None

	# Direction of the declaration
	direction = None

	# Flag if component is an instance (used for distinguishing between entity and
	# component
	isInstance = False

	# Upper and lower boundary of std_logic_vector
	upBound = None
	lowBound = None

	# If semicoln should be added at the end of declaration
	addSemicoln = True

	# Internal type to distinguish between various formats of declaration
	# (e.g. enum element declaration has different format than structure
	#  element declaration)
	intType = None
	# IntType so far has: initialized, enum, bitfield
	
	def __init__(self, name, value, type=None, bitWidth=None, specifier=None,
					alignLen=50, gap=0, bitIndex=None, intType=None, comment=None):
		self.name = name
		self.value = value
		self.alignLen = alignLen
		self.gap = gap
		self.ports = {}
		self.generics = {}

		if (comment != None):
			self.comment = comment
		if (type != None):
			self.type = type
		if (bitWidth != None):
			self.bitWidth = bitWidth
		if (specifier != None):
			self.specifier = specifier
		if (bitIndex != None):
			self.bitIndex = bitIndex
		if (intType != None):
			self.intType = intType
	
