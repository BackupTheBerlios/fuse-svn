#!/usr/bin/env python

import sys
import logging
import random

from objc import YES, NO
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder

import twisted.internet.cfreactorreactor = twisted.internet.cfreactor.install()from twisted.internet import deferfrom twisted.web.xmlrpc import Proxy
from twisted.spread import pb

from client import EditorRoot
import events

##
# constant placeholders -- to be replaced with looked-up or pref values

SERVER_HOST_NAME = "subpython.local."
SERVER_PORT = 8910
USERNAME = "me"
DOCNAME = "Untitled"

##
# constants

COLORS = ['black', 'blue', 'green', 'magenta', 'orange']

##
# logging init

logging.basicConfig()
logging.getLogger('').setLevel(logging.INFO)
log = logging.getLogger(__name__)

##
# rdvz announce service
import time

rdvz_type   ="_fuse._tcp"
rdvz_domain = ""
rdvz_port   = SERVER_PORT
rdvz_name   = "the fused thing"

class AnnounceDelegate(NSObject):

# note to self, figure out how to stick actual obj init code
# in the init() called from alloc().init() ish

    def initmyself(self):
        self.services = []

    def netServiceWillPublish_( self, svc ):
        pass
        # print ">>> netServiceWillPublish_"

    def netService_didNotPublish( self, svc, errordict ):
        pass
        # might want to handle this
        # print ">>> netService_didNotPublish"

    def netServiceDidStop( self, svc ):
        pass
        # might want to handle this
        # print ">>> netServiceDidStop"

####################
# text view delegate - gather and package selection events, etc

class TextViewDelegate(NSObject):
    def textViewDidChangeSelection( self, notif ):
        print 'textViewDidChangeSelection_'

##
#

class Event:
    """placeholder for a future real event"""
    def __init__(self, data, nscolor):
        self.data = data
        self.nscolor = nscolor
     
def randomColor():
    return getattr(NSColor, "%sColor" % COLORS[random.randrange(len(COLORS))])()


##
# app delegate

#NibClassBuilder.extractClasses("MainMenu")
#
#class AppDelegate(NibClassBuilder.AutoBaseClass, NSApplicationDelegate):
#        
#    def applicationDidFinishLaunching_(self, aNotification):
#        log.debug('app did finish launching')

##
# document

NibClassBuilder.extractClasses("FuseDocument")

class FuseDocument(NibClassBuilder.AutoBaseClass):
    # actual base class is NSDocument
    
    """outlets:
            - mainText: main text entry widget, an NSTextView
            - sharingButton
            - sharingStatusLabel
    """
    
    ##
    # ivars -- set in windowControllerDidLoadNib()
    #       - path: path to file
    #       - isshared: boolean, whether document is accepting connections
    
    ##
    # class vars
    
    sharingStates = {True: ('Stop', 'Document sharing on'), False: ('Stop', 'Document sharing off')}
    
    def updateSharingStatusDisplay(self):
        state = self.sharingStates[self.isshared]
        self.sharingButton.setTitle_(state[0])
        self.sharingStatusLabel.setStringValue_(state[1])
        
    def docLabel(self):
        """provide a simple info label for this document"""
        return "%(DOCNAME)s / %(USERNAME)s@%(SERVER_HOST_NAME)s:%(SERVER_PORT)s" % globals()
        
    # called by receiver of network events from server
    def handleEditEvent(self, anEventString ):
        log.debug("handling event: " + anEventString )
#        attributes = NSDictionary.dictionaryWithObject_forKey_(anEvent.nscolor, NSBackgroundColorAttributeName)
#        attrString = NSAttributedString.alloc().initWithString_attributes_(anEvent.data, attributes)
        payload = events.unpackevent(anEventString)['text']  # text
        attrString = NSAttributedString.alloc().initWithString_(payload)
        insertionPoint = self.mainText.selectedRange()[0]
        self.mainText.textStorage().insertAttributedString_atIndex_(attrString, insertionPoint)

    # called by the twisted reactor when there's an event
    def callRemote(self, eventName, event):
        log.debug("received event %s: %s" % (eventName, event))
        self.handleEditEvent(event)
        
    ##
    # IB actions
    
    def toggleSharing_(self, sender):
        self.isshared = not self.isshared
        self.updateSharingStatusDisplay()
        # tell reactor to listen/not listen
        # ... (not implemented yet)
        
    
    ##
    # NSDocument delegate methods
    
    # receives keyboard events as text view's delegate
    def textView_shouldChangeTextInRange_replacementString_(self, aTextView, affectedCharRange, replacementString):
        """delegate method of mainText NSTextView, reroutes key to event 'queue' """
        log.debug("new string: " + replacementString)
        # outbound to server
        myEvent = events.packevent(0, 'local', text=replacementString)
        self.editResponder.remote_event(myEvent)
#        self.handleEditEvent(Event(replacementString, randomColor()))
        return NO  # disallows edit in textview, return YES to accept
        
    ##
    # NSDocument overrides
    
    def windowNibName(self):
        return "FuseDocument"

    def readFromFile_ofType_(self, path, tp):
        if self.mainText is None:
            # we're not yet fully loaded
            self.path = path
        else:
            # "revert"
            self.readFromUTF8(path)
        return True

    def writeToFile_ofType_(self, path, tp):
        f = file(path, "w")
        text = self.mainText.string()
        f.write(text.encode("utf8"))
        f.close()
        return True

    # adhoc init method until we put in a real one
    def windowControllerDidLoadNib_(self, controller):
        self.isshared = False
        try:
            if self.path:
                self.readFromUTF8(self.path)
        except AttributeError:
            self.path = None
 
        ##
        # add the delegate for rdvz to our app
        service = NSNetService.alloc().initWithDomain_type_name_port_(
                rdvz_domain, rdvz_type, rdvz_name, rdvz_port)
        adel    = AnnounceDelegate.alloc().init()
        adel.initmyself()
        if service is not None:
            service.setDelegate_( adel )
            service.publish()
 
        ##
        # add the delegate for the textview
        tvd = TextViewDelegate.alloc().init()
        self.mainText.setDelegate_( tvd )

        # twisted reactor stuff
        if not reactor.running:
            log.debug('starting cfreactor')
            # copied out of client.py:server_main()
            self.editResponder = EditorRoot()
            self.editResponder.remote_attach(self)  # commits us to support callRemote(evtName, evt) method            f = pb.PBServerFactory(self.editResponder)
            p = reactor.listenTCP(8910, f)
            reactor.run()

    def readFromUTF8(self, path):
        f = file(path)
        text = unicode(f.read(), "utf8")
        f.close()
        self.mainText.setString_(text)
    
##
# main

if __name__ == '__main__':
    sys.exit(NSApplicationMain(sys.argv))
