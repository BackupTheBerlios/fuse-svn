#!/usr/bin/env python
#Subetha edit paper here: http://squeak.local./~twl/subethaedit-paper.pdf
#SubPythonEdit Client Piece
# Jean-Paul "exarkun" Calderone
# Allen "dash" Short

import sys, socket
from twisted.spread import pb
from optparse import OptionParser
import events

# nasty global thingy
spe_port = 8910
spe_hostname = ''
spe_server = 'client'

# cocoa imports go here.
from twisted.internet import reactor

from twisted.python import log
#log.startLogging(open("sub.log", 'w'))

class Client(pb.Referenceable):
    def remote_event(self, event):
        print 'Got an event', events.unpackevent( event )
#        print 'Got an event', repr( event )
# this dude calls the handleEditEvent in the pyobjc goop (manages the inbound event from twisted)
# like this:
#            self.handleEditEvent(Event(replacementString, randomColor()))
        

from twisted.internet import stdio

def cbGotRootObject(root):
    print 'Got root object', root
    c = Client()
    stdio.StandardIO(UserInputProtocol(root, c))
    return root.callRemote('attach', c)
        
def ebGotRootObject(failure):
    print 'ONONONONONO', failure
    reactor.stop()

from twisted.protocols import basic

class UserInputProtocol(basic.LineReceiver):
    from os import linesep as delimiter
    
    def __init__(self, root, client):
        self.root = root
        self.client = client
        
    def lineReceived(self, line):
#        print 'Got a line' #from stdio
#        ev = events.Event( line )
        try:
#            self.root.callRemote('event', ev)
            user = '%s:%s'%(socket.gethostbyname(socket.gethostname()),'rpk')
            eventydoo = events.packevent( user, events.fuseInsert, 0, 0, line )
            self.root.callRemote('event', eventydoo )
        except pb.DeadReferenceError:
            print 'Server went away'
            reactor.stop()

# In the callback, we want
# something.root.callRemote('event', eventobject)
# event object should (for ease) subclass pb.Copyable
#  (other types Referenceable, Cacheable)
#

"""
from twisted.internet import cfsupport
cfsupport.install(top-level-object)
"""

# refactor: use twisted.Application (launch via twistd)
def main():
    parser = OptionParser()
    parser.add_option('-s','--server', dest='spe_server', default=False,
                        help='configure me to be a server')
    parser.add_option('-n', '--hostname', dest='spe_hostname', default='',
                        help='Hostname of server')
    parser.add_option('-p', '--port', dest='spe_port', default=8910,
                        help='subpythonedit server port')
    
    (options, args) = parser.parse_args()
    if len(sys.argv) > 1:
        hostname = sys.argv[1]
    else:
        hostname = "127.0.0.1"

    f = pb.PBClientFactory()
    rootDeferred = f.getRootObject()
    rootDeferred.addCallback(cbGotRootObject)
    rootDeferred.addErrback(ebGotRootObject)
    c = reactor.connectTCP(hostname, 8910, f)
    reactor.run()

if __name__ == '__main__':
    main()
    

