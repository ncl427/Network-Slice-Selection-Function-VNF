from bjsonrpc.handlers import BaseHandler
from bjsonrpc import createserver
from NSSF import attach, dettach
import threading
import time
import pickle


class ServerHandler(BaseHandler):

    def networkAttach(self,ConnObject):
        return pickle.dumps(attach(MDDvector))

    def networkDetach(self,ConnObject):
        dettach(MDDvector)



#def thread():
time.sleep(0.2)
print "NSSF Running"
s = createserver(host="127.0.0.1", port = 10123, handler_factory=ServerHandler)
s.debug_socket(True)
s.serve()

#threading.Thread(target=thread).start()
