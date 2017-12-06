# Network-Slice-Selection-Function---NSSF
## Introduction
A Network Slice Selection Function is in charge of making the selection of an appropriate Network Slice in base of some parameters that a UE will send when it wants to attach to a Network. In the next sections the level of functionality achieved and the steps that are required for running this module will be described

## Description
The <b>NSSF</b> is part of the 3gpp solution for having E2E slicing in a Mobile Network. According to documentation,
the <b>NSSF</b> sits between the <b>RAN</b> and the <b>MME</b> and it is present mainly in the Attach and Detach procedures of a 5G mobile network.
According to <b>3gpp</b> documentation during Session Establishment the NSSF will be involved in Reselection of a Network Slice only if, the Network Configuration changed. Because of this is not part of the scope of our project, Slice reselection is not included in the functionality.

### Attach/Reattach
The following Flow chart, shows the Attach/Reattach procedure of the NSSF

![ALT text](/Images/NSSF_Attach.png "Flowchart of the Network Slice Selection Function")
