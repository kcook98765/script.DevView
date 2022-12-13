"""
Initail code from: https://github.com/romanvm/plugin.video.example
video plugin that is compatible with Kodi 19.x "Matrix" and above
"""
import sys, re
import xbmcvfs
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
import xbmcaddon
import os
import pickle
import json
import sqlite3
import contextlib



# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])


ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ID = ADDON.getAddonInfo("id")

profilePath = xbmcvfs.translatePath( ADDON.getAddonInfo('profile') )
if not os.path.exists(profilePath):
    os.makedirs(profilePath)

DB_PATH = xbmcvfs.translatePath(os.path.join(profilePath, 'devview4.db'))


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(_URL, urlencode(kwargs))

def show_directory():
    # Show available lists
    xbmcplugin.setPluginCategory(_HANDLE, 'DevView Report')
    xbmcplugin.setContent(_HANDLE, 'videos')

    # make a listitem for each report section
    DB = sqlite3.connect(DB_PATH)
    query = "SELECT A.code_type FROM results AS A WHERE 1 GROUP BY A.code_type ORDER BY A.code_type"
    
    try:
        cursor = DB.cursor()
        cursor.execute(query)
        db_data = cursor.fetchall()
        
    except:
        debug = 'script.DevView - DB Connection/sql error'
        xbmc.log(debug, level=xbmc.LOGINFO)


    else:
        for stuff in db_data:
            
            if stuff[0] == 'JsonRPC':
                # produce entries for each type
                
                query2 = "SELECT A.base_code FROM results AS A WHERE A.code_type = 'JsonRPC' GROUP BY A.base_code ORDER BY A.base_code"
                
                try:
                    cursor2 = DB.cursor()
                    cursor2.execute(query2)
                    db_data2 = cursor2.fetchall()
                    
                except:
                    debug = 'script.DevView - DB Connection/sql error (2)'
                    xbmc.log(debug, level=xbmc.LOGINFO)
            
            
                else:
                    for stuff2 in db_data2:
                        this_label = 'JsonRPC-' + stuff2[0]

                        list_item = xbmcgui.ListItem(label=this_label)
                        list_item.setInfo('video', {'title': this_label,
                                                'genre': '',
                                                'mediatype': 'video'})
                        is_folder = True
                        list_url = get_url(action='listing', dbName=this_label)
                        # log( filename, LOGNOTICE);
                        xbmcplugin.addDirectoryItem(_HANDLE, list_url, listitem=list_item, isFolder=is_folder)
                        # Add a sort methods for the virtual folder items
                        xbmcplugin.addSortMethod( _HANDLE, xbmcplugin.SORT_METHOD_TITLE)                
                
            else:
                list_item = xbmcgui.ListItem(label=stuff[0])
                list_item.setInfo('video', {'title': stuff[0],
                                        'genre': '',
                                        'mediatype': 'video'})
                is_folder = True
                list_url = get_url(action='listing', dbName=stuff[0])
                # log( filename, LOGNOTICE);
                xbmcplugin.addDirectoryItem(_HANDLE, list_url, listitem=list_item, isFolder=is_folder)
                # Add a sort methods for the virtual folder items
                xbmcplugin.addSortMethod( _HANDLE, xbmcplugin.SORT_METHOD_TITLE)

        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(_HANDLE)

def show_details(dbName):

    DB = sqlite3.connect(DB_PATH)
    
    # JsonRPC - specific call
    if re.search("^JsonRPC",dbName) :
        # split off the actual call (after the hyphen) and run insert here
        [dbName, jcall] = dbName.split('-')

        try:
            cursor = DB.cursor()
            cursor.execute("""
                SELECT A.base_code,A.code_run,A.results
                FROM results AS A 
                WHERE A.code_type = ? AND A.base_code = ? ORDER BY A.base_code,A.code_run
                """, [dbName, jcall])
            db_data = cursor.fetchall()
            
        except:
            debug = 'script.DevView - DB Connection/sql error (3)'
            xbmc.log(debug, level=xbmc.LOGINFO)
    
        else:
            for stuff in db_data:
                title = str(stuff[1])
                plot = str(stuff[2])
   
                this_infolabels = {
                    "title": title,
                    "plot": plot,
                }
        
                li = xbmcgui.ListItem(str(stuff[1]))
                li.setProperty('IsPlayable', 'false')
                li.setInfo(type="video", infoLabels=this_infolabels)
    #                li.addContextMenuItems( commands )
                is_folder = False
                
                filename = ''
        
                # Add listitem to directory
                xbmcplugin.addDirectoryItem(_HANDLE, url=filename, listitem=li, isFolder=is_folder)
    
                
            breadrumb = "DevView / " + dbName + ' - ' + jcall
            xbmcplugin.setPluginCategory(_HANDLE, breadrumb)
            xbmcplugin.setContent(_HANDLE, "movies")  # Container.Content
            xbmcplugin.endOfDirectory(_HANDLE)







    
    
    else:
    
        try:
            cursor = DB.cursor()
            cursor.execute("""
                SELECT A.base_code,A.code_run,A.results,
                B.notes,V.notes
                FROM results AS A 
                LEFT JOIN listitem AS B ON B.listitem = A.base_code
                LEFT JOIN infotag AS V ON V.function_name = A.base_code
                WHERE A.code_type = ? ORDER BY A.base_code,A.code_run
                """, [dbName])
            db_data = cursor.fetchall()
            
        except:
            debug = 'script.DevView - DB Connection/sql error (4)'
            xbmc.log(debug, level=xbmc.LOGINFO)
    
        else:
            for stuff in db_data:
                title = str(stuff[1])
                plot = str(stuff[2])
                if stuff[3] != '' and stuff[3] != None:
                    plot = plot + "\n" + ' (' + str(stuff[3]) + ')'
                elif stuff[4] != '' and stuff[4] != None:
                    plot = plot + "\n" + ' (' + str(stuff[4]) + ')'
                 
    
                this_infolabels = {
                    "title": title,
                    "plot": plot,
                }
        
                li = xbmcgui.ListItem(str(stuff[1]))
                li.setProperty('IsPlayable', 'false')
                li.setInfo(type="video", infoLabels=this_infolabels)
    #                li.addContextMenuItems( commands )
                is_folder = False
                
                filename = ''
        
                # Add listitem to directory
                xbmcplugin.addDirectoryItem(_HANDLE, url=filename, listitem=li, isFolder=is_folder)
    
                
            breadrumb = "DevView / " + dbName
            xbmcplugin.setPluginCategory(_HANDLE, breadrumb)
            xbmcplugin.setContent(_HANDLE, "movies")  # Container.Content
            xbmcplugin.endOfDirectory(_HANDLE)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))

    if params:
        if params['action'] is not None:
            if params['action'] == 'listing':
                show_details(params['dbName'])
            else:
                debug = 'script.DevView - Action Unknown : ' + str(params['action'])
                xbmc.log(debug, level=xbmc.LOGINFO)
    else:
        # called without action param, so display "directory" of report sections
        show_directory()
    
    
if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
    
