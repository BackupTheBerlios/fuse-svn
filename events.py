#!/usr/bin/env python
# SubPythonEdit Event Classes

import os, unittest
from twisted.spread import pb
#from twisted.spread.flavors import Copyable
#import twisted.spread
#import twisted.spread.flavors

# w a r n i n g
# w a r n i n g
# don't be fooled, these events aren't in use right now. use the
# packevent and unpackevent method at the bottom

######################################################################
# Data flavors. 
######################################################################

class Data:
    def __init__(self):
        pass

class textData( Data ):
    def __init__(self,text=''):
        self.text = text

######################################################################
# Event flavors
######################################################################

class Event( pb.Copyable ):
    """
    -source:    event poster, a unique id
    -data:      a python object (a string for keys, possibly other things?)
    -position:  (row, col) tuple
    -timestamp: set upon receipt at server
    """
    def __init__(self,position=(0,0)):
        self.id = 'fuse/subPythonEditEvent'
        self.position = position
        pass

######################################################################
class EditEvent( Event ):
    """
        insert object
        delete object
        undo
    """
    def __init__(self):
        pass

class InsertEvent( EditEvent ):
    """
    """
    def __init__(self,payload):
        self.payload = payload
        pass

class DeleteEvent( EditEvent ):
    """
    """
    def __init__(self):
        pass
    
######################################################################

class CursorEvent( Event ):
    """
    """
    def __init__(self):
        pass

class SelectEvent( CursorEvent ):
    """
        select region
    """
    def __init__( self, endpos=(0,0) ):
        self.endpos = endpos
        pass

######################################################################
# magic to make the class unpackable by both cli/srv
######################################################################

class receiverEvent( pb.RemoteCopy, Event ):
    pass
pb.setUnjellyableForClass( Event, receiverEvent )

# hack for event stuff for now

fuseInsert = 'insert'
fuseDelete = 'delete'
fuseCursor = 'cursor'
fuseSelect = 'select'

eventkeys = [ 'docnum', 'user', 'type', 'begpos', 'endpos', 'text' ]

def packevent( docnum=0, user='', type=fuseInsert, begpos=0, endpos=0, text='',  ):
    return '%d,%s,%s,%d,%d,%s'%(docnum, user,type,begpos,endpos,text)
    
def unpackevent( evstring='' ):
    return dict( zip( eventkeys, evstring.split(',') ) )

######################################################################

class eventTester(unittest.TestCase):
    
    def setUp(self):
        pass

    def testCreateDelete(self):
        # how to instantiate the class hierarchy automatically?
        self.assertEqual( True, True )

class eventPackTester(unittest.TestCase):
    
    def setUp(self):
        pass

    def testPackUnpack(self):
        preEventMap = { 'docnum':16, 'user':'rpk', 'type':fuseCursor,
                        'begpos':33, 'endpos':21, 'text':'this is a test' }
        packedEvent = packevent( preEventMap[ 'docnum' ], preEventMap[ 'user' ], preEventMap[ 'type' ],
                    preEventMap[ 'begpos' ], preEventMap[ 'endpos' ], preEventMap[ 'text' ] )
        postEventMap = unpackevent( packedEvent )
        print preEventMap, postEventMap
        self.assertEqual( preEventMap, postEventMap )

######################################################################

if __name__ == '__main__':
    unittest.main()

