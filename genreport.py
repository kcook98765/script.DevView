import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import sys, re, os
import json
import xbmcvfs
import csv
import sqlite3
import contextlib
import urllib.parse
from cProfile import label

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ID = ADDON.getAddonInfo("id")

profilePath = xbmcvfs.translatePath( ADDON.getAddonInfo('profile') )
if not os.path.exists(profilePath):
    os.makedirs(profilePath)

DB_PATH = xbmcvfs.translatePath(os.path.join(profilePath, 'devview4.db'))
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
        
        def flatten(adict):
            stack = [[adict, []]]
            x=0
            out = ''
            while stack:
                d, pre = stack.pop()
                if isinstance(d, dict):
                    for key, value in d.items():
                        if isinstance(value, dict):
                            stack.append([value, pre + [key]])
                        elif isinstance(value, (list, tuple)):
                            if isinstance(value, list):
                                x=0
                            for v in value:
                                stack.append([v, pre + [key] + [x]])
                                x=x+1
                        else:
                            out = out + str((pre + [key])) + "\t" + str(value) + "\n"
                else:
                    out = out + str((pre))+  "\t" + str(d) + "\n"
            return out


        def store_json_results(results,command):
            lines = results.split('\n')
            for line in lines:

                if line != None and "\t" in line:

#                    debug = 'store_json_results line: ' + str(line)
#                    xbmc.log(debug, level=xbmc.LOGINFO)                
    
                    [path, result] = line.split('\t')
                    code_path = re.sub(r", ", '][', path)
    
#                    debug = 'store_json_results after regex: ' + str(code_path) + ':' + result
#                    xbmc.log(debug, level=xbmc.LOGINFO)                       
                    
    
                    store_results('JsonRPC',command,code_path,result)
            return ''

        def jsonrpc_properties (param,field):
            props = ''
            command = '{ "jsonrpc": "2.0", "method": "JSONRPC.Introspect", "params": { "filter": { "id": "' + param + '", "type": "method" } }, "id": 1 }'
            result = json.loads(xbmc.executeJSONRPC(command))
            log_introspect = param + '_introspect'
            json_call[log_introspect] = command
            if 'items' in result['result']['types'][field]:
                prop = result['result']['types'][field]['items']['enums']
            else:
                prop = result['result']['types'][field]['enums']
            x = 0
            for p in prop:
                # empty param returned for at least Settings.GetSettings !
                if p != '':
                    if x > 0:
                        props = props + ', '
                    x = 1
                    props = props + '"' + p + '"'
#            store_results('JsonRPC',log_introspect,'introspect',props)
            return props

        
        def store_results (code_type,base_code,code_run,results):
            
