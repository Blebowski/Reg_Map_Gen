"""
    Internal Intermediate representation of IP-XACT.
    HW Component - single HW component as defined in IP-XACT and Kactus

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

from .iir_object import IirObject
from .iir_memory_map import IirMemoryMap
from .iir_top_object import IirTopObject
from .iir_reset_type import IirResetType
from .iir_named_object import IirNamedObject
from .iir_parameter import IirParameter
from .iir_vlnv import IirVlnv
from .iir_vendor_extension import IirVendorExtension


class IirHwComponent(IirTopObject, IirNamedObject):

    parameters: List[IirParameter]
    reset_types: List[IirResetType]
    memory_maps: List[IirMemoryMap]
    vendor_extensions: List[IirVendorExtension]

    def __init__(self, vlnv: IirVlnv, description=None, author=None, license=None,
                 xml_header=None, parent: IirObject = None):
        super().__init__(vlnv, author, license, parent)
        self.name = vlnv.name
        self.description = description

    def __str__(self):
        return "IIR_HW_COMPONENT: {}".format(self.iir_id)

    def set_memory_maps(self, memory_maps: List[IirMemoryMap]):
        self.memory_maps = memory_maps
        for memory_map in memory_maps:
            memory_map.parent = self

    def set_reset_types(self, reset_types: List[IirResetType]):
        self.reset_types = reset_types
        for reset_type in reset_types:
            reset_type.parent = self

    def set_parameters(self, parameters: List[IirParameter]):
        self.parameters = parameters
        for parameter in parameters:
            parameter.parent = self

    def set_vendor_extensions(self, vendor_extensions: List[IirVendorExtension]):
        self.vendor_extensions = vendor_extensions
        for vendor_extension in vendor_extensions:
            vendor_extension.parent = self





