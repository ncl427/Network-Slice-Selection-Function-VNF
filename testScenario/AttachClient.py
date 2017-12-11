from bjsonrpc import connect
from bjsonrpc.handlers import BaseHandler
from Mdd import Mdd
import pickle


c = connect(host="117.17.102.129",port=10123)

#MDDVector = MDDVector(4,"117.17.102.21")
#pickledMDDVector = pickle.dumps(MDDVector)
Authentication = pickle.loads(c.call.networkAttach("117.17.102.21", 4))
# do something here ...
print "Network State -", "User Equipment:", Authentication.nesId, "Will connect",
print "to Network Slice:", Authentication.nesId
