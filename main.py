#!/usr/bin/python3.6
"""
    Internal Intermediate representation of IP-XACT.
    Common IIR routines

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

from ip_xact_iir_utils import *


if __name__ == "__main__":

    parser = IpXactParser()
    hw_component = parser.parse_ip_xact(
        "../../spec/CTU/ip/CAN_FD_IP_Core/2.1/CAN_FD_IP_Core.2.1.xml")

    hw_component.print(True)