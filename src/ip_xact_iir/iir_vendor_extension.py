"""
    Internal Intermediate representation of IP-XACT.
    IIR object - Base class for all objects

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


class IirVendorExtension(IirObject):

    tag: str
    text: str
    attributes = None

    # Children can be arbitrary amount of levels of IIR_Object
    children: List[IirObject]

    def __init__(self, tag, text=None, attrributes=None):
        super().__init__()
        self.tag = tag
        self.text = text
        self.attributes = attrributes

    def __str__(self):
        return "IIR_VENDOR_EXTENSION: " + str(self.iir_id)