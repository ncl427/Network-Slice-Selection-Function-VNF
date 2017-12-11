from bjsonrpc.handlers import BaseHandler
from bjsonrpc import createserver
from NSSF import attach, detach
from models.ueAttachObj import ueAttachObj
import threading
import time
import pickle


class ServerHandler(BaseHandler):

    def networkAttach(self, ConnObject):
        MDDVector = pickle.dumps(attach(ConnObject))
        return MDDVector

    def networkDetach(self,ConnObject):
        detach(ConnObject)



#def thread():
time.sleep(0.2)
print "NSSF Running"
s = createserver(host="117.17.102.129", port = 10123, handler_factory=ServerHandler)
s.debug_socket(True)
s.serve()

#threading.Thread(target=thread).start()
