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
##   VHDL Generator Class for PyXact parsed obejects from IP-Xact specification 
##	
##	Revision history:
##		16.01.2018	Implemented the script
##
################################################################################
"""

import math
import re

from pyXact_generator.gen_lib import *
from pyXact_generator.languages.gen_lan_base import LanBaseGenerator

from pyXact_generator.languages.declaration import LanDeclaration


class VhdlGenerator(LanBaseGenerator):

    def __init__(self):
        super().__init__()
        self.supportedTypes = ["std_logic", "natural"]
        self.commentSign = "-"

    ################################################################################
    #	LanBaseGenerator inherited function
    ################################################################################

    def __wr_line(self, line):
        super(VhdlGenerator, self).wr_line(line)

    def wr_line(self, line):
        self.__wr_line(line)

    def is_supported_type(self, type):
        return super().is_supported_type(type)

    ################################################################################
    #	VHDL syntax specific generation functions
    ################################################################################

    def write_comm_line(self, gap=2):
        """
        Write VHDL comment line in format: (gap)---- aligned to 80 characters
        Arguments:
            gap		 Number of tabs before the comment line
        """
        self.__wr_line('{:{fill}<80}\n'.format(" " * gap, fill=self.commentSign))

    def logic_op_to_str(self, logicOp):
        """
        """
        assert (type(logicOp) == self.LogicOp), "'logicOp' should have type LogicOp"
        if (logicOp == self.LogicOp.OP_ASIGN):
            return "<="
        if (logicOp == self.LogicOp.OP_COMPARE):
            return "="
        if (logicOp == self.LogicOp.OP_AND):
            return " and "
        if (logicOp == self.LogicOp.OP_OR):
            return " or "
        if (logicOp == self.LogicOp.OP_XOR):
            return " xor "
        if (logicOp == self.LogicOp.OP_ADD):
            return "+"
        if (logicOp == self.LogicOp.OP_SUB):
            return "-"
        if (logicOp == self.LogicOp.OP_MUL):
            return "*"
        if (logicOp == self.LogicOp.OP_DIV):
            return "/"
        if (logicOp == self.LogicOp.OP_NOT):
            return " not "

    def write_comment(self, input, gap=0, caption=None, small=False, wrapLine=True):
        """
        Write VHDL comment in format:
            --------------------------------------------------------------------
            -- caption
            --
            -- Comment text
            --------------------------------------------------------------------
        Arguments:
            input	 Text of the comment
            gap		 Number of tabs before the comment line
            caption	 Text of the caption
            small    If set to True the first and last line of above described
                     format are ommitted
        """
        if (small == False):
            self.write_comm_line(gap)

        if (caption != None):
            self.__wr_line(" " * gap + self.commentSign + self.commentSign +
                           " {}\n{}\n".format(caption, " " * gap + "--"))

        if (wrapLine):
            lines = split_string(input, 75)
            for line in lines:
                self.__wr_line('{}{} {}\n'.format(" " * gap, self.commentSign * 2,
                                                  line))
        else:
            self.__wr_line('{}{} {}'.format(" " * gap, self.commentSign * 2, input))

        if (small == False):
            self.write_comm_line(gap)

    def write_gen_note(self, small=True):
        """
        """
        self.write_comment("This file is autogenerated, DO NOT EDIT!",
                           0, small=small)

    def create_includes(self, library, includeList):
        """
        Create VHDL include list from a library.
        Arguments:
            includeList		List of includes from given library
        """
        if (includeList == None):
            return False

        self.__wr_line("Library {};\n".format(library))
        for include in includeList:
            self.__wr_line("use {}.{};\n".format(library, include))

    def format_int_std_log_decl_val(self, decl):
        """
        Format value of std_logic or std_logic_vector declaration given as
        integer value.
        """
        strVal = ""

        # For single bit, this is written as '1', '0'
        if (decl.bitWidth == 1):
            strVal = "'{}'".format(decl.value)
            return strVal

        # If width is multiple of 4 -> use hex format, binary otherwise
        if (decl.bitWidth % 4 == 0):
            fmt = ':0{}x'.format(math.ceil(float(decl.bitWidth / 4)))
            hPref = 'x'
        else:
            fmt = ':0{}b'.format(math.ceil(float(decl.bitWidth)))
            hPref = ''
        fmt = '{' + fmt + '}'

        strVal = strVal + hPref + '"' + fmt.format(int(decl.value)).upper() + '"'

        ## For longer logic vectors which have equal value of each
        ## bit use (OTHERS => )
        if ((decl.bitWidth > 8 and hPref == '') or decl.bitWidth > 32):
            binStr = str(':0{}b'.format(decl.value))
            isBinaryEq = True
            for binChr in binStr[1:-1]:
                if (binChr != binStr[1]):
                    isBinaryEq = False

            if (isBinaryEq):
                strVal = "(OTHERS => '{}')".format(binStr[1])

        return strVal

    def format_str_std_log_decl_val(self, decl):
        """
        Format value of std_logic or std_logic_vector declaration given as
        string object.
        """
        strVal = ""
        if (decl.bitWidth == 1):
            strVal = "'" + decl.value + "'"
        else:
            strVal = '"' + decl.value + '"'

        return strVal

    def format_std_log_decl_val(self, decl):
        """
        Create VHDL declaration of std_logic or std_logic_vector!
        CAN be used for declaration of signal, constant, generic, IO
        port of entity or element of VHDL record.
            decl		Declaration object
        """
        strVal = ""

        # If value of declaration is a string try to parse it separately
        if (type(decl.value) == str):
            strVal = self.format_str_std_log_decl_val(decl)

        # In other cases parse all other formats as if integers... see
        # what happends ;)
        else:
            strVal = self.format_int_std_log_decl_val(decl)

        return strVal

    def format_std_log_decl_type(self, decl):
        """
        Formats "type" specifier for std_logic and std_logic_vector.
        types. Supports Integer and String Bitwidths.
            decl		Declaration object
        """
        strType = decl.type

        # If Both bounds are given, use the bounds
        if (decl.upBound != None and decl.lowBound != None):
            if (decl.type == "std_logic"):
                strType += "_vector"
            strType += "({} downto {})".format(decl.upBound, decl.lowBound)

        # If only numeric bitWidth is given, use it and go till zero
        elif (str(decl.bitWidth).isdigit() and decl.bitWidth > 1):
            if (decl.type == "std_logic"):
                strType += "_vector"
            strType += "({} downto 0)".format(decl.bitWidth - 1)

        # If digit is 0 -> nothing is needed we keep std_logic
        elif (decl.bitWidth == 1):
            return strType

        # If nothing is specified, we don't know how to format the vector ->
        # FUCK IT!
        else:
            print("WARNING: No std_logic_vector range! Assuming without range.")

        return strType

    def format_decl_type_and_val(self, decl):
        """
        Format value of a declaration into string.
        """
        strType = ""
        strVal = ""

        # For std_logic or std_logic_vector parse it separately
        if (decl.type == "std_logic" or decl.type == "std_logic_vector"):
            if (decl.value != "" and decl.value != None):
                strVal = self.format_std_log_decl_val(decl)

            strType = self.format_std_log_decl_type(decl)

        # All other types
        else:
            strType = decl.type
            strVal = decl.value

        return [strType, strVal]

    def format_decl_dir(self, decl):
        """
        Format declaration direction into a string. If no direction is
        specified, empty string is chosen
        """
        dirStr = ""
        if (decl.direction != "" and decl.direction != None):
            dirStr = decl.direction

        return dirStr

    def format_decl_name(self, decl):
        """
        Format name of a declaration into a string.
        """
        if (decl.specifier == "constant"):
            return decl.name.upper()
        else:
            return decl.name.lower()

    def write_decl(self, decl):
        """
        Create VHDL declaration of simple type. CAN be used for either
        component ports (with direction), generics or signal/constant
        declaration without binding to entity/component.
        Arguments:
            decl		    Declaration object
        """
        [strType, strVal] = self.format_decl_type_and_val(decl)

        dirStr = self.format_decl_dir(decl)
        name_fmt = self.format_decl_name(decl)

        # Declare prefix and postfix, two parts of declaration
        pref_string = ""
        if (decl.specifier != None):
            pref_string = decl.specifier
        pref = '  {} {}'.format(pref_string, name_fmt)

        post = ' :{} {}'.format(dirStr, strType)

        # Distinguish between initialized and non-initialized declarations!
        if (not ((decl.value == "") or (decl.value == None))):
            post += " := {}".format(strVal)

        # Append semicoln
        if (decl.addSemicoln):
            post += ";"
        post += "\n";

        # Following aligning section is a little nasty thing and one might
        # wonder how it works... Author does not know either, so this should
        # be reworked in future. Bottom line is: There are no clear rules
        # on how alignement of declaration objects should be done. It should
        # be generic enough to cover maximal line length, left, right alignments
        # inited, non-inited vectors so that each generated code looks NICE!

        # When Aligning left, align prefix
        if (decl.alignLeft):
            pref = '{:<{}}'.format(pref, decl.alignLen)

        # When Aligning left, align postfix
        if (decl.alignRight):
            post = '{:>{}}'.format(post, decl.alignLen - len(pref))

        newLineChar = ""
        if (len(pref) + len(post) > 80 and decl.wrap):
            newLineChar = "\n                "

        self.__wr_line(" " * decl.gap + pref + newLineChar + post)
        return True

    def push_parallel_assignment(self, signalName, gap=2):
        """
        Start parallel assignment ('signal_A <= ')
        """
        self.__wr_line("{}{} <=".format(" " * gap, signalName))
        self.append_line(";\n")

    def format_vector_range(self, signalName, u_ind, l_ind, direction="downto"):
        """
        Format declaration of vector range.
        """
        return "{}({} {} {})".format(signalName, u_ind, direction, l_ind);

    def format_logic_op(self, operand_lst, logic_op):
        """
        """
        assert (type(operand_lst) == list), "'operand_lst' should have type list"
        assert (type(logic_op) == self.LogicOp), "'logic_op' should have type LogicOperation"
        assert (len(operand_lst) > 0), "'operand_lst' should be non-empty"

        retStr = "({}".format(operand_lst[0])
        if (len(operand_lst) > 1):
            for val in operand_lst[1:]:
                retStr += "{}{}".format(self.logic_op_to_str(logic_op), val)
        retStr += ")"
        return retStr

    def format_bin_const(self, const):
        """
        Format binary constant
        """
        assert (type(const) == str), "'const' should be string type"
        if (len(const) == 1):
            return "'{}'".format(const)
        return '"{}"'.format(const)

    def format_vector_index(self, signalName, ind):
        """
        Format vector index
        """
        return "{}({})".format(signalName, ind)

    def format_concatenation(self, vals):
        """
        """
        assert type(vals) == list, "'vals' argument should be list"
        assert len(vals) > 0, "'vals' should have more than 0 elements"
        concat_val = vals[0]
        if (len(vals) > 1):
            for val in vals[1:]:
                concat_val += "& {}".format(val)
        return concat_val

    def format_decls(self, decls, gap, alignLeft, alignRight, alignLen, wrap):
        """
        Format list or dictionary of declarations to have common alignment
        settings!
        """
        lst = []
        if (type(decls) == list):
            lst = decls
        elif (type(decls) == dict):
            for key, value in decls.items():
                lst.append(value)

        for decl in lst:
            decl.alignLen = alignLen
            decl.alignLeft = alignLeft
            decl.alignRight = alignRight
            decl.gap = gap
            decl.wrap = wrap

    def write_connection(self, decl, specDir=False):
        """
        Create component port or generic connection on VHDL entity.
        Arguments:
            decl     Declaration object
            specDir  If Direction should be specified in the connection
                     in VHDL comment
        """
        portDelim = ""
        if (decl.addSemicoln):
            portDelim = ","

        pref = " {} {} ".format(" " * decl.gap, decl.name)
        pref = pref + " " * (40 - len(pref)) + "=>"
        post = " {} {}".format(decl.value, portDelim)

        if (specDir and (decl.direction != None and decl.direction != "")):
            post = post + "-- {}".format(decl.direction)

        post = post + "\n"
        self.__wr_line(pref + post)

    def create_package(self, name):
        """
        Create VHDL package.
        Arguments:
            name		name of the package
        """
        self.__wr_line("package {} is\n".format(name))
        self.append_line("end package;\n")

    def create_structure(self, name, decls, gap=0):
        """
        Create VHDL record.
        Arguments:
            decls		Declaration structures
        """
        if (not decls):
            return False
        self.__wr_line(" " * gap + "type {} is record\n".format(name))
        for decl in decls:
            self.write_decl(decl)
        self.__wr_line(" " * gap + "end record;\n")
        return True

    def create_enum(self, name, decls, gap=0):
        """
        Create VHDL enum.
        Arguments:
            decls		Declaration structures
        """
        if (not decls):
            return False
        self.__wr_line(" " * gap + "type {} is (\n".format(name))
        for (i, item) in enumerate(decls):
            self.__wr_line(" " * item.gap + item.name)
            if (i == len(decls) - 1):
                self.__wr_line('\n')
            else:
                self.__wr_line(',\n')
        self.__wr_line(" " * gap + ");")
        return True

    def write_ports_or_declarations(self, decl, decls, isInstance):
        """
        Writes Dictionary of ports or declarations. 
        Arguments:
            decl		Declaration object of entity for which
            decls       Declarations List (VhdlCompDeclaration)
            isInstance  "True" indicates ports should be written.
        """
        for (i, key) in enumerate(decls):

            if (i == len(decls) - 1 and decl.intType != "architecture"):
                decls[key].addSemicoln = False
            else:
                decls[key].addSemicoln = True

            if (isInstance):
                self.write_connection(decls[key], specDir=True)
            else:
                self.write_decl(decls[key])

    def format_entity_decl(self, decl, base_indent=4, alignLen=30):
        """
        Format declaration of entity or architecture with increasing indent for
        """
        if (decl.intType != "entity" and decl.intType != "architecture"):
            print("ERROR: Unsupported declaration type:" + decl.intType + \
                  " Should be entity or architecture!")
            return

        self.format_decls(decl.ports, gap=base_indent + 2, alignLeft=True,
                          alignRight=False, alignLen=alignLen, wrap=False)
        self.format_decls(decl.generics, gap=base_indent + 2, alignLeft=True,
                          alignRight=False, alignLen=alignLen, wrap=False)
        self.format_decls([decl], gap=base_indent, alignLeft=True,
                          alignRight=False, alignLen=alignLen, wrap=False)

    def create_comp_instance(self, decl):
        """
        Create component instance of VHDL entity, entity declaration, component
        declaration or architecture declaration.
        Arguments:
            decl        Declaration object (VhdlCompDeclaration)
            specDir     If Direction should be specified in the connection
                        in VHDL comment
        """
        titleStr = ["generic {}(\n", "port {}(\n"]
        mapSuf = ""
        semicoln = ""
        gstr = " " * decl.gap

        self.__wr_line("\n")

        # Write instance title and name, entity name or component name
        if (decl.intType == "entity"):
            if (decl.isInstance):
                title = decl.value + " : " + decl.name + "\n"
                mapSuf = "map"
            else:
                title = decl.intType + " " + decl.name + " is" + "\n"

        # For architecture, there is no disnitguishing between instance
        # or declaration. "value" now contains entity name!
        elif (decl.intType == "architecture"):
            title = decl.intType + " " + decl.name + " of " + decl.value
            title = title + " is\n"
        else:
            print("Unsupported component type!")
            return

        self.__wr_line(gstr + title)

        # Go through Generics and Ports
        for (i, title) in enumerate(titleStr):
            items = decl.generics if (i == 0) else decl.ports

            # If no generics are defined -> skip them.
            if (len(items) == 0):
                # print("Skipping: " + title)
                continue;

            # Add semicoln for ports in instance, or generic and port of decl.
            if ((i == 1) or (decl.isInstance == False)):
                semicoln = ";"

            # Write "generic/port" and "map". Skip for architecture (no generic
            # nor ports)
            if (decl.intType != "architecture"):
                title = title.format(mapSuf)
                self.__wr_line(gstr + title)
                self.append_line(gstr + ")" + semicoln + "\n")

            # Write ports or generics
            self.write_ports_or_declarations(decl, items, decl.isInstance)

            # Appending final bracket for entities always, for components
            # only with ports!
            if (decl.intType != "architecture"):
                self.commit_append_line(1)

        # After printing declarations of architecture, print "BEGIN"
        if (decl.intType == "architecture"):
            self.__wr_line("begin\n")
            self.append_line("end architecture " + decl.name + ";\n")

        # Finalize component / entity. skip for architecture!
        if (decl.isInstance == False and decl.intType != "architecture"):
            endStr = "end {} {};\n".format(decl.intType, decl.name)
            self.__wr_line(endStr)

        self.__wr_line("\n")

    def create_gate(self, result, signals, gate, gap=2):
        """
        Create basic logic function two two signals.
        Arguments:
            result		Name of resulting signal
            signals		List with original signal names
            gate		String with gate function
        """
        gStr = " " * gap
        line = gStr + result + " <= " + signals[0] + " " + gate + " " + signals[1] + ";\n"
        self.__wr_line(line)

    def create_signal_connection(self, result, driver, gap=0):
        """
        """
        line = " " * gap + result + " <= " + driver + ";\n"
        self.__wr_line(line)

    def create_with_select(self, result, selector, values, conditions, gap=2):
        """
        Create "with/select" VHDL statement
        Arguments:
            TODO
        """
        line = " " * gap + "with " + selector + " select " + result + " <=\n"
        self.__wr_line(initLine)

        if (not (len(values) == len(conditions))):
            print("values and conditions must have equal lengths")
            return;

        for (value, condition) in (values, conditions):
            line = " " * (gap + 4) + value + " when " + condition

            # Append "," for all but last line where ";" is used
            if (value == values[-1]):
                line.append(";\n")
            else:
                line.append(",\n")

        self.__wr_line("\n")

    def create_if_generate(self, name, condition, value, gap=2):
        """
        Create "if generate" VHDL statement
        Arguments:
            TODO
        """
        line = " " * gap + name + " : if (" + condition
        line += " = " + value + ")" + " generate\n"

        self.__wr_line(line)
        self.append_line(" " * gap + "end generate " + name + ";\n")

    def create_for_generate(self, name, var, indices, gap=2):
        """
        Create "for generate" VHDL statement.
        Arguments:
            TODO
        """

        if (not (len(indices) == 2)):
            print("'For generate' statement should have exactly two indices")

        line = " " * gap + name + " : for " + var + " in " + indices[0]
        line.append(" to " + indices[1] + " generate\n")
        self.__wr_line(line)
        self.append_line(" " * gap + "end generate " + name + ";\n")

    def is_valid_dir(self, direction):
        """
        Checks if specified direction is valid in VHDL.
        Accepts: in, out, inout, buffer
        """
        acceptDirs = ["in", "out", "buffer", "inout"]
        for acceptDir in acceptDirs:
            if (direction == acceptDir):
                return True

        return False

    def strip_spaces(self, string):
        """
        Strips spaces from a string and returns string without spaces
        """
        return "".join([x for x in string if x != " "])

    def parse_gen_or_port(self, line):
        """
        Parses input line which is a port or generic declaration into a
         declaration object.
        On ports, direction must be specified. On generics, it must NOT be
        speciffied.
        If line could not be parsed, None is returned. Otherwise declaration
        object is returned.
        Each line must start with 'signal' for port declarations, or 'constant'
        for generic declarations.

        """
        decl = LanDeclaration("new", value="")
        # decl.alignRight = False
        # decl.alignLength = 80
        # decl.doIndent = True

        # Find all separated words and numbers
        cmn_re = re.compile("[\w]+")
        wrds = cmn_re.findall(line)

        # Allow only signal and constant prefixes
        if (len(wrds) > 2 and
                (wrds[0] == "signal" or wrds[0] == "constant")):
            decl.specifier = wrds[0]
        else:
            return None

        # For Ports, Direction must be valid VHDL port direction
        if (wrds[0] == "signal" and (not self.is_valid_dir(wrds[2]))):
            return None

        # Name is common for generics and ports
        decl.name = wrds[1]

        if (wrds[0] == "signal"):
            decl.direction = wrds[2]
            decl.type = wrds[3]

        if (wrds[0] == "constant"):
            # Initialized default value (for generics only)
            if (":=" in line):
                decl.value = wrds[-1]
            decl.type = wrds[2]

        # Process std_logic_vector specially to determine range. Support
        # only downto, we don't need to be too generic
        # print("DEEEECL")
        # print(decl.name)
        # print(decl.type)
        # print("\n")
        if (decl.type == "std_logic_vector"):
            stdv_re = re.compile("\([ ]*.+ downto .*[ ]*\)")
            rng_spec = stdv_re.findall(line)

            # Skip vectors without range (e.g. generics)
            if (len(rng_spec) == 0):
                return decl

            # Strip brackets and take vector boundaries
            ths = rng_spec[0][1:-1].split("downto")
            decl.upBound = ths[0].strip()
            decl.lowBound = ths[1].strip()

            # Calculate bitWidth, but only for integers, for strings
            # leave only boundaries, we don't need complicated parsing logic
            if (decl.upBound.isdigit() and decl.lowBound.isdigit()):
                decl.bitWidth = eval(decl.upBound + " - " + decl.lowBound + "+ 1")

        elif (decl.type == "std_logic"):
            decl.bitWidth = 1

        return decl

    def load_entity_template(self, path):
        """
        Load entity template from VHDL file. Recognizes: entity name,
        Entity ports, generics. Note that on each generic "constant"
        must be explicitly specified. On each port "signal" must be
        explicitly specified. Direction must be specified on each signal!
        Parsing stops upon "architecture" definition start.
        Return declaration object of parsed entity.
        Arguments:
            TODO
        """
        if (not (path.endswith(".vhd"))):
            print("Only VHDL files are supported for parsing!")
            return

        fd = open(path)

        # Entity name parser
        ent_re = re.compile("^[ ]*entity[ ]*[\w]+[ ]*is$")

        # Architecture parser
        # Upon start of architecture parsing is finished, otherwise internal
        # signals would be parsed too!
        architecture_re = re.compile("^[ ]*architecture[ ]+[\w]+[ ]+of[ ]+[\w]+[ ]+is[ ]*$")

        entity = LanDeclaration("name", value="")
        entity.intType = "entity"

        for line in fd:
            line = line.lower()

            # Finish when architecture starts
            arch_res = architecture_re.match(line)
            if (arch_res):
                break

            # Get name of entity
            ent_res = ent_re.match(line)
            if (ent_res):
                mtch = re.compile("[\w]+").findall(line)
                entity.name = mtch[1]

            # Parse ports or generics
            port_or_gen = self.parse_gen_or_port(line)
            if (port_or_gen == None):
                continue

            if (port_or_gen.specifier == "signal"):
                entity.ports[port_or_gen.name] = port_or_gen

            elif (port_or_gen.specifier == "constant"):
                entity.generics[port_or_gen.name] = port_or_gen

        fd.close()
        return entity

    def write_assertion(self, name, asrt_type, sequence, gap=4):
        """
        """
        assert (type(name) == str), "'name' type should be string"

        self.write_comment("psl {} : {}".format(name, asrt_type), gap=4,
                           small=True)
        self.write_comment("{{{}}};".format(sequence), gap=4, small=True,
                           wrapLine=False)
        self.__wr_line("\n")
