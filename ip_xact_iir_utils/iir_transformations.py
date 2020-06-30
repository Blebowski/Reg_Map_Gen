"""
    Internal Intermediate representation of IP-XACT.
    IIR Reset type - Reset source

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

import os
import sys

proj_dir = os.path.abspath(os.path.join(__file__, ".."))
sys.path.append(proj_dir)

from ip_xact_iir import *


class IirTransformations:

    @staticmethod
    def convert_underscore_to_cammel_case(iir_object: IirObject, recurse=False):
        for attribute, value in iir_object.__dict__.items():

            # Skip reference values -> Not to screq UID
            if isinstance(iir_object, IirReferenceValue):
                continue

            # Recurse on other attributes
            if recurse and isinstance(iir_object, IirObject) and attribute != "parent" and :
                IirTransformations.convert_underscore_to_cammel_case(iir_object, True)

            # Convert Name
            if attribute == "name":
                value_split = value.lower().split("_")
                res = ""
                for it in value_split:
                    res += it.capitalize()
                value = value_split

            # TODO: We should walk through descriptions and replace exact match of the string by
            #       the value post conversion!