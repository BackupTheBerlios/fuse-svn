#!/usr/bin/env python

# fuse server

import sys

import twisted.spread.newjelly
from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import log

log.startLogging(sys.stdout)

# http://twistedmatrix.com/documents/howto/pb-copyable

class EditorRoot(pb.Root):
#    __implements__ = (pb.IPBRoot,)

    def __init__(self):
        self.notificationList = []
        self.version = 0.1

    def remote_event(self, event):
        """
        Receive client events and process according to event class
        Event Types:  attach, detach, sync, insert, delete, cursor, ???
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

# refactor: use twisted.Application (launch via twistd)
def main():
    f = pb.PBServerFactory(EditorRoot())
    p = reactor.listenTCP(8910, f)
    reactor.run()

if __name__ == '__main__':
    main()