#            debug = 'store_results called with: ' + str(code_type) + ':' + str(base_code) + ':' + str(code_run) + ':' + str(results)
#            xbmc.log(debug, level=xbmc.LOGINFO)
            
            
            
            
            with contextlib.closing(sqlite3.connect(DB_PATH)) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                        INSERT INTO results (code_type,base_code,code_run,results)
                        VALUES (?, ?, ?, ?)
                        """, [str(code_type),str(base_code),str(code_run),str(results)])
        
                connection.commit()
            return ''

        if xbmc.getCondVisibility("Window.IsActive(busydialog)"):
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            xbmc.sleep(800)
    #        xbmc.executebuiltin("Container.Refresh") 
    
        screenshot_file = file = os.path.join(profilePath, 'screenshot.png')
        action = "TakeScreenshot(" + str(screenshot_file) + ")"
        xbmc.executebuiltin(action)
    
    
        # clear out results table
        with contextlib.closing(sqlite3.connect(DB_PATH)) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM results")
            connection.commit()
    
    #    win = xbmcgui.Window(10000)
        windowID = xbmcgui.getCurrentWindowId()
        currwin = xbmcgui.Window(windowID)
        container = xbmc.getInfoLabel('System.CurrentControlID')
        
        build_version = xbmc.getInfoLabel('System.BuildVersion')
        
        build_version = re.sub(r"\..*$", "", build_version)
            

        
        
        videoInfoTag = sys.listitem.getVideoInfoTag()
        musicinfo = sys.listitem.getMusicInfoTag()
        has_pvr = xbmc.getInfoLabel('System.HasPVRAddon')
        
        # seems this is not accurate for "season", but getMediaType does work ?
        # dbtype = xbmc.getInfoLabel('ListItem.DBTYPE')
        
        dbtype = videoInfoTag.getMediaType()

        # videos (video, movie, set, tvshow, season, episode, musicvideo) or for audio (music, song, album, artist).
        
        if dbtype == 'video' or dbtype == 'movie' or dbtype == 'set' or dbtype == 'tvshow' or dbtype == 'season' or dbtype == 'episode' or dbtype == 'musicvideo':
    

        
            

            # See what "get" options are available
            whatup = dir(videoInfoTag)

            # open DB, select all appropriate entries for this dbtype
            query = "SELECT function_name,data_type,keys,return_type,notes,V19,V20 FROM infotag WHERE data_type = 'video' ORDER BY function_name"
            try:
                cursor = self.DB.cursor()
                cursor.execute(query)
                db_data = cursor.fetchall()
                
            except:
                store_results('Internal','DB connect','DB connect','DB Connection/sql error')
           
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
                            store_results('getVideoInfoTag()',q_function_name,q_function_name,'Unavailable on Nexus')
                        else:
                            if cq_function_name in whatup:
                                try:
                                    f = getattr(videoInfoTag, cq_function_name)
                                except:
                                   store_results('getVideoInfoTag()',cq_function_name,cq_function_name,'gettattr failure')
                                else:
                                    if q_keys != '':
                                        keys = q_keys.split()
                                        for thing in keys:
                                            try:
                                                this_thing = f(thing)
                                            except:
                                                store_results('getVideoInfoTag()',q_function_name,thing,'Function Failure')
                                            else:
                                                lbl = cq_function_name + "('" + thing + "')"
                                                store_results('getVideoInfoTag()',q_function_name,lbl,this_thing)
                                    else:
                                        try:
                                            this_thing = f()
                                        except:
                                            store_results('getVideoInfoTag()',q_function_name,this_thing,'function failure')
                                        else:
                                            store_results('getVideoInfoTag()',q_function_name,q_function_name,this_thing)
                            
                            else:
                                store_results('getVideoInfoTag()',q_function_name,q_function_name,'not found in dir(getVideoInfoTag)')

                    else:
                        if q_v19 == 'U':
                            store_results('getVideoInfoTag()',q_function_name,q_function_name,'Unavailable on Matrix')
                        else:
                            if cq_function_name in whatup:
                                try:
                                    f = getattr(videoInfoTag, cq_function_name)
                                except:
                                    store_results('getVideoInfoTag()',cq_function_name,cq_function_name,'gettattr failure')
                                else:

                                    if q_keys != '':
                                        keys = q_keys.split()
                                        for thing in keys:
                                            try:
                                                this_thing = f(thing)
                                            except:
                                                store_results('getVideoInfoTag()',cq_function_name,this_thing,'function failure')
                                            else:
                                                lbl = cq_function_name + "('" + thing + "')"
                                                store_results('getVideoInfoTag()',cq_function_name,lbl,thing)
                                    else:
                                        try:
                                            this_thing = f()
                                        except:
                                            store_results('getVideoInfoTag()',cq_function_name,cq_function_name,'function failure')
                                        else:
                                            store_results('getVideoInfoTag()',q_function_name,q_function_name,this_thing)
                            else:
                                store_results('getVideoInfoTag()',q_function_name,q_function_name,'not found in dir(getVideoInfoTag)')
        
        elif dbtype == 'music' or dbtype == 'song' or dbtype == 'album' or dbtype == 'artist':
        
            

            # See what "get" options are available
            whatup = dir(musicinfo)

            # open DB, select all appropriate entries for this dbtype
            query = "SELECT function_name,data_type,keys,return_type,notes,V19,V20 FROM infotag WHERE data_type = 'music' ORDER BY function_name"
            try:
                cursor = self.DB.cursor()
                cursor.execute(query)
                db_data = cursor.fetchall()
            except:
                store_results('getMusicInfoTag()','DB connect','DB connect','DB Connection/sql error')
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
                             store_results('getMusicInfoTag()',q_function_name,q_function_name,'Unavailable for Nexus')
                        else:
                            if cq_function_name in whatup:
                                try:
                                    f = getattr(musicinfo, cq_function_name)
                                except:
                                    store_results('getMusicInfoTag()',cq_function_name,cq_function_name,'gettattr failure')
                                else:
                                    if q_keys != '':
                                        keys = q_keys.split()
                                        for thing in keys:
                                            try:
                                                this_thing = f(thing)
                                            except:
                                                store_results('getMusicInfoTag()',cq_function_name,thing,'function failure')
                                            else:
                                                store_results('getMusicInfoTag()',cq_function_name,lbl,this_thing)
                                    else:
                                        try:
                                            this_thing = f()
                                        except:
                                            store_results('getMusicInfoTag()',q_function_name,thing,'function failure')
                                        else:
                                            store_results('getMusicInfoTag()',q_function_name,q_function_name,this_thing)
                            else:
                                store_results('getMusicInfoTag()',cq_function_name,cq_function_name,'dir(getVideoInfoTag) not found')
                    else:
                        if q_v19 == 'U':
                            store_results('getMusicInfoTag()',q_function_name,q_function_name,'Unavailable in Matrix')
                        else:
                            if cq_function_name in whatup:
                                try:
                                    f = getattr(musicinfo, cq_function_name)
                                except:
                                    store_results('getMusicInfoTag()',cq_function_name,cq_function_name,'gettattr failure')
                                else:
                                    if q_keys != '':
                                        keys = q_keys.split()
                                        for thing in keys:
                                            try:
                                                this_thing = f(thing)
                                            except:
                                                store_results('getMusicInfoTag()',cq_function_name,thing,'function failure')
                                            else:
                                                lbl = cq_function_name + "('" + thing + "')"
                                                store_results('getMusicInfoTag()',cq_function_name,lbl,this_thing)
                                    else:
                                        try:
                                            this_thing = f()
                                        except:
                                            store_results('getMusicInfoTag()',cq_function_name,cq_function_name,'function failure')
                                        else:
                                            store_results('getMusicInfoTag()',q_function_name,q_function_name,this_thing)
                            else:
                                store_results('getMusicInfoTag()',q_function_name,q_function_name,'dir(getMusicInfoTag) not found')
                                

        # now do listitems

        # open DB, select all listitems
        query = "SELECT listitem,notes FROM listitem WHERE 1 ORDER BY listitem"
        try:
            cursor = self.DB.cursor()
            cursor.execute(query)
            db_data = cursor.fetchall()
            
        except:
            store_results('xbmc.getInfoLabel','DB CONNECT','DB CONNECT','DB Connection/sql error')
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
                    store_results('xbmc.getInfoLabel',key,key,xbmcresult_txt)
        
        json_call = {}
        video_dbid = videoInfoTag.getDbId()
        audio_dbid = musicinfo.getDbId()


        if video_dbid > 0 and (dbtype == 'video' or dbtype == 'movie'):
            prop_name = 'VideoLibrary.GetMovieDetails'
            props = jsonrpc_properties(prop_name,'Video.Fields.Movie')
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "movieid" : %s, ' \
                    '"properties": [%s] }, "id": 1}' % (prop_name, video_dbid, props)
            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)            

        if video_dbid > 0 and dbtype == 'set':
            prop_name = 'VideoLibrary.GetMovieSetDetails'
            props = jsonrpc_properties(prop_name,'Video.Fields.Movie')
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "setid" : %s, ' \
                    '"properties": [%s] }, "id": 1}' % (prop_name, video_dbid, props)
            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)       


        if video_dbid > 0 and dbtype == 'tvshow':
            prop_name = 'VideoLibrary.GetTVShowDetails'
            props = jsonrpc_properties(prop_name,'Video.Fields.TVShow')
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "tvshowid": %s, ' \
                    '"properties": [%s] }, "id": 1}' % (prop_name, video_dbid, props)

            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)

        if video_dbid > 0 and dbtype == 'season':
            prop_name = 'VideoLibrary.GetSeasonDetails'
            props = jsonrpc_properties(prop_name,'Video.Fields.Season')
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "seasonid": %s, ' \
                    '"properties": [%s] }, "id": 1}' % (prop_name, video_dbid, props)

            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)


        if video_dbid > 0 and dbtype == 'episode':
            prop_name = 'VideoLibrary.GetEpisodeDetails'
            props = jsonrpc_properties(prop_name,'Video.Fields.Episode')
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "episodeid": %s, ' \
                    '"properties": [%s] }, "id": 1}' % (prop_name, video_dbid, props)

            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)


        if video_dbid > 0 and dbtype == 'musicvideo':
            prop_name = 'VideoLibrary.GetMusicVideoDetails'
            props = jsonrpc_properties(prop_name,'Video.Fields.MusicVideo')
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "musicvideoid": %s, ' \
                    '"properties": [%s] }, "id": 1}' % (prop_name, video_dbid, props)

            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)


        if audio_dbid > 0 and dbtype == 'artist':
            prop_name = 'AudioLibrary.GetArtistDetails'
            props = jsonrpc_properties(prop_name,'Audio.Fields.Artist')
            
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "filter": { "artistid" : %s }, ' \
                    '"properties": [%s] }, "id": 1}' % (prop_name, audio_dbid, props)
    
            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)



        if audio_dbid > 0 and dbtype == 'album':
            prop_name = 'AudioLibrary.GetAlbumDetails'
            props = jsonrpc_properties(prop_name,'Audio.Fields.Album')
            
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "filter": { "albumid" : %s }, ' \
                    '"properties": [%s] }, "id": 1}' % (prop_name, audio_dbid, props)
    
            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)


        if audio_dbid > 0 and dbtype == 'song':
            prop_name = 'AudioLibrary.GetSongDetails'
            props = jsonrpc_properties(prop_name,'Audio.Fields.Song')
            
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "songid" : %s , ' \
                    '"properties": [%s] }, "id": 1}' % (prop_name, audio_dbid, props)
    
            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)

        
        if has_pvr:
            prop_name = 'PVR.GetProperties'
            props = jsonrpc_properties(prop_name,'PVR.Property.Name')
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "properties": [%s] }, "id": 1}' % (prop_name, props)
            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)




        if 1 == 2:
            
            # need broadcastid and playerid below to trigger
            prop_name = 'PVR.GetBroadcastDetails'
            props = jsonrpc_properties(prop_name,'PVR.Fields.Broadcast')
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "broadcastid" : %s "properties": [%s] }, "id": 1}' % (prop_name, broadcastid, props)
            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)
    
            prop_name = 'Player.GetItem'
            props = jsonrpc_properties(prop_name,'List.Fields.All')
            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "playerid" : %s, "properties": [%s] }, "id": 1}' % (prop_name, playerid, props)
            json_call[prop_name] = command
            result = json.loads(xbmc.executeJSONRPC(command))
            data = flatten(result)
            store_json_results(data,prop_name)

        # these can run every time



        prop_name = 'Application.GetProperties'
        props = jsonrpc_properties(prop_name,'Application.Property.Name')
        command = '{"jsonrpc": "2.0", "method": "%s", "params": { "properties": [%s] }, "id": 1}' % (prop_name, props)
        json_call[prop_name] = command
        result = json.loads(xbmc.executeJSONRPC(command))
        data = flatten(result)
        store_json_results(data,prop_name)

        prop_name = 'System.GetProperties'
        props = jsonrpc_properties(prop_name,'System.Property.Name')
        command = '{"jsonrpc": "2.0", "method": "%s", "params": { "properties": [%s] }, "id": 1}' % (prop_name, props)
        json_call[prop_name] = command
        result = json.loads(xbmc.executeJSONRPC(command))
        data = flatten(result)
        store_json_results(data,prop_name)

            # 5.1.3 Addons.GetAddons
            # http://127.0.0.1:8080/jsonrpc?request={%20%22jsonrpc%22:%20%222.0%22,%20%22method%22:%20%22JSONRPC.Introspect%22,%20%22params%22:%20{%20%22filter%22:%20{%20%22id%22:%20%22Addons.GetAddons%22,%20%22type%22:%20%22method%22%20}%20},%20%22id%22:%201%20}
# this one takes a while, commented out for now, maybe add setting to enable/disable this lookup?
#            prop_name = 'Addons.GetAddons'
#            props = jsonrpc_properties(prop_name,'Addon.Fields')
#            command = '{"jsonrpc": "2.0", "method": "%s", "params": { "properties": [%s] }, "id": 1}' % (prop_name, props)
#            json_call[prop_name] = command
#            result = json.loads(xbmc.executeJSONRPC(command))
#            data = flatten(result)
#            store_json_results(data,prop_name)

            # http://127.0.0.1:8080/jsonrpc?request={%20%22jsonrpc%22:%20%222.0%22,%20%22method%22:%20%22JSONRPC.Introspect%22,%20%22params%22:%20{%20%22filter%22:%20{%20%22id%22:%20%22Settings.GetSettings%22,%20%22type%22:%20%22method%22%20}%20},%20%22id%22:%201%20}
# takes a while, maybe use setting to enable/disable
#            prop_name = 'Settings.GetSettings'
#            command = '{"jsonrpc": "2.0", "method": "%s", "params": { }, "id": 1}' % (prop_name)
#            json_call[prop_name] = command
#            result = json.loads(xbmc.executeJSONRPC(command))
#            data = flatten(result)
#            store_json_results(data,prop_name)



#        if dbtype == 'music' or dbtype == 'song' or dbtype == 'album' or dbtype == 'artist':
#        if dbtype == 'video' or dbtype == 'movie' or dbtype == 'set' or dbtype == 'tvshow' or dbtype == 'season' or dbtype == 'episode' or dbtype == 'musicvideo':
            








        ######################################
        # now that all data has been saved to database, can build the reports here
    
        content = '<html><head><title>DevView</title></head>'
        content = content + '<body>' + "\n"
        content = content + '<table border=1><tr><td><img src="screenshot.png" width="400"></td>' + "\n";     
        content = content + '<td>System.Date : <b>' + xbmc.getInfoLabel('System.Date') + '</b><br>'
        content = content + 'System.Time : <b>' + xbmc.getInfoLabel('System.Time') + '</b><br>'
        content = content + 'System.BuildVersion : <b>' + xbmc.getInfoLabel('System.BuildVersion') + '</b><br>'
        content = content + 'Window.Property(xmlfile) : <b>' + xbmc.getInfoLabel('Window.Property(xmlfile)') + '</b><br>'
        content = content + 'System.ScreenResolution : <b>' + xbmc.getInfoLabel('System.ScreenResolution') + '</b><br>'
        content = content + 'ListItem.DBTYPE : <b>' + xbmc.getInfoLabel('ListItem.DBTYPE') + '</b><br>'
        content = content + 'DBID : <b>' + xbmc.getInfoLabel('ListItem.DBID') + '</b><br>'
        content = content + 'windowID : <b>' + str(windowID) + '</b><br>'
        content = content + 'Container : <b>' + str(container) + '</b></td></tr></table>'
    
        # see if there is any getVideoInfoTag() data and output it

        # videos (video, movie, set, tvshow, season, episode, musicvideo) or for audio (music, song, album, artist).
        
        if dbtype == 'video' or dbtype == 'movie' or dbtype == 'set' or dbtype == 'tvshow' or dbtype == 'season' or dbtype == 'episode' or dbtype == 'musicvideo':
            query = """SELECT B.V19,B.V20,A.base_code,B.keys,A.code_run,A.results,B.data_type,B.return_type,B.notes
            FROM results AS A LEFT JOIN infotag AS B ON B.function_name = A.base_code
            WHERE A.code_type = 'getVideoInfoTag()' AND B.data_type = 'video' ORDER BY A.base_code,A.code_run"""
            h_label = 'getVideoInfoTag()'
        else:
            query = """SELECT B.V19,B.V20,A.base_code,B.keys,A.code_run,A.results,B.data_type,B.return_type,B.notes
            FROM results AS A LEFT JOIN infotag AS B ON B.function_name = A.base_code
            WHERE A.code_type = 'getMusicInfoTag()' AND B.data_type = 'music' ORDER BY A.base_code,A.code_run"""
            h_label = 'getMusicInfoTag()'
            
        try:
            cursor = self.DB.cursor()
            cursor.execute(query)
            db_data = cursor.fetchall()
            
        except:
            content = content + '<h2>DB Connection/sql error</h2>' + "\n" + '<textarea>' + query + '</textarea>' + "\n" 
        
        else:   
            
            content = content + '<table border=1><tr><td colspan=9 align=center><h1>sys.listitem.' + h_label + ' :</h1></td></tr>'  + "\n"
            
            content = content + """<tr><td colspan=9 align=center>
                <b>A</b>vailable, <font color=green><b>N</b></font>ew, <font color=red><b>U</b></font>navailable,
                <font color=yellow><b>D</b></font>epricated</td></tr>"""
            
            content = content + '<tr><td>V19</td><td>V20</td><td>Base Code</td><td>Keys Used</td><td>Code run</td><td>Result</td>'
            content = content + '<td>Data Type</td><td>Return Type</td><td>Doc Notes</td></tr>' + "\n"
           
            for stuff in db_data:
                
                my_stuff = list(stuff)
                
                if my_stuff[0] == 'A':
                    my_stuff[0] = '<b>A</b>'
                elif my_stuff[0] == 'N':
                    my_stuff[0] = '<font color=green><b>N</b></font>'
                elif my_stuff[0] == 'U':
                    my_stuff[0] = '<font color=red><b>U</b></font>'
                elif my_stuff[0] == 'D':
                    my_stuff[0] = '<font color=yellow><b>D</b></font>'
                else:
                    my_stuff[0] = 'ERROR'
                
                if my_stuff[1] == 'A':
                    my_stuff[1] = '<b>A</b>'
                elif my_stuff[1] == 'N':
                    my_stuff[1] = '<font color=green><b>N</b></font>'
                elif my_stuff[1] == 'U':
                    my_stuff[1] = '<font color=red><b>U</b></font>'
                elif my_stuff[1] == 'D':
                    my_stuff[1] = '<font color=yellow><b>D</b></font>'
                else:
                    my_stuff[1] = 'ERROR'                
                
                stuff = tuple(my_stuff)
                
                content = content + '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' \
                    '<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % stuff
                content = content + "\n"
    
    
    
        # see if there is any xbmc.getInfoLabel data and output it
        query = "SELECT A.base_code,A.code_run,A.results,B.notes"
        query = query + " FROM results AS A LEFT JOIN listitem AS B ON B.listitem = A.base_code"
        query = query + " WHERE A.code_type = 'xbmc.getInfoLabel' ORDER BY A.base_code,A.code_run"
        
        try:
            cursor = self.DB.cursor()
            cursor.execute(query)
            db_data = cursor.fetchall()
            
        except:
            content = content + '<h2>DB Connection/sql error</h2>' + "\n" 
        
        else:   
            
            content = content + '<table border=1><tr><td colspan=4 align=center><h1>xbmc.getInfoLabel :</h1></td></tr>'  + "\n"
            content = content + '<tr><td>Base Code</td><td>Code run</td><td>Result</td><td>Doc Notes</td></tr>' + "\n"
           
            for stuff in db_data:
                content = content + '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td>' % stuff
                content = content + "\n"





        # display any Json RPC data
        query = "SELECT A.base_code,A.code_run,A.results"
        query = query + " FROM results AS A"
        query = query + " WHERE A.code_type = 'JsonRPC' ORDER BY A.base_code,A.code_run"
        
        try:
            cursor = self.DB.cursor()
            cursor.execute(query)
            db_data = cursor.fetchall()
            
        except:
            content = content + '<h2>DB Connection/sql error</h2>' + "\n" 
        
        else:   
            
            content = content + '<table border=1><tr><td colspan=3 align=center><h1>JsonRPC :</h1></td></tr>'  + "\n"
            content = content + '<tr><td>Json Call</td><td>Result Path</td><td>Result</td></tr>' + "\n"
            
            curr_call = ''
           
            for stuff in db_data:
                if curr_call != stuff[0]:
                    curr_call = stuff[0]
                    content = content + '<tr><td colspan=3 align=center><b>' + stuff[0] + '<b></td></tr>' + "\n"
                    content = content + '<tr><td colspan=3 align=center><b>' + json_call[curr_call] + '<b></td></tr>' + "\n"
                    
                    
                    
                # if stuff[2] =~ /^image::(XXXXXXXXXX)
                # take this url, urldecode it, then insert in html image tags and add to end of stuff[2] to display image in html
                
                
                a = str(stuff[0])
                b = str(stuff[1])
                c = str(stuff[2])
                
                if re.search("^image\:\/\/",c) :
                    image = c.replace("image://","")
                    image = re.sub(r"/$","", image)
                    image = urllib.parse.unquote_plus(image)
                    
                    if not re.search("^http", image):
                        image = image.replace('\\','/')
                        image = 'file:///' + image
                    
                    
                    
                    html_image = '<img src="' + image + '" height=200>'
                    c = c + html_image

                content = content + '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (a, b, c)
                content = content + "\n"        

        content = content + '</table>' + "\n" 


        file = os.path.join(profilePath, 'index.html')
        buffer = content
        with xbmcvfs.File(file, 'w') as f:
            result = f.write(buffer)
            
#        file = os.path.join(profilePath, 'index.txt')
#        buffer = content_txt
#        with xbmcvfs.File(file, 'w') as f:
#            result = f.write(buffer)
    
#        file = os.path.join(profilePath, 'index.tab')
#        buffer = content_db
#        with xbmcvfs.File(file, 'w') as f:
#            result = f.write(buffer)
#     TODO , dump results table to a csv file for export        
    
    
        return ''

