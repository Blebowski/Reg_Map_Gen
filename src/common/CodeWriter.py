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
##   Base class for writers. Implements common operations for code generation.
##
################################################################################
"""

class CodeWriter:

    # File object in which code is generated
    __output_file = None

    # Character used as comment
    comment_char = None

    # Stack for posting generated code.
    # E.g. when we start writing struct definition we do
    #   Write following:
    #       struct {
    #
    #   Push following on stack:
    #       };
    # First item in the list is first item of the stack
    __code_stack = []

    # If false, Tabs are used
    use_spaces = None

    # Indent size
    base_indent = None

    # Current indent
    curr_indent = None

    # Maximal length of line (used for comments and alignment, generated lines are not split)
    max_line_length = None

    def __split_line(self, line):
        """
        Splits line into multiple lines by words. Each split line has max_line_length length
        :param line: Line to split
        """
        ret_val = []
        words = line.split(" ")
        curr_line = ""
        for word in words:
            # Takes into account character delimiter and space
            if len(curr_line) + len(word) < self.max_line_length - 3:
                curr_line += word + " "
            else:
                ret_val.append(curr_line)
                curr_line = word + " "

        ret_val.append(curr_line)
        print(ret_val)
        return ret_val

    def __generate_indent(self):
        if self.use_spaces:
            indent_char = " "
        else:
            indent_char = "\t"
        return indent_char * self.curr_indent

    def write_line(self, line):
        """
        Writes one line of code to __output_file
        :param line: Line to write
        """
        self.__output_file.write("{}{}\n".format(self.__generate_indent(), str(line)))

    def write_new_line(self):
        """
        Writes new line to __output_file
        """
        self.__output_file.write('\n')

    def push_item(self, item):
        """
        Pushes item on stack for later generation
        :param item: Item to be pushed on the stack
        """
        self.__code_stack.append(item)

    def pop_item(self, count=1):
        """
        Pops top-most items from generation stack and write to __output_file
        :param count: Number of items to pop
        """
        for i in range(0, min(count, len(self.__code_stack))):
            self.write_line(self.__code_stack.pop(0))

    def pop_all_items(self):
        """
        Pops all items from generation stack and write to __output_file
        """
        for i in range(0, len(self.__code_stack)):
            self.write_line(self.__code_stack.pop(0))

    def increase_indent(self, increment_by: int = -1):
        """
        Increases indent of generated code
        :param increment_by:Number of spaces/tabs to increase indent by
        """
        if increment_by == -1:
            increment_by = self.base_indent
        self.curr_indent += increment_by

    def decrease_indent(self, decrement_by: int = -1):
        """
        Decreases indent of generated code
        :param decrement_by: Number of spaces/tabs to decrease indent by
        """
        if decrement_by == -1:
            decrement_by = self.base_indent
        self.curr_indent -= decrement_by
        if self.curr_indent < 0:
            self.curr_indent = 0

    def write_comment_line(self):
        """
        Writes line full of comment characters to __output_file
        """
        self.write_line(self.comment_char * (self.max_line_length - self.curr_indent))

    def write_comment(self, comment, caption=None, small=False, wrap=True):
        """
        Writes comment to __output_file
        :param comment: Comment to write
        :param caption: Caption of the comment
        :param small: True - Single line comment
                      False - Multi-line comment surrounded by whole line of comment characters.
        :param wrap: True - Wrap comment if it is longer than max_line_length, split by spaces
                     False - Write as is (no wrapping)
        """
        if not small:
            self.write_comment_line()

        if caption:
            self.write_line(self.comment_char * 2 + " " + caption)
            self.write_line(self.comment_char * 2)

        if wrap:
            lines = self.__split_line(comment)
            for line in lines:
                self.write_line(self.comment_char * 2 + " " + line)
        else:
            self.write_line(self.comment_char * 2 + comment)

        if not small:
            self.write_comment_line()

    def __init__(self, path, indent=2, comment_char='/', max_line_length=80, use_spaces=True):
        self.__output_file = open(path, 'w')
        self.comment_char = comment_char
        self.base_indent = indent
        self.max_line_length = max_line_length
        self.use_spaces = use_spaces
        self.curr_indent = 0

    def __del__(self):
        self.__output_file.close()
