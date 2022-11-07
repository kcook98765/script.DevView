import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import sys, re, os
import json
from genreport import *

# used logviewer code to help display info
# https://github.com/i96751414/script.logviewer

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ID = ADDON.getAddonInfo("id")

KEY_NAV_BACK = 92
ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10


def window(title, content):
    w = TextWindow("script.DevView-textwindow-fullscreen.xml", ADDON_PATH, title=title, content=content)
    w.doModal()
    del w

class TextWindow(xbmcgui.WindowXMLDialog):
    def __init__(self, xml_filename, script_path, title, content):
        super(TextWindow, self).__init__(xml_filename, script_path)
        self.title = title
        self.content = content
        # Controls IDs
        self.close_button_id = 32500
        self.title_label_id = 32501
        self.text_box_id = 32503

    def onInit(self):
        # noinspection PyUnresolvedReferences
        self.getControl(self.title_label_id).setLabel(self.title)
        # noinspection PyUnresolvedReferences
        self.getControl(self.text_box_id).setText(self.content)

    def onClick(self, control_id):
        if control_id == self.close_button_id:
            # Close Button
            self.close()

    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK, ACTION_PREVIOUS_MENU]:
            self.close()


if __name__ == '__main__':
    # run report
    debug = 'DevView: calling gather_data()'
    xbmc.log(debug, level=xbmc.LOGINFO)
    
    report = report()
    report.gather_data()
    
    debug = 'DevView: completed call to gather_data()'
    xbmc.log(debug, level=xbmc.LOGINFO)    
    
    
    # sleep until report complete
#    while (xbmcgui.Window(xbmcgui.getCurrentWindowId()).getProperty("DevView.ExternalRunning") == "True"):
#        time.sleep(1)

    # now display the custom window with data from the index.html file
    profilePath = xbmcvfs.translatePath( ADDON.getAddonInfo('profile') )
    file = os.path.join(profilePath, 'index.html')
    with xbmcvfs.File(file) as data:
        content = data.read()
    
    window(ADDON_NAME, content)
    
    




            