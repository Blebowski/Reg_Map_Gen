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
##   Class for generation of Lyx tables from VHDL entity interfaces!
##   
##	Revision history:
##      17.3.2019  First implementation
##
################################################################################

import argparse
import sys
import time
import importlib.util
import os
import inspect
import math

from .gen_lib import *
from .doc_gen.vhdl_lyx_interface_gen import VhdlLyxEntityGenerator


class VhdlLyxEntityGeneratorWrapper():

	# Output where to write the VHDL package.
	config = None

	# Lyx template path
	lyxTemplate = ""

	# Lyx generator
	gen = None

	def set_config(self, config):
		self.config = config


	def do_update(self):
		"""
		"""

		if (not "source_list" in self.config):
			print("Source list for conversion is not defined")
			return

		if (not "template" in self.config):
			print("Lyx template for conversion is not defined")
			return

		self.lyxTemplate = self.config["template"]

		#print(self.config)
		#print(self.config["source_list"].items())

		for (name, cfg) in self.config["source_list"].items():

			print("*" * 80)
			print("Processing {} entity".format(name))
			print("*" * 80)

			self.gen = VhdlLyxEntityGenerator()

			out_f = open(cfg["lyx_output"], 'w') 
			self.gen.set_of(out_f)

			self.gen.lyxGen.load_lyx_template(self.lyxTemplate)

			in_f = open(cfg["vhdl_file"], 'r')
			self.gen.set_vhdlFile(in_f)

			self.gen.generate_lyx_table_from_vhdl_entity()

			self.gen.lyxGen.commit_append_lines_all()
			self.gen.commit_to_file()

			out_f.close()
			in_f.close()

	if __name__ == '__main__':
		self.do_update()
