import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import sys, re, os
import json
import xbmcvfs

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ID = ADDON.getAddonInfo("id")

profilePath = xbmcvfs.translatePath( ADDON.getAddonInfo('profile') )
if not os.path.exists(profilePath):
    os.makedirs(profilePath)


class report():

    def __init__(self):
    # https://kodi.wiki/view/InfoLabels
    
        self.listitem_dict = {
            "Container(id).Column": "The column number of the focused position in a panel container. v16 Skinning engine changes:[New Infolabel] Container(id).Column",
            "Container(id).Column(parameter)": "True if the column number of the focused position matches the specified parameter.",
            "Container(id).CurrentItem": "The current item in the container or grouplist with given id. NoteIf no id is specified it grabs the current container. v15 Skinning engine changes:[New Infolabel] Container(id).CurrentItem",
            "Container(id).CurrentPage": "The current page in the container with given id. NoteIf no id is specified it grabs the current container.",
            "Container(id).HasFocus(item_number)": "True if the container with id (or current container if id is omitted) has static content and is focused on the item with id item_number.",
            "Container(id).HasNext": "True if the container or textbox with id (id) has a next page.",
            "Container(id).HasParent": "True when the container with given id contains a parent ('..') item. NoteIf no id is specified it grabs the current container. v16 Skinning engine changes:[New Boolean Condition] Container.HasParent",
            "Container(id).HasPrevious": "True if the container or textbox with id (id) has a previous page.",
            "Container(id).IsUpdating": "True if the container with dynamic list content is currently updating.",
            "Container(id).ListItem(offset).Property": "The property of the ListItem with a given offset. Parameters offset- The offset for the listitem. NoteProperty has to be replaced with Label, Label2, Icon etc. Example: Container(50).Listitem(2).Label",
            "Container(id).ListItemAbsolute(x).[infolabel]": "The infolabel for an item in a Container. Parameters x- the absolute position in the container. NoteExample: Container(50).ListItemAbsolute(4).Genre v16 Skinning engine changes:[New Infolabel] Container(id).ListItemAbsolute(x).[infolabel]",
            "Container(id).ListItemNoWrap(offset).Property": "The same as Container(id).ListItem(offset).Property but it won't wrap. Parameters offset- The offset for the listitem. NoteThat means if the last item of a list is focused, ListItemNoWrap(1) will be empty while ListItem(1) will return the first item of the list. Property has to be replaced with Label, Label2, Icon etc. Example: Container(50).ListitemNoWrap(1).Plot",
            "Container(id).ListItemPosition(x).[infolabel]": "The infolabel for an item in a Container. Parameters x- the position in the container relative to the cursor position. NoteExample: Container(50).ListItemPosition(4).Genre",
            "Container(id).NumAllItems": "The number of all items in the container or grouplist with given id including parent folder item. NoteIf no id is specified it grabs the current container. v18 Skinning engine changes:[New Infolabel] Container(id).NumAllItems",
            "Container(id).NumItems": "The number of items in the container or grouplist with given id excluding parent folder item. NoteIf no id is specified it grabs the current container.",
            "Container(id).NumNonFolderItems": "The Number of items in the container or grouplist with given id excluding all folder items. NoteExample: pvr recordings folders, parent '..' folder). If no id is specified it grabs the current container. v18 Skinning engine changes:[New Infolabel] Container(id).NumNonFolderItems",
            "Container(id).NumPages": "The number of pages in the container with given id. If no id is specified it grabs the current container.",
            "Container(id).OnNext": "True if the container with id (or current container if id is omitted) is moving to the next item. Allows views to be custom-designed (such as 3D coverviews etc.)",
            "Container(id).OnPrevious": "True if the container with id (or current container if id is omitted) is moving to the previous item. Allows views to be custom-designed (such as 3D coverviews etc).",
            "Container(id).OnScrollNext": "True if the container with id (or current container if id is omitted) is scrolling to the next item. Differs from OnNext in that OnNext triggers on movement even if there is no scroll involved.",
            "Container(id).OnScrollPrevious": "True if the container with id (or current container if id is omitted) is scrolling to the previous item. Differs from OnPrevious in that OnPrevious triggers on movement even if there is no scroll involved.",
            "Container(id).Position": "The current focused position of container / grouplist (id) as a numeric label. v16 Skinning engine changes:[Infolabel Updated] Container(id).Position now also returns the position for items inside a grouplist.",
            "Container(id).Position(parameter)": "True if the container with id (or current container if id is omitted) is focused on the specified position.",
            "Container(id).Row": "The row number of the focused position in a panel container. v16 Skinning engine changes:[New Infolabel] Container(id).Row",
            "Container(id).Row(parameter)": "True if the row number of the focused position matches the specified parameter.",
            "Container(id).Scrolling": "True if the user is currently scrolling through the container with id (or current container if id is omitted). NoteThis is slightly delayed from the actual scroll start. Use Container(id).OnScrollNext or Container(id).OnScrollPrevious to trigger animations immediately on scroll.",
            "Container(id).SubItem(item_number)": "True if the container with id (or current container if id is omitted) is focused on the specified subitem. NoteIf no id is specified it grabs the current container.",
            "Container.Art(type)": "The path to the art image file for the given type of the current container. Parameters type- the art type to request. Todo:List of all art types v16 Skinning engine changes:[Infolabel Updated] Container.Art(type) set.fanart as possible type value. v15 Skinning engine changes:[New Infolabel] Container.Art(type)",
            "Container.CanFilter": "True when the current container can be filtered.",
            "Container.CanFilterAdvanced": "True when advanced filtering can be applied to the current container.",
            "Container.Content": "The content of the current container. v16 Skinning engine changes:[New Infolabel] Container.Content",
            "Container.Content(parameter)": "True if the current container you are in contains the following: files songs artists albums movies tvshows seasons episodes musicvideos genres years actors playlists plugins studios directors sets tags NoteThese currently only work in the Video and Music Library or unless a Plugin has set the value) also available are Addons true when a list of add-ons is shown LiveTV true when a htsp (tvheadend) directory is shown",
            "Container.Filtered": "True when a mediafilter is applied to the current container.",
            "Container.FolderName": "The top most folder in currently displayed folder.",
            "Container.FolderPath": "The complete path of currently displayed folder.",
            "Container.HasFiles": "True if the container contains files.",
            "Container.HasFolders": "True if the container contains folders.",
            "Container.HasThumb": "True if the current container you are in has a thumb assigned to it.",
            "Container.IsStacked": "True if the container is currently in stacked mode.",
            "Container.PluginCategory": "The current plugins category (set by the scripter). v17 Skinning engine changes:[New Infolabel] Container.PluginCategory",
            "Container.PluginName": "The current plugins base folder name.",
            "Container.Property(addoncategory)": "The current add-on category.",
            "Container.Property(reponame)": "The current add-on repository name.",
            "Container.ShowPlot": "The TV Show plot of the current container and can be used at season and episode level.",
            "Container.ShowTitle": "The TV Show title of the current container and can be used at season and episode level. v17 Skinning engine changes:[New Infolabel] Container.ShowTitle",
            "Container.SortDirection(direction)": "True if the sort direction of a container equals direction. Parameters direction- The direction to check. It can be: ascending descending",
            "Container.SortMethod": "The current sort method (returns a localized value).",
            "Container.SortMethod(sortid)": "True if the current sort method matches the specified SortID (see SortUtils).",
            "Container.SortOrder": "The current sort order (Ascending/Descending). v16 Skinning engine changes:[New Infolabel] Container.SortOrder",
            "Container.Totaltime": "The total time of all items in the current container.",
            "Container.TotalUnWatched": "The number of unwatched items in the container. Parameters id- [opt] if not supplied the current container will be used. v16 Skinning engine changes:[New Infolabel] Container(id).TotalUnWatched",
            "Container.TotalWatched": "The number of watched items in the container. Parameters id- [opt] if not supplied the current container will be used. v16 Skinning engine changes:[New Infolabel] Container(id).TotalWatched",
            "Container.ViewCount": "The number of available skin view modes for the current container listing. v17 Skinning engine changes:[New Infolabel] Container.ViewCount",
            "Container.Viewmode": "The current viewmode (list, icons etc).",
            "Control.GetLabel(id)[.index()]": "The label value or texture name of the control with the given id. Parameters id- The id of the control index- [opt] Optionally you can specify index(1) to retrieve label2 from an Edit control. v15 Skinning engine changes:[Infolabel Updated] Control.GetLabel(id) added index parameter - allows skinner to retrieve label2 of a control. Only edit controls are supported. Example** : Control.GetLabel(999).index(1) where: index(0) = label index(1) = label2",
            "Control.HasFocus(id)": "True if the currently focused control has id 'id'. Parameters id- The id of the control",
            "Control.IsEnabled(id)": "True if the control with id 'id' is enabled. Parameters id- The id of the control",
            "Control.IsVisible(id)": "True if the control with id 'id' is visible. Parameters id- The id of the control",
            "Fanart.Color1": "The first of three colors included in the currently selected Fanart theme for the parent TV Show. NoteColors are arranged Lightest to Darkest.",
            "Fanart.Color2": "The second of three colors included in the currently selected Fanart theme for the parent TV Show. NoteColors are arranged Lightest to Darkest.",
            "Fanart.Color3": "The third of three colors included in the currently selected Fanart theme for the parent TV Show. NoteColors are arranged Lightest to Darkest.",
            "Fanart.Image": "The fanart image, if any",
            "Library.HasContent(boxsets)": "True if there are albums in the library which are boxsets. v19 Skinning engine changes:[New Boolean Condition] Library.HasContent(boxsets)",
            "Library.HasContent(compilations)": "True if the library has compilations.",
            "Library.HasContent(movies)": "True if the library has movies.",
            "Library.HasContent(moviesets)": "True if the library has movie sets.",
            "Library.HasContent(music)": "True if the library has music content.",
            "Library.HasContent(musicvideos)": "True if the library has music videos.",
            "Library.HasContent(Role.Arranger)": "True if there are songs in the library which have an arranger. v17 Skinning engine changes:[New Boolean Condition] Library.HasContent(Role.Arranger)",
            "Library.HasContent(Role.Composer)": "True if there are songs in the library which have composers. v17 Skinning engine changes:[New Boolean Condition] Library.HasContent(Role.Composer)",
            "Library.HasContent(Role.Conductor)": "True if there are songs in the library which have a conductor. v17 Skinning engine changes:[New Boolean Condition] Library.HasContent(Role.Conductor)",
            "Library.HasContent(Role.DJMixer)": "True if there are songs in the library which have a DJMixer. v17 Skinning engine changes:[New Boolean Condition] Library.HasContent(Role.DJMixer)",
            "Library.HasContent(Role.Engineer)": "True if there are songs in the library which have an engineer. v17 Skinning engine changes:[New Boolean Condition] Library.HasContent(Role.Engineer)",
            "Library.HasContent(Role.Lyricist)": "True if there are songs in the library which have a lyricist. v17 Skinning engine changes:[New Boolean Condition] Library.HasContent(Role.Lyricist)",
            "Library.HasContent(Role.Mixer)": "True if there are songs in the library which have a mixer. v17 Skinning engine changes:[New Boolean Condition] Library.HasContent(Role.Mixer)",
            "Library.HasContent(Role.Orchestra)": "True if there are songs in the library which have an orchestra. v17 Skinning engine changes:[New Boolean Condition] Library.HasContent(Role.Orchestra)",
            "Library.HasContent(Role.Producer)": "True if there are songs in the library which have an producer. v17 Skinning engine changes:[New Boolean Condition] Library.HasContent(Role.Producer)",
            "Library.HasContent(Role.Remixer)": "True if there are songs in the library which have a remixer. v17 Skinning engine changes:[New Boolean Condition] Library.HasContent(Role.Remixer)",
            "Library.HasContent(singles)": "True if the library has singles.",
            "Library.HasContent(tvshows)": "True if the library has tvshows.",
            "Library.HasContent(video)": "True if the library has video content.",
            "Library.HasNode(path)": "True if there the node is present in the library. v19 Skinning engine changes:[New Boolean Condition] Library.HasNode(path)",
            "Library.IsScanning": "True if the library is being scanned.",
            "Library.IsScanningMusic": "True if the music library is being scanned.",
            "Library.IsScanningVideo": "True if the video library is being scanned.",
            "ListItem.ActualIcon": "The icon of the currently selected item in a list or thumb control.",
            "ListItem.AddonBroken": "A message when the addon is marked as broken in the repo. Deprecated:but still available, use ListItem.AddonLifecycleDesc instead v17 Skinning engine changes:[Infolabel Updated] ListItem.AddonBroken replaces ListItem.Property(Addon.Broken).",
            "ListItem.AddonCreator": "The name of the author the currently selected addon. v17 Skinning engine changes:[Infolabel Updated] ListItem.AddonCreator replaces ListItem.Property(Addon.Creator).",
            "ListItem.AddonDescription": "The full description of the currently selected addon. v17 Skinning engine changes:[Infolabel Updated] ListItem.AddonDescription replaces ListItem.Property(Addon.Description).",
            "ListItem.AddonDisclaimer": "The disclaimer of the currently selected addon. v17 Skinning engine changes:[Infolabel Updated] ListItem.AddonDisclaimer replaces ListItem.Property(Addon.Disclaimer).",
            "ListItem.AddonLifecycleDesc": "From addon defined message text when it is marked as special condition inside repository. v19 Skinning engine changes:[New Infolabel] ListItem.AddonLifecycleDesc\endlink replacesListItem.AddonBroken`.",
            "ListItem.AddonLifecycleType": "String name when the addon is marked as special condition in the repo. Label: 24169 (Normal) - Used if an add-on has no special lifecycle state which is the default state Label: 24170 (Deprecated) - The add-on should be marked as deprecated but is still usable Label: 24171 (Broken) - The add-on should marked as broken in the repository v19 Skinning engine changes:[New Infolabel] ListItem.AddonLifecycleType replaces ListItem.AddonBroken.",
            "ListItem.AddonName": "The name of the currently selected addon. v17 Skinning engine changes:[Infolabel Updated] ListItem.AddonName replaces ListItem.Property(Addon.Name).",
            "ListItem.AddonSummary": "A short description of the currently selected addon. v17 Skinning engine changes:[Infolabel Updated] ListItem.AddonSummary replaces ListItem.Property(Addon.Summary).",
            "ListItem.AddonVersion": "The version of the currently selected addon. v17 Skinning engine changes:[Infolabel Updated] ListItem.AddonVersion replaces ListItem.Property(Addon.Version).",
            "ListItem.Album": "The album of the currently selected song in a container.",
            "ListItem.AlbumArtist": "The artist of the currently selected album in a list.",
            "ListItem.Appearances": "The number of movies featuring the selected actor / directed by the selected director. v17 Skinning engine changes:[New Infolabel] ListItem.Appearances",
            "ListItem.Artist": "The artist of the currently selected song in a container.",
            "ListItem.AudioChannels": "The number of audio channels of the currently selected video. Possible values: 1 2 4 5 6 8 10 v16 Skinning engine changes:[Infolabel Updated] ListItem.AudioChannels if a video contains no audio, these infolabels will now return empty. (they used to return 0)",
            "ListItem.AudioCodec": "The audio codec of the currently selected video. Common values: aac ac3 cook dca dtshd_hra dtshd_ma eac3 mp1 mp2 mp3 pcm_s16be pcm_s16le pcm_u8 truehd vorbis wmapro wmav2",
            "ListItem.AudioLanguage": "The audio language of the currently selected video (an ISO 639-2 three character code: e.g. eng, epo, deu)",
            "ListItem.Cast": "A concatenated string of cast members of the currently selected movie, for use in dialogvideoinfo.xml. v15 Skinning engine changes:[Infolabel Updated] ListItem.Cast also supports EPG.",
            "ListItem.CastAndRole": "A concatenated string of cast members and roles of the currently selected movie, for use in dialogvideoinfo.xml.",
            "ListItem.ChannelGroup": "The channel group of the selected item (PVR).",
            "ListItem.ChannelName": "The name of current selected TV channel in a container.",
            "ListItem.ChannelNumberLabel": "The channel and subchannel number of the currently selected channel that's currently playing (PVR). v14 Skinning engine changes:[New Infolabel] ListItem.ChannelNumberLabel",
            "ListItem.Comment": "The comment assigned to the item (PVR/MUSIC).",
            "ListItem.ContributorAndRole": "The list of all people and their role who've contributed to the selected song. v17 Skinning engine changes:[New Infolabel] ListItem.ContributorAndRole",
            "ListItem.Contributors": "The list of all people who've contributed to the selected song. v17 Skinning engine changes:[New Infolabel] ListItem.Contributors",
            "ListItem.Country": "The production country of the currently selected movie in a container.",
            "ListItem.Date": "The file date of the currently selected song or movie in a container / Aired date of an episode / Day, start time and end time of current selected TV programme (PVR).",
            "ListItem.DateAdded": "The date the currently selected item was added to the library / Date and time of an event in the EventLog window.",
            "ListItem.DateTime": "The date and time a certain event happened (event log). v16 Skinning engine changes:[New Infolabel] ListItem.DateTime",
            "ListItem.DBID": "The database id of the currently selected listitem in a container.",
            "ListItem.DBTYPE": "The database type of the ListItem.DBID for videos (movie, set, genre, actor, tvshow, season, episode). It does not return any value for the music library. NoteBeware with season, the '*all seasons' entry does give a DBTYPE 'season' and a DBID, but you can't get the details of that entry since it's a virtual entry in the Video Library. v17 Skinning engine changes:[Infolabel Updated] ListItem.DBTYPE now available in the music library.",
            "ListItem.Director": "The director of the currently selected movie in a container. v15 Skinning engine changes:[Infolabel Updated] ListItem.Director also supports EPG.",
            "ListItem.DiscNumber": "The disc number of the currently selected song in a container.",
            "ListItem.Duration": "The duration of the currently selected item in a container in the format hh:mm:ss. Notehh: will be omitted if hours value is zero. v18 Skinning engine changes:[Infolabel Updated] ListItem.Duration will return hh:mm:ss instead of the duration in minutes.",
            "ListItem.Duration(format)": "The duration of the currently selected item in a container in different formats. Parameters format[opt] The format of the return time value. See TIME_FORMAT for the list of possible values.",
            "ListItem.EndDate": "The end date of current selected TV programme in a container.",
            "ListItem.EndTime": "The end time of current selected TV programme in a container.",
            "ListItem.EndTimeResume": "the time a video will end if you resume it, instead of playing it from the beginning. v17 Skinning engine changes:[New Infolabel] ListItem.EndTimeResume",
            "ListItem.EpgEventIcon": "The thumbnail for the EPG event associated with the item (if it exists). v18 Skinning engine changes:[New Infolabel] ListItem.EpgEventIcon",
            "ListItem.EpgEventTitle": "The title of the epg event associated with the item, if any.",
            "ListItem.Episode": "The episode number value for the currently selected episode. It also returns the number of total, watched or unwatched episodes for the currently selected tvshow or season, based on the the current watched filter. v15 Skinning engine changes:[Infolabel Updated] ListItem.Episode also supports EPG.",
            "ListItem.EpisodeName": "The name of the episode if the selected EPG item is a TV Show (PVR). v15 Skinning engine changes:[New Infolabel] ListItem.EpisodeName",
            "ListItem.FileExtension": "The file extension (without leading dot) of the currently selected item in a container.",
            "ListItem.FileName": "The filename of the currently selected song or movie in a container.",
            "ListItem.FileNameAndPath": "The full path with filename of the currently selected song or movie in a container.",
            "ListItem.FileNameNoExtension": "The filename without extension of the currently selected item in a container. v19 Skinning engine changes:[New Infolabel] ListItem.FileNameNoExtension",
            "ListItem.FolderName": "The top most folder of the path of the currently selected song or movie in a container.",
            "ListItem.FolderPath": "The complete path of the currently selected song or movie in a container (without user details).",
            "ListItem.Genre": "The genre of the currently selected song, album or movie in a container.",
            "ListItem.HasArchive": "True when the selected channel has a server-side back buffer (PVR) v19 Skinning engine changes:[New Boolean Condition] ListItem.HasArchive",
            "ListItem.HasEpg": "True when the selected programme has epg info (PVR).",
            "ListItem.HasRecording": "True if a given epg tag item currently gets recorded or has been recorded.",
            "ListItem.HasReminder": "True if the item has a reminder set (PVR). v19 Skinning engine changes:[New Boolean Condition] ListItem.HasReminder",
            "ListItem.HasReminderRule": "True if the item was scheduled by a reminder timer rule (PVR). v19 Skinning engine changes:[New Boolean Condition] ListItem.HasReminderRule",
            "ListItem.HasTimer": "True when a recording timer has been set for the selected programme (PVR).",
            "ListItem.HasTimerSchedule": "True if the item was scheduled by a timer rule (PVR). v16 Skinning engine changes:[New Boolean Condition] ListItem.HasTimerSchedule",
            "ListItem.Icon": "The thumbnail (if it exists) of the currently selected item in a list or thumb control. NoteIf no thumbnail image exists, it will show the icon.",
            "ListItem.IMDBNumber": "The IMDb ID of the selected Video in a container. v15 Skinning engine changes:[New Infolabel] ListItem.IMDBNumber",
            "ListItem.InProgress": "True if the EPG event item is currently active (time-wise).",
            "ListItem.IsAutoUpdateable": "True if this add-on can be updated automatically. v19 Skinning engine changes:[New Boolean Condition] ListItem.IsAutoUpdateable",
            "ListItem.IsCollection": "True when the current ListItem is a movie set. v15 Skinning engine changes:[New Boolean Condition] ListItem.IsCollection",
            "ListItem.IsEncrypted": "True when the selected programme is encrypted (PVR).",
            "ListItem.IsFolder": "True if the current ListItem is a folder.",
            "ListItem.IsParentFolder": "True if the current list item is the goto parent folder '..'. v17 Skinning engine changes:[New Boolean Condition] ListItem.IsParentFolder",
            "ListItem.IsPlayable": "True when the selected programme can be played (PVR) v19 Skinning engine changes:[New Boolean Condition] ListItem.IsPlayable",
            "ListItem.IsPlaying": "True if the current ListItem.* info labels and images are currently Playing media.",
            "ListItem.IsRecording": "True when the selected programme is being recorded (PVR).",
            "ListItem.IsResumable": "True when the current ListItem has been partially played.",
            "ListItem.IsSelected": "True if the current ListItem is selected (f.e. currently playing in playlist window).",
            "ListItem.IsStereoscopic": "True when the selected video is a 3D (stereoscopic) video. v13 Skinning engine changes:[New Boolean Condition] ListItem.IsStereoscopic",
            "ListItem.Label": "The left label of the currently selected item in a container.",
            "ListItem.Label2": "The right label of the currently selected item in a container.",
            "ListItem.LastPlayed": "The last play date of Video in a container.",
            "ListItem.Mood": "The mood of the selected song. v17 Skinning engine changes:[New Infolabel] ListItem.Mood",
            "ListItem.Mpaa": "The MPAA rating of the currently selected movie in a container.",
            "ListItem.NextDuration": "The duration of the next item (PVR) in the format hh:mm:ss. Notehh: will be omitted if hours value is zero. v18 Skinning engine changes:[New Infolabel] ListItem.NextDuration",
            "ListItem.NextDuration(format)": "The duration of the next item (PVR) in different formats. Parameters format[opt] The format of the return time value. See TIME_FORMAT for the list of possible values. v18 Skinning engine changes:[New Infolabel] ListItem.NextDuration(format)",
            "ListItem.NextEndDate": "The end date of the next item (PVR).",
            "ListItem.NextEndTime": "The end of the next item (PVR).",
            "ListItem.NextGenre": "The genre of the next item (PVR).",
            "ListItem.NextPlot": "The plot of the next item (PVR).",
            "ListItem.NextPlotOutline": "The plot outline of the next item (PVR).",
            "ListItem.NextStartDate": "The start date of the next item (PVR).",
            "ListItem.NextStartTime": "The start time of the next item (PVR).",
            "ListItem.NextTitle": "The title of the next item (PVR).",
            "ListItem.OriginalTitle": "The original title of the currently selected movie in a container.",
            "ListItem.Overlay": "The overlay icon status of the currently selected item in a list or thumb control. compressed file - OverlayRAR.png watched - OverlayWatched.png unwatched - OverlayUnwatched.png locked - OverlayLocked.png",
            "ListItem.Path": "The complete path of the currently selected song or movie in a container.",
            "ListItem.PercentPlayed": "The percentage value [0-100] of how far the selected video has been played.",
            "ListItem.PictureAperture": "The F-stop used to take the selected picture. NoteThis is the value of the EXIF FNumber tag (hex code 0x829D).",
            "ListItem.PictureAuthor": "The name of the person involved in writing about the selected picture. NoteThis is the value of the IPTC Writer tag (hex code 0x7A). v13 Skinning engine changes:[New Infolabel] ListItem.PictureAuthor",
            "ListItem.PictureByline": "The name of the person who created the selected picture. NoteThis is the value of the IPTC Byline tag (hex code 0x50). v13 Skinning engine changes:[New Infolabel] ListItem.PictureByline",
            "ListItem.PictureBylineTitle": "The title of the person who created the selected picture. NoteThis is the value of the IPTC BylineTitle tag (hex code 0x55). v13 Skinning engine changes:[New Infolabel] ListItem.PictureBylineTitle",
            "ListItem.PictureCamMake": "The manufacturer of the camera used to take the selected picture. NoteThis is the value of the EXIF Make tag (hex code 0x010F).",
            "ListItem.PictureCamModel": "The manufacturer's model name or number of the camera used to take the selected picture. NoteThis is the value of the EXIF Model tag (hex code 0x0110).",
            "ListItem.PictureCaption": "A description of the selected picture. NoteThis is the value of the IPTC Caption tag (hex code 0x78).",
            "ListItem.PictureCategory": "The subject of the selected picture as a category code. NoteThis is the value of the IPTC Category tag (hex code 0x0F). v13 Skinning engine changes:[New Infolabel] ListItem.PictureCategory",
            "ListItem.PictureCCDWidth": "The width of the CCD in the camera used to take the selected picture. NoteThis is calculated from three EXIF tags (0xA002 * 0xA210 / 0xA20e). v13 Skinning engine changes:[New Infolabel] ListItem.PictureCCDWidth",
            "ListItem.PictureCity": "The city where the selected picture was taken. NoteThis is the value of the IPTC City tag (hex code 0x5A). v13 Skinning engine changes:[New Infolabel] ListItem.PictureCity",
            "ListItem.PictureColour": "Whether the selected picture is 'Colour' or 'Black and White'. v13 Skinning engine changes:[New Infolabel] ListItem.PictureColour",
            "ListItem.PictureComment": "A description of the selected picture. NoteThis is the value of the EXIF User Comment tag (hex code 0x9286). This is the same value as Slideshow.SlideComment.",
            "ListItem.PictureCopyrightNotice": "The copyright notice of the selected picture. NoteThis is the value of the IPTC Copyright tag (hex code 0x74). v13 Skinning engine changes:[New Infolabel] ListItem.PictureCopyrightNotice",
            "ListItem.PictureCountry": "The full name of the country where the selected picture was taken. NoteThis is the value of the IPTC CountryName tag (hex code 0x65). v13 Skinning engine changes:[New Infolabel] ListItem.PictureCountry",
            "ListItem.PictureCountryCode": "The country code of the country where the selected picture was taken. NoteThis is the value of the IPTC CountryCode tag (hex code 0x64). v13 Skinning engine changes:[New Infolabel] ListItem.PictureCountryCode",
            "ListItem.PictureCredit": "Who provided the selected picture. NoteThis is the value of the IPTC Credit tag (hex code 0x6E). v13 Skinning engine changes:[New Infolabel] ListItem.PictureCredit",
            "ListItem.PictureDate": "The localized date of the selected picture. The short form of the date is used. NoteThe value of the EXIF DateTimeOriginal tag (hex code 0x9003) is preferred. If the DateTimeOriginal tag is not found, the value of DateTimeDigitized (hex code 0x9004) or of DateTime (hex code 0x0132) might be used. v13 Skinning engine changes:[New Infolabel] ListItem.PictureDate",
            "ListItem.PictureDatetime": "The date/timestamp of the selected picture. The localized short form of the date and time is used. NoteThe value of the EXIF DateTimeOriginal tag (hex code 0x9003) is preferred. If the DateTimeOriginal tag is not found, the value of DateTimeDigitized (hex code 0x9004) or of DateTime (hex code 0x0132) might be used. v13 Skinning engine changes:[New Infolabel] ListItem.PictureDatetime",
            "ListItem.PictureDesc": "A short description of the selected picture. The SlideComment, EXIFComment, or Caption values might contain a longer description. NoteThis is the value of the EXIF ImageDescription tag (hex code 0x010E).",
            "ListItem.PictureDigitalZoom": "The digital zoom ratio when the selected picture was taken. NoteThis is the value of the EXIF DigitalZoomRatio tag (hex code 0xA404). v13 Skinning engine changes:[New Infolabel] ListItem.PictureDigitalZoom",
            "ListItem.PictureExpMode": "The exposure mode of the selected picture. The possible values are: 'Automatic' 'Manual' 'Auto bracketing' NoteThis is the value of the EXIF ExposureMode tag (hex code 0xA402).",
            "ListItem.PictureExposure": "The class of the program used by the camera to set exposure when the selected picture was taken. Values include: 'Manual' 'Program (Auto)' 'Aperture priority (Semi-Auto)' 'Shutter priority (semi-auto)' etc NoteThis is the value of the EXIF ExposureProgram tag (hex code 0x8822). v13 Skinning engine changes:[New Infolabel] ListItem.PictureExposure",
            "ListItem.PictureExposureBias": "The exposure bias of the selected picture. Typically this is a number between -99.99 and 99.99. NoteThis is the value of the EXIF ExposureBiasValue tag (hex code 0x9204). v13 Skinning engine changes:[New Infolabel] ListItem.PictureExposureBias",
            "ListItem.PictureExpTime": "The exposure time of the selected picture, in seconds. NoteThis is the value of the EXIF ExposureTime tag (hex code 0x829A). If the ExposureTime tag is not found, the ShutterSpeedValue tag (hex code 0x9201) might be used.",
            "ListItem.PictureFlashUsed": "The status of flash when the selected picture was taken. The value will be either 'Yes' or 'No', and might include additional information. NoteThis is the value of the EXIF Flash tag (hex code 0x9209). v13 Skinning engine changes:[New Infolabel] ListItem.PictureFlashUsed",
            "ListItem.PictureFocalLen": "The lens focal length of the selected picture.",
            "ListItem.PictureFocusDist": "The focal length of the lens, in mm. NoteThis is the value of the EXIF FocalLength tag (hex code 0x920A).",
            "ListItem.PictureGPSAlt": "The altitude in meters where the selected picture was taken. NoteThis is the value of the EXIF GPSInfo.GPSAltitude tag.",
            "ListItem.PictureGPSLat": "The latitude where the selected picture was taken (degrees, minutes, seconds North or South). NoteThis is the value of the EXIF GPSInfo.GPSLatitude and GPSInfo.GPSLatitudeRef tags.",
            "ListItem.PictureGPSLon": "The longitude where the selected picture was taken (degrees, minutes, seconds East or West). NoteThis is the value of the EXIF GPSInfo.GPSLongitude and GPSInfo.GPSLongitudeRef tags.",
            "ListItem.PictureHeadline": "A synopsis of the contents of the selected picture. NoteThis is the value of the IPTC Headline tag (hex code 0x69). v13 Skinning engine changes:[New Infolabel] ListItem.PictureHeadline",
            "ListItem.PictureImageType": "The color components of the selected picture. NoteThis is the value of the IPTC ImageType tag (hex code 0x82). v13 Skinning engine changes:[New Infolabel] ListItem.PictureImageType",
            "ListItem.PictureIPTCDate": "The date when the intellectual content of the selected picture was created, rather than when the picture was created. NoteThis is the value of the IPTC DateCreated tag (hex code 0x37). v13 Skinning engine changes:[New Infolabel] ListItem.PictureIPTCDate",
            "ListItem.PictureIPTCTime": "The time when the intellectual content of the selected picture was created, rather than when the picture was created. NoteThis is the value of the IPTC TimeCreated tag (hex code 0x3C). v13 Skinning engine changes:[New Infolabel] ListItem.PictureIPTCTime",
            "ListItem.PictureISO": "The ISO speed of the camera when the selected picture was taken. NoteThis is the value of the EXIF ISOSpeedRatings tag (hex code 0x8827).",
            "ListItem.PictureKeywords": "The keywords assigned to the selected picture. NoteThis is the value of the IPTC Keywords tag (hex code 0x19).",
            "ListItem.PictureLightSource": "The kind of light source when the picture was taken. Possible values include: 'Daylight' 'Fluorescent' 'Incandescent' etc NoteThis is the value of the EXIF LightSource tag (hex code 0x9208). v13 Skinning engine changes:[New Infolabel] ListItem.PictureLightSource",
            "ListItem.PictureLongDate": "Only the localized date of the selected picture. The long form of the date is used. NoteThe value of the EXIF DateTimeOriginal tag (hex code 0x9003) is preferred. If the DateTimeOriginal tag is not found, the value of DateTimeDigitized (hex code 0x9004) or of DateTime (hex code 0x0132) might be used. v13 Skinning engine changes:[New Infolabel] ListItem.PictureLongDate",
            "ListItem.PictureLongDatetime": "The date/timestamp of the selected picture. The localized long form of the date and time is used. NoteThe value of the EXIF DateTimeOriginal tag (hex code 0x9003) is preferred. if the DateTimeOriginal tag is not found, the value of DateTimeDigitized (hex code 0x9004) or of DateTime (hex code 0x0132) might be used.",
            "ListItem.PictureMeteringMode": "The metering mode used when the selected picture was taken. The possible values are: 'Center weight' 'Spot' 'Matrix' NoteThis is the value of the EXIF MeteringMode tag (hex code 0x9207). v13 Skinning engine changes:[New Infolabel] ListItem.PictureMeteringMode",
            "ListItem.PictureObjectName": "A shorthand reference for the selected picture. NoteThis is the value of the IPTC ObjectName tag (hex code 0x05). v13 Skinning engine changes:[New Infolabel] ListItem.PictureObjectName",
            "ListItem.PictureOrientation": "The orientation of the selected picture. Possible values are: 'Top Left' 'Top Right' 'Left Top' 'Right Bottom' etc NoteThis is the value of the EXIF Orientation tag (hex code 0x0112). v13 Skinning engine changes:[New Infolabel] ListItem.PictureOrientation",
            "ListItem.PicturePath": "The filename and path of the selected picture.",
            "ListItem.PictureProcess": "The process used to compress the selected picture. v13 Skinning engine changes:[New Infolabel] ListItem.PictureProcess",
            "ListItem.PictureReferenceService": "The Service Identifier of a prior envelope to which the selected picture refers. NoteThis is the value of the IPTC ReferenceService tag (hex code 0x2D). v13 Skinning engine changes:[New Infolabel] ListItem.PictureReferenceService",
            "ListItem.PictureResolution": "The dimensions of the selected picture.",
            "ListItem.PictureSource": "The original owner of the selected picture. NoteThis is the value of the IPTC Source tag (hex code 0x73). v13 Skinning engine changes:[New Infolabel] ListItem.PictureSource",
            "ListItem.PictureSpecialInstructions": "Other editorial instructions concerning the use of the selected picture. NoteThis is the value of the IPTC SpecialInstructions tag (hex code 0x28). v13 Skinning engine changes:[New Infolabel] ListItem.PictureSpecialInstructions",
            "ListItem.PictureState": "The State/Province where the selected picture was taken. NoteThis is the value of the IPTC ProvinceState tag (hex code 0x5F). v13 Skinning engine changes:[New Infolabel] ListItem.PictureState",
            "ListItem.PictureSublocation": "The location within a city where the selected picture was taken - might indicate the nearest landmark. NoteThis is the value of the IPTC SubLocation tag (hex code 0x5C). v13 Skinning engine changes:[New Infolabel] ListItem.PictureSublocation",
            "ListItem.PictureSupplementalCategories": "A supplemental category codes to further refine the subject of the selected picture. NoteThis is the value of the IPTC SuppCategory tag (hex code 0x14). v13 Skinning engine changes:[New Infolabel] ListItem.PictureSupplementalCategories",
            "ListItem.PictureTransmissionReference": "A code representing the location of original transmission of the selected picture. NoteThis is the value of the IPTC TransmissionReference tag (hex code 0x67). v13 Skinning engine changes:[New Infolabel] ListItem.PictureTransmissionReference",
            "ListItem.PictureUrgency": "The urgency of the selected picture. Values are 1-9. NoteThe '1' is most urgent. Some image management programs use urgency to indicate picture rating, where urgency '1' is 5 stars and urgency '5' is 1 star. Urgencies 6-9 are not used for rating. This is the value of the IPTC Urgency tag (hex code 0x0A). v13 Skinning engine changes:[New Infolabel] ListItem.PictureUrgency",
            "ListItem.PictureWhiteBalance": "The white balance mode set when the selected picture was taken. The possible values are: 'Manual' 'Auto' NoteThis is the value of the EXIF WhiteBalance tag (hex code 0xA403). v13 Skinning engine changes:[New Infolabel] ListItem.PictureWhiteBalance",
            "ListItem.PlayCount": "The playcount of Video in a container.",
            "ListItem.Plot": "The complete Text Summary of Video in a container.",
            "ListItem.PlotOutline": "A small Summary of current Video in a container.",
            "ListItem.Premiered": "The release/aired date of the currently selected episode, show, movie or EPG item in a container. v15 Skinning engine changes:[Infolabel Updated] ListItem.Premiered now also available for EPG items.",
            "ListItem.ProgramCount": "The number of times an xbe has been run from 'my programs'. Todo:description might be outdated",
            "ListItem.Progress": "The part of the programme that's been played (PVR).",
            "ListItem.Property(Addon.Changelog)": "The changelog of the currently selected addon.",
            "ListItem.Property(Addon.Disclaimer)": "The disclaimer of the currently selected addon.",
            "ListItem.Property(Addon.HasUpdate)": "True when there's an update available for the selected addon. v17 Skinning engine changes:[Boolean Condition Updated] ListItem.Property(Addon.HasUpdate) replaces ListItem.Property(Addon.UpdateAvail).",
            "ListItem.Property(Addon.ID)": "The identifier of the currently selected addon.",
            "ListItem.Property(Addon.IsBinary)": "True if this add-on is a binary addon. v19 Skinning engine changes:[New Boolean Condition] ListItem.Property(Addon.IsBinary)",
            "ListItem.Property(Addon.IsEnabled)": "True when the selected addon is enabled (for use in the addon info dialog only). v17 Skinning engine changes:[Boolean Condition Updated] ListItem.Property(Addon.IsEnabled) replaces ListItem.Property(Addon.Enabled). [Infolabel Updated] ListItem.Ratings for songs it's now the scraped rating. [Infolabel Updated] ListItem.RatingAndVotes now available for albums/songs.",
            "ListItem.Property(Addon.IsFromOfficialRepo)": "True if this add-on is from an official repository. v19 Skinning engine changes:[New Boolean Condition] ListItem.Property(Addon.IsFromOfficialRepo)",
            "ListItem.Property(Addon.IsInstalled)": "True when the selected addon is installed (for use in the addon info dialog only). v17 Skinning engine changes:[Boolean Condition Updated] ListItem.Property(Addon.IsInstalled) replaces ListItem.Property(Addon.Installed).",
            "ListItem.Property(Addon.IsUpdate)": "True if this add-on is a valid update of an installed outdated add-on. v19 Skinning engine changes:[New Boolean Condition] ListItem.Property(Addon.IsUpdate)",
            "ListItem.Property(Addon.Orphaned)": "True if the Addon is orphanad. Todo:missing reference in GuiInfoManager.cpp making it hard to track. v17 Skinning engine changes:[New Boolean Condition] ListItem.Property(Addon.Orphaned)",
            "ListItem.Property(Addon.Path)": "The path of the currently selected addon.",
            "ListItem.Property(Addon.Status)": "The status of the currently selected addon. Todo:missing reference in GuiInfoManager.cpp making it hard to track.",
            "ListItem.Property(Album_Description)": "A review of the currently selected Album.",
            "ListItem.Property(Album_Duration)": "The duration of the album in HH:MM:SS. v19 Skinning engine changes:[New Infolabel] ListItem.Property(Album_Duration)",
            "ListItem.Property(Album_Isboxset)": "True if the album is a boxset. v19 Skinning engine changes:[New Infobool] ListItem.Property(Album_Isboxset)",
            "ListItem.Property(Album_Label)": "The record label of the currently selected Album.",
            "ListItem.Property(Album_Mood)": "The moods of the currently selected Album.",
            "ListItem.Property(Album_Style)": "The styles of the currently selected Album.",
            "ListItem.Property(Album_Theme)": "The themes of the currently selected Album.",
            "ListItem.Property(Album_Totaldiscs)": "The total number of discs belonging to an album. v19 Skinning engine changes:[New Infolabel] ListItem.Property(Album_Totaldiscs)",
            "ListItem.Property(Album_Type)": "The Album Type (e.g. compilation, enhanced, explicit lyrics) of the currently selected Album.",
            "ListItem.Property(Artist_Born)": "The date of Birth of the currently selected Artist.",
            "ListItem.Property(Artist_Description)": "A biography of the currently selected artist.",
            "ListItem.Property(Artist_Died)": "The date of Death of the currently selected Artist.",
            "ListItem.Property(Artist_Disambiguation)": "A Brief description of the currently selected Artist that differentiates them from others with the same name. v18 Skinning engine changes:[New Infolabel] ListItem.Property(Artist_Disambiguation)",
            "ListItem.Property(Artist_Disbanded)": "The disbanding date of the currently selected Band.",
            "ListItem.Property(Artist_Formed)": "The formation date of the currently selected Band.",
            "ListItem.Property(Artist_Gender)": "The Gender of the currently selected Artist - male, female, other. v18 Skinning engine changes:[New Infolabel] ListItem.Property(Artist_Gender)",
            "ListItem.Property(Artist_Genre)": "The genre of the currently selected artist.",
            "ListItem.Property(Artist_Instrument)": "The instruments played by the currently selected artist.",
            "ListItem.Property(Artist_Mood)": "The moods of the currently selected artist.",
            "ListItem.Property(Artist_Sortname)": "The sortname of the currently selected Artist. v18 Skinning engine changes:[New Infolabel] ListItem.Property(Artist_Sortname)",
            "ListItem.Property(Artist_Style)": "The styles of the currently selected artist.",
            "ListItem.Property(Artist_Type)": "The type of the currently selected Artist - person, group, orchestra, choir etc. v18 Skinning engine changes:[New Infolabel] ListItem.Property(Artist_Type)",
            "ListItem.Property(Artist_YearsActive)": "The years the currently selected artist has been active.",
            "ListItem.Property(AudioChannels.[n])": "The number of audio channels of the currently selected video Parameters n- the number of the audiostream (values: see ListItem.AudioChannels) v16 Skinning engine changes:[New Infolabel] ListItem.Property(AudioChannels.[n])",
            "ListItem.Property(AudioCodec.[n])": "The audio codec of the currently selected video Parameters n- the number of the audiostream (values: see ListItem.AudioCodec) v16 Skinning engine changes:[New Infolabel] ListItem.Property(AudioCodec.[n])",
            "ListItem.Property(AudioLanguage.[n])": "The audio language of the currently selected video Parameters n- the number of the audiostream (values: see ListItem.AudioLanguage) v16 Skinning engine changes:[New Infolabel] ListItem.Property(AudioLanguage.[n])",
            "ListItem.Property(DateLabel)": "True if the item is a date label, returns false if the item is a time label. NoteCan be used in the rulerlayout of the epggrid control.",
            "ListItem.Property(IsSpecial)": "True if the current Season/Episode is a Special.",
            "ListItem.Property(NumEpisodes)": "The number of total, watched or unwatched episodes for the currently selected tvshow or season, based on the the current watched filter.",
            "ListItem.Property(SubtitleLanguage.[n])": "The subtitle language of the currently selected video Parameters n- the number of the subtitle (values: see ListItem.SubtitleLanguage) v16 Skinning engine changes:[New Infolabel] ListItem.Property(SubtitleLanguage.[n])",
            "ListItem.Property(TotalEpisodes)": "The total number of episodes for the currently selected tvshow or season.",
            "ListItem.Property(TotalSeasons)": "The total number of seasons for the currently selected tvshow.",
            "ListItem.Property(UnWatchedEpisodes)": "The number of unwatched episodes for the currently selected tvshow or season.",
            "ListItem.Property(WatchedEpisodes)": "The number of watched episodes for the currently selected tvshow or season.",
            "ListItem.Rating([name])": "The scraped rating of the currently selected item in a container (1-10). Parameters name- [opt] you can specify the name of the scraper to retrieve a specific rating, for use in dialogvideoinfo.xml. v18 Skinning engine changes:[Infolabel Updated] ListItem.Rating([name]) replaces the old ListItem.Ratings([name]) infolabel. v17 Skinning engine changes:[New Infolabel] ListItem.Ratings([name])",
            "ListItem.RatingAndVotes([name])": "The scraped rating and votes of the currently selected movie in a container (1-10). Parameters name- [opt] you can specify the name of the scraper to retrieve specific votes, for use in dialogvideoinfo.xml. v17 Skinning engine changes:[New Infolabel] ListItem.RatingAndVotes([name])",
            "ListItem.Season": "The season value for the currently selected tvshow. v15 Skinning engine changes:[Infolabel Updated] ListItem.Season also supports EPG.",
            "ListItem.Set": "The name of the set the movie is part of. v17 Skinning engine changes:[New Infolabel] ListItem.Set",
            "ListItem.SetId": "The id of the set the movie is part of. v17 Skinning engine changes:[New Infolabel] ListItem.SetId",
            "ListItem.Size": "The file size of the currently selected song or movie in a container.",
            "ListItem.SortLetter": "The first letter of the current file in a container.",
            "ListItem.StartDate": "The start date of current selected TV programme in a container.",
            "ListItem.StartTime": "The start time of current selected TV programme in a container.",
            "ListItem.Status": "ReturnsOne of the following status: 'returning series' 'in production' 'planned' 'cancelled' 'ended' NoteFor use with tv shows. v17 Skinning engine changes:[New Infolabel] ListItem.Status",
            "ListItem.StereoscopicMode": "The stereomode of the selected video: mono split_vertical split_horizontal row_interleaved anaglyph_cyan_red anaglyph_green_magenta v13 Skinning engine changes:[New Infolabel] ListItem.StereoscopicMode",
            "ListItem.Studio": "The studio of current selected Music Video in a container.",
            "ListItem.SubtitleLanguage": "The subtitle language of the currently selected video (an ISO 639-2 three character code: e.g. eng, epo, deu)",
            "ListItem.Tag": "The summary of current Video in a container. v17 Skinning engine changes:[New Infolabel] ListItem.Tag",
            "ListItem.Tagline": "A Small Summary of current Video in a container.",
            "ListItem.Thumb": "The thumbnail (if it exists) of the currently selected item in a list or thumb control. Deprecated:but still available, returns the same as ListItem.Art(thumb)",
            "ListItem.TimerHasConflict": "True if the item has a timer and it won't be recorded because of a conflict (PVR). v17 Skinning engine changes:[New Boolean Condition] ListItem.TimerHasConflict",
            "ListItem.TimerHasError": "True if the item has a timer and it won't be recorded because of an error (PVR). v17 Skinning engine changes:[New Boolean Condition] ListItem.TimerHasError",
            "ListItem.TimerIsActive": "True if the item has a timer that will be recorded, i.e. the timer is enabled (PVR). v17 Skinning engine changes:[New Boolean Condition] ListItem.TimerIsActive",
            "ListItem.TimerType": "The type of the PVR timer / timer rule item as a human readable string.",
            "ListItem.Title": "The title of the currently selected song, movie, game in a container. v18 Skinning engine changes:[Infolabel Updated] ListItem.Title extended to support games",
            "ListItem.Top250": "The IMDb top250 position of the currently selected listitem in a container.",
            "ListItem.TrackNumber": "The track number of the currently selected song in a container.",
            "ListItem.Trailer": "The full trailer path with filename of the currently selected movie in a container.",
            "ListItem.TVShowTitle": "The name value for the currently selected tvshow in the season and episode depth of the video library.",
            "ListItem.UserRating": "The user rating of the currently selected item in a container (1-10). v17 Skinning engine changes:[Infolabel Updated] ListItem.UserRating now available for albums/songs. v16 Skinning engine changes:[New Infolabel] ListItem.UserRating",
            "ListItem.VideoAspect": "The aspect ratio of the currently selected video. Possible values: 1.33 1.37 1.66 1.78 1.85 2.20 2.35 2.40 2.55 2.76",
            "ListItem.VideoCodec": "The video codec of the currently selected video. Common values: 3iv2 av1 avc1 div2 div3 divx divx4 dx50 flv h264 microsoft mp42 mp43 mp4v mpeg1video mpeg2video mpg4 rv40 svq1 svq3 theora vp6f wmv2 wmv3 wvc1 xvid etc",
            "ListItem.VideoResolution": "The resolution of the currently selected video. Possible values: 480 576 540 720 1080 4K 8K Note540 usually means a widescreen format (around 960x540) while 576 means PAL resolutions (normally 720x576), therefore 540 is actually better resolution than 576. v18 Skinning engine changes:[Updated Infolabel] ListItem.VideoResolution added 8K as a possible value.",
            "ListItem.Votes([name])": "The scraped votes of the currently selected movie in a container. Parameters name- [opt] you can specify the name of the scraper to retrieve specific votes, for use in dialogvideoinfo.xml. v17 Skinning engine changes:[Infolabel Updated] ListItem.Votes([name]) add optional param name to specify the scrapper. v13 Skinning engine changes:[New Infolabel] ListItem.Votes",
            "ListItem.Writer": "The name of Writer of current Video in a container. v15 Skinning engine changes:[Infolabel Updated] ListItem.Writer also supports EPG.",
            "ListItem.Year": "The year of the currently selected song, album, movie, game in a container. v18 Skinning engine changes:[Infolabel Updated] ListItem.Title extended to support games",
            "MusicPartyMode.Enabled": "True if Party Mode is enabled.",
            "MusicPartyMode.MatchingSongs": "The number of songs available to Party Mode.",
            "MusicPartyMode.MatchingSongsLeft": "The number of songs left to be picked from for Party Mode.",
            "MusicPartyMode.MatchingSongsPicked": "The number of songs picked already for Party Mode.",
            "MusicPartyMode.RandomSongsPicked": "The number of unique random songs picked during Party Mode.",
            "MusicPartyMode.RelaxedSongsPicked": "Todo:Not currently used",
            "MusicPartyMode.SongsPlayed": "The number of songs played during Party Mode.",
            "MusicPlayer.Album": "The album from which the current song is from.",
            "MusicPlayer.AlbumArtist": "The album artist of the currently playing song.",
            "MusicPlayer.Artist": "Artist(s) of current song.",
            "MusicPlayer.BitRate": "The bitrate of current song.",
            "MusicPlayer.BitsPerSample": "The number of bits per sample of current song.",
            "MusicPlayer.BPM": "The bpm of the track currently playing. v19 Skinning engine changes:[New Infolabel] MusicPlayer.BPM",
            "MusicPlayer.ChannelGroup": "The channel group of the radio programme that's currently playing (PVR).",
            "MusicPlayer.ChannelName": "The channel name of the radio programme that's currently playing (PVR).",
            "MusicPlayer.ChannelNumberLabel": "The channel and subchannel number of the radio channel that's currently playing (PVR). v14 Skinning engine changes:[New Infolabel] MusicPlayer.ChannelNumberLabel",
            "MusicPlayer.Channels": "The number of channels of current song.",
            "MusicPlayer.Codec": "The codec of current playing song.",
            "MusicPlayer.Comment": "The Comment of current song stored in ID tag info.",
            "MusicPlayer.ContributorAndRole": "The list of all people and their role who've contributed to the currently playing song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.ContributorAndRole",
            "MusicPlayer.Contributors": "The list of all people who've contributed to the currently playing song v17 Skinning engine changes:[New Infolabel] MusicPlayer.Contributors",
            "MusicPlayer.Cover": "The album cover of currently playing song.",
            "MusicPlayer.DBID": "The database id of the currently playing song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.DBID",
            "MusicPlayer.DiscNumber": "The Disc Number of current song stored in ID tag info.",
            "MusicPlayer.DiscTitle": "The title of the disc currently playing. v19 Skinning engine changes:[New Infolabel] MusicPlayer.DiscTitle",
            "MusicPlayer.Duration": "The duration of the current song.",
            "MusicPlayer.Exists(relative,position)": "True if the currently playing playlist has a song queued at the given position. Parameters relative- bool - If the position is relative position- int - The position of the song NoteIt is possible to define whether the position is relative or not, default is false.",
            "MusicPlayer.Genre": "The genre(s) of current song.",
            "MusicPlayer.HasNext": "True if the music player has a next song queued in the Playlist.",
            "MusicPlayer.HasPrevious": "True if the music player has a a Previous Song in the Playlist.",
            "MusicPlayer.IsMultiDisc": "true if the album currently playing has more than one disc. v19 Skinning engine changes:[New Infolabel] MusicPlayer.IsMultiDisc",
            "MusicPlayer.LastPlayed": "The last play date of currently playing song, if it's in the database.",
            "MusicPlayer.Lyrics": "The lyrics of current song stored in ID tag info.",
            "MusicPlayer.Mood": "The mood of the currently playing song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Mood",
            "MusicPlayer.offset(number).Album": "The album from which the song with offset number with respect to the current song is from. Parameters number- the offset number with respect to the current playing song",
            "MusicPlayer.offset(number).Artist": "Artist(s) of the song which has an offset number with respect to the current playing song. Parameters number- the offset of the song with respect to the current playing song",
            "MusicPlayer.offset(number).Comment": "The Comment of current song stored in ID tag info for the song with an offset number with respect to the playing song. Parameters number- The offset value for the song with respect to the playing song.",
            "MusicPlayer.offset(number).DiscNumber": "The Disc Number of current song stored in ID tag info for the song with an offset number with respect to the playing song. Parameters number- The offset value for the song with respect to the playing song.",
            "MusicPlayer.offset(number).Duration": "The duration of the song with an offset number with respect to the current playing song. Parameters number- the offset number of the song with respect to the current playing song",
            "MusicPlayer.Offset(number).Exists": "True if the music players playlist has a song queued in position (number). Parameters number- song position",
            "MusicPlayer.offset(number).Genre": "The genre(s) of the song with an offset number with respect to the current playing song. Parameters number- the offset song number with respect to the current playing song.",
            "MusicPlayer.offset(number).Rating": "The numeric Rating of song with an offset number with respect to the current playing song. Parameters number- the offset with respect to the current playing song",
            "MusicPlayer.offset(number).Title": "The title of the song which has an offset number with respect to the current playing song. Parameters number- the offset number with respect to the current playing song",
            "MusicPlayer.offset(number).TrackNumber": "The track number of the song with an offset number with respect to the current playing song. Parameters number- The offset number of the song with respect to the playing song",
            "MusicPlayer.offset(number).Year": "The year of release of the song with an offset number with respect to the current playing song. Parameters number- the offset numbet with respect to the current song.",
            "MusicPlayer.OriginalDate": "The original release date of the song currently playing. v19 Skinning engine changes:[New Infolabel] MusicPlayer.OriginalDate",
            "MusicPlayer.PlayCount": "The play count of currently playing song, if it's in the database.",
            "MusicPlayer.PlaylistLength": "The total size of the current music playlist.",
            "MusicPlayer.PlaylistPlaying": "True if a playlist is currently playing.",
            "MusicPlayer.PlaylistPosition": "The position of the current song in the current music playlist.",
            "MusicPlayer.Position(number).Album": "The album from which the song with offset number with respect to the start of the playlist is from. Parameters number- the offset number with respect to the start of the playlist",
            "MusicPlayer.Position(number).Artist": "Artist(s) of the song which has an offset number with respect to the start of the playlist. Parameters number- the offset of the song with respect to the start of the playlist",
            "MusicPlayer.Position(number).Comment": "The Comment of current song stored in ID tag info for the song with an offset number with respect to the start of the playlist. Parameters number- The offset value for the song with respect to the start of the playlist.",
            "MusicPlayer.Position(number).DiscNumber": "The Disc Number of current song stored in ID tag info for the song with an offset number with respect to the start of the playlist. Parameters number- The offset value for the song with respect to the start of the playlist.",
            "MusicPlayer.Position(number).Duration": "The duration of the song with an offset number with respect to the start of the playlist. Parameters number- the offset number of the song with respect to the start of the playlist",
            "MusicPlayer.Position(number).Genre": "The genre(s) of the song with an offset number with respect to the start of the playlist. Parameters number- the offset song number with respect to the start of the playlist song.",
            "MusicPlayer.Position(number).Rating": "The numeric Rating of song with an offset number with respect to the start of the playlist. Parameters number- the offset with respect to the start of the playlist",
            "MusicPlayer.Position(number).Title": "The title of the song which as an offset number with respect to the start of the playlist. Parameters number- the offset number with respect to the start of the playlist",
            "MusicPlayer.Position(number).TrackNumber": "The track number of the song with an offset number with respect to start of the playlist. Parameters number- The offset number of the song with respect to start of the playlist",
            "MusicPlayer.Position(number).Year": "The year of release of the song with an offset number with respect to the start of the playlist. Parameters number- the offset numbet with respect to the start of the playlist.",
            "MusicPlayer.Property(Album_Description)": "A review of the currently playing album",
            "MusicPlayer.Property(Album_Label)": "The record label of the currently playing album.",
            "MusicPlayer.Property(Album_Mood)": "The moods of the currently playing Album",
            "MusicPlayer.Property(Album_Mood)": "The moods of the currently playing Album",
            "MusicPlayer.Property(Album_Style)": "The styles of the currently playing Album.",
            "MusicPlayer.Property(Album_Theme)": "The themes of the currently playing Album",
            "MusicPlayer.Property(Album_Type)": "The album type (e.g. compilation, enhanced, explicit lyrics) of the currently playing album.",
            "MusicPlayer.Property(Artist_Born)": "The date of Birth of the currently playing Artist.",
            "MusicPlayer.Property(Artist_Description)": "A biography of the currently playing artist.",
            "MusicPlayer.Property(Artist_Died)": "The date of Death of the currently playing Artist.",
            "MusicPlayer.Property(Artist_Disambiguation)": "A brief description of the currently playing Artist that differentiates them from others with the same name. v18 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Artist_Disambiguation)",
            "MusicPlayer.Property(Artist_Disbanded)": "The disbanding date of the currently playing Artist/Band.",
            "MusicPlayer.Property(Artist_Formed)": "The Formation date of the currently playing Artist/Band.",
            "MusicPlayer.Property(Artist_Gender)": "The gender of the currently playing Artist - male, female, other. v18 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Artist_Gender)",
            "MusicPlayer.Property(Artist_Genre)": "The genre of the currently playing artist.",
            "MusicPlayer.Property(Artist_Instrument)": "The instruments played by the currently playing artist.",
            "MusicPlayer.Property(Artist_Mood)": "The moods of the currently playing artist.",
            "MusicPlayer.Property(Artist_Sortname)": "The sortname of the currently playing Artist. v18 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Artist_Sortname)",
            "MusicPlayer.Property(Artist_Style)": "The styles of the currently playing artist.",
            "MusicPlayer.Property(Artist_Type)": "The type of the currently playing Artist - person, group, orchestra, choir etc. v18 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Artist_Type)",
            "MusicPlayer.Property(Artist_YearsActive)": "The years the currently Playing artist has been active.",
            "MusicPlayer.Property(propname)": "The requested property value of the currently playing item. Parameters propname- The requested property",
            "MusicPlayer.Property(Role.Arranger)": "The name of the person who arranged the selected song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Role.Arranger)",
            "MusicPlayer.Property(Role.Composer)": "The name of the person who composed the selected song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Role.Composer)",
            "MusicPlayer.Property(Role.Conductor)": "The name of the person who conducted the selected song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Role.Conductor)",
            "MusicPlayer.Property(Role.DJMixer)": "The name of the dj who remixed the selected song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Role.DJMixer)",
            "MusicPlayer.Property(Role.Engineer)": "The name of the person who was the engineer of the selected song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Role.Engineer)",
            "MusicPlayer.Property(Role.Lyricist)": "The name of the person who wrote the lyrics of the selected song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Role.Lyricist)",
            "MusicPlayer.Property(Role.Mixer)": "The name of the dj who remixed the selected song. Todo:So maybe rather than a row each have one entry for Role.XXXXX with composer, arranger etc. as listed values NoteMusicPlayer.Property(Role.any_custom_role) also works, where any_custom_role could be an instrument violin or some other production activity e.g. sound engineer. The roles listed (composer, arranger etc.) are standard ones but there are many possible. Music file tagging allows for the musicians and all other people involved in the recording to be added, Kodi will gathers and stores that data, and it is availlable to GUI. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Role.Mixer)",
            "MusicPlayer.Property(Role.Orchestra)": "The name of the orchestra performing the selected song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Role.Orchestra)",
            "MusicPlayer.Property(Role.Producer)": "The name of the person who produced the selected song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Role.Producer)",
            "MusicPlayer.Property(Role.Remixer)": "The name of the person who remixed the selected song. v17 Skinning engine changes:[New Infolabel] MusicPlayer.Property(Role.Remixer)",
            "MusicPlayer.Rating": "The numeric Rating of current song (1-10).",
            "MusicPlayer.RatingAndVotes": "The scraped rating and votes of currently playing song, if it's in the database.",
            "MusicPlayer.ReleaseDate": "The release date of the song currently playing. v19 Skinning engine changes:[New Infolabel] MusicPlayer.ReleaseDate",
            "MusicPlayer.SampleRate": "The samplerate of current playing song.",
            "MusicPlayer.Station": "The name of the radio station currently playing (if available). v19 Skinning engine changes:[New Infolabel] MusicPlayer.Station",
            "MusicPlayer.Title": "The title of the currently playing song.",
            "MusicPlayer.TotalDiscs": "The number of discs associated with the currently playing album. v19 Skinning engine changes:[New Infolabel] MusicPlayer.TotalDiscs",
            "MusicPlayer.TrackNumber": "The track number of current song.",
            "MusicPlayer.UserRating": "The scraped rating of the currently playing song (1-10). v17 Skinning engine changes:[New Infolabel] MusicPlayer.UserRating",
            "MusicPlayer.Votes": "The scraped votes of currently playing song, if it's in the database.",
            "MusicPlayer.Year": "The year of release of current song.",
            "Network.DHCPAddress": "The DHCP IP address.",
            "Network.DNS1Address": "The network DNS 1 address.",
            "Network.DNS2Address": "The network DNS 2 address.",
            "Network.GatewayAddress": "The network gateway address.",
            "Network.IPAddress": "The system's IP Address. e.g. 192.168.1.15",
            "Network.IsDHCP": "True if the network type is DHCP. NoteNetwork type can be either DHCP or FIXED",
            "Network.LinkState": "The network linkstate e.g. 10mbit/100mbit etc.",
            "Network.MacAddress": "The system's MAC address.",
            "Network.SubnetMask": "The network subnet mask.",
            "Player.Art(type)": "The Image for the defined art type for the current playing ListItem. Parameters type- The art type. The type is defined by scripts and scrappers and can have any value. Common example values for type are: fanart thumb poster banner clearlogo tvshow.poster tvshow.banner etc Todo:get a way of centralize all random art strings used in core so we can point users to them while still making it clear they can have any value.",
            "Player.AudioDelay": "The used audio delay with the format %2.3f s",
            "Player.CacheLevel": "The used cache level as a string with an integer number.",
            "Player.Caching": "True if the player is current re-caching data (internet based video playback).",
            "Player.ChannelPreviewActive": "True if PVR channel preview is active (used channel tag different from played tag)",
            "Player.Chapter": "The current chapter of current playing media.",
            "Player.ChapterCount": "The total number of chapters of current playing media.",
            "Player.ChapterName": "The name of currently used chapter if available.",
            "Player.Chapters": "The chapters of the currently playing item as csv in the format start1,end1,start2,end2,... Tokens must have values in the range from 0.0 to 100.0. end token must be less or equal than start token. v19 Skinning engine changes:[New Infolabel] Player.Chapters",
            "Player.Cutlist": "The cutlist of the currently playing item as csv in the format start1,end1,start2,end2,... Tokens must have values in the range from 0.0 to 100.0. end token must be less or equal than start token. v19 Skinning engine changes:[New Infolabel] Player.Cutlist",
            "Player.DisplayAfterSeek": "True for the first 2.5 seconds after a seek.",
            "Player.Duration([format])": "The total duration of the current playing media in a given format. Parameters format[opt] The format of the return time value. See TIME_FORMAT for the list of possible values.",
            "Player.Filename": "The filename of the currently playing media. v13 Skinning engine changes:[New Infolabel] Player.Filename",
            "Player.FilenameAndPath": "The full path with filename of the currently playing song or movie",
            "Player.FinishTime([format])": "The time at which the playing media will end (in a specified format). Parameters format[opt] The format of the return time value. See TIME_FORMAT for the list of possible values.",
            "Player.Folderpath": "The full path of the currently playing song or movie",
            "Player.Forwarding": "True if the player is fast forwarding.",
            "Player.Forwarding16x": "True if the player is fast forwarding at 16x.",
            "Player.Forwarding2x": "True if the player is fast forwarding at 2x.",
            "Player.Forwarding32x": "True if the player is fast forwarding at 32x.",
            "Player.Forwarding4x": "True if the player is fast forwarding at 4x.",
            "Player.Forwarding8x": "True if the player is fast forwarding at 8x.",
            "Player.FrameAdvance": "True if player is in frame advance mode. NoteSkins should hide seek bar in this mode v18 Skinning engine changes:[New Boolean Condition] Player.FrameAdvance",
            "Player.HasAudio": "True if the player has an audio file.",
            "Player.HasDuration": "True if Media is not a true stream.",
            "Player.HasGame": "True if the player has a game file (RETROPLAYER). v18 Skinning engine changes:[New Boolean Condition] Player.HasGame",
            "Player.HasMedia": "True if the player has an audio or video file.",
            "Player.HasPrograms": "True if the media file being played has programs, i.e. groups of streams. NoteEx: if a media file has multiple streams (quality, channels, etc) a program represents a particular stream combo.",
            "Player.HasResolutions": "True if the player is allowed to switch resolution and refresh rate (i.e. if whitelist modes are configured in Kodi's System/Display settings) v18 Skinning engine changes:[New Boolean Condition] Player.HasResolutions",
            "Player.HasVideo": "True if the player has a video file.",
            "Player.Icon": "The thumbnail of the currently playing item. If no thumbnail image exists, the icon will be returned, if available. v18 Skinning engine changes:[New Infolabel] Player.Icon",
            "Player.IsInternetStream": "True if the player is playing an internet stream.",
            "Player.IsTempo": "True if player has tempo (i.e. is playing with a playback speed higher or lower than normal playback speed) v17 Skinning engine changes:[New Boolean Condition] Player.IsTempo",
            "Player.Muted": "True if the volume is muted.",
            "Player.offset(number).Filename": "The filename of audio or video file which has an offset number with respect to the currently playing item. v19 Skinning engine changes:[New Infolabel] Player.offset(number).Filename",
            "Player.offset(number).FilenameAndPath": "The full path with filename of audio or video file which has an offset number with respect to the currently playing item. v19 Skinning engine changes:[New Infolabel] Player.offset(number).FilenameAndPath",
            "Player.offset(number).Folderpath": "The full path of the audio or video file which has an offset number with respect to the currently playing item. v19 Skinning engine changes:[New Infolabel] Player.offset(number).Folderpath",
            "Player.offset(number).Title": "The title of audio or video which has an offset number with respect to the currently playing item. v19 Skinning engine changes:[New Infolabel] Player.offset(number).Title",
            "Player.Passthrough": "True if the player is using audio passthrough.",
            "Player.Paused": "True if the player is paused.",
            "Player.PauseEnabled": "True if played stream is paused.",
            "Player.Playing": "True if the player is currently playing (i.e. not ffwding, rewinding or paused.)",
            "Player.PlaySpeed": "The player playback speed with the format %1.2f (1.00 means normal playback speed). NoteFor Tempo, the default range is 0.80 - 1.50 (it can be changed in advanced settings). If Player.PlaySpeed returns a value different from 1.00 and Player.IsTempo is false it means the player is in ff/rw mode.",
            "Player.position(number).Filename": "The filename of the audio or video file which has an offset number with respect to the start of the playlist. > v19 Skinning engine changes:[New Infolabel] Player.position(number).Filename",
            "Player.position(number).FilenameAndPath": "The full path with filename of the audio or video file which has an offset number with respect to the start of the playlist. > v19 Skinning engine changes:[New Infolabel] Player.position(number).FilenameAndPath",
            "Player.position(number).Folderpath": "The full path of the audio or video file which has an offset number with respect to the start of the playlist. > v19 Skinning engine changes:[New Infolabel] Player.position(number).Folderpath",
            "Player.position(number).Title": "The title of the audio or video which has an offset number with respect to the start of the playlist. > v19 Skinning engine changes:[New Infolabel] Player.position(number).Title",
            "Player.Process(audiobitspersample)": "The bits per sample of the currently playing item. v17 Skinning engine changes:[New Infolabel] Player.Process(audiobitspersample)",
            "Player.Process(audiochannels)": "The audiodecoder name of the currently playing item. v17 Skinning engine changes:[New Infolabel] Player.Process(audiochannels)",
            "Player.Process(audiodecoder)": "The audiodecoder name of the currently playing item. v17 Skinning engine changes:[New Infolabel] Player.Process(audiodecoder)",
            "Player.Process(audiosamplerate)": "The samplerate of the currently playing item. v17 Skinning engine changes:[New Infolabel] Player.Process(audiosamplerate)",
            "Player.Process(deintmethod)": "The deinterlace method of the currently playing video. v17 Skinning engine changes:[New Infolabel] Player.Process(deintmethod)",
            "Player.Process(pixformat)": "The pixel format of the currently playing video. v17 Skinning engine changes:[New Infolabel] Player.Process(pixformat)",
            "Player.Process(videodar)": "The display aspect ratio of the currently playing video. v17 Skinning engine changes:[New Infolabel] Player.Process(videodar)",
            "Player.Process(videodecoder)": "The videodecoder name of the currently playing video. v17 Skinning engine changes:[New Infolabel] Player.Process(videodecoder)",
            "Player.Process(videofps)": "The video framerate of the currently playing video. v17 Skinning engine changes:[New Infolabel] Player.Process(videofps)",
            "Player.Process(videoheight)": "The width of the currently playing video. v17 Skinning engine changes:[New Infolabel] Player.Process(videoheight)",
            "Player.Process(videohwdecoder)": "True if the currently playing video is decoded in hardware. v17 Skinning engine changes:[New Boolean Condition] Player.Process(videohwdecoder)",
            "Player.Process(videowidth)": "The width of the currently playing video. v17 Skinning engine changes:[New Infolabel] Player.Process(videowidth)",
            "Player.Progress": "The progress position as percentage. v19 Skinning engine changes:Player.Progress infolabel also exposed as a string.",
            "Player.ProgressCache": "How much of the file is cached above current play percentage v19 Skinning engine changes:Player.ProgressCache infolabel also exposed as a string.",
            "Player.Rewinding": "True if the player is rewinding.",
            "Player.Rewinding16x": "True if the player is rewinding at 16x.",
            "Player.Rewinding2x": "True if the player is rewinding at 2x.",
            "Player.Rewinding32x": "True if the player is rewinding at 32x.",
            "Player.Rewinding4x": "True if the player is rewinding at 4x.",
            "Player.Rewinding8x": "True if the player is rewinding at 8x.",
            "Player.Seekbar": "The percentage of one seek to other position.",
            "Player.SeekEnabled": "True if seek on playing is enabled.",
            "Player.Seeking": "True if a seek is in progress.",
            "Player.SeekNumeric([format])": "The time at which the playing media began (in a specified format). Parameters format[opt] The format of the return time value. See TIME_FORMAT for the list of possible values.",
            "Player.SeekOffset([format])": "The seek offset after a seek press in a given format. Parameters format[opt] The format of the return time value. See TIME_FORMAT for the list of possible values. NoteExample: user presses BigStepForward, player.seekoffset returns +10:00",
            "Player.SeekStepSize": "The seek step size. v15 Skinning engine changes:[New Infolabel] Player.SeekStepSize",
            "Player.SeekTime": "The time to which the user is seeking.",
            "Player.ShowInfo": "True if the user has requested the song info to show (occurs in visualisation fullscreen and slideshow).",
            "Player.ShowTime": "True if the user has requested the time to show (occurs in video fullscreen).",

            "System.Time": "Current time",
            "System.Time(hh:mm:ss)": "Shows hours (hh), minutes (mm) or seconds (ss). When 12 hour clock is used (xx) will return AM/PM. Also supported: (hh:mm), (mm:ss), (hh:mm:ss), (hh:mm:ss). (xx) option added after dharma",
            "System.Date": "Current date",
            'System.Date(mm dd yyyy)': "Show current date using format, available markings: d (day of month 1-31), dd (day of month 01-31), ddd (short day of the week Mon-Sun), DDD (long day of the week Monday-Sunday), m (month 1-12), mm (month 01-12), mmm (short month name Jan-Dec), MMM (long month name January-December), yy (2-digit year), yyyy (4-digit year). Added after dharma.",
            "System.AlarmPos": "Shutdown Timer position",
            "System.BatteryLevel": "the remaining battery level in range 0-100",
            "System.FreeSpace": "Total Freespace on the drive",
            "System.UsedSpace": "Total Usedspace on the drive",
            "System.TotalSpace": "Totalspace on the drive",
            "System.UsedSpacePercent": "Total Usedspace Percent on the drive",
            "System.FreeSpacePercent": "Total Freespace Percent on the drive",
            "System.CPUTemperature": "Current CPU temperature",
            "System.CpuUsage": "Displays the cpu usage for each individual cpu core.",
            "System.CoreUsage(0)": "Displays the usage of the cpu core with the given 'id'",
            "System.CoreUsage(1)": "Displays the usage of the cpu core with the given 'id'",
            "System.CoreUsage(2)": "Displays the usage of the cpu core with the given 'id'",
            "System.CoreUsage(3)": "Displays the usage of the cpu core with the given 'id'",
            "System.CoreUsage(4)": "Displays the usage of the cpu core with the given 'id'",
            "System.CoreUsage(5)": "Displays the usage of the cpu core with the given 'id'",
            "System.CoreUsage(6)": "Displays the usage of the cpu core with the given 'id'",     
            "System.CoreUsage(7)": "Displays the usage of the cpu core with the given 'id'",    
            "System.CoreUsage(8)": "Displays the usage of the cpu core with the given 'id'",    
            "System.GPUTemperature": "Current GPU temperature",
            "System.FanSpeed": "Current fan speed",
            "System.BuildVersion": "Version of build",
            "System.BuildDate": "Date of build",
            "System.FriendlyName": "the Kodi instance name. It will auto append (%hostname%) in case the device name was not changed. eg. 'Kodi (htpc)'",
            "System.FPS": "Current rendering speed (frames per second)",
            "System.FreeMemory": "Amount of free memory in Mb",
            "System.Memory(used)": "Available formats: used, used.percent, free, free.percent, total",
            "System.Memory(used.percent)": "Available formats: used, used.percent, free, free.percent, total",
            "System.Memory(free)": "Available formats: used, used.percent, free, free.percent, total",    
            "System.Memory(free.percent)": "Available formats: used, used.percent, free, free.percent, total",    
            "System.Memory(total)": "Available formats: used, used.percent, free, free.percent, total",    
            "System.ScreenMode": "Screenmode (eg windowed / fullscreen)",
            "System.ScreenWidth": "Width of screen in pixels",
            "System.ScreenHeight": "Height of screen in pixels",
            "System.StartupWindow": "The Window Kodi will load on startup",
            "System.CurrentWindow": "Current Window we are in",
            "System.CurrentControl": "Current focused control",
            "System.CurrentControlID": "ID of the currently focused control.",
            "System.DVDLabel": "Label of the disk in the DVD-ROM drive",
            "System.HddTemperature": "Hdd temperature",
            "System.OSVersionInfo": "System name + kernel version",
            "System.KernelVersion": "(deprecated)     System name + kernel version",
            "System.Uptime": "System current uptime",
            "System.TotalUptime": "System total uptime",
            "System.CpuFrequency": "System cpu frequency",
            "System.ScreenResolution": "Screen resolution",
            "System.VideoEncoderInfo": "Video encoder info",
            "System.InternetState": "Will return the internet state, 'connected' or 'not connected' (localized)",
            "System.Language": "Shows the current language",
            "System.ProfileName": "Shows the User name of the currently logged in Kodi user",
            "System.ProfileCount": "Shows the number of defined profiles",
            "System.ProfileAutoLogin": "The profile Kodi will auto login to",
            "System.Progressbar": "The percentage of the currently active progress.",
            "System.StereoscopicMode": "The prefered stereoscopic mode (settings > video > playback)",
            "System.TemperatureUnits": "Shows Celsius or Fahrenheit symbol",
            "System.BuildVersionCode": "The internal version of the kodi build",
            "System.BuildVersionGit": "The git version (sha) of the kodi build",
            "System.AddonUpdateCount": "The number of available addon updates",        
        
        }
    



    
    def gather_data(self):
        if xbmc.getCondVisibility("Window.IsActive(busydialog)"):
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            xbmc.sleep(800)
    #        xbmc.executebuiltin("Container.Refresh") 
    
    #    win = xbmcgui.Window(10000)
        windowID = xbmcgui.getCurrentWindowId()
        currwin = xbmcgui.Window(windowID)
        container = xbmc.getInfoLabel('System.CurrentControlID')
        
        build_version = xbmc.getInfoLabel('System.BuildVersion')
        
        build_version = re.sub(r"\..*$", "", build_version)
            
            
        
        
        divider = '<hr>'
        divider_txt = '-------------------------' + "\n";
    
        content = '<html><head><title>DevView</title></head><body>'
        content_txt = 'DevView' + "\n";
    
        content = content + '<h1>windowID : ' + str(windowID) + ' / ' + 'Container : ' + str(container) + '</h1>' + "\n"
        
        content_txt = content_txt + 'windowID: ' + str(windowID) + ' / ' + 'Container : ' + str(container) + "\n"

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

        if dbtype != 'song':

    
            content = content + divider + '<table border=1><tr><td colspan=2><h1>sys.listitem.getVideoInfoTag() :</h1></td></tr>'  + "\n"
            
            content_txt = content_txt + divider_txt + 'sys.listitem.getVideoInfoTag() :' + "\n"

        
            videoInfoTag = sys.listitem.getVideoInfoTag()
        
            if build_version == '20':
                z = videoInfoTag.getActors()
                content = content + "<tr><td>(V20+)getActors()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getActors() :' + str(z) + "\n"
            
            z = videoInfoTag.getAlbum()
            content = content + "<tr><td>getAlbum()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getAlbum() :' + str(z) + "\n"
            z = videoInfoTag.getArtist()
            content = content + "<tr><td>getArtist()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getArtist() :' + str(z) + "\n"
            z = videoInfoTag.getCast()
            content = content + "<tr><td>getCast()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getCast() :' + str(z) + "\n"
            z = videoInfoTag.getDbId()
            content = content + "<tr><td>getDbId()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getDbId() :' + str(z) + "\n"
            z = videoInfoTag.getDirector()
            content = content + "<tr><td>getDirector()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getDirector() :' + str(z) + "\n"
            
            if build_version == '20':
                z = videoInfoTag.getDirectors()
                content = content + "<tr><td>(V20+)getDirectors()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getDirectors() :' + str(z) + "\n"
                
            z = videoInfoTag.getDuration()
            content = content + "<tr><td>getDuration()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getDuration() :' + str(z) + "\n"
            z = videoInfoTag.getEpisode()
            content = content + "<tr><td>getEpisode()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getEpisode() :' + str(z) + "\n"
            z = videoInfoTag.getFile()
            content = content + "<tr><td>getFile()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getFile() :' + str(z) + "\n"
            
            if build_version == '20':
                z = videoInfoTag.getFilenameAndPath()
                content = content + "<tr><td>(V20+)getFilenameAndPath()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getFilenameAndPath() :' + str(z) + "\n"

            z = videoInfoTag.getFirstAired()
            content = content + "<tr><td>getFirstAired()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getFirstAired() :' + str(z) + "\n"
            
            if build_version == '20':
                z = videoInfoTag.getFirstAiredAsW3C()
                content = content + "<tr><td>(V20+)getFirstAiredAsW3C()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getFirstAiredAsW3C() :' + str(z) + "\n"
                
            z = videoInfoTag.getGenre()
            content = content + "<tr><td>getGenre()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getGenre() :' + str(z) + "\n"
            
            if build_version == '20':
                z = videoInfoTag.getGenres()
                content = content + "<tr><td>(V20+)getGenres()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getGenres() :' + str(z) + "\n"
                
            z = videoInfoTag.getIMDBNumber()
            content = content + "<tr><td>getIMDBNumber()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getIMDBNumber() :' + str(z) + "\n"
            z = videoInfoTag.getLastPlayed()
            content = content + "<tr><td>getLastPlayed()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getLastPlayed() :' + str(z) + "\n"
            
            if build_version == '20':
                z = videoInfoTag.getLastPlayedAsW3C()
                content = content + "<tr><td>(V20+)getLastPlayedAsW3C()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getLastPlayedAsW3C() :' + str(z) + "\n"

            z = videoInfoTag.getMediaType()
            content = content + "<tr><td>getMediaType()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getMediaType() :' + str(z) + "\n"
            z = videoInfoTag.getOriginalTitle()
            content = content + "<tr><td>getOriginalTitle()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getOriginalTitle() :' + str(z) + "\n"
            z = videoInfoTag.getPath()
            content = content + "<tr><td>getPath()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getPath() :' + str(z) + "\n"
            z = videoInfoTag.getPictureURL()
            content = content + "<tr><td>getPictureURL()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getPictureURL() :' + str(z) + "\n"
            z = videoInfoTag.getPlayCount()
            content = content + "<tr><td>getPlayCount()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getPlayCount() :' + str(z) + "\n"
            z = videoInfoTag.getPlot()
            content = content + "<tr><td>getPlot()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getPlot() :' + str(z) + "\n"
            z = videoInfoTag.getPlotOutline()
            content = content + "<tr><td>getPlotOutline()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getPlotOutline() :' + str(z) + "\n"
            z = videoInfoTag.getPremiered()
            content = content + "<tr><td>getPremiered()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getPremiered() :' + str(z) + "\n"
            
            if build_version == '20':
                z = videoInfoTag.getPremieredAsW3C()
                content = content + "<tr><td>(V20+)getPremieredAsW3C()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getPremieredAsW3C() :' + str(z) + "\n"
            
            z = videoInfoTag.getRating('imdb')
            content = content + "<tr><td>getRating()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + "getRating() :" + str(z) + "\n"

            if build_version == '20':
                z = videoInfoTag.getRating('imdb')
                content = content + "<tr><td>(V20+)getRating('imdb')</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + "(V20+)getRating(imdb') :" + str(z) + "\n"
                z = videoInfoTag.getRating('tvdb')
                content = content + "<tr><td>(V20+)getRating('tvdb')</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + "(V20+)getRating('tvdb') :" + str(z) + "\n"
                z = videoInfoTag.getRating('tmdb')
                content = content + "<tr><td>(V20+)getRating('tmdb')</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + "(V20+)getRating('tmdb') :" + str(z) + "\n"
                z = videoInfoTag.getRating('anidb')
                content = content + "<tr><td>(V20+)getRating('anidb')</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + "(V20+)getRating('anidb') :" + str(z) + "\n"
                z = videoInfoTag.getResumeTime()
                content = content + "<tr><td>(V20+)getResumeTime()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getResumeTime() :' + str(z) + "\n"

            
            
            
            z = videoInfoTag.getSeason()
            content = content + "<tr><td>getSeason()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getSeason() :' + str(z) + "\n"
            z = videoInfoTag.getTagLine()
            content = content + "<tr><td>getTagLine()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getTagLine() :' + str(z) + "\n"
            z = videoInfoTag.getTitle()
            content = content + "<tr><td>getTitle()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getTitle() :' + str(z) + "\n"
            z = videoInfoTag.getTrack()
            content = content + "<tr><td>getTrack()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getTrack() :' + str(z) + "\n"

            if build_version == '20':
                z = videoInfoTag.getTrailer()
                content = content + "<tr><td>(V20+)getTrailer()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getTrailer() :' + str(z) + "\n"
                
            z = videoInfoTag.getTVShowTitle()
            content = content + "<tr><td>getTVShowTitle()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getTVShowTitle() :' + str(z) + "\n"

            if build_version == '20':
                z = videoInfoTag.getUniqueID('imdb')
                content = content + "<tr><td>(V20+)getUniqueID('imdb')</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + "(V20+)getUniqueID('imdb') :" + str(z) + "\n"
                z = videoInfoTag.getUniqueID('tvdb')
                content = content + "<tr><td>(V20+)getUniqueID('tvdb')</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + "(V20+)getUniqueID('tvdb') :" + str(z) + "\n"
                z = videoInfoTag.getUniqueID('tmdb')
                content = content + "<tr><td>(V20+)getUniqueID('tmdb')</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + "(V20+)getUniqueID('tmdb') :" + str(z) + "\n"
                z = videoInfoTag.getUniqueID('anidb')
                content = content + "<tr><td>(V20+)getUniqueID('anidb')</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + "(V20+)getUniqueID('anidb') :" + str(z) + "\n"

            z = videoInfoTag.getUserRating()
            content = content + "<tr><td>getUserRating()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getUserRating() :' + str(z) + "\n"
            z = videoInfoTag.getVotes()
            content = content + "<tr><td>getVotes()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getVotes() :' + str(z) + "\n"

            if build_version == '20':
                z = videoInfoTag.getVotesAsInt()
                content = content + "<tr><td>(V20+)getVotesAsInt()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getVotesAsInt() :' + str(z) + "\n"
                z = videoInfoTag.getWriters()
                content = content + "<tr><td>(V20+)getWriters()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getWriters() :' + str(z) + "\n"

            z = videoInfoTag.getWritingCredits()
            content = content + "<tr><td>getWritingCredits()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getWritingCredits() :' + str(z) + "\n"
            z = videoInfoTag.getYear()
            content = content + "<tr><td>getYear()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getYear() :' + str(z) + "\n"
    
        
            content = content + '</table>'
            content_txt = content_txt + divider_txt

        else:
#############################################################################

            content = content + divider + '<table border=1><tr><td colspan=2><h1>sys.listitem.InfoTagMusic() :</h1></td></tr>'  + "\n"
            content_txt = content_txt + divider_txt + 'sys.listitem.InfoTagMusic() :' + "\n"
    
            musicinfo = xbmc.InfoTagMusic()
    
            z = musicinfo.getAlbum()
            content = content + "<tr><td>getAlbum()</td><td>" + str(z) + '</td></tr>' + "\n" 
            content_txt = content_txt + 'getAlbum() :' + str(z) + "\n"
            z = musicinfo.getAlbumArtist()
            content = content + "<tr><td>getAlbumArtist()</td><td>" + str(z) + '</td></tr>' + "\n" 
            content_txt = content_txt + 'getAlbumArtist() :' + str(z) + "\n"
            z = musicinfo.getArtist()
            content = content + "<tr><td>getArtist()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getArtist() :' + str(z) + "\n"
            z = musicinfo.getComment()
            content = content + "<tr><td>getComment()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getComment() :' + str(z) + "\n"
            z = musicinfo.getDbId()
            content = content + "<tr><td>getDbId()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getDbId() :' + str(z) + "\n"
            z = musicinfo.getDisc()
            content = content + "<tr><td>getDisc()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getDisc() :' + str(z) + "\n"
            z = musicinfo.getDuration()
            content = content + "<tr><td>getDuration()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getDuration() :' + str(z) + "\n"
            z = musicinfo.getGenre()
            content = content + "<tr><td>getGenre()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getGenre() :' + str(z) + "\n"
            z = musicinfo.getGenres()
            content = content + "<tr><td>getGenres()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getGenres() :' + str(z) + "\n"
            z = musicinfo.getLastPlayed()
            content = content + "<tr><td>getLastPlayed()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getLastPlayed() :' + str(z) + "\n"

            if build_version == '20':
                z = musicinfo.getLastPlayedAsW3C()
                content = content + "<tr><td>(V20+)getLastPlayedAsW3C()</td><td>" + str(z) + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR red](V20+)[/COLOR]getLastPlayedAsW3C() :' + str(z) + "\n"
            
            z = musicinfo.getListeners()
            content = content + "<tr><td>getListeners()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getListeners() :' + str(z) + "\n"
            z = musicinfo.getLyrics()
            content = content + "<tr><td>getLyrics()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getLyrics() :' + str(z) + "\n"
            z = musicinfo.getMediaType()
            content = content + "<tr><td>getMediaType()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getMediaType() :' + str(z) + "\n"
            z = musicinfo.getMusicBrainzAlbumArtistID()
            content = content + "<tr><td>getMusicBrainzAlbumArtistID()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getMusicBrainzAlbumArtistID() :' + str(z) + "\n"
            z = musicinfo.getMusicBrainzAlbumID()
            content = content + "<tr><td>getMusicBrainzAlbumID()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getMusicBrainzAlbumID() :' + str(z) + "\n"
            z = musicinfo.getMusicBrainzArtistID()
            content = content + "<tr><td>getMusicBrainzArtistID()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getMusicBrainzArtistID() :' + str(z) + "\n"
            z = musicinfo.getMusicBrainzReleaseGroupID()
            content = content + "<tr><td>getMusicBrainzReleaseGroupID()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getMusicBrainzReleaseGroupID() :' + str(z) + "\n"
            z = musicinfo.getMusicBrainzTrackID()
            content = content + "<tr><td>getMusicBrainzTrackID()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getMusicBrainzTrackID() :' + str(z) + "\n"
            z = musicinfo.getPlayCount()
            content = content + "<tr><td>getPlayCount()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getPlayCount() :' + str(z) + "\n"
            z = musicinfo.getRating()
            content = content + "<tr><td>getRating()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getRating() :' + str(z) + "\n"
            z = musicinfo.getReleaseDate()
            content = content + "<tr><td>getReleaseDate()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getReleaseDate() :' + str(z) + "\n"
            z = musicinfo.getTitle()
            content = content + "<tr><td>getTitle()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getTitle() :' + str(z) + "\n"
            z = musicinfo.getTrack()
            content = content + "<tr><td>getTrack()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getTrack() :' + str(z) + "\n"
            z = musicinfo.getURL()
            content = content + "<tr><td>getURL()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getURL() :' + str(z) + "\n"
            z = musicinfo.getUserRating()
            content = content + "<tr><td>getUserRating()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getUserRating() :' + str(z) + "\n"
            z = musicinfo.getYear()
            content = content + "<tr><td>getYear()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getYear() :' + str(z) + "\n"
    
            content = content + '</table>'
            content_txt = content_txt + divider_txt



    
        outlist = sorted(self.listitem_dict.items())
        
        content = content + divider + '<table border=1><tr><td colspan=3><h1>xbmc.getInfoLabel :</h1></td></tr>'  + "\n"
        content_txt = content_txt + divider_txt + 'xbmc.getInfoLabel :' + "\n"
        
        this_lookup = 'Container(id).Position'
        this_lookup = re.sub(r"Container\(id\)", "Container(" + container + ")", this_lookup)
        
        container_position = xbmc.getInfoLabel(this_lookup)
        
        this_lookup = 'Container(id).Row'
        this_lookup = re.sub(r"Container\(id\)", "Container(" + container + ")", this_lookup)
        
        container_row = xbmc.getInfoLabel(this_lookup)
        
        
        
        
        
        
        for key, value in outlist :
            
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
                
                content = content + '<tr><td>' + key + '</td><td>' + xbmcresult + '</td>' + '<td>' + value + '</td></tr>' + "\n"
                content_txt = content_txt + '[COLOR blue]' + key + '[/COLOR] : [COLOR yellow]' + xbmcresult_txt + '[/COLOR] : [COLOR green]' + "\n" + value + '[/COLOR]' + "\n"







    
        content = content + '</table>'
        content_txt = content_txt + divider_txt
    
        file = xbmc.getInfoLabel("ListItem.FileNameAndPath")
    
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



