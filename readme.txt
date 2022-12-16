DevView

As you interact with kodi, use this tool to view data/information related to the current highlighted item.

When highlighted on a Movie, TV episode or music track, use the context menu "DevView".

This will bring up a fullscreen view of a text version of the report

Best view of data is via a web browser on same machine, access via web browser:

http://127.0.0.1:9999

This html view is a copy of the last "DevView" run , and is much nicer to view.

Details can include (depending on the media item highlighted when triggering this addon):

Screenshot.png generation
sys.listitem.getVideoInfoTag()
sys.listitem.getMusicInfoTag()
xbmc.getInfoLabel()

And Various JSON calls (uses introspect lookup to find all possible "properties" to return:
Application.GetProperties
System.GetProperties

VideoLibrary.GetMovieDetails
VideoLibrary.GetMovieSetDetails
VideoLibrary.GetTVShowDetails
VideoLibrary.GetSeasonDetails
VideoLibrary.GetEpisodeDetails
VideoLibrary.GetMusicVideoDetails
AudioLibrary.GetArtistDetails
AudioLibrary.GetAlbumDetails
AudioLibrary.GetSongDetails
PVR.GetProperties ( and if channelid found: PVR.GetBroadcasts is run then any "match" for the "ListItem.DateTime" (accounting for UTC differences) is searched for,  and if found, the "broadcastid" is used to run "PVR.GetBroadcastDetails" )

I am thinking about making a couple more calls available, but they seem to take a very long time to execute:
Addons.GetAddons
Settings.GetSettings

I might add a setting to enable/disable(default) for these with note they can take a long time to execute.