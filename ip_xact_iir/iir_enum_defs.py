"""
    Internal Intermediate representation of IP-XACT.
    Common enum definitions

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

from enum import Enum


class IirEnumeratedValueUsage(Enum):
    empty = 0
    read = 1
    write = 2
    read_write = 3

    @staticmethod
    def from_str(in_str: str):
        if in_str.lower() == "read":
            return IirEnumeratedValueUsage.read
        if in_str.lower() == "write":
            return IirEnumeratedValueUsage.write
        if in_str.lower() == "read-write":
            return  IirEnumeratedValueUsage.read_write
        return  IirEnumeratedValueUsage.empty


class IirAccess(Enum):
    empty = 0,
    read_write = 1,
    read_only = 2,
    write_only = 3,
    read_write_once = 4,
    write_once = 5

    def is_readable(self) -> bool:
        if (self.value == IirAccess.read_write or
            self.value == IirAccess.read_only or
            self.value == IirAccess.read_write_once):
            return True
        return False

    def is_writable(self) -> bool:
        if (self.read_write == IirAccess.read_write or
            self.write_only == IirAccess.write_only or
            self.write_once == IirAccess.write_once):
            return True
        return False

    def is_set(self) -> bool:
        if self.value == IirAccess.empty:
            return False
        return True

    @staticmethod
    def from_str(in_str: str):
        if in_str.lower() == "read-write":
            return IirAccess.read_write
        if in_str.lower() == "read-only":
            return IirAccess.read_only
        if in_str.lower() == "write-only":
            return IirAccess.write_only
        if in_str.lower() == "read-writeonce":
            return IirAccess.read_write_once
        if in_str.lower() == "writeonce":
            return IirAccess.write_once
        return IirAccess.empty


class IirModifiedWriteValue(Enum):
    empty = 0,      # Default: Object is written as is
    one_to_clear = 1,
    one_to_set = 2,
    one_to_toggle = 3,
    zero_to_clear = 4,
    zero_to_set = 5,
    zero_to_toggle = 6,
    clear = 7,
    set = 8,
    modify = 9

    def has_side_effect(self) -> bool:
        if self.value == IirModifiedWriteValue.empty:
            return False
        return True

    @staticmethod
    def from_str(in_str: str):
        if in_str.lower() == "onetoclear":
            return IirModifiedWriteValue.one_to_clear
        if in_str.lower() == "onetoset":
            return IirModifiedWriteValue.one_to_set
        if in_str.lower() == "onetotoggle":
            return IirModifiedWriteValue.one_to_toggle
        if in_str.lower() == "zerotoclear":
            return IirModifiedWriteValue.zero_to_clear
        if in_str.lower() == "zerotoset":
            return IirModifiedWriteValue.zero_to_set
        if in_str.lower() == "zerototoggle":
            return IirModifiedWriteValue.zero_to_toggle
        if in_str.lower() == "clear":
            return IirModifiedWriteValue.clear
        if in_str.lower() == "set":
            return IirModifiedWriteValue.set
        if in_str.lower() == "modify":
            return IirModifiedWriteValue.modify
        return IirModifiedWriteValue.empty


class IirReadAction(Enum):
    empty = 0,      # Default: No side effect
    clear = 1,
    set = 2,
    modify = 3

    def has_side_effect(self) -> bool:
        if self.value == IirReadAction.empty:
            return False
        return True

    @staticmethod
    def from_str(in_str: str):
        if in_str.lower() == "clear":
            return IirReadAction.clear
        if in_str.lower() == "set":
            return IirReadAction.set
        if in_str.lower() == "modify":
            return IirReadAction.modify
        return IirReadAction.empty


class IirTestConstraint(Enum):
    empty = 0,      # Default: No constraint
    unconstrained = 1,
    restore = 2,
    write_as_read = 3,
    read_only = 4

    def has_constraint(self) -> bool:
        if (self.value == IirTestConstraint.empty or
            self.value == IirTestConstraint.unconstrained):
            return False
        return True

    @staticmethod
    def from_str(in_str: str):
        if in_str.lower() == "unconstrained":
            return IirTestConstraint.unconstrained
        if in_str.lower() == "restore":
            return IirTestConstraint.restore
        if in_str.lower() == "writeasread":
            return IirTestConstraint.write_as_read
        if in_str.lower() == "readonly":
            return IirTestConstraint.read_only
        return IirTestConstraint.empty


class IirWriteValueConstraint(Enum):
    no_constraints = 0,
    write_as_read = 1,
    use_enumerated_values = 2,
    set_minimum_and_maximum_limits = 3

    def has_constraints(self) -> bool:
        if self.value == IirWriteValueConstraint.no_constraints:
            return True
        return False

    @staticmethod
    def from_str(in_str: str):
        if in_str.lower() == "writeasread":
            return IirWriteValueConstraint.write_as_read
        if in_str.lower() == "useenumeratedvalues":
            return IirWriteValueConstraint.use_enumerated_values
        if in_str.lower() == "setminimumandmaximumlimits":
            return IirWriteValueConstraint.set_minimum_and_maximum_limits
        return IirWriteValueConstraint.no_constraints


class IirVolatile(Enum):
    empty = 0,
    true = 1,
    false = 2

    @staticmethod
    def from_str(in_str: str):
        if in_str.lower() == "true":
            return IirVolatile.true
        if in_str.lower() == "false":
            return IirVolatile.false
        return IirVolatile.empty


class IirTestable(Enum):
    empty = 0,
    true = 1
    false = 2


class IirAddressBlockUsage(Enum):
    empty = 0,
    register = 1,
    memory = 2,
    reserved = 3

    @staticmethod
    def from_str(input_str: str):
        if input_str.lower() == "register":
            return IirAddressBlockUsage.register
        if input_str.lower() == "memory":
            return IirAddressBlockUsage.memory
        if input_str.lower() == "reserved":
            return IirAddressBlockUsage.reserved
        return IirAddressBlockUsage.empty


class IirParameterType(Enum):
    empty = 0,
    bit = 1,
    byte = 2,
    short_int = 3,
    int = 4,
    long_int = 5,
    short_real = 6,
    real = 7,
    string = 8

    @staticmethod
    def from_str(in_str: str):
        if in_str == "bit":
            return IirParameterType.bit
        if in_str == "byte":
            return IirParameterType.byte
        if in_str == "shortInt":
            return IirParameterType.short_int
        if in_str == "int":
            return IirParameterType.int
        if in_str == "longInt":
            return IirParameterType.long_int
        if in_str == "shortReal":
            return IirParameterType.short_real
        if in_str == "real":
            return IirParameterType.real
        if in_str == "string":
            return IirParameterType.string
