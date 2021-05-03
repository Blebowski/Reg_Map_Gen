"""
    Internal Intermediate representation of IP-XACT.
    IIR parameter - Parameter class

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
from .iir_enum_defs import *
from .iir_reference_value import IirReferenceValue


class IirParameter(IirNamedObject):

    # Name, Display name and Description inherited
    parameter_type: IirParameterType
    value: IirReferenceValue
    parameter_id: str

    # TODO: Other attributes are not represented since these are not used in generator now!
    #       Check Kactus2 or IP-XACT spec for description!

    def __init__(self, name, parameter_id, value: IirReferenceValue, description=None,
                 display_name=None, parameter_type: IirParameterType = IirParameterType.empty,
                 parent: IirObject = None):
        super().__init__(name, description, display_name, parent)
        self.value = value
        self.parameter_id = parameter_id
        self.parameter_type = parameter_type

        if self.value:
            self.value.parent = self

    def __str__(self):
        return "IIR_PARAMETER: {}".format(self.iir_id)