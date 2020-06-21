"""
################################################################################
##
## Register map generation tool
##
## Copyright (C) 2018 Ondrej Ille <ondrej.ille@gmail.com>
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
##   Address map generator to Lyx document from IP-XACT parsed memory map
##	 with pyXact framework.
## 
##	Revision history:
##		25.01.2018	First implementation
##
################################################################################
"""

import math

from pyXact_generator.ip_xact.addr_generator import IpXactAddrGenerator
from pyXact_generator.languages.gen_lyx import LyxGenerator
from pyXact_generator.gen_lib import *


def reg_append_short_enums(field):
    """
    Create line with enums for given register field. Enum name and description
    are addedd to each line.
    """
    append_text = ""
    if not field.enumeratedValues:
        return append_text

    if len(field.enumeratedValues[0].enumeratedValue) > 0:
        for es in field.enumeratedValues:
            for (i, e) in enumerate(sorted(es.enumeratedValue, key=lambda x: x.value)):
                append_text += "\\begin_inset Newline newline\\end_inset\n"
                bin_size = "{:0" + "{}".format(field.bitWidth) + "b}"
                bin_fmt = bin_size.format(e.value)
                append_text += "		0b{}  - {} - {}".format(bin_fmt, e.name,
                                                                e.description)

    return append_text


def get_bit(val, bitIndex):
    """
    """
    tmp = "{0:032b}".format(val)
    return tmp[31 - bitIndex]


def reg_unwrap_fields(reg):
    """
    """
    ret_val = [[], [], [], []]

    for i in range(0, int(reg.size / 8)):
        for j in range(0, 8):
            ret_val[i].append([])

            # Check if such a field exists
            field_exist = False
            for field in sorted(reg.field, key=lambda a: a.bitOffset):
                tmp = (7 - j) + i * 8
                if field.bitOffset <= tmp < field.bitOffset + field.bitWidth:
                    field_exist = True
                    break

            # Insert the field or reserved field
            if field_exist:
                field_name = field.name
                if (field.resets is not None) and (field.resets.reset is not None):
                    field_rst = get_bit(field.resets.reset.value,
                                        tmp - field.bitOffset)
                else:
                    field_rst = "X"

                # If the field is overllaped over several 8 bit registers
                # add index to define it more clearly
                if (int(field.bitOffset / 8) !=
                        int((field.bitOffset + field.bitWidth - 1) / 8)):
                    h_ind = min(field.bitOffset + field.bitWidth - 1,
                               ((i + 1) * 8) - 1)
                    l_ind = max(field.bitOffset, (i * 8))
                    h_ind = h_ind - field.bitOffset
                    l_ind = l_ind - field.bitOffset
                    append = "[{}".format(h_ind)
                    if h_ind != l_ind:
                        append += ":{}]".format(l_ind)
                    else:
                        append += "]"
                    field_name = field_name + append
            else:
                field_name = "Reserved"
                field_rst = "-"

            ret_val[i][j].append(field_name)
            ret_val[i][j].append(field_rst)
    return ret_val


