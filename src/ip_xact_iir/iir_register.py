"""
    Internal Intermediate representation of IP-XACT.
    IIR register - Class for memory register

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

from .iir_named_object import IirNamedObject
from .iir_object import IirObject
from .iir_reference_value import IirReferenceValue
from .iir_enum_defs import *
from .iir_register_field import IirRegisterField


class IirRegister(IirNamedObject):

    # Name, Display name and Description inherited from Named object

    # Register definition
    offset: IirReferenceValue
    size: IirReferenceValue
    dimension: IirReferenceValue
    is_present: IirReferenceValue
    volatile: IirVolatile
    access: IirAccess

    # Field summary
    fields: List[IirRegisterField]

    def __init__(self, name, offset: IirReferenceValue,
                 size: IirReferenceValue, fields: List[IirRegisterField],
                 description=None, display_name=None,
                 dimension: IirReferenceValue = None,
                 is_present: IirReferenceValue = None,
                 volatile: IirVolatile = None,
                 access: IirAccess = IirAccess.empty,
                 parent: IirObject = None):
        super().__init__(name, display_name, parent)
        self.offset = offset
        self.size = size
        self.fields = fields
        self.description = description
        self.display_name = display_name
        self.dimension = dimension
        self.is_present = is_present
        self.volatile = volatile
        self.access = access

        if self.fields:
            for field in fields:
                field.parent = self
        if self.offset:
            offset.parent = self
        if self.size:
            size.parent = self

        if self.dimension:
            self.dimension.parent = self
        if self.is_present:
            self.is_present.parent = self

    def __str__(self):
        return "IIR_REGISTER: {}".format(self.iir_id)