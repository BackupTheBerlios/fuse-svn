#!/usr/bin/env python
# Subetha edit paper here: http://squeak.local./~twl/subethaedit-paper.pdf
# SubPythonEdit Client and Server Piece
#  Jean-Paul "exarkun" Calderone
#  Allen "dash" Short
#  Abhay "ark3" Saxena

import sys, socket
from optparse import OptionParser

from twisted.spread import pb
import twisted.spread.newjelly

# cocoa imports go here, before the reactor is imported.
"""
from twisted.internet import cfsupport
cfsupport.install(top-level-object)
"""

from twisted.internet import reactor
from twisted.python import log

import events

# XXX ought to pick appropriate name for log file based on
# server/client status and client unique ID
#log.startLogging(open("sub.log", 'w')) 
log.startLogging(sys.stdout)

# nasty global thingy
spe_port = 8910
spe_hostname = ''
spe_server = 'client'

# ------------------------------------------------------------------
# Server Code
# ------------------------------------------------------------------

# http://twistedmatrix.com/documents/howto/pb-copyable
class EditorRoot(pb.Root):
    #__implements__ = (pb.IPBRoot,)

    def __init__(self):
        self.notificationList = []
        self.version = 0.1

    def remote_event(self, event):
        """
        Receive client events and process according to event class
        Event Types:  insert/delete, cursor/select
            Sync is a large 'insert' -- see readme for idea caching
        """
        print 'Event received', event
        dead = []
        for client in self.notificationList:
            try:
                client.callRemote("event", event)
                # insert into pingList dictionary timestamp of last contact
                
            except pb.DeadReferenceError:
                dead.append(client)
        map(self.notificationList.remove, dead)

    def remote_attach(self, client):
        """
        Receive attach event from twisted - insert client into broadcast list
        """
        print 'Client attached', client
        self.notificationList.append(client)
        # add client name/id into ping list to track timed-out clients

    def remote_detach(self, client):
        """
        Receive detach event from twisted - remove client from the broadcast list
        """
        print 'Client detached', client
        self.notificationList.remove(client)
        # remove client name/id from ping list

# ------------------------------------------------------------------
# Client Code
# ------------------------------------------------------------------

class Client(pb.Referenceable):
    def remote_event(self, event):
        print 'Got an event', events.unpackevent( event )
#        print 'Got an event', repr( event )
# this dude calls the handleEditEvent in the pyobjc goop (manages the inbound event from twisted)
# like this:
#            self.handleEditEvent(Event(replacementString, randomColor()))
        

from twisted.internet import stdio  # This is going away, right?

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

# ------------------------------------------------------------------
# Main/Startup code
# ------------------------------------------------------------------

# refactor: use twisted.Application (launch via twistd)
def server_main(port):
    f = pb.PBServerFactory(EditorRoot())
    p = reactor.listenTCP(port, f)
    reactor.run()

def client_main(hostname, port):
    f = pb.PBClientFactory()
    rootDeferred = f.getRootObject()
    rootDeferred.addCallback(cbGotRootObject)
    rootDeferred.addErrback(ebGotRootObject)
    c = reactor.connectTCP(hostname, port, f)
    reactor.run()

# refactor: use twisted.Application (launch via twistd)
def main():
    parser = OptionParser()
    parser.add_option('-s','--server', action='store_true', dest='isserver',
                           default=False, help='configure me to be a server')
    parser.add_option('-n', '--hostname', dest='hostname', default='127.0.0.1',
                        help='Hostname of server')
    parser.add_option('-p', '--port', dest='port', default=8910,
                        help='subpythonedit server port')
    
    (options, args) = parser.parse_args()

    print options
    if options.isserver:
        # run as server
        # ...
        server_main(options.port)

    client_main(options.hostname, options.port)

if __name__ == '__main__':
    main()
    

