"""
    Internal Intermediate representation of IP-XACT.
    IIR register - Class for memory map

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

# TODO: Memory re-map states not supported. Memory map directly contains address blocks without any
#       re-mapping capability

from typing import List

from .iir_object import IirObject
from .iir_named_object import IirNamedObject
from .iir_reference_value import IirReferenceValue
from .iir_address_block import IirAddressBlock


class IirMemoryMap(IirNamedObject):

    # Name, Display Name and Description inherited
    address_unit_bits: int
    is_present: IirReferenceValue

    address_blocks: List[IirAddressBlock]

    def __init__(self, name, display_name=None, description=None, address_unit_bits=None,
                 is_present: IirReferenceValue = None,
                 address_blocks: List[IirAddressBlock] = None,
                 parent: IirObject = None):
        super().__init__(name, display_name, description, parent)
        self.is_present = is_present
        self.address_blocks = address_blocks

        if address_blocks:
            for address_block in address_blocks:
                address_block.parent = self
        if is_present:
            self.is_present.parent = self

    def __str__(self):
        return "IIR_MEMORY_MAP: {}".format(self.iir_id)