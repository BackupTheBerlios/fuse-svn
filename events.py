#!/usr/bin/env python
# SubPythonEdit Event Classes

import os, unittest
from twisted.spread import pb
#from twisted.spread.flavors import Copyable
#import twisted.spread
#import twisted.spread.flavors

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

def packevent( user='', type=fuseInsert, begpos=0, endpos=0, text='',  ):
    return '%s,%s,%d,%d,%s'%(user,type,begpos,endpos,text)
    
def unpackevent( evstring='' ):
    return evstring.split(',')

######################################################################

class eventTester(unittest.TestCase):
    
    def setUp(self):
        pass

    def createDelete(self):
        # how to instantiate the class hierarchy automatically?
        self.assertEqual( True, True )

######################################################################

def main():
    print "%d/%d event tests ran, %d passed"%( 0, 0, 0 )

if __name__ == '__main__':
    unittest.main()

