"""
    Internal Intermediate representation of IP-XACT.
    IIR register - Class for address block

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this SW component and associated documentation files (the "Component"),
    to deal in the Component without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Component, and to permit persons to whom the
    Component is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Component.

    THE COMPONENT IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHTHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE COMPONENT OR THE USE OR OTHER
    DEALINGS IN THE COMPONENT.
"""

from typing import List

from .iir_enum_defs import *
from .iir_object import IirObject
from .iir_named_object import IirNamedObject
from .iir_reference_value import IirReferenceValue
from .iir_register import IirRegister


class IirAddressBlock(IirNamedObject):

    # Name, display name and description inherited

    # Address block definition
    base_address: IirReferenceValue
    block_range: IirReferenceValue
    width: IirReferenceValue
    is_present: IirReferenceValue
    usage: IirAddressBlockUsage
    access: IirAccess
    volatile: IirVolatile

    registers: List[IirRegister]

    # TODO: Register files summary not supported -> No use case for now!

    def __init__(self, name, base_address: IirReferenceValue,
                 block_range: IirReferenceValue,
                 width: IirReferenceValue,
                 display_name=None,
                 description=None,
                 is_present: IirReferenceValue = None,
                 usage: IirAddressBlockUsage = IirAddressBlockUsage.empty,
                 access: IirAccess = IirAccess.empty,
                 volatile: IirVolatile = IirVolatile.empty,
                 registers: List[IirRegister] = None,
                 parent: IirObject = None):
        super().__init__(name, display_name, description, parent)
        self.base_address = base_address
        self.block_range = block_range
        self.width = width
        self.is_present = is_present
        self.usage = usage
        self.access = access
        self.volatile = volatile
        self.registers = registers
        self.parent = parent

        if registers:
            for register in registers:
                register.parent = self

        if self.block_range:
            self.block_range.parent = self
        if self.width:
            self.width.parent = self
        if is_present:
            self.is_present.parent = self
        if usage:
            self.usage.parent = self
        if access:
            self.access.parent = self
        if volatile:
            self.volatile.parent = self

    def __str__(self):
        return "IIR_ADDRESS_BLOCK: {}".format(self.iir_id)