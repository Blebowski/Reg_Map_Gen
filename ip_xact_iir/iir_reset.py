"""
    Internal Intermediate representation of IP-XACT.
    IIR Reset - Reset object of a register

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

from .iir_reset_type import IirResetType
from .iir_object import IirObject
from .iir_reference_value import IirReferenceValue


class IirReset(IirObject):

    reset_reference_str: str
    reset_reference: IirResetType
    reset_value: IirReferenceValue
    reset_mask: IirReferenceValue

    def __init__(self, reset_value: IirReferenceValue,
                 reset_reference: IirResetType = None,
                 reset_mask: IirReferenceValue = None,
                 parent: IirObject = None):
        super().__init__(parent)
        self.reset_value = reset_value
        self.reset_mask = reset_mask
        self.reset_reference = reset_reference
        reset_value.parent = self
        reset_mask.parent = self

    def __init__(self, reset_value: IirReferenceValue,
                 reset_reference_str: str = None,
                 reset_mask: IirReferenceValue = None,
                 parent: IirObject = None):
        super().__init__(parent)
        self.reset_value = reset_value
        self.reset_mask = reset_mask
        self.reset_reference_str = reset_reference_str

        if self.reset_value:
            self.reset_value.parent = self

        if self.reset_mask:
            self.reset_mask.parent = self

    def __str__(self):
        return "IIR_RESET: {}".format(self.iir_id)
