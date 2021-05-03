"""
################################################################################
##
## Register map generation tool
##
## Copyright (C) 2021 Ondrej Ille <ondrej.ille@gmail.com>
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this SW component and associated documentation files (the "Component"),
## to deal in the Component without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Component, and to permit persons to whom the
## Component is furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Component.
##
## THE COMPONENT IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHTHOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE COMPONENT OR THE USE OR OTHER DEALINGS
## IN THE COMPONENT.
##
###############################################################################

###############################################################################
##
##   Unit test for CodeWriter class.
##
################################################################################
"""

from ..src.common.CodeWriter import CodeWriter

freakishly_long_comment = (
    "Permission is hereby granted, free of charge, to any person obtaining a copy of this SW " 
    "component and associated documentation files (the 'Component'), to deal in the Component "
    "without restriction, including without limitation the rights to use, copy, modify, merge, "
    "publish, distribute, sublicense, and/or sell copies of the Component, and to permit persons "
    "to whom the Component is furnished to do so, subject to the following conditions: "
)


def test_code_writer():
    cw = CodeWriter("example.c")

    # Test Small comment
    cw.write_comment("Example of small comment", small=True)
    cw.write_new_line()

    # Test Big comment
    cw.write_comment("Example of Big comment", small=False)
    cw.write_new_line()

    # Test wrapping to 80 characters
    cw.write_comment(freakishly_long_comment)
    cw.write_new_line()

    # Test comment with caption
    cw.write_comment("Very detailed description of this thing", "MY_FANCY_CAPTION")
    cw.write_new_line()

    # Test simple line
    cw.write_line("int a;")

    # Test indents
    cw.write_line("struct {")
    cw.push_item("}")
    cw.increase_indent()

    cw.write_line("union {")
    cw.push_item("}")
    cw.increase_indent()

    cw.write_line("uint32_t a;")
    cw.write_line("uint32_t b;")
    cw.write_line("uint32_t c;")

    cw.decrease_indent()
    cw.pop_item()

    cw.decrease_indent()
    cw.pop_item()

    del cw


if __name__ == "__main__":
    test_code_writer()