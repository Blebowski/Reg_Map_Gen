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
##   Base language generator class. Supports methods for basic source code
##   generation (declarations, enums, structures).
##
##	Revision history:
##		25.01.2018	First implementation
##
################################################################################

from abc import ABCMeta, abstractmethod
from pyXact_generator.languages.gen_base import BaseGenerator
from enum import Enum

class LanBaseGenerator(BaseGenerator):
	
	# Field of declaration supported types for given language generator
	supportedTypes = None
	
	# Bit sizes of the types defined in "supportedTypes"
	typeSizes = None
	
	def __init__(self):
		super().__init__()
		self.supportedTypes = []
		self.typesSizes = []


################################################################################
#	BaseGenerator inherited functions		
################################################################################		

	def wr_line(self, line):
		return super().wr_line(line)
	
	def append_line(self, line):
		return super().append_line(line)
	
	def wr_nl(self):
		return super().wr_nl()
	
	def commit_append_line(self, count):
		return super().commit_append_line(count)
		
	def commit_append_lines_all(self):
		return super().commit_append_lines_all()

	class LogicOp(Enum):
		OP_ASIGN = 0
		OP_COMPARE = 1
		OP_AND = 2
		OP_OR = 3
		OP_XOR = 4
		OP_ADD = 5
		OP_SUB = 6
		OP_MUL = 7
		OP_DIV = 8
		OP_NOT = 9

		
################################################################################
#	Language generator specific functions which should be implemented
#	by each child and provide language specific way of implementing the
#	given construct.
################################################################################			

	def is_supported_type(self, type):
		"""
		Check if declaration type is supported by this language generator
		Arguments:
			type		 Declaration type
		"""
		for i in self.supportedTypes:
			if (type == i):
				return True
		print("{} is not supported type for {} class".format(
					type, self.__class__.__name__))
		return False


	@abstractmethod
	def create_includes(self, includeList):
		"""
		Create includes in the language generator output
		Arguments:
			includeList		List of includes to be written
		"""
		pass
	
	@abstractmethod
	def write_decl(self, decl):
		"""
		Write declaration into the language generator output
		Arguments:
			decl		Declaration to write (LanDeclaration)
		"""
		pass
	
	@abstractmethod
	def create_package(self, name):
		"""
		Create language specific package into the language generator output
		Arguments:
			name		Package name
		"""
		pass

	@abstractmethod
	def create_structure(self, name, decls):
		"""
		Create a structure into the language generator output.
		Arguments:
			name		Structure name
			decls		List of structure declarations
		"""
		pass
		
	@abstractmethod
	def create_enum(self, name, decls):
		"""
		Create an enum into the language generator output
		Arguments:
			name		Enum name
			decls		List of enum declarations
		"""
		pass	
