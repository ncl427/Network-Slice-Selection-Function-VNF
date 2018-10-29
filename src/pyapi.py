
import rpyc


def nssf(a):
    nSSAI = a
    service = nSSAI[-1:]
    c = rpyc.connect("10.0.10.2", 18861)
    b = c.root.selectSlice(a,service)
    print "Will compute", a

    return b
