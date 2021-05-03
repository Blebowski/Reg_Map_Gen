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
##   Address map generator to C header file.  
## 
##	Revision history:
##		25.01.2018	First implementation
##
################################################################################
"""

from pyXact_generator.ip_xact.addr_generator import IpXactAddrGenerator

from pyXact_generator.languages.gen_h import HeaderGenerator
from pyXact_generator.languages.declaration import LanDeclaration


def create_field_enum_decls(field):
    """
    Create declaration objects for enumerated values of IP-XACT field object.
    """
    enum_decls = []

    if len(field.enumeratedValues[0].enumeratedValue) > 0:
        for es in field.enumeratedValues:
            for (i, e) in enumerate(sorted(es.enumeratedValue, key=lambda x: x.value)):
                enum_decl = LanDeclaration(e.name.upper(), e.value)
                enum_decl.intType = "enum"
                enum_decls.append(enum_decl)

    return enum_decls


class HeaderAddrGenerator(IpXactAddrGenerator):
    headerGen = None
    prefix = ""

    def __init__(self, pyXactComp, memMap, wrdWidthBit):
        super().__init__(pyXactComp, memMap, wrdWidthBit)
        self.headerGen = HeaderGenerator()

    def commit_to_file(self):
        for line in self.headerGen.out:
            self.of.write(line)

    def create_reg_field_decl(self, reg, field):
        """
        Create declaration object from IP-XACT register and field object.
        """
        field_decl = LanDeclaration(name=field.name.lower(), value=0)
        field_decl.type = "uint{}_t".format(self.wrdWidthBit)
        field_decl.bitWidth = field.bitWidth
        field_decl.gap = 2
        field_decl.alignLen = 40
        field_decl.bitIndex = field.bitOffset + \
                             ((int(reg.addressOffset) * 8) % self.wrdWidthBit)
        field_decl.intType = "bitfield"

        return field_decl

    def write_reg_group_union(self, regGroup):
        """
        Write group of IP-XACT register objects as a single union to generator
        output. Group of registers should reside within the same memory word.

        Example of union with 32 bit wrdWidth:
            union <joined_name> {
                uint32 u32;
                struct <joined_name>_s {
                    uint32  bitfield_first : <width_of_bitfield>)
                      ...
                    uint32  bitfield_last  : <width_of_bitfield>
                }

        Name of union <joined_name> is concatenated from all register names
        within input group of registers.
        Arguments:
            regGroup 	List of IP-XACT register objects.
        """
        field_decls = []
        enum_decls = []
        un_name = self.prefix + "_"

        for (j, reg) in enumerate(regGroup):

            # Create declaration objects for each field of IP-XACT register.
            for (i, field) in enumerate(sorted(reg.field, key=lambda a: a.bitOffset)):
                field_decl = self.create_reg_field_decl(reg, field)
                field_decl.comment = None
                if i == 0:
                    field_decl.comment = reg.name.upper()

                field_decls.append(field_decl)

            # Append register name to the union name
            un_name += reg.name.lower()
            if j != len(regGroup) - 1:
                un_name += "_"

        # Create declaration of u<wrd_width> union member
        unsigned_decl = LanDeclaration("u{}".format(self.wrdWidthBit), value=0)
        unsigned_decl.type = "uint{}_t".format(self.wrdWidthBit)
        unsigned_decl.gap = 1

        # Append declarations to the list of declarations within an enum
        enum_decls.append(unsigned_decl)
        enum_decls.append(field_decls)

        self.headerGen.create_union(un_name, enum_decls)
        self.headerGen.wr_nl()

    def write_reg_field_enums(self, reg):
        """
        Write enumerated values of all register fields within IP-XACT register
        object as C enums. Name  of the C enum is:
            <prefix>_<register_name>_<field_name>
        """
        for (i, field) in enumerate(sorted(reg.field, key=lambda a: a.bitOffset)):

            # Skip field if there are no enums
            if not field.enumeratedValues:
                continue

            # Create declaration objects for each enumerated value of field
            enum_elements = create_field_enum_decls(field)

            # Write enum to the output file
            enum_name = (self.prefix + "_" + reg.name + "_" + field.name).lower()
            self.headerGen.create_enum(enum_name, enum_elements)
            self.headerGen.wr_nl()

    def sort_regs_to_wrd_groups(self, regs):
        """
        Sort list of IP-XACT register objects into groups. Each group is
        represented by a list. Each list contains registers located within
        a single memory word.
        """
        reg_groups = [[]]
        low_ind = 0

        # Sort the registers from field map into sub-lists
        for reg in sorted(regs, key=lambda a: a.addressOffset):

            # We hit the register aligned create new group
            if reg.addressOffset >= low_ind + self.wrdWidthByte:
                low_ind = reg.addressOffset - reg.addressOffset % 4
                reg_groups.append([])

            reg_groups[-1].append(reg)

        return reg_groups

    def write_reg_unions_and_enums(self, regs):
        """
        Write registers from IP-XACT registers object into generator output.
        Following artifacts are written:
            - union for each memory word with registers
            - enums for each enumerated values of register fields
        """
        # First sort the registerinto word-aligned groups.
        reg_groups = self.sort_regs_to_wrd_groups(regs)

        # Write each group
        for reg_group in reg_groups:

            # Create union for each group of registers within a single memory
            # word.
            self.write_reg_group_union(reg_group)

            # Create enums for fields of registers.
            for reg in reg_group:
                self.write_reg_field_enums(reg)

    def write_mem_map_fields(self):
        """
        Process registers within "memBlock" IP-XACT memory block and write to
        register output.
        """
        for block in self.memMap.addressBlock:

            # Skip memory blocks.
            if block.usage == "memory":
                continue

            # Write unions and enums of registers within memory block
            self.write_reg_unions_and_enums(block.register)

    def write_mem_map_addr_enum(self):
        """
        Write addresses of registers within "memBlock" IP-XACT memory block as
        enum to generator output.
        """
        cmnt = "{} memory map".format(self.memMap.name)
        self.headerGen.write_comment(cmnt, 0, small=True)
        decls = []

        for block in self.memMap.addressBlock:
            for reg in sorted(block.register, key=lambda a: a.addressOffset):
                decls.append(LanDeclaration((self.prefix + "_" + reg.name).upper(),
                                            value=reg.addressOffset + block.baseAddress,
                                            intType="enum"))

        self.headerGen.create_enum(self.prefix.lower() + "_" + self.memMap.name.lower(),
                                   decls)

    def create_addr_map_package(self, name):
        """
        Create C header file package for "memMap" IP-XACT memory block.
        Package contains:
            1. Enum with addresses of each register
            2. Unions for each memory word with registers.
            3. Enums for each enumerated values of Register fields.
        """
        self.headerGen.wr_nl()
        self.headerGen.write_comment("This file is autogenerated, DO NOT EDIT!",
                                     0, small=True)
        self.headerGen.wr_nl()
        self.headerGen.create_package((self.prefix + "_" + name).upper())
        self.headerGen.wr_nl()

        # Write memory map address enum
        if self.memMap:
            print("Writing addresses of '%s' register map" % self.memMap.name)
            self.write_mem_map_addr_enum()

        self.headerGen.wr_nl()
        self.headerGen.wr_nl()

        self.headerGen.write_comment("Register descriptions:",
                                     0, small=False)

        # Write memory map register unions and register field enums
        if self.memMap:
            print("Writing bit fields of '%s' register map" % self.memMap.name)
            self.write_mem_map_fields()

        self.headerGen.commit_append_line(1)
