# Network Slice Selection Function USER GUIDE
## Installation steps

### Linux

If you are running a fresh Linux installation first open `Terminal` and run:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential
```
After it finishes installing, make sure that you have `pip` installed in your machine by runnning:

```
sudo apt-get install python-pip
```
Then we proceed to install the pip dependencies as following:
```
pip install rpyc
```

## How to Run

As you know, this NSSF is part of a M-CORD deployment. It depends on a database that is created by the NSSF XOS Service which do all the configuration that is required for the VNF to work (Assign IP, Hosts, Database Script)

For it to run, the installation need to be part of a CORD deployment.
There is a script to automate the CORD installation procedure, based on version 4.0, you can find it in the main page of our repository *Not yet created*

The only step that can be done manually is running the RPC server by doing:
```
python nssf.py
```

The server will be ready to listen to requests from the **vMME**
