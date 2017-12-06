from bjsonrpc import connect
from bjsonrpc.handlers import BaseHandler
from NSlice import UENS
import pickle


c = connect(host="127.0.0.1",port=10123)

MDDVector = UENS(4,50)
pickledMDDVector = pickle.dumps(MDDVector)
Authentication = pickle.loads(c.call.networkAttach(pickledMDDVector))
# do something here ...
print "Network State -", "User Equipment:", Authentication.UEId, "Will connect",
print "to Network Slice:", Authentication.NSId
