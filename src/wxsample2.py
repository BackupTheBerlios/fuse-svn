import wx

import wx.stc as stc

ID_ABOUT=101
ID_EXIT=110

class MySTC(stc.StyledTextCtrl):
	EVENT_NAMES = ((stc.STC_MOD_INSERTTEXT, "InsertText"),
				   (stc.STC_MOD_DELETETEXT, "DeleteText"),
				   (stc.STC_MOD_CHANGESTYLE, "ChangeStyle"),
				   (stc.STC_MOD_CHANGEFOLD, "ChangeFold"),
				   (stc.STC_PERFORMED_USER, "UserFlag"),
				   (stc.STC_PERFORMED_UNDO, "Undo"),
				   (stc.STC_PERFORMED_REDO, "Redo"),
				   (stc.STC_LASTSTEPINUNDOREDO, "Last-Undo/Redo"),
				   (stc.STC_MOD_CHANGEMARKER, "ChangeMarker"),
				   (stc.STC_MOD_BEFOREINSERT, "B4-Insert"),
				   (stc.STC_MOD_BEFOREDELETE, "B4-Delete"),)
	def setNetwork( self, network ):
		"""Initialise the STC control with a network sink"""
		self.network = network

	def Hello(self):
		print 1

	def OnModified(self, evt):
		#print repr(self.GetText())
		print 'Event type'
		modType = evt.GetModificationType()
		bits = []
		for bit, name in self.EVENT_NAMES:
			if bit & modType:
				print name, bit
				bits.append( name )
		print evt.GetText()
		if modType & stc.STC_MOD_BEFOREINSERT and evt.GetText() == 'a':
			#self.Cancel()
			print "Cancel attempt"
		self.network.send( (bits, evt.GetText(), evt.GetPosition()) )

	def OnChar(self, evt):
		print "keycode:", evt.GetKeyCode()
		if evt.GetKeyCode() == ord('a'):
			print "Cancel attempt"
			return
		else:
			evt.Skip()

class Network( object ):
	def __init__( self, target ):
		"""Initialise the network with connection parameters"""
		self.target = target
	def send( self, message ):
		"""Send message to the other window (whereever it is)"""
		self.target.messageReceived( message )

class MainWindow(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(200, 100),
					   style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
		self.control = MySTC(self, -1, style=wx.TE_MULTILINE)
		self.CreateStatusBar() # A Statusbar in the bottom of the window
		stc.EVT_STC_MODIFIED(self.control, self.control.GetId(), self.control.OnModified)
		wx.EVT_CHAR(self.control, self.control.OnChar)
		self.Show(True)
	
	def setNetwork(self, network):
		self.network = network
		self.control.setNetwork(network)
		

class EchoWindow(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(200, 100),
					   style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
		self.control = MySTC(self, 1, style=wx.TE_MULTILINE)
		self.CreateStatusBar() # A Statusbar in the bottom of the window		
		self.Show(True)

	def messageReceived( self, message ):
		"""Handle an update message from the network"""
		print 'Got message on client', message
		bits, text, pos = message
		if "InsertText" in bits:
			self.preserved(self.onInsert, message)
		elif "DeleteText" in bits:
			self.preserved(self.onDelete, message)

	def onInsert(self, evt):
		bits, text, pos = evt
		self.control.InsertText(pos, text)

	def onDelete(self, evt):
		bits, text, pos = evt
		self.control.SetSelection(pos, pos+len(text))
		self.control.ReplaceSelection("")
				
	def preserved(self, func, evt, *args, **kargs):
		bits, text, pos = evt
		curanchor = self.control.GetAnchor()
		cursel = self.control.GetSelection()
		curpos = self.control.GetCurrentPos()
		print "Curpos: ", curpos
		print "curanchor:", curanchor, "pos:", pos, "len(text):", len(text), "cursel:", cursel
		# Logic problem here, this adjustment assumes deletion
		if curanchor > pos+len(text):
			curanchor -= len(text)
		elif curanchor > pos:
			curanchor = pos
		try:
			return func(evt, *args, **kargs)
		finally:
			self.control.SetAnchor(curanchor)
			self.control.SetSelection( * cursel)

app = wx.PySimpleApp()
frame = MainWindow(None, 200, "Hello World")
frame2 = EchoWindow(frame, 201, "dlroW olleH")
network = Network(frame2)
frame.setNetwork( network )
#app.SetTopFrame(frame)
app.MainLoop()