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
##   Address map generator to C header file (Linux kernel style)
## 
##	Revision history:
##		29.05.2021	First implementation
##
################################################################################

from abc import ABCMeta, abstractmethod
from pyXact_generator.ip_xact.addr_generator import IpXactAddrGenerator

from pyXact_generator.languages.gen_h import HeaderGenerator
from pyXact_generator.languages.declaration import LanDeclaration


class KernHeaderAddrGenerator(IpXactAddrGenerator):

	headerGen = None
	prefix	= ""

	def __init__(self, pyXactComp, memMap, wrdWidthBit):
		super().__init__(pyXactComp, memMap, wrdWidthBit)
		self.headerGen = HeaderGenerator()

	def commit_to_file(self):
		for line in self.headerGen.out :
			self.of.write(line)

	def sort_regs_to_wrd_groups(self, regs):
		"""
		Sort list of IP-XACT register objects into groups. Each group is
		represented by a list. Each list contains registers located within
		a single memory word.
		"""
		regGroups = [[]]
		lowInd = 0

		# Sort the registers from field map into sub-lists
		for reg in sorted(regs, key=lambda a: a.addressOffset):

			# We hit the register aligned create new group
			if (reg.addressOffset >= lowInd + self.wrdWidthByte):
				lowInd = reg.addressOffset - reg.addressOffset % 4
				regGroups.append([])

			regGroups[-1].append(reg)

		return regGroups

	def write_mem_map_addr_enum(self):
		"""
		Write addresses of registers within "memBlock" IP-XACT memory block as
		enum to generator output.
		"""
		cmnt = "{} memory map".format(self.memMap.name)
		self.headerGen.write_comment(cmnt, 0, small=True)
		decls = []

		for block in self.memMap.addressBlock:
			for reg in sorted(block.register, key=lambda a: a.addressOffset):
				decls.append(LanDeclaration(("CTUCANFD_" + reg.name).upper(),
											value=reg.addressOffset + block.baseAddress,
											intType="enum"))

		self.headerGen.create_enum(self.prefix.lower() + "_" + self.memMap.name.lower(),
								   decls)

	def write_reg_group(self, reg_group):
		# Write comment with memory word
		comment = ""
		for (j,reg) in enumerate(reg_group):
			comment = "{} {}".format(comment, reg.name.upper())
		comment += " register"
		if len(reg_group) > 0:
			comment += "s"
		self.headerGen.write_comment(comment, 0)

		# Choose name of first register as common name
		reg_base_name = ""
		for (j,reg) in enumerate(reg_group):
			# Append register name to the union name
			reg_base_name += reg.name.upper()
			break
		reg_base_name = "REG_{}".format(reg_base_name)

		# Go through each register and write fields
		for (j, reg) in enumerate(reg_group):
			#if j == 0:
				# Write address
				#self.headerGen.write_macro(reg_base_name, hex(reg.addressOffset).upper())

			for (i, field) in enumerate(sorted(reg.field, key=lambda a: a.bitOffset)):
				field_name = "{}_{}".format(reg_base_name, field.name)

				offset = field.bitOffset + (reg.addressOffset % 4) * 8
				# Single fields -> BIT(INDEX)
				# Multiple fields -> GEN_MASK(HIGH, LOW)
				field_val = None
				if field.bitWidth == 1:
					field_val = "BIT({})".format(offset)
				else:
					field_val = "GEN_MASK({}, {})".format(offset + field.bitWidth - 1, offset)


				self.headerGen.write_macro(field_name, field_val)

		self.headerGen.wr_nl()

	def write_memory_map(self):
		for block in self.memMap.addressBlock:

			# Skip memory blocks.
			if block.usage == "memory":
				continue

			self.headerGen.write_comment(block.name + " memory region", 0, small=False)
			self.headerGen.wr_nl()

			# Sort registers to groups by memory word.
			reg_groups = self.sort_regs_to_wrd_groups(block.register)
			for reg_group in reg_groups:
				self.write_reg_group(reg_group)

			return
	
	def create_addrMap_package(self, name):
		"""
		Create C header file package for "memMap" IP-XACT memory block.
		Package contains for each register within memory block:
			1. Define with register address offset.
			2. Defines for each register field.
		"""
		self.headerGen.wr_nl()
		self.headerGen.write_comment("This file is autogenerated, DO NOT EDIT!", 0, small=True)

		self.headerGen.wr_nl()
		self.headerGen.create_package((self.prefix + "_" + name).upper())
		self.headerGen.wr_nl()

		self.headerGen.write_include("linux/bits.h")
		self.headerGen.wr_nl()

		# Write memory map address enum
		if self.memMap:
			print("Writing addresses of '%s' register map" % self.memMap.name)
			self.write_mem_map_addr_enum()

		# Write memory map fields
		if self.memMap:
			print("Writing kernel header of '%s' register map" % self.memMap.name)
			self.write_memory_map()

		self.headerGen.commit_append_line(1)
