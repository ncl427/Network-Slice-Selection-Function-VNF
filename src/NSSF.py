import rpyc
import threading
import MySQLdb
import sys
import time
import Queue
from rpyc.utils.server import ThreadedServer

connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "linux", db = "nssf_db")
q = Queue.Queue()
cursor = connection.cursor ()

class NssF(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        q.put("quit")
        print ("\n")
        print ("*****Connection Established*******")
        time.sleep(0.5)
        print ("\n")
        cursor.execute ("select s.service, pg.pgwc_ins from spgwc pg join services s on pg.id = s.id")
        # fetch all of the rows from the query
        data = cursor.fetchall ()
        print "NSSF can serve the following slices"
        print ("\n")
        #Counter and For Loop for showing the Slices that are available
        counter = 0
        for row in data :
            counter +=1
            print "Slice ",counter,": for Service ",row[0]," is served by SPGW ",row[1]
        pass


    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        """We are going to erase the Slice information of the UE that was connected"""
        # (to finalize the service, if needed)
        pass

    def exposed_selectSlice(self, uEId, sliceDiff): # this is an exposed method
        serviceId = sliceDiff
        ueId = uEId
        query = ("select pgwc_ins from spgwc "
                 "where id = %s ")
        cursor.execute (query, (serviceId, ))
        isSlice = cursor.fetchall ()
        #Checks if Slice exists if not, selects the Default Slice - WEB
        if not isSlice:
            print "\n"
            print "Slice for that type of service does not exist"
            print "Assigning to Default Slice"
            print "\n"
            slice = self.get_defaultSlice()
            #Inserts UE and Servie in Slice DB for local handler
            self.insertSlice(ueId,1)
        else:
            counter = 0
            for row in isSlice :
            #    print row
                counter += 1
            slice = row[0]
            #Inserts UE and Service in Slice DB for local handle
            self.insertSlice(ueId,serviceId)
        return slice

    def insertSlice(self, uEId, sliceDiff):  # while this method is not exposed
        verify_slice = "select users_imsi, slice_diff from slices where users_imsi = %s and slice_diff = %s"
        cursor.execute(verify_slice, (uEId, sliceDiff))

        verify = cursor.fetchall()

        if not verify:
            add_slice = ("insert into slices "
                        "(users_imsi, slice_diff)"
                        "values (%s, %s)")
            cursor.execute (add_slice, (uEId, sliceDiff))
            connection.commit()
        else:
            pass
        #After Inserting the Slice Relationship
        #Shows the Full Information of Slices that is Available
        self.showFullSlice()
        print "User Information added to Local DB"
        pass

    def get_defaultSlice(self):
        query = ("select pgwc_ins from spgwc "
                 "where id = 1")
        cursor.execute (query)
        default = cursor.fetchall ()
        for row in default :
            print "Default Slice Slected: ",row[0]
        return row[0]

    def showFullSlice(self):
        #Shows the Full table of UE assigned to an Slice in the Slices DB
        query = ("select ns.id, ns.users_imsi, s.service, pg.pgwc_ins "
                 "from slices ns, spgwc pg, services s "
                 "where ns.slice_diff = s.id and ns.slice_diff = pg.id")
        cursor.execute (query)
        data = cursor.fetchall ()
        print ("\n")
        print "Connection Information inside NSSF"
        print ("\n")
        for row in data:
            print row
        pass

def run():
    """ Method that runs forever """
    """Good for Verbosity"""
    while True:
        try:
            item = q.get(True, 1)
            if item == 'quit':
                break
        except:
            pass
        print("Listening for request from the vMME")
        print("...")
        time.sleep(0.5)
        print("...")
        time.sleep(0.5)


if __name__ == "__main__":
    t = ThreadedServer(NssF, port=18861)
    print ("\n")
    print "***************************************************"
    print "*Network Slice Selection Function Service Starting*"
    print "***************************************************"
    print ("\n")
    thread = threading.Thread(target=run, args=())
    thread.daemon = True                            # Daemonize thread
    thread.start()                                # Start the execution
    t.start()
