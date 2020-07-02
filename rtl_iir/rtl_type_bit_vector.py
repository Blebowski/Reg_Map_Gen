"""
    Internal Intermediate representation of IP-XACT.
    RTL representation - Bit vector

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

from .rtl_type import RtlType
from enum import Enum


class RtlBitVectorDirection(Enum):
    none = 0
    downto = 1
    to = 2


class RtlTypeBitVector(RtlType):

    range_from: int
    range_to: int
    range_specified: bool

    direction: RtlBitVectorDirection

    def __init__(self, range_from=None, range_to=0):
        if range_from is None:
            self.range_specified = False
            self.direction = RtlBitVectorDirection.none
            return

        self.range_from = range_from
        self.range_to = range_to

        self.range_specified = True
        if range_from > range_to:
            self.direction = RtlBitVectorDirection.downto
        else
            self.direction = RtlBitVectorDirection.to

    def get_bit_width(self):
        return abs(self.range_from - self.range_to) + 1

