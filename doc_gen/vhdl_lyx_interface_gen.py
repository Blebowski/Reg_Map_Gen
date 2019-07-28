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
##   Generator of Lyx tables from VHDL entity interface.
##
##   Supports following VHDL entity declaration features:
##      1. Generics and Ports.
##      2. Comments per port/generic above the generic/port declaration.
##		3. Sections in ports/generics which are started by line solely of '-'
##         character.
##      4. Support for detection of std_logic_vector width.
##      5. Support for direction of port
##
##
##	  Note that VHDL entity declaration must have following format (apart from
##    comments):
##
##	  entity parsable_entity is
##		port(		-- '(' bracket must be on this line)
##			-- Signal comment
##			signal_one 	: IN std_logic;
##
##			-------------------------------------------------------------------
##			-- Section to which the second signal belongs
##			-------------------------------------------------------------------
##			-- Another signal comment
##			signal_two  : OUT std_logic_vector(1 downto 0)
##		);	-- port end bracket must be on this line !!
##
## 
##	Revision history:
##		17.03.2019	First implementation
##
################################################################################

import math

from abc import ABCMeta, abstractmethod
from enum import Enum

from pyXact_generator.languages.gen_lyx import LyxGenerator
from pyXact_generator.languages.declaration import LanDeclaration

from pyXact_generator.gen_lib import *

class VhdlEntityParserState(Enum):
	NONE = 1
	ENTITY = 2
	PORTS = 3
	GENERICS = 4
	SECTION = 5	
	FINISH = 6	


