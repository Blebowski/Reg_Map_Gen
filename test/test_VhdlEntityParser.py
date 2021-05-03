"""
###############################################################################
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
##   Unit test for VhdlEntityParserClass
##
################################################################################
"""
import os.path
import filecmp

from ..src.parsers.VhdlEntityParser import VhdlEntityParser


def test_vhdl_entity_parser():
    test_input = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              "test_inputs", "test_vhdl_entity_parser_input.vhd")

    # Parse the file
    psr = VhdlEntityParser()
    parsed_entity = psr.parse(test_input)
    del psr

    # Save the output
    test_output = open("test_vhdl_entity_parser", 'w')
    test_output.write(str(parsed_entity))

    # Compare with reference
    assert filecmp.cmp("test_vhdl_entity_parser",
                       os.path.join("test_outputs", "test_vhdl_entity_parser"))

    # Cleanup
    os.remove("test_vhdl_entity_parser")


if __name__ == "__main__":
    test_vhdl_entity_parser()

