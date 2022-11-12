import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import sys, re, os
import json
import xbmcvfs
import csv
import sqlite3
import contextlib
from cProfile import label

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ID = ADDON.getAddonInfo("id")

profilePath = xbmcvfs.translatePath( ADDON.getAddonInfo('profile') )
if not os.path.exists(profilePath):
    os.makedirs(profilePath)

DB_PATH = xbmcvfs.translatePath(os.path.join(profilePath, 'devview.db'))
SQL_PATH = xbmcvfs.translatePath(os.path.join(ADDON_PATH, 'resources', 'lib', 'tables.sql'))
DB_DATA_INFOTAG = xbmcvfs.translatePath(os.path.join(ADDON_PATH, 'resources', 'lib', 'infotag.csv'))
DB_DATA_LISTITEM = xbmcvfs.translatePath(os.path.join(ADDON_PATH, 'resources', 'lib', 'listitem.csv'))

class report():

    def __init__(self):
        
        # see if DB available, if not build and load it
        if not xbmcvfs.exists(DB_PATH):
            self.createDB()
        self.DB = sqlite3.connect(DB_PATH)

        if self.DB is None:
            debug = 'DevView __init__: Failed to initialize DB, closing.'
            xbmc.log(debug, level=xbmc.LOGINFO)
            self.close()
        
    def createDB(self):
        debug = 'DevView: createDB()'
        xbmc.log(debug, level=xbmc.LOGINFO)
        sql_file = xbmcvfs.File(SQL_PATH)
        sql = sql_file.read()
        sql_file.close()

        db = sqlite3.connect(DB_PATH)
        cursor = db.cursor()
        if sql != "":
            try:
                cursor.executescript(sql)
                db.commit()
            except sqlite3.Error as err:
                error = 'DevView createDB(): Failed to create DB tables, error => %s' % err
                xbmc.log(error, level=xbmc.LOGINFO)
                self.Last_Error = error
            except Exception as exc:
                error = 'createDB(): Failed to create DB tables, exception => %s' % exc
                xbmc.log(error, level=xbmc.LOGINFO)
                self.Last_Error = error
        db.close()        
        
        # load up the tables
        with contextlib.closing(sqlite3.connect(DB_PATH)) as connection:
            cursor = connection.cursor()
            with open(DB_DATA_INFOTAG, "r") as file:
                for index, row in enumerate(csv.reader(file)):
                    cursor.execute("""
                        INSERT INTO infotag (function_name, data_type, keys, return_type, notes, V19, V20)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, [*row])
        
            connection.commit()

        with contextlib.closing(sqlite3.connect(DB_PATH)) as connection:
            cursor = connection.cursor()
            with open(DB_DATA_LISTITEM, "r") as file:
                for index, row in enumerate(csv.reader(file)):
                    cursor.execute("""
                        INSERT INTO listitem (listitem, notes)
                        VALUES (?, ?)
                        """, [*row])
        
            connection.commit()    



       
    
    def gather_data(self):

        
        def format_report_txt(label,result,notes,V19,V20):
            if V19 == 'N':
                x = '[COLOR green]M[/COLOR]'
            elif V19 == 'A':
                x = 'M'
            elif V19 == 'D':
                x = '[COLOR yellow]M[/COLOR]'
            elif V19 == 'U':
                x = '[COLOR red]M[/COLOR]'
            else:
                x = '[COLOR red]?[/COLOR]'
    
            if V20 == 'N':
                x = x + '/' + '[COLOR green]N[/COLOR]'
            elif V20 == 'A':
                x = x + '/' + 'N'
            elif V20 == 'D':
                x = x + '/' + '[COLOR yellow]N[/COLOR]'
            elif V20 == 'U':
                x = x + '/' + '[COLOR red]N[/COLOR]'
            else:
                x = x + '/' + '[COLOR red]?[/COLOR]'
            

            
            x = x + ' :: ' + label+ ' :: '
            
            
            x = x + str(result) +"\n" + str(notes) + "\n" + '------------------------------------' + "\n"
    
            return x
            
    
        def format_report_html(label,result,notes,V19,V20):
            x = '<tr><td>'
            if V19 == 'N':
                x = x + '<font color=green>M</font>'
            elif V19 == 'A':
                x = x + 'M'
            elif V19 == 'D':
                x = x + '<font color=yellow>M</font>'
            elif V19 == 'U':
                x = x + '<font color=red>M</font>'
            else:
                x = x + '<font color=red>?</font>'
    
            if V20 == 'N':
                x = x + '/' + '<font color=green>N</font>'
            elif V20 == 'A':
                x = x + '/' + 'N'
            elif V20 == 'D':
                x = x + '/' + '<font color=yellow>N</font>'
            elif V20 == 'U':
                x = x + '/' + '<font color=red>N</font>'
            else:
                x = x + '/' + '<font color=red>?</font>'        
            
            x = x + '</td><td>' + label + '</td><td>' + str(result) + '</td><td>' + str(notes) + '</td></tr>' + "\n"
    
            return x        
        
        
        
        
        
        
        if xbmc.getCondVisibility("Window.IsActive(busydialog)"):
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            xbmc.sleep(800)
    #        xbmc.executebuiltin("Container.Refresh") 
    
        screenshot_file = file = os.path.join(profilePath, 'screenshot.png')
        action = "TakeScreenshot(" + str(screenshot_file) + ")"
        xbmc.executebuiltin(action)
    
    
    #    win = xbmcgui.Window(10000)
        windowID = xbmcgui.getCurrentWindowId()
        currwin = xbmcgui.Window(windowID)
        container = xbmc.getInfoLabel('System.CurrentControlID')
        
        build_version = xbmc.getInfoLabel('System.BuildVersion')
        
        build_version = re.sub(r"\..*$", "", build_version)
            
            
        
        
        divider = '<hr>'
        divider_txt = '-------------------------' + "\n";
    
        content = '<html><head><title>DevView</title></head>'
        content = content + '<body>' + "\n"
        
        content_txt = 'DevView' + "\n";

        content = content + '<img src="/screenshot.png" width="400">' + "\n";

    
    
        content = content + '<h1>windowID : ' + str(windowID) + ' / ' + 'Container : ' + str(container) + '</h1>' + "\n"
        
        content_txt = content_txt + 'windowID: ' + str(windowID) + ' / ' + 'Container : ' + str(container) + "\n"


        content_txt = content_txt + 'Matrix availability : ' + "\n"
        content_txt = content_txt + '    [COLOR red]M[/COLOR] = Unavailable ' + "\n"
        content_txt = content_txt + '    M = Available ' + "\n"
        content_txt = content_txt + '    [COLOR yellow]M[/COLOR] = Deprecated ' + "\n"
        content_txt = content_txt + '    [COLOR green]M[/COLOR] = New for Matrix ' + "\n"

        content_txt = content_txt + 'Nexus availability : ' + "\n"
        content_txt = content_txt + '    [COLOR red]N[/COLOR] = Unavailable ' + "\n"
        content_txt = content_txt + '    N = Available ' + "\n"
        content_txt = content_txt + '    [COLOR yellow]N[/COLOR] = Deprecated ' + "\n"
        content_txt = content_txt + '    [COLOR green]N[/COLOR] = New for Nexus ' + "\n"


        content = content + 'Matrix availability : <br>' + "\n"
        content = content + '--- <font color=red>M</font> = Unavailable <br>' + "\n"
        content = content + '--- M = Available <br>' + "\n"
        content = content + '--- <font color=yellow>M</font> = Deprecated <br>' + "\n"
        content = content + '--- <font color=green>M</font> = New for Matrix <br>' + "\n"

        content = content + 'Nexus availability : <br>' + "\n"
        content = content + '--- <font color=red>N</font> = Unavailable <br>' + "\n"
        content = content + '--- N = Available <br>' + "\n"
        content = content + '--- <font color=yellow>N</font> = Deprecated <br>' + "\n"
        content = content + '--- <font color=green>N</font> = New for Nexus <br>' + "\n"





# additional header details.....
# Window.Property(xmlfile)    Home.xml
# Displays the name of the xml file currently shown

# Window(AddonBrowser).Property(Updated)  11/08/2022 10:51:20 AM
# Shows the date and time the addon repo was last checked for updates

# System.Time    11:07 AM    Current time

# System.StartupWindow    10000    The Window Kodi will load on startup

# System.ScreenResolution    1918x1002 - Windowed    Screen resolution

# System.ProfileName    Master user    Shows the User name of the currently logged in Kodi user

# System.Date    Tuesday, November 8, 2022    Current date

# System.CurrentControlID    1601    ID of the currently focused control.

# ListItem.DBTYPE    movie





        dbtype = xbmc.getInfoLabel('ListItem.DBTYPE')

# videos (video, movie, set, tvshow, season, episode, musicvideo) or for audio (music, song, album, artist).
        
        if dbtype == 'video' or dbtype == 'movie' or dbtype == 'set' or dbtype == 'tvshow' or dbtype == 'season' or dbtype == 'episode' or dbtype == 'musicvideo':
    
            content = content + divider + '<table border=1><tr><td colspan=4><h1>sys.listitem.getVideoInfoTag() :</h1></td></tr>'  + "\n"
            
            
            content = content + '<tr><td>Version</td><td>Function Call</td><td>Result</td><td>Notes</td></tr>' + "\n"
            
            content_txt = content_txt + divider_txt + 'sys.listitem.getVideoInfoTag() :' + "\n"
        
            videoInfoTag = sys.listitem.getVideoInfoTag()

            # See what "get" options are available
            whatup = dir(videoInfoTag)
            
            
            json_fileandpath = videoInfoTag.getFilenameAndPath()
            
            

            # open DB, select all appropriate entries for this dbtype
            query = "SELECT function_name,data_type,keys,return_type,notes,V19,V20 FROM infotag WHERE data_type = 'video' ORDER BY function_name"
            try:
                cursor = self.DB.cursor()
                cursor.execute(query)
                db_data = cursor.fetchall()
                
            except:
                content= content + '<tr><td>DB Connection/sql error</td><td></td></tr>' + "\n" 
                content_txt = content_txt + 'DB Connection/sql error'  + "\n" 
            
            else:   
                
                for stuff in db_data:
                    q_function_name = stuff[0]
                    cq_function_name = re.sub(r"\(\)$", '', q_function_name)
                    q_data_type = stuff[1]
                    q_keys = stuff[2]
                    q_return_type = stuff[3]
                    q_notes = stuff[4]
                    q_v19 = stuff[5]
                    q_v20 = stuff[6]       
                    
                    if build_version == '20':
                        if q_v20 == 'U':
                            content_txt = content_txt + format_report_txt(q_function_name,'[COLOR RED]N/A[/COLOR]',q_notes,q_v19,q_v20)
                            content = content + format_report_html(q_function_name,'<font color=red>N/A</font>',q_notes,q_v19,q_v20)
                        else:
                            if cq_function_name in whatup:
                                try:
                                    f = getattr(videoInfoTag, cq_function_name)
                                except:
                                    content= content + '<tr><td>gettattr failure</td><td>' + cq_function_name + '</td></tr>' + "\n" 
                                    content_txt = content_txt + 'gettattr failure :' + cq_function_name + "\n" 
                                else:
                                    if q_keys != '':
                                        keys = q_keys.split()
                                        for thing in keys:
                                            try:
                                                this_thing = f(thing)
                                            except:
                                                content= content + '<tr><td>function failure</td><td>' + thing + '</td></tr>' + "\n" 
                                                content_txt = content_txt + 'function failure :' + thing + "\n" 
                                            else:
                                                lbl = cq_function_name + "('" + thing + "')"
                                                content_txt = content_txt + format_report_txt(lbl,this_thing,q_notes,q_v19,q_v20)
                                                content = content + format_report_html(lbl,this_thing,q_notes,q_v19,q_v20)
                                    else:
                                        try:
                                            this_thing = f()
                                        except:
                                            content= content + '<tr><td>function failure</td><td>' + thing + '</td></tr>' + "\n" 
                                            content_txt = content_txt + 'function failure :' + thing + "\n" 
                                        else:
                                            content_txt = content_txt + format_report_txt(q_function_name,this_thing,q_notes,q_v19,q_v20)
                                            content = content + format_report_html(q_function_name,this_thing,q_notes,q_v19,q_v20)
                            
                            else:
                                content_txt = content_txt + format_report_txt(cq_function_name,'[COLOR RED]dir(getVideoInfoTag) not found![/COLOR]',q_notes,q_v19,q_v20)
                                content = content + format_report_html(cq_function_name,'<font color=red>dir(getVideoInfoTag) not found!</font>',q_notes,q_v19,q_v20)

                    else:
                        if q_V19 == 'U':
                            content_txt = content_txt + format_report_txt(q_function_name,'[COLOR RED]N/A[/COLOR]',q_notes,q_v19,q_v20)
                            content = content + format_report_html(q_function_name,'<font color=red>N/A</font>',q_notes,q_v19,q_v20)
                        else:
                            if cq_function_name in whatup:
                                try:
                                    f = getattr(videoInfoTag, cq_function_name)
                                except:
                                    content= content + '<tr><td>gettattr failure</td><td>' + cq_function_name + '</td></tr>' + "\n" 
                                    content_txt = content_txt + 'gettattr failure :' + cq_function_name + "\n" 
                                else:

                                    if q_keys != '':
                                        keys = q_keys.split()
                                        for thing in keys:
                                            try:
                                                this_thing = f(thing)
                                            except:
                                                content= content + '<tr><td>function failure</td><td>' + thing + '</td></tr>' + "\n" 
                                                content_txt = content_txt + 'function failure :' + thing + "\n" 
                                            else:
                                                lbl = cq_function_name + "('" + thing + "')"
                                                content_txt = content_txt + format_report_txt(lbl,this_thing,q_notes,q_v19,q_v20)
                                                content = content + format_report_html(lbl,this_thing,q_notes,q_v19,q_v20)

                                    else:
                                        try:
                                            this_thing = f()
                                        except:
                                            content= content + '<tr><td>function failure</td><td>' + thing + '</td></tr>' + "\n" 
                                            content_txt = content_txt + 'function failure :' + thing + "\n" 
                                        else:
                                            content_txt = content_txt + format_report_txt(q_function_name,this_thing,q_notes,q_v19,q_v20)
                                            content = content + format_report_html(q_function_name,this_thing,q_notes,q_v19,q_v20)
                                              
                                        
                            else:
                                content_txt = content_txt + format_report_txt(q_function_name,'[COLOR RED]dir(getVideoInfoTag) not found![/COLOR]',q_notes,q_v19,q_v20)
                                content = content + format_report_html(q_function_name,'<font color=red>dir(getVideoInfoTag) not found!</font>',q_notes,q_v19,q_v20)
                                
            content = content + '</table>'          
         
         
         
         
        else:
            musicinfo = xbmc.InfoTagMusic()
            
            # this probably works (see similar above for non songs) , scan for "getxxxx" in result!
#            whatup = dir(musicinfo)
#            content= content + "<tr><td>test dir : </td><td>" + str(whatup) + '</td></tr>' + "\n" 
#            content_txt = content_txt + 'test dir :' + str(whatup) + "\n"
             
                             
                         

            
        # now do listitems
        
        
        content = content + divider + '<table border=1><tr><td colspan=3><h1>xbmc.getInfoLabel :</h1></td></tr>'  + "\n"

        content = content + '<tr><td>Function</td><td>Results</td><td>Notes</td></tr>' + "\n"
            
        content_txt = content_txt + divider_txt + 'xbmc.getInfoLabel :' + "\n"
        
        
        
        # open DB, select all listitems
        query = "SELECT listitem,notes FROM listitem WHERE 1 ORDER BY listitem"
        try:
            cursor = self.DB.cursor()
            cursor.execute(query)
            db_data = cursor.fetchall()
            
        except:
            content= content + '<tr><td>DB Connection/sql error</td><td></td><td></td></tr>' + "\n" 
            content_txt = content_txt + 'DB Connection/sql error'  + "\n" 
        
        else:   

            this_lookup = 'Container(id).Position'
            this_lookup = re.sub(r"Container\(id\)", "Container(" + container + ")", this_lookup)
            
            container_position = xbmc.getInfoLabel(this_lookup)
            
            this_lookup = 'Container(id).Row'
            this_lookup = re.sub(r"Container\(id\)", "Container(" + container + ")", this_lookup)
            
            container_row = xbmc.getInfoLabel(this_lookup)
            
            for stuff in db_data:
                key = stuff[0]
                q_notes = stuff[1]
                orig_key = key
                
                if key == 'Container(id).Column(parameter)':
                    key = re.sub(r"\(id\)", "(" + container + ")", key)
                    key = re.sub(r"\(parameter\)", "(" + container_position + ")", key)
                    
                if key == 'Container(id).HasFocus(item_number)':
                    key = re.sub(r"\(id\)", "(" + container + ")", key)
                    key = re.sub(r"\(item_number\)", "(" + container_position + ")", key)
                    
                if key == 'Container(id).Position(parameter)':
                    key = re.sub(r"\(id\)", "(" + container + ")", key)
                    key = re.sub(r"\(item_number\)", "(" + container_position + ")", key)
                
                
                if key == 'Container(id).Row(parameter)':
                    key = re.sub(r"\(id\)", "(" + container + ")", key)
                    key = re.sub(r"\(parameter\)", "(" + container_row + ")", key)
                
                key = re.sub(r"Container\(id\)", "Container(" + container + ")", key)
                
                lookup = xbmc.getInfoLabel(key)
                xbmcresult = xbmc.getInfoLabel(key)
                xbmcresult_txt = xbmcresult
                
                if lookup == key:
                    xbmcresult = ''
                    xbmcresult_txt = ''
                
                if xbmcresult != '':
                    x = re.search("^http", xbmcresult)
                    if x and key != 'ListItem.Path' and key != 'ListItem.FileNameAndPath':
                        xbmcresult = xbmcresult + '<img src="' + xbmcresult + '" height=200>'     
                    
                    content = content + '<tr><td>' + key + '</td><td>' + xbmcresult + '</td>' + '<td>' + q_notes + '</td></tr>' + "\n"
                    content_txt = content_txt + key + ' : ' + xbmcresult_txt + ' : ' + "\n[COLOR green]" + q_notes + "[/COLOR]\n"
    
        
            content = content + '</table>'
            content_txt = content_txt + divider_txt
        
            if json_fileandpath is None or json_fileandpath == '':
                json_fileandpath = xbmc.getInfoLabel('ListItem.FileNameAndPath')

        file = json_fileandpath
        
        
        
        
    
        if not file or file == "-1":
            file = "ListItem.FileNameAndPath not found"
            content = content + 'ListItem.FileNameAndPath not found, unable to display additional data.'
            content_txt = content_txt + 'ListItem.FileNameAndPath not found, unable to display additional data.'
        else:
    
            command = '{"jsonrpc": "2.0", ' \
                    '"method": "VideoLibrary.GetMovies", ' \
                    '"params": { ' \
                    '"filter": {"field": "filename", "operator": "is", "value": "%s"}, ' \
                    '"sort": { "order": "ascending", "method": "label" }, ' \
                    '"properties": ["dateadded", "file", "lastplayed", "plot", "title", "art", "playcount", ' \
                    '"streamdetails", "director", "resume", "runtime", "plotoutline", "sorttitle", ' \
                    '"cast", "votes", "showlink", "top250", "trailer", "year", "country", ' \
                    '"studio", "set", "genre", "mpaa", "setid", "rating", "tag", "tagline", ' \
                    '"writer", "originaltitle", "imdbnumber", "uniqueid"] ' \
                    '}, "id": 1}' % file            
    
    #    debug = 'DevView DEBUG json call: ' + str(command)
    #    xbmc.log(debug, level=xbmc.LOGINFO)
    
    
            result = json.loads(xbmc.executeJSONRPC(command))
            
            matches = result['result']['limits']['total']
            
            if matches > 0:
                content = content +  '<h1>Jsonrpc VideoLibrary.GetMovies data available:</h1>' + divider + "\n"
                content = content + command + "\n"
                content = content + "<pre>\n"
                content = content + json.dumps(result, indent=2)
                content = content +  "</pre>\n"
                
                content_txt = content_txt + 'Jsonrpc VideoLibrary.GetMovies data available:' + divider_txt + "\n"
                content_txt = content_txt + command + "\n"
                content_txt = content_txt + json.dumps(result, indent=2) + "\n";
                content_txt = content_txt + divider_txt + "\n"
    
    
            command = '{"jsonrpc": "2.0", ' \
                    '"method": "VideoLibrary.GetEpisodes", ' \
                    '"params": { ' \
                    '"filter": {"field": "filename", "operator": "is", "value": "%s"}, ' \
                    '"sort": { "order": "ascending", "method": "label" }, ' \
                    '"properties": [ "title", "plot", "votes", "rating", ' \
                    '"writer","firstaired","playcount","runtime","director", ' \
                    '"productioncode","season","episode","originaltitle", ' \
                    '"showtitle","cast","streamdetails","lastplayed","fanart", ' \
                    '"thumbnail","file","resume","tvshowid","dateadded", ' \
                    '"uniqueid","art","specialsortseason","specialsortepisode", ' \
                    '"userrating","seasonid","ratings"] ' \
                    '}, "id": 1}' % file            
    
    #    debug = 'DevView DEBUG json call: ' + str(command)
    #    xbmc.log(debug, level=xbmc.LOGINFO)
    
    
            result = json.loads(xbmc.executeJSONRPC(command))
            
            matches = result['result']['limits']['total']
            
            if matches > 0:
                content = content + divider + '<h1>Jsonrpc VideoLibrary.GetEpisodes data available:</h1>' + divider + "\n"
                content = content + command + "\n"
                content = content + "<pre>\n"
                content = content + json.dumps(result, indent=2)
                content = content +  "</pre>\n"
                content_txt = content_txt + 'Jsonrpc VideoLibrary.GetEpisodes data available:' + divider_txt + "\n"
                content_txt = content_txt + command + "\n"
                content_txt = content_txt + json.dumps(result, indent=2) + "\n";
                content_txt = content_txt + divider_txt + "\n"

    
            song_file = xbmc.getInfoLabel('ListItem.Path')
    
            command = '{"jsonrpc": "2.0", ' \
                    '"method": "AudioLibrary.GetSongs", ' \
                    '"params": { ' \
                    '"filter": {"field": "path", "operator": "is", "value": "%s"}, ' \
                    '"sort": { "order": "ascending", "method": "label" }, ' \
                    '"properties": [ "title", "artist", "albumartist", "genre", ' \
                    '"year", "rating", "album", "track", "duration", "comment", ' \
                    '"lyrics", "musicbrainztrackid", "musicbrainzartistid", ' \
                    '"musicbrainzalbumid", "musicbrainzalbumartistid", ' \
                    '"playcount", "fanart", "thumbnail", "file", "albumid", ' \
                    '"lastplayed", "disc", "genreid", "artistid", "displayartist", ' \
                    '"albumartistid", "albumreleasetype", "dateadded", "votes", ' \
                    '"userrating", "mood", "contributors", "displaycomposer", ' \
                    '"displayconductor", "displayorchestra", "displaylyricist", ' \
                    '"sortartist", "art", "sourceid", "disctitle", "releasedate", ' \
                    '"originaldate", "bpm", "samplerate", "bitrate", "channels", ' \
                    '"datemodified","datenew" ] ' \
                    '}, "id": 1}' % song_file            
    
    #    debug = 'DevView DEBUG json call: ' + str(command)
    #    xbmc.log(debug, level=xbmc.LOGINFO)
    
            result = json.loads(xbmc.executeJSONRPC(command))
            
            matches = result['result']['limits']['total']            
            
            if matches > 0:
                content = content + divider + '<h1>Jsonrpc AudioLibrary.GetSongs data available:</h1>' + divider + "\n"
                content = content + command + "\n"
                content = content + "<pre>\n"
                content = content + json.dumps(result, indent=2)
                content = content +  "</pre>\n"
                content_txt = content_txt + 'Jsonrpc VideoLibrary.GetEpisodes data available:' + divider_txt + "\n"
                content_txt = content_txt + command + "\n"
                content_txt = content_txt + json.dumps(result, indent=2) + "\n";
                content_txt = content_txt + divider_txt + "\n"

            
            content = content + '</body></html>' + "\n"
            
        file = os.path.join(profilePath, 'index.html')
        buffer = content
        with xbmcvfs.File(file, 'w') as f:
            result = f.write(buffer)
            
        file = os.path.join(profilePath, 'index.txt')
        buffer = content_txt
        with xbmcvfs.File(file, 'w') as f:
            result = f.write(buffer)
    
        return ''

