Contributors:

 Ian Jones ianjones@umich.edu
 Bob Kuehne rpk@blue-newt.com
 Mike "bear" Taylor bear@code-bear.com



"""
 features
  - authentication
  - client undo open issue. undo is weird.
  - later, non-text edits. have events that support payloads of
    things other than text blocks. and other doc types. for
    example, payloads of images, formatted text, etc.
  - rehost server

 notes
   - text sequences are a logical unit. two kinds:
    - whitespace
    - contiguous char+syms
   - cli/srv is sync in that char entered on cli don't appear on
   
"""

"""
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

"""

