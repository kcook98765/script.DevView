import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import sys, re, os
import json
from genreport import *

if __name__ == '__main__':
    # run report
    debug = 'DevView: calling gather_data()'
    xbmc.log(debug, level=xbmc.LOGINFO)
    
    report = report()
    report.gather_data()
    
    debug = 'DevView: completed call to gather_data()'
    xbmc.log(debug, level=xbmc.LOGINFO)    
    
    xbmc.executebuiltin('ActivateWindow(Videos,plugin://script.DevView,return)')




            