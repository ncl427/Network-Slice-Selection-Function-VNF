# Network Slice Selection Function USER GUIDE
## Installation steps
### Windows

First of all, we need to install Python 2.7 . (Make sure to add python to the Environment Variables)

After that we need to run the following commands:
```
pip install ZODB
pip install ZEO
```

If you get an error while installing `ZEO` you need to install `Microsoft Visual C++ Compiler for Python 2.7` from: [C++ Compiler](https://www.microsoft.com/en-us/download/details.aspx?id=44266).

After installing these dependencies and downloading/cloning the repository, navigate to `bjsonrpc/` folder in your `cmd` and run the following command:
```
python setup.py install
```
Which will install the required dependencies for working with `bJSON RPC`.

Next, proceed to [**How to Run Section**](https://github.com/ncl427/NSSF/blob/master/src/UserGuide.md#how-to-run).

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
sudo pip install ZODB
sudo pip install ZEO
```
After installing these dependencies and downloading/cloning the repository, navigate to `bjsonrpc/` folder in your `cmd` and run the following command:
```
sudo python setup.py install
```
Which will install the required dependencies for working with `bJSON RPC`.

## How to Run

Before we run our `NSSF Server` we need to initialize the **Data Base Server**. In `Terminal` or `cmd` navigate to `Database/` folder and run the following:
```
runzeo -C zeo.config
```
It will load the configuration for the local databases that are needed to store **connection** and **slice** information.

Then, navigate to the `src/` folder and open the `NSSFServer.py` with a *tex editor* and modify the Ip address to match the IP of the machine where we are gonna run the *server* (This machine)

After that, we need to open the `NSSF.py` file and modify the `vMMEIp` variable to match IP of the **vMME** machine

When the IPs are updated run the file `NSSFServer.py`:
```
python NSSFServer.py
```

The server will be ready to listen to requests from the **vBBU**
