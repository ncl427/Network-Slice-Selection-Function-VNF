# Network Slice Selection Function NSSF
## Introduction
A Network Slice Selection Function is in charge of making the selection of an appropriate Network Slice in base of some parameters that a **UE** will send when it wants to attach to a Network. In the next sections the level of functionality achieved and the steps that are required for running this module will be described

## Description
The **NSSF** is part of the 3gpp solution for having E2E slicing in a Mobile Network. According to documentation,
the **NSSF** sits between the **vBBU** and the **MME** and it is present mainly in the Attach and Detach procedures of a 5G mobile network.
According to **3gpp** documentation during Session Establishment the NSSF will be involved in Reselection of a Network Slice only if, the Network Configuration changed. Because of this is not part of the scope of our project, Slice reselection is not included in the functionality.

The current functionality present in the code is:
- Assign a Network Slice during Network Attach/Reattach procedure
- Erase UE slice assignation during the Network Detach procedure

It is important to make clear, the NSSF is not in charge of doing the Attach/Reattach procedure, it only passes the information received from **vBBU** to the **MME**, and once the UE is allowed to have connection will assign the Network Slice based on the Type of Service that the UE requires.

### Functionality during UE Attach/Reattach procedure
The following Flow chart, shows the Attach/Reattach procedure of the NSSF

![ALT text](/Images/NSSF_Attach_v2.png "Flowchart of the Network Slice Selection Function")

1. The NSSF receives from **vBBU** the **UE** connection information, in our scenario it is contained inside an **Object**, the 2 main attributes required by the **NSSF** are **UE** Id (In our Scenario is the IP of the machine) and the **Service Type**.

2. Once the NSSF has the UE information, it verifies with its local Connection Database, if the UE has already being connected before (Without a detach). *The local connection database will have the information of the UE as long as this one haven't disconnected from the network.*

   - **2.a** From this point 2 things can happen. If the UE information is not in the local Database, it means that we are working in the Attach Procedure, for which we need to forward the UE connection information that we receive to the MME to handle the connection, after doing this, the MME will reply with updated connection information (Required for the **Temporary Id**) or will not allow the connection (Based on its own policies)

   - **2.b** If the User equipment information was already inside the Local Connection Database it means that we are working with a Reattach procedure, for which we do not need to send any request to the MME and we proceed directly to the **Network Slice Selection**.

#### Network Slice Selection

3. Before sending the Connection Information to the **vMME**, we need to verify if there is a **Network Slice** for  **Service Type** that is requested.

    - **3.a** If there is no Network Slice that can serve the UE, the NSSF will trigger a request to ..... for creating a Connection that can serve the UE **(This is not implemented in our scenario)** *If for some reason we reach this stage in our scenario, the connection is interrupted*  

    - **3.b** When there is a Slice with the right Type of Service, the **NSSF** will get the **NSId** that corresponds to the **Service Type** and forward it to the **vMME** as part or the connection information required for Authentication.

4. When the MME reply our attach request, we add in our Local Connection Database, the **UEId** that is registered in the connection.

5. The **NSSF** will update the Slice Database, assigning for each slice, which UE and Core Network Instance is gonna be served.

6. Proceed to register the **NSId** in the Local Connection Database, that way it is possible to know which **UE** is assigned to which **NS** while the connection is still active.

7. Once we reach this step, we need to complete the connection information that is going to be contained inside the **MDDVector** which is an object similar to the one that we received from the **vBBU** at the beginning of the flow, but with the addition of a **NSId** plus a **Temporary ID** that contains the **UEId** plus other Core Network information received from the **MME** during the attach procedure.

8. Once we have the **MDDVector** we will reply it to the **vBBU** ending the Attach/Reattach Request Procedure.

### Functionality During Detach

When the Detach procedure is triggered, the NSSF will do Two tasks:
1. It will update the Network Slice Database, removing the **UEId** that was assigned to the Network Slice. This way we clean the Slices that are being served.
2. It will erase all the UE related information from the Local Connection Database. Effectively disconnecting the device from the network.

## Code

The present GitHub repository has 3 directories for running the module:
  - **bjsonrpc** Which contains all the functionality of the Remote Procedure Calls that allow communication between the modules. *This code is from an Open Source repository, it is a modified JSON RPC made by David Martínez Martí.*
  You can follow the link here for more information about it: [Deavid Repo](https://github.com/deavid/bjsonrpc)
  - **src** It is where the actual code of the NSSF reside
  - **testScenario** As you may see, the NSSF is not a standalone function, and because it sits between the **vBBU** and the **MME** the functionality requires that every module that is part of the Mobile Network Scenario to be Running too. Nonetheless for having local tests of the module I provide some Attach and Detach clients that can be run in a single machine to illustrate the functionality of it.

Steps on how to run the Code and the requirements that are needed for having a Deployment Environment are in the User Guide that you can access inside the **src** folder or in this [here](https://github.com/ncl427/NSSF/blob/master/src/UserGuide.md)

## Impact of the NSSF in our Mobile Network scenario

Because the NSSF has a very specific role, the existence of this Function is mandatory if we want to have **E2E slicing** inside a Mobile Network, or any kind of Network that requires slicing. *Although is not possible to see right now*, the functionality of **NSSF** really comes into place, when the number of Slices that are created in a Network is High and there is a mechanism to provide Dynamic Network Slice Creation.

## Glossary
- **3gpp** The 3rd Generation Partnership Project
- **E2E** End to End slicing
- **MME** Mobile Management Entity
- **MDDVector** Multi Dimensional Descriptor Vector
- **NS** - **NSId** Network Slice, Network Slice Id
- **NSSF** Network Slice Selection Function
- **vBBU** Virtual Broadband Base Unit
