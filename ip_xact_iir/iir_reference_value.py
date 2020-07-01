"""
    Internal Intermediate representation of IP-XACT.
    IIR Reset - Value of an object given directly or as reference to other
                object

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

from .iir_value import IirValue
from .iir_object import IirObject


class IirReferenceValue(IirValue):

    # UUID of parameter that this value refers to
    uuid: str = None

    # IIR object that parameter refers to
    reference_object: IirObject = None

    def __init__(self, uuid, value=None, reference_object: IirObject = None):
        super().__init__(value)
        self.uuid = uuid

        # If no value is specified, then set it to UUID. Thisway, if reference parameter is created
        # with hard-coded value (no reference), it will get propagated to value and uuid too. In
        # such case, uuid will be set to rubbish, this will be later cleared during link resolution.
        if value is None:
            self.value = uuid
        else:
            self.value = value
        self.reference_object = reference_object

    def __str__(self):
        return "IIR_REFERENCE_VALUE: {}".format(self.iir_id)