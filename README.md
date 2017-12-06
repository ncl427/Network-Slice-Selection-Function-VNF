# Network-Slice-Selection-Function---NSSF
## Introduction
A Network Slice Selection Function is in charge of making the selection of an appropriate Network Slice in base of some parameters that a UE will send when it wants to attach to a Network. In the next sections the level of functionality achieved and the steps that are required for running this module will be described

## Description
The <b>NSSF</b> is part of the 3gpp solution for having E2E slicing in a Mobile Network. According to documentation,
the <b>NSSF</b> sits between the <b>RAN</b> and the <b>MME</b> and it is present mainly in the Attach and Detach procedures of a 5G mobile network.
According to <b>3gpp</b> documentation during Session Establishment the NSSF will be involved in Reselection of a Network Slice only if, the Network Configuration changed. Because of this is not part of the scope of our project, Slice reselection is not included in the functionality.

The current functionality present in the code is:
- Assign a Network Slice during Network Attach/Reattach procedure
- Erase UE slice assignation during the Network Detach procedure

It is important to make clear, the NSSF is not in charge of doing the Attach/Reattach procedure, it only passes the information received from <b>RAN</b> to the <b>MME</b>, and once the UE is allowed to have connection will assign the Network Slice based on the Type of Service that the UE requires.

### Functionality during UE Attach/Reattach procedure
The following Flow chart, shows the Attach/Reattach procedure of the NSSF

![ALT text](/Images/NSSF_Attach.png "Flowchart of the Network Slice Selection Function")

1. The NSSF receives from RAN the UE connection information, in our scenario it is contained inside an <b>Object</b>, the 2 main attributes required by the NSSF are UE Id (In our Scenario is the IP of the machine) and the Type of service.

2. Once the NSSF has the UE information, it verifies with its local Connection Database, if the UE has already being served. (The local connection database will have the information of the UE as long as this one haven't disconnected from the network).

  - 2.a From this point 2 things can happen. If the UE information is not in the local Database, it means that we are working in the Attach Procedure, for which we need to forward the UE connection information that we receive to the MME to handle the connection, after doing this, the MME will reply with updated connection information (Required for the TempId) or will not allow the connection (Based on its own policies)
