"""
    Internal Intermediate representation of IP-XACT.
    Basic for RTL declaration.

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

from .rtl_object import  RtlObject
from .rtl_named_object import RtlNamedObject
from .rtl_type import RtlType
from .rtl_enum_defs import *


class RtlDeclaration(RtlNamedObject):

    type: RtlType
    specifier: RtlDeclarationSpecifier
    value = RtlObject

    def __init__(self, name, type: RtlType, specifier=RtlDeclarationSpecifier.no_specifier,
                 value=None):
        super.__init__(name)
        self.name = name
        self.type = type
        self.specifier = specifier
        self.value = value



