"""
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
##   Class for component declaration and instantantion in VHDL.
##
##	Revision history:
##		06.10.2018	First implementation
##
################################################################################
"""


class VhdlCompDeclaration(LanDeclaration):
    # VHDL component declaration inherits following attributes from
    # LanDeclaration:
    #   type = name of the entity, architecture or component 
    #   value = name of instance in case of component instatiation.
    #   comment = VHDL comment before the component instantiation
    #   intType = "component", "entity" or "architecture"

    # When true, component instance will be created, When false component 
    # declaration will be created.
    instance = True

    # List of "LanDeclarations" with signals which are ports of entity or
    # component. For architecture it contains list of internal signals.
    ports = None

    # List of "LanDeclarations" with constants which are generics of entity.
    generics = None

    def __init__(self, name, value, type=None, bitWidth=None, specifier=None,
                 alignLen=50, gap=0, bitIndex=None, intType=None, comment=None):
        self.name = name
        self.value = value
        self.alignLen = alignLen
        self.gap = gap

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