class LyxAddrGenerator(IpXactAddrGenerator):
    lyxGen = None

    genFieldDesc = None
    genRegions = None

    # Whether register should be skiped based on Config. This is used to
    # generate datasheet for particular top level generics.
    skipConditional = False

    # Top level configuration (parsed from YAML config)
    config = None

    def __init__(self, pyXactComp, memMap, wrdWidthBit, genRegions=True,
                 genFiDesc=True):
        super().__init__(pyXactComp, memMap, wrdWidthBit)

        self.lyxGen = LyxGenerator()

        self.genFieldDesc = str_arg_to_bool(str(genFiDesc))
        self.genRegions = str_arg_to_bool(str(genRegions))

    def commit_to_file(self):
        for line in self.lyxGen.out:
            self.of.write(line)

    def is_reg_present(self, reg):
        """
        Check whether register should be written to documentation. Affected by:
            1. Skip conditional attribute in document config.
            2. isPresent IP-XACT parameter of register. Parameter value read
               from config file!
        """
        if not self.config["skip_conditional"]:
            return True

        param_name = self.parameter_lookup(reg.isPresent)

        # Not conditioned by any parameter -> Keep it!
        if param_name is None:
            return True

        # Conditioned by parameter -> keep it if parameter is set to true!
        if self.config["parameters"][param_name]:
            return True

        return False

    def write_reg_field_desc(self, reg):
        """
        Write description of register fields. Each field will have enums listed
        if enums are defined.
        """
        for field in sorted(reg.field, key=lambda a: a.bitOffset):
            self.lyxGen.insert_layout("Description")
            descText = field.description
            descText += reg_append_short_enums(field)
            self.lyxGen.wr_line("{} {}\n".format(field.name, descText))
            self.lyxGen.commit_append_line(1)

    def write_reg_field_table(self, reg):
        """
        """
        reg_fields = reg_unwrap_fields(reg)

        for i in reversed(range(1, int(reg.size / 8 + 1))):
            table = self.lyxGen.build_table(9, 3)

            # Set the width
            self.lyxGen.set_columns_option(table, range(1, 9),
                                           [["width", "1.4cm"] for j in range(1, 9)])

            # Title row
            self.lyxGen.set_cell_object(table, 0, 0, "Bit index")
            bit_indexes = [str((8 * i) - j) for j in range(1, 9)]
            self.lyxGen.set_cells_object(table, [[0, j + 1] for j in range(8)],
                                         bit_indexes)

            # Field name row
            self.lyxGen.set_cell_object(table, 1, 0, "Field name")
            cells = [[1, j + 1] for j in range(8)]
            field_names = [reg_fields[i - 1][j][0] for j in range(8)]
            self.lyxGen.set_cells_object(table, cells, field_names)

            # Restart value row
            self.lyxGen.set_cell_object(table, 2, 0, "Reset value")
            cells = [[2, j + 1] for j in range(8)]
            rst_vals = [reg_fields[i - 1][j][1] for j in range(8)]
            self.lyxGen.set_cells_object(table, cells, rst_vals)

            # Merge adjacent fields with the same names
            self.lyxGen.merge_common_fields(table, [1], startCol=1)

            # Set header colors
            self.lyxGen.set_cells_color(table, [[0, i] for i in range(9)], "gray")
            self.lyxGen.set_cells_color(table, [[1, 0], [2, 0]], "cyan")

            self.lyxGen.insert_table(table)

    def write_reg_header(self, block, reg):
        """
        Write register header with:
            - Register name (Subsection)
            - Register type
            - Register address
            - Register size
            - Conditional presence note (optional)
            - Description
        """
        # Add the Section title
        self.lyxGen.write_layout_text("Subsection", "{}\n".format(reg.name),
                                      label="label")

        # Register type, address, size and description
        self.lyxGen.write_layout_text("Description", "Type: {}\n".format(
            reg.access))

        # Address
        self.lyxGen.write_layout_text("Description", "Address: {}\n".format(
            "0x{:X}".format(reg.addressOffset +
                            block.baseAddress)))

        # Size
        plural_ap = "s" if (reg.size > 8) else ""
        self.lyxGen.write_layout_text("Description", "Size: {} byte{}\n".format(
            int(reg.size / 8), plural_ap))

        # Conditional presence:
        if reg.isPresent != "" and self.config["skip_conditional"] is False:
            param_name = self.parameter_lookup(reg.isPresent)
            self.lyxGen.write_layout_text("Description",
                                          "Note: Register is present only when {} = true. Otherwise "
                                          "this address is reserved.\n".format(param_name))

        # Lock access
        lock_props = self.get_reg_lock(reg)
        if lock_props[0] == "true":
            self.lyxGen.write_layout_text("Description",
                                          "Note: {}".format(lock_props[1]))

        # Description
        self.lyxGen.write_layout_text("Standard", "{}\n".format(
            reg.description))

    def write_regs(self, block):
        """
        """
        # Memory type blocks dont need to be described by field! We use it
        # to express mapping to other registers and thus It means we dont
        # want unnecessary words described!
        if block.usage == "memory":
            return

        for reg in sorted(block.register, key=lambda a: a.addressOffset):

            if not self.is_reg_present(reg):
                continue

            # Register header
            self.write_reg_header(block, reg)

            # Bit table and bit field descriptions
            if self.genFieldDesc:
                self.write_reg_field_table(reg)
                self.write_reg_field_desc(reg)

            # Separation from next register
            self.lyxGen.insert_layout("Standard")
            self.lyxGen.insert_inset("VSpace bigskip")
            self.lyxGen.commit_append_line(2)

    def write_mem_map_title(self):
        """
        """
        self.lyxGen.write_layout_text("Chapter", "{}\n".format(
            self.memMap.displayName), label="label")

        self.lyxGen.write_layout_text("Standard", "{}\n".format(self.memMap
                                                                .description))

    def write_mem_map_regions(self, memMap):
        """
        """
        table = self.lyxGen.build_table(2, len(memMap.addressBlock) + 1)
        self.lyxGen.set_columns_option(table, range(0, 2),
                                       [["width", "4cm"] for j in range(0, 2)])

        title_cells = [[0, 0], [0, 1]]
        name_cells = [[i, 0] for i in range(1, len(memMap.addressBlock) + 1)]
        addr_cells = [[i, 1] for i in range(1, len(memMap.addressBlock) + 1)]

        name_vals = [block.displayName for block in memMap.addressBlock]
        addr_vals = ["0x{:03X}".format(block.baseAddress) for block in memMap.addressBlock]
        title_vals = ["Memory region", "Address offset"]

        self.lyxGen.set_cells_object(table, name_cells, name_vals)
        self.lyxGen.set_cells_object(table, addr_cells, addr_vals)
        self.lyxGen.set_cells_object(table, title_cells, title_vals)

        self.lyxGen.set_cells_color(table, [[0, 0], [0, 1]], "gray")

        self.lyxGen.insert_table(table)

    def calc_block_table_len(self, block):
        """
        """
        marks = [0] * (int(block.range / (block.width / 8)))
        for reg in sorted(block.register, key=lambda x: x.addressOffset):

            if not self.is_reg_present(reg):
                continue

            marks[int((reg.addressOffset * 8) / self.wrdWidthBit)] = 1

        table_len = 0
        change = True
        for mark in marks:
            if mark == 1 or change == True:
                table_len += 1
            change = True if (mark == 1) else False
        return table_len

    def write_mem_map_reg_single(self, table, reg, row):
        """
        """
        cells = []
        beg_off = int(reg.addressOffset % 4)
        for i in range(beg_off, beg_off + int(reg.size / 8)):
            cells += [[row, 3 - i]]
        text = [reg.name for i in range(self.wrdWidthByte)]
        self.lyxGen.set_cells_object(table, cells, text)
        self.lyxGen.set_cells_text_label(table, cells, ["hyperref" for i in
                                                        range(0, len(cells))])

    def write_mem_map_reg_table(self, block):
        """
        """
        self.lyxGen.write_layout_text("Section", "{}\n".format(
            block.displayName))
        table_len = self.calc_block_table_len(block)
        table = self.lyxGen.build_table(5, table_len + 1, longTable=True)

        self.lyxGen.write_layout_text("Standard", block.description)

        # Create the header
        cells = [[0, i] for i in range(5)]
        text = ["Bits [{}:{}]".format((i + 1) * 8 - 1, i * 8)
                for i in reversed(range(0, self.wrdWidthByte))]
        text += ["Address offset"]
        self.lyxGen.set_cells_object(table, cells, text)

        self.lyxGen.set_columns_option(table, range(0, 4),
                                       [["width", "3cm"] for j in range(0, 4)])
        self.lyxGen.set_column_option(table, 4, "width", "1.5cm")

        # Pre write the addresses with "..." for reserved fields
        cells = [[i + 1, 4] for i in range(table_len)]
        text = ["..." for i in range(table_len)]
        self.lyxGen.set_cells_object(table, cells, text)

        # Write the registers and addresses
        row = 1
        addr = 0
        for reg in sorted(block.register, key=lambda x: x.addressOffset):

            # Skip registers
            if not self.is_reg_present(reg):
                continue

            reg_diff = math.floor(reg.addressOffset / 4) - addr
            if reg_diff == 1:
                row += 1
            elif reg_diff > 1:
                row += 2
            addr += reg_diff
            self.write_mem_map_reg_single(table, reg, row)
            self.lyxGen.set_cell_object(table, row, 4,
                                        "0x{:X}".format(4 * math.floor(reg.addressOffset / 4) +
                                                        block.baseAddress))

        self.lyxGen.merge_common_fields(table, [i for i in range(1, table_len + 1)],
                                        endCol=4)

        # Set header color
        self.lyxGen.set_cells_color(table, [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]], "gray")

        self.lyxGen.insert_table(table)

    ################################################################################
    #  Write the memory map region overview for given memory map
    ################################################################################
    def write_mem_map_addr(self):
        if self.genRegions:
            self.write_mem_map_regions(self.memMap)

    ################################################################################
    # Write the bitfield map into the output file
    ################################################################################
    def write_mem_map_fields(self):
        for block in self.memMap.addressBlock:
            self.lyxGen.insert_new_page()
            self.write_mem_map_reg_table(block)
            self.write_regs(block)

    ################################################################################
    # Write both memory maps into the output file
    #
    # Arguments:
    #  of		 	- Output file to write
    ################################################################################
    def write_mem_map_both(self):
        self.write_mem_map_title()
        self.write_mem_map_addr()
        self.write_mem_map_fields()

    ################################################################################
    # Write register fields constants of single register
    #
    # Arguments:
    ################################################################################
    def write_reg(self, reg, writeFields, writeRstVal, writeEnums):
        pass
