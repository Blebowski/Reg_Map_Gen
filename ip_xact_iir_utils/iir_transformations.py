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

from enum import Enum

proj_dir = os.path.abspath(os.path.join(__file__, ".."))
sys.path.append(proj_dir)

from ip_xact_iir import *


class IirTransformations(Enum):

    underscore_to_camel_case = 0
    camel_case_to_underscore = 1

    @staticmethod
    def __underscore_to_camel(input) -> str:
        in_split = str(input).split("_")
        res = ""
        for val in in_split:
            res += val.capitalize()
        return res

    @staticmethod
    def __camel_to_underscore(input) -> str:
        res = ""
        for character in str(input):
            if character.isUpper() and character != str(input)[0]:
                res += "_{}".format(character)
            else:
                res += character
        return res.lower()

    @staticmethod
    def __convert_descriptions(iir_object: IirObject, original: str, replacement: str) -> str:
        for attribute, value in iir_object.__dict__.items():

            # Skip reference values, parent
            if isinstance(value, IirReferenceValue) or attribute == "parent":
                continue

            # Recurse on other IIrObjects
            if isinstance(value, IirObject):
                IirTransformations.__convert_descriptions(value, original, replacement)

            # Go through lists and recurse on Iir Objects
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, IirObject):
                        IirTransformations.__convert_descriptions(item, original, replacement)

            # Replace text in description attribute. Ignore if there is no white space before.
            # Does not replace when name is suffix of other name. Does replace if separated by
            # white space, dot or bracket. This allows to have [] bitfield addressing
            if (attribute == "description") and (value is not None):
                if (str(" " + original + " ") in value) or \
                   (str(" " + original + "[") in value) or \
                   (str(" " + original + "(") in value) or \
                   (str(" " + original + ".") in value) or \
                   (str(" " + original + "{") in value):
                    iir_object.__setattr__(attribute, value.replace(original, replacement))

    @staticmethod
    def transform(iir_object: IirObject, iir_top_object: IirObject, transformation,
                  attribute_name, iir_type_to_convert=IirObject, iir_convert_description: bool =
                  False):
        for attribute, value in iir_object.__dict__.items():

            # Skip reference values -> Not to screw UID
            if isinstance(value, IirReferenceValue) or attribute == "parent":
                continue

            # Recurse on other IirObjects
            if isinstance(value, IirObject):
                IirTransformations.transform(value, iir_top_object, transformation,
                                             attribute_name, iir_type_to_convert,
                                             iir_convert_description)

            # Go through lists and recurse on Iir Objects
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, IirObject):
                        IirTransformations.transform(item, iir_top_object, transformation,
                                                     attribute_name, iir_type_to_convert,
                                                     iir_convert_description)

            # Check if object is of desired type (by default it is IIrObject)
            if not isinstance(iir_object, iir_type_to_convert):
                continue

            # Transform if it is attribute we were looking for and fix descriptions in whole tree
            if attribute == attribute_name:

                if transformation == IirTransformations.underscore_to_camel_case:
                    new_value = IirTransformations.__underscore_to_camel(value)
                elif transformation == IirTransformations.camel_case_to_underscore:
                    new_value = IirTransformations.__camel_to_underscore(value)
                else:
                    print("ERROR: Invalid transformation type: {}".format(transformation))
                    break

                if iir_convert_description:
                    IirTransformations.__convert_descriptions(iir_top_object, value, new_value)
                iir_object.__setattr__(attribute, new_value)
