from StringIO import StringIO
from array import array
import Queue

#------------------------------------
# two simple events

class Event(object):

    def __init__(self):
        raise NotImplementedError
        
    def apply(self, buffer):
        """buffer is an array.array of type char"""
        raise NotImplementedError, "subclass must implement 'apply()'"

    def __repr__(self):
        return "%s: %s" % (type(self), self.__dict__)

        
class Insert(Event):
    """insert payload (a string), starting at index"""
    
    def __init__(self, userid, index, payload):
        self.userid = userid
        self.index = index #max(0, index)
        self.payload = payload
        
    def apply(self, buffer):
        "buffer is an array of char"
        assert 0 <= self.index <= len(buffer), (self.index, len(buffer))
        for i, char in enumerate(self.payload):
            buffer.insert(self.index + i, char)


class Delete(Event):
    """delete length characters from buffer, starting at index"""

    def __init__(self, userid, index, length):
        self.userid = userid
        self.index = index #max(0, index)
        self.length = length
        
    def apply(self, buffer):
        "buffer is an array of char"
        assert 0 <= self.index <= len(buffer), (self.index, len(buffer))
        assert self.length >= 0
        assert self.length+self.index <= len(buffer)
        for i in range(self.length):
            buffer.pop(self.index)


class Buffer(object):
    """representation of a document's bytes"""

    def __init__(self, initvalue=""):
        self._buf = array('c')
        for c in initvalue:
            self._buf.append(c)
    
    ##
    # delegate to self._buf
    
    def insert(self, i, c):
        self._buf.insert(i, c)
        
    def pop(self, i):
        self._buf.pop(i)
        
    def __repr__(self):
        return self._buf.tostring()
        
    def __len__(self):
        return len(self._buf)

##### delete tests 

def test_len():
    ss = "one"
    buf = Buffer(ss)
    assert len(buf) == len(ss)
    
def test_delete():
    ss = "abcdefghijklmnop"
    buf = Buffer(ss)
    d = Delete("bob", 5, 3)
    d.apply(buf)
    assert repr(buf) == "abcdeijklmnop"

def test_delete_posttail():
    ss = "abcdefghijklmnop"
    buf = Buffer(ss)
    d = Delete("bob", 22, 3)
    d.apply(buf)
    assert repr(buf) == "abcdeijklmnop"

def test_delete_prehead():
    try:
        ss = "aaa"
        buf = Buffer(ss)
        ii = Delete( "ian", -4, 3 );
        ii.apply(buf)
    except AssertionError, t:
        return
    assert 0

def test_delete_posttail():
    try:
        ss = "aaa"
        buf = Buffer(ss)
        ii = Delete( "ian", 44, 3 );
        ii.apply(buf)
    except AssertionError, t:
        return
    assert 0

# we might want to create two more of the complete perumtations, but we're lazy.
# test_delete_posttail_neglength
# test_delete_prehead_neglength

def test_delete_neglength():
    try:
        ss = "aaa"
        buf = Buffer(ss)
        ii = Delete( "ian", 0, -4 );
        ii.apply(buf)
    except AssertionError, t:
        return
    assert 0
    
##### insert tests

def test_insert_common():
    # common insert
    ss = "abcdeijklmnop"
    buf = Buffer(ss)
    d = Insert("abhay", 5, "fgh")
    d.apply(buf)
    assert repr(buf) == "abcdefghijklmnop"
    before = repr(buf)
    null = Insert("nugatory", 5, "")
    null.apply(buf)
    assert before == repr(buf)

def test_insert_head():
    ss = "aaa"
    buf = Buffer(ss)
    d = Insert("abhay", 0, "xxx")
    d.apply(buf)
    assert repr(buf) == "xxxaaa"

def test_insert_tail():
    ss = "aaa"
    buf = Buffer(ss)
    d = Insert("abhay", 3, "xxx")
    d.apply(buf)
    assert repr(buf) == "aaaxxx"

def test_insert_posttail():
    try:
        ss = "aaa"
        buf = Buffer(ss)
        ii = Insert( "ian", 44, "abcd" );
        ii.apply(buf)
    except AssertionError, t:
        return
    assert 0

def test_insert_prehead():
    try:
        ss = "aaa"
        buf = Buffer(ss)
        ii = Insert( "ian", -44, "abcd" );
        ii.apply(buf)
    except AssertionError, t:
        return
    assert 0

def test_assert():
    try:
        assert 0
    except AssertionError, t:
        return
    assert 0
    
#------------------------------------
# http://codespeak.net/py/current/doc/

