"""
    Internal Intermediate representation of IP-XACT.
    Enumerated value of register field.

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

from .iir_object import IirObject
from .iir_named_object import IirNamedObject
from .iir_value import IirValue
from .iir_enum_defs import *


class IirEnumeratedValue(IirNamedObject):

    enumeration_name: str
    value: IirValue
    usage: IirEnumeratedValueUsage

    def __init__(self, enumeration_name,
                 value: IirValue,
                 display_name=None,
                 usage: IirEnumeratedValueUsage = IirEnumeratedValueUsage.empty,
                 description=None,
                 parent: IirObject = None):
        super().__init__(enumeration_name, display_name, description, parent)
        self.enumeration_name = enumeration_name
        self.value = value
        self.usage = usage
        if value:
            value.parent = self

    def __str__(self):
        return "IIR_ENUMERATED_VALUE: {}".format(self.iir_id)
