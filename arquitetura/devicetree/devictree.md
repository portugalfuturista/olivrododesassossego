The devicetree.org wword and logos and related marks are trade-marks and service marks licensed by Linaro Ltd. 
Implementation of certain elements of this document may require
licenses under third party intellectual property rights, including without limitation, patent rights. Linaro and its
Members are not, and shall not be held, responsible in any manner for identifying or failing to identify any or all
such third party intellectual property rights.

The Power Architecture and Power.org word marks and the Power and Power.org logos and related marks are
trademarks and service marks licensed by Power.org. Implementation of certain elements of this document may
require licenses under third party intellectual property rights, including without limitation, patent rights. Power.org
and its Members are not, and shall not be held, responsible in any manner for identifying or failing to identify any
or all such third party intellectual property rights.


# CHAPTER 1
## Introduction
#### 1.1 Purpose and Scope

To initialize and boot a computer system, various software components interact. Firmware performs low-level initialization of the system hardware before passing control to software such as an operating system, bootloader, or hypervisor. Bootloaders and hypervisors can, in turn, load and transfer control to operating systems. Standard, consistent interfaces and conventions facilitate the interactions between these software components.

In this document, the term boot program refers to a software component that initializes the system state and executes another software component, referred to as a client program. Examples of boot programs include firmware, bootloaders, and hypervisors. Examples of client programs include bootloaders, hypervisors, operating systems, and special-purpose programs. A piece of software may be both a client program and a boot program (e.g., a hypervisor).

This specification, the Devicetree Specification (DTSpec), provides a complete boot program to client program interface definition, combined with minimum system requirements that facilitate the development of a wide variety of systems.

This specification is targeted towards the requirements of embedded systems. An embedded system typically consists of system hardware, an operating system, and application software that are custom-designed to perform a fixed, specific set of tasks. This is unlike general-purpose computers, which are designed to be customized by a user with a variety of software and I/O devices. Other characteristics of embedded systems may include:

A fixed set of I/O devices, possibly highly customized for the application
A system board optimized for size and cost
Limited user interface
Resource constraints like limited memory and limited nonvolatile storage
Real-time constraints
Use of a wide variety of operating systems, including Linux, real-time operating systems, and custom or proprietary operating systems
Organization of this Document:

Chapter 1 introduces the architecture specified by DTSpec.
Chapter 2 introduces the devicetree concept and describes its logical structure and standard properties.
Chapter 3 specifies the definition of a base set of device nodes required by DTSpec-compliant devicetrees.
Chapter 4 describes device bindings for certain classes of devices and specific device types.
Chapter 5 specifies the physical structure of devicetrees.
Conventions Used in this Document:

The word shall is used to indicate mandatory requirements strictly to be followed to conform to the standard.
The word should is used to indicate that among several possibilities, one is recommended as particularly suitable.
The word may is used to indicate a course of action permissible within the limits of the standard.
Examples of devicetree constructs are frequently shown in Devicetree Syntax form. See section 6 for an overview of this syntax.

#### 1.2 Definitions