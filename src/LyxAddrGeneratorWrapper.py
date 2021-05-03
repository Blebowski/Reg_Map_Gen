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
##   Class for generation of Lyx document from IP-XACT specification.
##   
##   In case of CAN FD Core the register map is specified with two register 
##   maps. 8-bit map with register fields described. 32 bit register maps with
##   name aliases used on 32 bit Avalon and AXI.
##
##	Revision history:
##		31.01.2018	Implemented the script
##      27.11.2018  Changed script to be a class
##
################################################################################

import argparse
import sys
import time
import importlib.util
import os
import inspect
import math
import yaml

from .gen_lib import *
from .ip_xact.lyx_addr_generator import LyxAddrGenerator


class LyxAddrGeneratorWrapper():

	# Path to a IP-XACT specification file with register maps
	xactSpec = ""

	# Name of the IP-XACT Memory map which should be used for VHDL package generatio.
	memMap = None

	# Size of the access bus word. Register bit field offsets are concatenated into 
	# word width size instead of simple offset from beginning of register. (E.g. 32 bit  ->
	# bitfields from first four 8-bit register are concatenated into 32 bit values)
	wordWidth = 32

	# Output where to write the VHDL package.
	outFile = ""

	# If memory map region overview should be generated
	genRegions = False

	# If field descriptions should be generated
	genFiDesc = False

	# Lyx template path
	lyxTemplate = ""

	# Path to configuration of generics
	configPath = None

	def do_update(self):

		args = parse_args()
		with open(self.xactSpec) as f:
			name = None
			offset = 0
			addrMap = None
			fieldMap = None

			component = Component()
			component.load(f)

			with open_output(self.outFile) as of:

				lyxGen = LyxAddrGenerator(component, self.memMap, self.wordWidth, 
											genRegions=self.genRegions,
											genFiDesc=self.genFiDesc)
				lyxGen.set_of(of)
				lyxGen.lyxGen.load_lyx_template(self.lyxTemplate)

				with open(self.configPath, 'rt') as f:
					lyxGen.config = yaml.safe_load(f)

					# Write the documentation
					lyxGen.write_mem_map_both()

					lyxGen.lyxGen.commit_append_lines_all()

					lyxGen.commit_to_file()

	if __name__ == '__main__':
		self.do_update()
