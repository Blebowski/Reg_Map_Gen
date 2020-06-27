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

from .iir_common import iir_generate_id


class IirObject:

    iir_id: int
    parent = None

    def __init__(self, iir_id=None, parent=None):
        if not iir_id:
            self.iir_id = iir_generate_id()
        else:
            self.iir_id = iir_id
        if parent:
            self.parent = parent

    def __str__(self):
        return "IIR_OBJECT: " + str(self.iir_id)

    def print(self, nest=True, indent=0, file=None):
        print(" " * indent + str(self))
        indent += 2
        ind_str = " " * indent

        for attribute, value in self.__dict__.items():
            # Skip IIR_ID, undefined or parent
            if (attribute == "iir_id") or (value is None) or (attribute == "parent"):
                continue

            attr = self.__getattribute__(attribute)

            # Nested objects
            if isinstance(attr, IirObject):
                if nest:
                    print(ind_str + attribute.capitalize() + ":")
                    attr.print(nest, indent + 2, file)
                else:
                    print("{}{}: {}".format(ind_str, attribute.capitalize(), value))
                continue

            # Lists of objects
            if isinstance(attr, list):
                print("{}{}: Entries: {}".format(ind_str, attribute.capitalize(), len(attr)))
                if nest:
                    indent += 2
                    ind_str = " " * indent
                    for list_item in attr:
                        if isinstance(list_item, IirObject):
                            list_item.print(nest, indent)
                        else:
                            print("{}{}: {}".format(ind_str, str(list_item).capitalize(), value))
                    indent -= 2
                    ind_str = " " * indent
                continue

            print("{}{}: {}".format(ind_str, attribute.capitalize(), value))
