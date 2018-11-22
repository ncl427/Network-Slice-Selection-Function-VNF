# Network Slice Selection Function NSSF
# M-CORD Based
## Introduction
A Network Slice Selection Function is in charge of making the selection of an appropriate Network Slice in base of some parameters that a **UE** will send when it wants to attach to a Network. In the next sections the level of functionality achieved and the steps that are required for running this module will be described

## Description
The **NSSF** is part of the 3gpp solution for having E2E slicing in a Mobile Network. According to documentation of the 5G Architecture,
the **NSSF** sits beside Access and Mobility Function **AMF**. As we are working with 4G open source components we have replaced the **AMF**  interaction by using the **MME**
According to **3gpp** documentation during Session Establishment the NSSF will be involved in Reselection of a Network Slice only if, the Network Configuration changed. Because of this is not part of the scope of our project, Slice reselection is not included in the functionality.

The current functionality present in the code is:
- Assign a Network Slice during Network Attach procedure
- Erase UE slice assignation during the Network Detach procedure *In progress*

It is important to make clear, the NSSF is not in charge of doing the Attach/Reattach procedure, it only passes the information received from **MME**, and once the UE is allowed to have connection will assign the Network Slice based on the Type of Service that the UE requires.

### Functionality during UE Attach/Reattach procedure
The following Flow chart, shows the Attach/Reattach procedure of the NSSF

![ALT text](/Images/NSSF.png "Flowchart of the Network Slice Selection Function")

The process for slice selection is the following:
 1. The **UE** sends the connection message to the **vMME** by means of the **eNodeB emulator (OAISIM)**. This information includes: *PLMN, IMSI, MNC, MCC.*

 2. The **vMME** forwards the **UE** information to the **vHSS** for checking if it is allowed to attach and register to network.

 3. Once the **vHSS** approves the **UE**, the **vMME** will forward the *IMSI* of the **UE** to the **NSSF** during session request.

 4. The **NSSF** will verify the *IMSI* and see if there is a specific **vSPGW** that can serve the connection.
    - a)	If the **vSPGW** exists, the **NSSF** will reply the **vMME** with the Id (Ip address) of the **vSPGW** that will be  used to serve.
    - b)	If it does not exist, it will use a default **vSPGW** for session establishment.

### Functionality During Detach

When the Detach procedure is triggered, the NSSF will do Two tasks:
1. It will update the Network Slice Database, removing the **UEId** that was assigned to the Network Slice. This way we clean the Slices that are being served.
2. It will erase all the UE related information from the Local Connection Database. Effectively disconnecting the device from the network.

## Code

The present GitHub repository has 1 directories for running the module:
  - **src** It is where the actual code of the NSSF reside

Steps on how to run the Code and the requirements that are needed for having a Deployment Environment are in the User Guide that you can access inside the **src** folder or in this [here](https://github.com/ncl427/NSSF/blob/master/src/UserGuide.md)

## Impact of the NSSF in our Mobile Network scenario

Because the NSSF has a very specific role, the existence of this Function is mandatory if we want to have **E2E slicing** inside a Mobile Network, or any kind of Network that requires slicing. The functionality of **NSSF** really comes into place, when the number of Slices that are created in a Network is High and there is a mechanism to provide Dynamic Network Slice Creation *M-CORD*.

## Acknowledgment
This research was supported by the MSIP (Ministry of Science, ICT and Future Planning), Korea, under the ITRC (Information Technology Research Center) support program (IITP-2017 2017-0-01633) supervised by the IITP (Institute for Information & communications Technology Promotion.

## Glossary
- **3gpp** The 3rd Generation Partnership Project
- **E2E** End to End slicing
- **MME** Mobile Management Entity
- **AMF** Access and Mobility Function
- **NSSF** Network Slice Selection Function
