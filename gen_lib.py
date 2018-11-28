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
## Library with auxiliarly functions for pyXact generator.   
##
##	Revision history:
##		24.01.2018	First implementation based on the previous stand-alone
##                  script for generation of VHDL package
##
################################################################################

import argparse
import sys
import time
import importlib.util
import os
import inspect
import math

################################################################################
# File path to the local repo of the PyXact framework
################################################################################
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
PYXACT_PATH = "./pyXact_generator/ipyxact_parser"

sys.path.insert(0, PYXACT_PATH)
from ipyxact.ipyxact import Component
from license_updater import *


def open_output(output):
	return open(output, 'w')

def split_string(input, size):
	return [input[start:start+size] for start in range(0, len(input), size)]
	
def str_arg_to_bool(input):
	if (input == "yes" or
		input == "true" or
		input == "True" or
		input == "y"):
		return True
	else:
		return False

def checkIsList(obj):
	"""
	"""
	if (not (type(obj)) == list):
		print(str(obj) + " should be a list!")
		return false
	return True

def checkIsDict(obj):
	"""
	"""
	if (not (type(obj)) == dict):
		print(str(obj) + " should be dictionary!")
		return False
	return True

