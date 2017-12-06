from bjsonrpc import connect
from bjsonrpc.handlers import BaseHandler
from NSlice import UENS
import pickle


c = connect(host="127.0.0.1",port=10123)

MDDVector = UENS(20,50)
pickledMDDVector = pickle.dumps(MDDVector)
c.call.networkDetach(pickledMDDVector)
# do something here ...
print "User Equipment Disconnected"
