taxonomy:

 - owner  : controls access / authentication
 - author : owner of segment(s)

-- Contributors --

 Ian Jones, ianjones@umich.edu
 Bob Kuehne, rpk@blue-newt.com, aim: rpk@mac.com
 Abhay Saxena, ark3@email.com
 Mike "bear" Taylor, bear@code-bear.com, aim: codebear42, msn: bear@code-bear.com
 Nick Bastin, nbastin@mac.com, aim: mondragon0
 Andrew Harrington, anh@cs.luc.edu, aim: 
 Linden Wright, lwright@mac.com, aim: Kusmeroglu
 Andrew Wright,,
 Jeffrey ...,,

-- source repo, defect mgmt, etc. --
http://developer.berlios.de/projects/fuse/
dev svn access:     svn+ssh://username@svn.berlios.de/svnroot/repos/fuse/
anon svn access:    svn co svn://svn.berlios.de/fuse

-- features --
  - authentication
    - subetha-style approve/deny on per-person basis
    - password control access to doc
    - batch approval, rejection
    - global notification of pending users
    - read/write approval on a per-participant basis
  - client undo open issue. undo is weird.
      (bear: something tells me undo will be server side only and passed to all
             - yeah, this bears (pi) further debate)
  - later, non-text edits. have events that support payloads of
    things other than text blocks. and other doc types. for
    example, payloads of images, formatted text, etc.
  - rehost server
  - Better local save support - no requirement for continual Save Copy As...
  - Also shared save support, I suppose - like on LAN NFS - everybody saves to the same point
      (some way of passing a uri or webdav or ???)

 notes
   - text sequences are a logical unit. two kinds:
    - whitespace
    - contiguous char+syms
   - cli/srv is sync in that char entered on cli don't appear on
   
-- old model --
    dataflow (client)
        client: user types text / edits / moves / selects
        client: packages text into an edit event, sends to server
        server: reflects event to all clients
        client: displays incoming events from server _only_
        client: retains list of recent server events as undo stack
        
    dataflow (server)
        server: waits for client connections
        server: when client connects, sends initial 'insert' event with current text
        server: waits for further client events (self is client too)

-- urls --

py lib/test/execthing:    http://codespeak.net/py/current/doc/
pyzeroconf:               http://sourceforge.net/projects/pyzeroconf
pyzeroconf disc:          http://www.amk.ca/python/zeroconf

