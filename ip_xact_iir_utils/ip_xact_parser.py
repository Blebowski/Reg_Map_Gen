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

import sys
import os
import xml.etree.ElementTree as Et

proj_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(proj_dir)

from ip_xact_iir import *


class IpXactParser:

    xml_path: os.path
    xml_file = None
    tree: Et.ElementTree
    root: Et.ElementTree

    @staticmethod
    def parse_named_object(node: Et.ElementTree):
        name = None
        display_name = None
        description = None

        for item in node:
            if item.tag == "name":
                name = item.text
            if item.tag == "description":
                description = item.text
            if item.tag == "displayName":
                display_name = item.text

        return name, display_name, description

    @staticmethod
    def parse_reference_value(node: Et.ElementTree, attribute_name) -> IirReferenceValue:
        for item in node:
            if item.tag == attribute_name:
                return IirReferenceValue(item.text)  # Reference will be linked later
        return None

    @staticmethod
    def parse_volatile(node: Et.ElementTree) -> IirVolatile:
        for item in node:
            if item.tag == "volatile":
                return IirVolatile.from_str(item.text)
        return IirVolatile.empty

    @staticmethod
    def parse_field_reset(node: Et.ElementTree) -> IirReset:
        reset_reference_str = node.attrib()["resetTypeRef"]
        reset_value = None
        reset_mask = None

        for item in node:
            if item.tag == "value":
                reset_value = IirReferenceValue(item.text)
            if item.tag == "mask":
                reset_mask = IirReferenceValue(item.text)

        return IirReset(reset_value, reset_reference_str=reset_reference_str, reset_mask=reset_mask)

    @staticmethod
    def parse_enumerated_value(node: Et.ElementTree) -> IirEnumeratedValue:
        value = None
        usage = None

        # First pass for Named object properties
        name, display_name, description = IpXactParser.parse_named_object(node)

        # Second pass for rest
        for item in node:
            if item.tag == "value":
                value = IirValue(item.text)
            if item.tag == "usage":
                usage = IirEnumeratedValueUsage.from_str(item.text)

        return IirEnumeratedValue(name, value, display_name, usage, description)

    @staticmethod
    def parse_register_field(node: Et.ElementTree) -> IirRegisterField:
        offset = None
        width = None
        is_present = None
        reserved = None
        resets: List[IirReset] = []
        enumerated_values = List[IirEnumeratedValue]

        volatile = IirVolatile.empty
        access = IirAccess.empty
        modified_write_value = IirModifiedWriteValue.empty
        read_action = IirReadAction.empty
        testable = IirTestable.empty
        test_constraint = IirTestConstraint.empty
        write_value_constraint = IirWriteValueConstraint.no_constraints
        write_constraint_minimum = None
        write_constraint_maximum = None

        # First pass for Named object properties
        name, display_name, description = IpXactParser.parse_named_object(node)

        field_id = None
        if "fieldID" in node.attrib:
            field_id = IirValue(node.attrib["fieldID"])

        # Second pass for rest
        for item in node:
            if item.tag == "offset":
                offset = IirReferenceValue(item.text)
            if item.tag == "width":
                width = IirReferenceValue(item.text)
            if item.tag == "isPresent":
                is_present = IirReferenceValue(item.text)
            if item.tag == "volatile":
                volatile = IirVolatile.from_str(item.text)
            if item.tag == "access":
                access = IirAccess.from_str(item.text)
            if item.tag == "modifiedWriteValue":
                modified_write_value = IirModifiedWriteValue.from_str(item.text)
            if item.tag == "readAction":
                read_action = IirReadAction.from_str(item.text)
            if item.tag == "testConstraint":
                test_constraint = IirTestConstraint.from_str(item.text)
            if item.tag == "writeValueConstraint":
                write_value_constraint = IirWriteValueConstraint.from_str(item.text)
            if item.tag == "writevalueminimum":
                write_constraint_minimum = IirReferenceValue(item.text)
            if item.tag == "writevaluemaximum":
                write_constraint_maximum = IirReferenceValue(item.text)
            if item.tag == "reserved":
                reserved = IirReferenceValue(item.text)
            if item.tag == "resets":
                for reset in item:
                    if reset.tag == "reset":
                        resets.append(IpXactParser.parse_field_reset(reset))
            if item.tag == "enumeratedValues":
                for enumerated_value in item:
                    if enumerated_value.tag == "enumeratedValue":
                        enumerated_values.append(IpXactParser.parse_enumerated_value(
                            enumerated_value))

            return IirRegisterField(name, offset, width, display_name, description, volatile,
                                    access, modified_write_value, read_action, testable,
                                    test_constraint, write_value_constraint,
                                    write_constraint_minimum, write_constraint_maximum, resets,
                                    is_present, reserved, field_id)

    @staticmethod
    def parse_register(node: Et.ElementTree) -> IirRegister:
        offset = None
        size = None
        dimension = None
        is_present = None
        volatile = IirVolatile.empty
        access = IirAccess.empty
        fields: List[IirRegisterField] = []

        # First pass for Named object properties
        name, display_name, description = IpXactParser.parse_named_object(node)

        # Second pass for rest
        for item in node:
            if item.tag == "offset":
                offset = IirReferenceValue(item.text)
            if item.tag == "size":
                size = IirReferenceValue(item.text)
            if item.tag == "dimension":
                dimension = IirReferenceValue(item.text)
            if item.tag == "isPresent":
                is_present = IirReferenceValue(item.text)
            if item.tag == "field":
                fields.append(IpXactParser.parse_register_field(item))

        return IirRegister(name, offset, size, fields, description, display_name, dimension,
                           is_present, volatile, access)

    @staticmethod
    def parse_address_block(node: Et.ElementTree) -> IirAddressBlock:
        registers: List[IirRegister] = []
        usage = IirAddressBlockUsage.empty
        access = IirAccess.empty

        base_address = None
        block_range = None
        width = None
        is_present = None
        volatile = IirVolatile.empty

        # First pass for Named object properties
        name, display_name, description = IpXactParser.parse_named_object(node)

        # Second pass pass for rest
        for item in node:
            if item.tag == "baseAddress":
                base_address = IirReferenceValue(item.text)
            if item.tag == "blockRange":
                block_range = IirReferenceValue(item.text)
            if item.tag == "width":
                block_range = IirReferenceValue(item.text)
            if item.tag == "isPresent":
                is_present = IirReferenceValue(item.text)
            if item.tag == "volatile":
                volatile = IirVolatile.from_str(item.text)
            if item.tag == "usage":
                usage = IirAddressBlockUsage.from_str(item.text)
            if item.tag == "access":
                access = IirAccess.from_str(item.text)
            if item.tag == "register":
                registers.append(IpXactParser.parse_register(item))

        return IirAddressBlock(name, base_address, block_range, width, display_name, description,
                               is_present, usage, access, volatile, registers)

    @staticmethod
    def parse_memory_maps(node: Et.ElementTree) -> List[IirMemoryMap]:
        memory_maps: List[IirMemoryMap] = []

        for item in node:
            address_unit_bits = None
            address_blocks: List[IirAddressBlock] = []

            # First pass for Named object properties
            name, display_name, description = IpXactParser.parse_named_object(item)

            # Second pass for isPresent
            is_present = IpXactParser.parse_reference_value(item, "isPresent")

            # Third pass for the rest
            for inner_item in item:
                if inner_item.tag == "addressUnitBits":
                    address_unit_bits = int(inner_item.text)
                if inner_item.tag == "addressBlock":
                    address_blocks.append(IpXactParser.parse_address_block(inner_item))

            memory_maps.append(IirMemoryMap(name, display_name, description, address_unit_bits,
                                            is_present, address_blocks))

        return memory_maps

    @staticmethod
    def parse_vlnv(node: Et.ElementTree) -> IirVlnv:
        vendor = None
        library = None
        name = None
        version = None

        for item in node:
            if item.tag == "vendor":
                vendor = item.text
            if item.tag == "library":
                library = item.text
            if item.tag == "name":
                name = item.text
            if item.tag == "version":
                version = item.text

        return IirVlnv(vendor, library, name, version)

    @staticmethod
    def parse_reset_types(node: Et.ElementTree) -> List[IirResetType]:
        reset_types: List[IirResetType] = []
        for item in node:
            if item.tag == "resetType":
                name, display_name, description = IpXactParser.parse_named_object(item)
                reset_types.append(IirResetType(name, display_name, description))
        return reset_types

    @staticmethod
    def parse_parameters(node: Et.ElementTree) -> List[IirParameter]:
        iir_parameters: List[IirParameter] = []
        for item in node:
            if item.tag == "parameter":
                parameter_id = item.attrib["parameterId"]  # ParameterId obligatory

                parameter_type_str = None
                if "parameterType" in item.attrib:
                    parameter_type_str = item.attrib["parameterType"]
                parameter_type = IirParameterType.from_str(parameter_type_str)

                name, display_name, description = IpXactParser.parse_named_object(item)

                value = None
                for inner_item in item:
                    if inner_item.tag == "value":
                        value = IirReferenceValue(inner_item.text)

                iir_parameters.append(IirParameter(name, parameter_id, value, description,
                                                   display_name, parameter_type))
        return iir_parameters

    @staticmethod
    def parse_vendor_extension(node: Et.ElementTree) -> IirVendorExtension:
        vendor_extension = IirVendorExtension(node.tag, node.text, node.attrib)
        vendor_extension.children = IpXactParser.parse_vendor_extensions(node)
        return vendor_extension

    @staticmethod
    def parse_vendor_extensions(node: Et.ElementTree) -> List[IirVendorExtension]:
        vendor_extensions = []
        for item in node:
            vendor_extensions.append(IpXactParser.parse_vendor_extension(item))
        return vendor_extensions

    @staticmethod
    def resolve_reference_parameter(reference_value: IirReferenceValue, parameters: List[
                                    IirParameter]):
        #print("Trying to resolve: {} {}".format(reference_value, reference_value.uuid))

        for parameter in parameters:
            if parameter.parameter_id == reference_value.uuid:
                reference_value.value = parameter.value
                print("Resolved reference value of: {} to parameter: {} with value: {}".format(
                    reference_value.uuid, parameter.name, parameter.value.value))
                return

        # Discard UID of reference value because it was not found
        reference_value.uuid = None

    @staticmethod
    def link_iir_object_parameters(iir_object: IirObject, parameters: List[IirParameter]):
        for attribute, value in iir_object.__dict__.items():

            # Resolve refernce value
            if isinstance(value, IirReferenceValue):
                IpXactParser.resolve_reference_parameter(value, parameters)
                continue

            # Nest on others from IIr_Object, basic types are ignored
            if isinstance(value, IirObject) and (attribute is not "parent"):
                IpXactParser.link_iir_object_parameters(value, parameters)

            # Iterate over lists and if its element is Iir_Object -> nest
            if isinstance(value, list):
                for item in value:
                    if isinstance(value, IirReferenceValue):
                        IpXactParser.resolve_reference_parameter(value, parameters)
                        continue
                    if isinstance(item, IirObject):
                        IpXactParser.link_iir_object_parameters(item, parameters)

    @staticmethod
    def link_hw_component_parameters(component: IirHwComponent):
        for memory_map in component.memory_maps:
            IpXactParser.link_iir_object_parameters(memory_map, component.parameters)
        pass

    @staticmethod
    def parse_hw_component(node: Et.ElementTree) -> IirHwComponent:
        author = None
        license = None
        memory_maps = None
        parameters: List[IirParameter] = []
        reset_types: List[IirResetType] = []
        description = None

        # First pass for VLNV
        vlnv = IpXactParser.parse_vlnv(node)

        # Second pass for rest
        for item in node:
            if item.tag == "author":
                author = item.text
            if item.tag == "license":
                license = item.text
            if item.tag == "description":
                description = description
            if item.tag == "memoryMaps":
                memory_maps = IpXactParser.parse_memory_maps(item)
            if item.tag == "resetTypes":
                reset_types = IpXactParser.parse_reset_types(item)
            if item.tag == "parameters":
                parameters = IpXactParser.parse_parameters(item)
            if item.tag == "vendorExtensions":
                vendor_extensions = IpXactParser.parse_vendor_extensions(item)
            #TODO: XML Header not parsed. Is it IP-XACT standard?

        hw_component = IirHwComponent(vlnv, description, author, license)
        hw_component.set_memory_maps(memory_maps)
        hw_component.set_parameters(parameters)
        hw_component.set_reset_types(reset_types)
        hw_component.set_vendor_extensions(vendor_extensions)
        IpXactParser.link_hw_component_parameters(hw_component)

        return hw_component

    def parse_ip_xact(self, path):
        self.xml_file = open(path, 'r')
        it = Et.iterparse(self.xml_file)

        # Remove namespaces
        for _, item in it:
            prefix, namespace, postfix = item.tag.partition("}")
            if namespace:
                item.tag = postfix
        self.root = it.root

        if not self.root.tag == "component":
            print("Unsupported IP_XACT item type {}".format(self.root.tag))
            sys.exit(1)

        return self.parse_hw_component(self.root)


