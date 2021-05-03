"""
    Internal Intermediate representation of IP-XACT.
    IIR Register field - Single field of register

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

from .iir_named_object import IirNamedObject
from .iir_object import IirObject
from .iir_enum_defs import *
from .iir_reference_value import IirReferenceValue, IirValue
from .iir_reset import IirReset
from .iir_enumerated_value import IirEnumeratedValue


class IirRegisterField(IirNamedObject):

    # Name, Description and Display name inherited from named object

    # Field constraints
    volatile: IirVolatile
    access: IirAccess
    modify_write_value: IirModifiedWriteValue
    read_action: IirReadAction
    testable: IirTestable
    test_constraint: IirTestConstraint
    write_value_constraint: IirWriteValueConstraint
    write_constraint_minimum: IirReferenceValue
    write_constraint_maximum: IirReferenceValue

    resets: List[IirReset]

    # Field definition
    offset: IirReferenceValue
    width: IirReferenceValue
    is_present: IirReferenceValue
    reserved: IirReferenceValue
    field_id: IirValue

    enumerated_values: List[IirEnumeratedValue]

    def __init__(self, name, offset: IirReferenceValue, width: IirReferenceValue,
                 display_name=None, description=None, volatile: IirVolatile = IirVolatile.empty,
                 access: IirAccess = IirAccess.empty,
                 modify_write_value: IirModifiedWriteValue = IirModifiedWriteValue.empty,
                 read_action: IirReadAction = IirReadAction.empty,
                 testable: IirTestable = IirTestable.empty,
                 test_constraint: IirTestConstraint = IirTestConstraint.empty,
                 write_value_constraint: IirWriteValueConstraint =
                 IirWriteValueConstraint.no_constraints,
                 write_constraint_minimum: IirReferenceValue = None,
                 write_constraint_maximum: IirReferenceValue = None,
                 resets: List[IirReset] = None,
                 is_present: IirReferenceValue = None,
                 reserved: IirReferenceValue = None,
                 field_id: IirValue = None,
                 enumerated_values: List[IirEnumeratedValue] = None,
                 parent: IirObject = None):
        super().__init__(name, display_name, description, parent)

        self.offset = offset
        self.width = width
        self.volatile = volatile
        self.acces = access
        self.modify_write_value = modify_write_value
        self.read_action = read_action
        self.testable = testable
        self.test_constraint = test_constraint
        self.write_value_constraint = write_value_constraint
        self.write_constraint_minimum = write_constraint_minimum
        self.write_constraint_maximum = write_constraint_maximum
        self.resets = resets
        self.is_present = is_present
        self.reserved = reserved
        self.field_id = field_id
        self.enumerated_values = enumerated_values

        if resets:
            for reset in resets:
                reset.parent = self
        if enumerated_values:
            for enumerated_value in enumerated_values:
                enumerated_value.parent = self

        if self.offset:
            self.offset.parent = self

        if self.width:
            self.width.parent = self

        if write_constraint_minimum:
            write_constraint_minimum.parent = self
        if write_constraint_maximum:
            write_constraint_maximum.parent = self
        if is_present:
            is_present.parent = self
        if reserved:
            reserved.parent = self
        if field_id:
            field_id.parent = self

    def __str__(self):
        return "IIR_REGISTER_FIELD: {}".format(self.iir_id)