class VhdlLyxEntityGenerator():

	lyxGen = None
	template = None

	# Output file
	of = None
	vhdlFile = None

	# Regexes
	ent_re = None
	arc_re = None
	gen_re = None
	port_re = None
	sect_re = None
	end_port_gen_re = None
	end_ent_re = None

	# Parsed entity
	ent_interface = {"ports" : [], "generics" : []}

	# Comment stack
	cmnt_stack = ""

	parserState = VhdlEntityParserState.NONE
	lastState = VhdlEntityParserState.NONE

	def __init__(self):
		self.lyxGen = LyxGenerator()
		self.lyxGen.out = []
		self.parserState = VhdlEntityParserState.NONE
		self.lastState = VhdlEntityParserState.NONE
		self.cmnt_stack = ""
		self.ent_interface = {"ports" : [], "generics" : []}

	def set_of(self, of):
		"""
		"""
		self.of = of


	def set_vhdlFile(self, vhdlFile):
		"""
		"""
		self.vhdlFile = vhdlFile


	def cmnt_stack_push(self, line):
		"""
		"""
		self.cmnt_stack += line.strip("-").strip(" ")


	def commit_to_file(self):
		for line in self.lyxGen.out :
			self.of.write(line)

	def cmnt_stack_get(self):
		"""
		"""
		return self.cmnt_stack


	def cmnt_stack_flush(self):
		"""
		"""
		self.cmnt_stack = ""


	def parser_fsm_move(self, new_state, line):
		"""
		"""
		print("Moving to {}".format(new_state))
		self.lastState = self.parserState;
		self.parserState = new_state


	def parse_state_NONE(self, line):
		"""
		"""
		print(line)
		if (self.ent_re.match(line)):
			self.parser_fsm_move(VhdlEntityParserState.ENTITY, line)


	def parse_state_ENTITY(self, line):
		"""
		"""
		if (self.gen_re.match(line.lower())):
			self.parser_fsm_move(VhdlEntityParserState.GENERICS, line)

		elif (self.port_re.match(line.lower())):
			self.parser_fsm_move(VhdlEntityParserState.PORTS, line)

		# End of an entity
		elif (self.end_ent_re.match(line)):
			self.parser_fsm_move(VhdlEntityParserState.FINISH, line)


	def parse_port_gen_cmn(self, line):
		"""
		"""
		# Move to section processing if section starts
		if (self.sect_re.match(line)):
			self.parser_fsm_move(VhdlEntityParserState.SECTION, line)
			self.cmnt_stack_flush()			
			return True

		# Process simple comment -> Add to comment stack
		if (self.cmnt_re.match(line)):			
			self.cmnt_stack_push(line)
			return True

		# End of generic or port -> go back to ENTITY state
		if (self.end_port_gen_re.match(line)):
			self.parser_fsm_move(VhdlEntityParserState.ENTITY, line)
			return True

		return False


	def parse_state_GENERICS(self, line):
		"""
		"""	

		# Process common stuff for port and generic (comment, section, end)
		if (self.parse_port_gen_cmn(line)):
			return

		# Process the generic
		line_split = re.split(":", line)

		if (len(line_split) < 2):
			return

		# Remove possible 'constant' statement
		if (line_split[0].strip(" ").startswith("constant")):
			line_split[0] = line_split[0].lower().strip("constant")

		# Parse out name, type and default value
		gen_name = line_split[0].strip(" ")
		gen_type = re.split('[(:;]', line_split[1].strip(" "))[0]

		gen_def_val = ""
		if (len(line_split) > 2):
			gen_def_val = re.sub("[ =;]", '', line_split[2])

		print(gen_name)
		print(gen_type)
		print(gen_def_val)


		gen_entry = {"entry_type" : "generic", \
				     "name" : gen_name, \
				     "type" : gen_type, \
				     "comment" : self.cmnt_stack_get(), \
				     "def_val" : gen_def_val}

		print ("Adding generic entry: ", gen_entry)
		self.ent_interface["generics"].append(gen_entry)

		# Flush the comment stack since the comment till now belongs to generic
		self.cmnt_stack_flush()


	def parse_state_PORTS(self, line):
		"""
		"""
		# Process common stuff for port and generic (comment, section, end)
		if (self.parse_port_gen_cmn(line)):
			return

		# Process the port
		line_split = re.split(":", line)

		if (len(line_split) < 2):
			return

		# Remove possible state
		if (line_split[0].strip(" ").startswith("signal")):
			line_split[0] = line_split[0].lower().strip("signal")

		suffix = line_split[1].split(" ", 1)

		# Parse out name, direction, type
		port_name = line_split[0].strip(" ")
		port_dir = suffix[0];
		port_type = suffix[1].strip(" ").strip("\n").strip(";")
		port_type = re.sub("\(", " (", port_type)

		port_entry = {"entry_type" : "port", \
					  "name" : port_name, \
					  "type" : port_type, \
					  "comment" : self.cmnt_stack_get(), \
					  "direction" : port_dir}
		self.ent_interface["ports"].append(port_entry)
		print ("Adding port entry: ", port_entry)
		# Flush the comment stack since the comment till now belongs to generic
		self.cmnt_stack_flush()


		return


	def parse_state_SECTION(self, line):
		"""
		"""
		if (not line.startswith("-")):
			print("WARNING: Non-comment VHDL code in comment section! -> SKIPPING!")
			return

		# Finish section processing if section ends
		if (self.sect_re.match(line)):

			if (self.lastState == VhdlEntityParserState.PORTS):
				key = "ports"
			elif (self.lastState == VhdlEntityParserState.GENERICS):
				key = "generics"
			else:
				print("WARNING: Invalid parser FSM last State: ".format(),
						self.lastState)
				return

			# Add section entry
			sect_entry = {"entry_type" : "section", \
						  "comment" : self.cmnt_stack_get()}
			print ("Adding section entry: ", sect_entry)
			self.ent_interface[key].append(sect_entry)
			self.cmnt_stack_flush()
			self.parser_fsm_move(self.lastState, line)
			return

		# Process simple comment -> Add to comment stack
		if (self.cmnt_re.match(line)):
			self.cmnt_stack_push(line)
			return

		return


	def process_section_entry_row(self, table, row_ind, val):
		for x in range(0, 4):
			self.lyxGen.set_cell_object(table, row_ind, x, val)
			self.lyxGen.set_cell_color(table, row_ind, x, "gray")

		self.lyxGen.merge_common_fields(table, [row_ind], endCol=4);
		

	def gen_generics_lyx_table(self):
		"""
		"""		
		height = len(self.ent_interface["generics"]) + 1
		width = 4 # Name, type, default value, description

		table = self.lyxGen.build_table(width, height, defCellText="")

		# Set widths of table to avoid text overflow
		self.lyxGen.set_column_option(table, 0, "width", "4cm")
		self.lyxGen.set_column_option(table, 1, "width", "3.5cm")
		self.lyxGen.set_column_option(table, 2, "width", "1.2cm")
		self.lyxGen.set_column_option(table, 3, "width", "7cm")

		# Title row
		self.lyxGen.set_cell_object(table, 0, 0, "Name")
		self.lyxGen.set_cell_object(table, 0, 1, "Type")
		self.lyxGen.set_cell_object(table, 0, 2, "Default value")
		self.lyxGen.set_cell_object(table, 0, 3, "Description")

		self.lyxGen.set_cells_color(table, [[0,0],[0,1],[0,2],[0,3]], "cyan")

		# Generic rows
		for y,gen in enumerate(self.ent_interface["generics"]):
			if (gen["entry_type"] == "section"):
				self.process_section_entry_row(table, y + 1, gen["comment"])
			else:
				self.lyxGen.set_cell_object(table, y + 1, 0, gen["name"])
				self.lyxGen.set_cell_object(table, y + 1, 1, gen["type"])
				self.lyxGen.set_cell_object(table, y + 1, 2, gen["def_val"])
				self.lyxGen.set_cell_object(table, y + 1, 3, gen["comment"])


		self.lyxGen.insert_table(table)


	def gen_ports_lyx_table(self):
		"""
		"""
		height = len(self.ent_interface["ports"]) + 1
		width = 4 # Name, direction, type, description

		table = self.lyxGen.build_table(width, height, defCellText="")

		# Set widths of table to avoid text overflow
		self.lyxGen.set_column_option(table, 0, "width", "4cm")
		self.lyxGen.set_column_option(table, 1, "width", "1.2cm")
		self.lyxGen.set_column_option(table, 2, "width", "3.5cm")
		self.lyxGen.set_column_option(table, 3, "width", "7cm")

		# Title row
		self.lyxGen.set_cell_object(table, 0, 0, "Name")
		self.lyxGen.set_cell_object(table, 0, 1, "Direction")
		self.lyxGen.set_cell_object(table, 0, 2, "Type")
		self.lyxGen.set_cell_object(table, 0, 3, "Description")

		self.lyxGen.set_cells_color(table, [[0,0],[0,1],[0,2],[0,3]], "cyan")

		# Port rows
		for y,port in enumerate(self.ent_interface["ports"]):

			if (port["entry_type"] == "section"):
				self.process_section_entry_row(table, y + 1, port["comment"])
			else:
				self.lyxGen.set_cell_object(table, y + 1, 0, port["name"])
				self.lyxGen.set_cell_object(table, y + 1, 1, port["direction"])
				port_type = self.lyxGen.insert_new_line_inset_at_char(port["type"], '(')
				self.lyxGen.set_cell_object(table, y + 1, 2, port_type)
				self.lyxGen.set_cell_object(table, y + 1, 3, port["comment"])

		self.lyxGen.insert_table(table)


	def gen_lyx_tables(self):
		"""
		"""
		if (len(self.ent_interface["generics"]) > 0):		
			self.lyxGen.write_layout_text("Description", "Generics")
			self.gen_generics_lyx_table()

		if (len(self.ent_interface["ports"]) > 0):
			self.lyxGen.write_layout_text("Description", "Ports")
			self.gen_ports_lyx_table()


	def generate_lyx_table_from_vhdl_entity(self):
		"""
		"""
		self.parserState = VhdlEntityParserState.NONE

		# Add regexes to recognize start of entity and architecture
		self.ent_re = re.compile("^[ ]*entity[ ]*[\w]+[ ]*is[ ]*$")
		self.arc_re = re.compile("^[ ]*architecture[ ]+[\w]+[ ]+of[ ]+[\w]+[ ]+is[ ]*$")
		self.port_re = re.compile("^[ ]*port[ ]*[(][ ]*$")
		self.gen_re = re.compile("^[ ]*generic[ ]*[(][ ]*$")
		self.cmnt_re = re.compile("^[ ]*--.*$")
		self.sect_re = re.compile("^[ ]*[-]{4,}.*$")
		self.end_port_gen_re = re.compile("^[ ]*\);[ ]*$")
		self.end_ent_re = re.compile("^[ ]*end[ ]+entity[ ]*;[ ]*$")

		# Prepare parser state machine
		parser_fsm = {VhdlEntityParserState.NONE : self.parse_state_NONE,
					  VhdlEntityParserState.ENTITY : self.parse_state_ENTITY,
					  VhdlEntityParserState.GENERICS : self.parse_state_GENERICS,
					  VhdlEntityParserState.PORTS : self.parse_state_PORTS,
					  VhdlEntityParserState.SECTION : self.parse_state_SECTION}

		lines = self.vhdlFile.readlines()
		for i,line in enumerate(lines):

			#if (self.parserState != VhdlEntityParserState.NONE):
				#print("Processing line : {}".format(line))
		
			line = line.strip(" ").strip("\n")
			
			# Find state we are in and execute appropriate callback
			for state, callback in parser_fsm.items():
				if (state == self.parserState):
					callback(line)
					break;

			if (self.parserState == VhdlEntityParserState.FINISH):
				break;

		# Generate Lyx Tables for generics and ports
		self.gen_lyx_tables()

