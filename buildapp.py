from bundlebuilder import buildapp
from plistlib import Plist, Dict

plist = Plist(
    CFBundleDocumentTypes = [
        Dict(
            CFBundleTypeExtensions = ["txt", "text", "*"],
            CFBundleTypeName = "Text File",
            CFBundleTypeRole = "Editor",
            NSDocumentClass = "FuseDocument",
        ),
    ]
)

buildapp(
	mainprogram = "fuse_gui_client.py",
	nibname = "MainMenu",
	resources = ["MainMenu.nib", "FuseDocument.nib", "client.py", "events.py"],
	plist = plist
)
