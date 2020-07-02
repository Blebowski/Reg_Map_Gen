"""
    Internal Intermediate representation of IP-XACT.
    RTL representation - Module representation (Entity + Architecture (VHDL), Module (verilog))

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

from .rtl_named_object import RtlNamedObject
from .rtl_declaration import RtlDeclaration
from .rtl_generic_declaration import RtlGenericDeclaration
from .rtl_port_declaration import RtlPortDeclaration
from .rtl_concurent_statement import RtlConcurentStatement


class RtlModule(RtlNamedObject):

    architecture_name: str        # VHDL only

    generics: List[RtlGenericDeclaration]
    ports: List[RtlPortDeclaration]
    signals: List[RtlDeclaration]
    statements: List[RtlConcurentStatement]

    def __init__(self, name, architecture_name="rtl", generics: List[RtlGenericDeclaration] =
                 None, ports: List[RtlPortDeclaration] = None):
        self.name = name
        self.architecture_name = architecture_name

        self.generics = generics
        self.ports = ports
