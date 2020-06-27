"""
    Internal Intermediate representation of IP-XACT.
    Common IIR object - Named object (Name, Display name, Description)

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


class IirNamedObject(IirObject):

    name: str
    display_name: str
    description: str

    def __init__(self, name, display_name=None, description=None, parent: IirObject = None):
        super().__init__(parent=parent)
        self.name = name
        self.display_name = display_name
        self.description = description

    def __str__(self):
        ret_val = "IIR_NAMED_OBJECT: {}".format(self.iir_id)
        return ret_val