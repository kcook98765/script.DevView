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
            "ListItem.Label": "Shows the left label of the currently selected item in a container",
            "ListItem.Label2": "Shows the right label of the currently selected item in a container",
            "ListItem.Title": "Shows the title of the currently selected song or movie in a container",
        
        
            "Container(id).ListItem.Property(Budget)": "Budget",
            "Container(id).ListItem.Property(Revenue)": "Revenue",
            "Container(id).ListItem.Property(Set.TMDb_ID)": "TMDb_ID of Set Movie Belongs To",
            "Container(id).ListItem.Property(Set.Name)": "Name of Set Movie Belongs To",
            "Container(id).ListItem.Property(Set.Poster)": "Poster of Set Movie Belongs To",
            "Container(id).ListItem.Property(Set.Fanart)": "Fanart of Set Movie Belongs To",
        
            "ListItem.Label": "Shows the left label of the currently selected item in a container",
            "ListItem.Label2": "Shows the right label of the currently selected item in a container",
            "ListItem.Title": "Shows the title of the currently selected song or movie in a container",
            "ListItem.OriginalTitle": "Shows the original title of the currently selected movie in a container",
            "ListItem.SortLetter": "Shows the first letter of the current file in a container",
            "ListItem.TrackNumber": "Shows the track number of the currently selected song in a container",
            "ListItem.Artist": "Shows the artist of the currently selected song in a container",
            "ListItem.AlbumArtist": "Shows the artist of the currently selected album in a list",
            "ListItem.Property(Artist_Born)": "Date of Birth of the currently selected Artist",
            "ListItem.Property(Artist_Died)": "Date of Death of the currently selected Artist",
            "ListItem.Property(Artist_Formed)": "Formation date of the currently selected Band",
            "ListItem.Property(Artist_Disbanded)": "Disbanding date of the currently selected Band",
            "ListItem.Property(Artist_YearsActive)": "Years the currently selected artist has been active",
            "ListItem.Property(Artist_Instrument)": "Instruments played by the currently selected artist",
            "ListItem.Property(Artist_Description)": "Shows a biography of the currently selected artist",
            "ListItem.Property(Artist_Mood)": "Shows the moods of the currently selected artist",
            "ListItem.Property(Artist_Style)": "Shows the styles of the currently selected artist",
            "ListItem.Property(Artist_Genre)": "Shows the genre of the currently selected artist",
            "Listitem.Property(Artist_Sortname)": "Sortname of the currently selected Artist",
            "Listitem.Property(Artist_Type)": "Type of the currently selected Artist - person, group, orchestra, choir etc.",
            "Listitem.Property(Artist_Gender)": "Gender of the currently selected Artist - male, female, other",
            "Listitem.Property(Artist_Disambiguation)": "Brief description of the currently selected Artist that differentiates them from others with the same name",
            "ListItem.Album": "Shows the album of the currently selected song in a container",
            "ListItem.Property(Album_Mood)": "Shows the moods of the currently selected Album",
            "ListItem.Property(Album_Style)": "Shows the styles of the currently selected Album",
            "ListItem.Property(Album_Theme)": "Shows the themes of the currently selected Album",
            "ListItem.Property(Album_Type)": "Shows the Album Type (e.g. compilation, enhanced, explicit lyrics) of the currently selected Album",
            "ListItem.Property(Album_Label)": "Shows the record label of the currently selected Album",
            "ListItem.Property(Album_Description)": "Shows a review of the currently selected Album",
            "ListItem.Property(Album_Rating)": "Shows the scraped rating of the currently selected Album",
            "ListItem.Property(Album_UserRating)": "Shows the user rating of the currently selected Album",
            "ListItem.DiscNumber": "Shows the disc number of the currently selected song in a container",
            "ListItem.Year": "Shows the year of the currently selected song, album or movie in a container",
            "ListItem.Premiered": "Shows the release/aired date of the currently selected episode, show, movie or EPG item in a container",
            "ListItem.Genre": "Shows the genre of the currently selected song, album or movie in a container",
            "ListItem.Director": "Shows the director of the currently selected movie in a container",
            "ListItem.Country": "Shows the production country of the currently selected movie in a container",
            "ListItem.Episode": "Shows the episode number value for the currently selected episode. It also shows the number of total, watched or unwatched episodes for the currently selected tvshow or season, based on the the current watched filter.",
            "ListItem.Season": "Shows the season value for the currently selected tvshow",
            "ListItem.TVShowTitle": "Shows the name value for the currently selected tvshow in the season and episode depth of the video library",
            "ListItem.Property(TotalSeasons)": "Shows the total number of seasons for the currently selected tvshow",
            "ListItem.Property(TotalEpisodes)": "Shows the total number of episodes for the currently selected tvshow or season",
            "ListItem.Property(WatchedEpisodes)": "Shows the number of watched episodes for the currently selected tvshow or season",
            "ListItem.Property(UnWatchedEpisodes)": "Shows the number of unwatched episodes for the currently selected tvshow or season",
            "ListItem.Property(NumEpisodes)": "Shows the number of total, watched or unwatched episodes for the currently selected tvshow or season, based on the the current watched filter.",
            "ListItem.PictureAperture": "Shows the F-stop used to take the selected picture. This is the value of the EXIF FNumber tag (hex code 0x829D).",
            "ListItem.PictureAuthor": "Shows the name of the person involved in writing about the selected picture. This is the value of the IPTC Writer tag (hex code 0x7A).",
            "ListItem.PictureByline": "Shows the name of the person who created the selected picture. This is the value of the IPTC Byline tag (hex code 0x50).",
            "ListItem.PictureBylineTitle": "Shows the title of the person who created the selected picture. This is the value of the IPTC BylineTitle tag (hex code 0x55).",
            "ListItem.PictureCamMake": "Shows the manufacturer of the camera used to take the selected picture. This is the value of the EXIF Make tag (hex code 0x010F).",
            "ListItem.PictureCamModel": "Shows the manufacturer's model name or number of the camera used to take the selected picture. This is the value of the EXIF Model tag (hex code 0x0110).",
            "ListItem.PictureCaption": "Shows a description of the selected picture. This is the value of the IPTC Caption tag (hex code 0x78).",
            "ListItem.PictureCategory": "Shows the subject of the selected picture as a category code. This is the value of the IPTC Category tag (hex code 0x0F).",
            "ListItem.PictureCCDWidth": "Shows the width of the CCD in the camera used to take the selected picture. This is calculated from three EXIF tags (0xA002 * 0xA210 / 0xA20e).",
            "ListItem.PictureCity": "Shows the city where the selected picture was taken. This is the value of the IPTC City tag (hex code 0x5A).",
            "ListItem.PictureColour": "Shows whether the selected picture is 'Colour' or 'Black and White'.",
            "ListItem.PictureComment": "Shows a description of the selected picture. This is the value of the EXIF User Comment tag (hex code 0x9286). This is the same value as Slideshow.SlideComment.",
            "ListItem.PictureCopyrightNotice": "Shows the copyright notice of the selected picture. This is the value of the IPTC Copyright tag (hex code 0x74).",
            "ListItem.PictureCountry": "Shows the full name of the country where the selected picture was taken. This is the value of the IPTC CountryName tag (hex code 0x65).",
            "ListItem.PictureCountryCode": "Shows the country code of the country where the selected picture was taken. This is the value of the IPTC CountryCode tag (hex code 0x64).",
            "ListItem.PictureCredit": "Shows who provided the selected picture. This is the value of the IPTC Credit tag (hex code 0x6E).",
            "ListItem.PictureDate": "Shows the localized date of the selected picture. The short form of the date is used. The value of the EXIF DateTimeOriginal tag (hex code 0x9003) is preferred. If the DateTimeOriginal tag is not found, the value of DateTimeDigitized (hex code 0x9004) or of DateTime (hex code 0x0132) might be used.",
            "ListItem.PictureDatetime": "Shows the date/timestamp of the selected picture. The localized short form of the date and time is used. The value of the EXIF DateTimeOriginal tag (hex code 0x9003) is preferred. If the DateTimeOriginal tag is not found, the value of DateTimeDigitized (hex code 0x9004) or of DateTime (hex code 0x0132) might be used.",
            "ListItem.PictureDesc": "Shows a short description of the selected picture. The SlideComment, EXIFComment, or Caption values might contain a longer description. This is the value of the EXIF ImageDescription tag (hex code 0x010E).",
            "ListItem.PictureDigitalZoom": "Shows the digital zoom ratio when the selected picture was taken. This is the value of the EXIF DigitalZoomRatio tag (hex code 0xA404).",
            "ListItem.PictureExpMode": "Shows the exposure mode of the selected picture. The possible values are 'Automatic', 'Manual', and 'Auto bracketing'. This is the value of the EXIF ExposureMode tag (hex code 0xA402).",
            "ListItem.PictureExposure": "Shows the class of the program used by the camera to set exposure when the selected picture was taken. Values include 'Manual', 'Program (Auto)', 'Aperture priority (Semi-Auto)', 'Shutter priority (semi-auto)', etc. This is the value of the EXIF ExposureProgram tag (hex code 0x8822).",
            "ListItem.PictureExposureBias": "Shows the exposure bias of the selected picture. Typically this is a number between -99.99 and 99.99. This is the value of the EXIF ExposureBiasValue tag (hex code 0x9204).",
            "ListItem.PictureExpTime": "Shows the exposure time of the selected picture, in seconds. This is the value of the EXIF ExposureTime tag (hex code 0x829A). If the ExposureTime tag is not found, the ShutterSpeedValue tag (hex code 0x9201) might be used.",
            "ListItem.PictureFlashUsed": "Shows the status of flash when the selected picture was taken. The value will be either 'Yes' or 'No', and might include additional information. This is the value of the EXIF Flash tag (hex code 0x9209).",
            "ListItem.PictureFocalLen": "Shows the lens focal length of the selected picture",
            "ListItem.PictureFocusDist": "Shows the focal length of the lens, in mm. This is the value of the EXIF FocalLength tag (hex code 0x920A).",
            "ListItem.PictureGPSLat": "Shows the latitude where the selected picture was taken (degrees, minutes, seconds North or South). This is the value of the EXIF GPSInfo.GPSLatitude and GPSInfo.GPSLatitudeRef tags.",
            "ListItem.PictureGPSLon": "Shows the longitude where the selected picture was taken (degrees, minutes, seconds East or West). This is the value of the EXIF GPSInfo.GPSLongitude and GPSInfo.GPSLongitudeRef tags.",
            "ListItem.PictureGPSAlt": "Shows the altitude in meters where the selected picture was taken. This is the value of the EXIF GPSInfo.GPSAltitude tag.",
            "ListItem.PictureHeadline": "Shows a synopsis of the contents of the selected picture. This is the value of the IPTC Headline tag (hex code 0x69).",
            "ListItem.PictureImageType": "Shows the color components of the selected picture. This is the value of the IPTC ImageType tag (hex code 0x82).",
            "ListItem.PictureIPTCDate": "Shows the date when the intellectual content of the selected picture was created, rather than when the picture was created. This is the value of the IPTC DateCreated tag (hex code 0x37).",
            "ListItem.PictureIPTCTime": "Shows the time when the intellectual content of the selected picture was created, rather than when the picture was created. This is the value of the IPTC TimeCreated tag (hex code 0x3C).",
            "ListItem.PictureISO": "Shows the ISO speed of the camera when the selected picture was taken. This is the value of the EXIF ISOSpeedRatings tag (hex code 0x8827).",
            "ListItem.PictureKeywords": "Shows keywords assigned to the selected picture. This is the value of the IPTC Keywords tag (hex code 0x19).",
            "ListItem.PictureLightSource": "Shows the kind of light source when the picture was taken. Possible values include 'Daylight', 'Fluorescent', 'Incandescent', etc. This is the value of the EXIF LightSource tag (hex code 0x9208).",
            "ListItem.PictureLongDate": "Shows only the localized date of the selected picture. The long form of the date is used. The value of the EXIF DateTimeOriginal tag (hex code 0x9003) is preferred. If the DateTimeOriginal tag is not found, the value of DateTimeDigitized (hex code 0x9004) or of DateTime (hex code 0x0132) might be used.",
            "ListItem.PictureLongDatetime": "Shows the date/timestamp of the selected picture. The localized long form of the date and time is used. The value of the EXIF DateTimeOriginal tag (hex code 0x9003) is preferred. if the DateTimeOriginal tag is not found, the value of DateTimeDigitized (hex code 0x9004) or of DateTime (hex code 0x0132) might be used.",
            "ListItem.PictureMeteringMode": "Shows the metering mode used when the selected picture was taken. The possible values are 'Center weight', 'Spot', or 'Matrix'. This is the value of the EXIF MeteringMode tag (hex code 0x9207).",
            "ListItem.PictureObjectName": "Shows a shorthand reference for the selected picture. This is the value of the IPTC ObjectName tag (hex code 0x05).",
            "ListItem.PictureOrientation": "Shows the orientation of the selected picture. Possible values are 'Top Left', 'Top Right', 'Left Top', 'Right Bottom', etc. This is the value of the EXIF Orientation tag (hex code 0x0112).",
            "ListItem.PicturePath": "Shows the filename and path of the selected picture",
            "ListItem.PictureProcess": "Shows the process used to compress the selected picture",
            "ListItem.PictureReferenceService": "Shows the Service Identifier of a prior envelope to which the selected picture refers. This is the value of the IPTC ReferenceService tag (hex code 0x2D).",
            "ListItem.PictureResolution": "Shows the dimensions of the selected picture",
            "ListItem.PictureSource": "Shows the original owner of the selected picture. This is the value of the IPTC Source tag (hex code 0x73).",
            "ListItem.PictureSpecialInstructions": "Shows other editorial instructions concerning the use of the selected picture. This is the value of the IPTC SpecialInstructions tag (hex code 0x28).",
            "ListItem.PictureState": "Shows the State/Province where the selected picture was taken. This is the value of the IPTC ProvinceState tag (hex code 0x5F).",
            "ListItem.PictureSublocation": "Shows the location within a city where the selected picture was taken - might indicate the nearest landmark. This is the value of the IPTC SubLocation tag (hex code 0x5C).",
            "ListItem.PictureSupplementalCategories": "Shows supplemental category codes to further refine the subject of the selected picture. This is the value of the IPTC SuppCategory tag (hex code 0x14).",
            "ListItem.PictureTransmissionReference": "Shows a code representing the location of original transmission of the selected picture. This is the value of the IPTC TransmissionReference tag (hex code 0x67).",
            "ListItem.PictureUrgency": "Shows the urgency of the selected picture. Values are 1-9. The '1' is most urgent. Some image management programs use urgency to indicate picture rating, where urgency '1' is 5 stars and urgency '5' is 1 star. Urgencies 6-9 are not used for rating. This is the value of the IPTC Urgency tag (hex code 0x0A).",
            "ListItem.PictureWhiteBalance": "Shows the white balance mode set when the selected picture was taken. The possible values are 'Manual' and 'Auto'. This is the value of the EXIF WhiteBalance tag (hex code 0xA403).",
            "ListItem.FileName": "Shows the filename of the currently selected song or movie in a container",
            "ListItem.FileNameNoExtension": "Returns the filename without its extension.",
            "ListItem.Path": "Shows the complete path of the currently selected song or movie in a container",
            "ListItem.FolderName": "Shows top most folder of the path of the currently selected song or movie in a container",
            "ListItem.FolderPath": "Shows the complete path of the currently selected song or movie in a container (without user details).",
            "ListItem.FileNameAndPath": "Shows the full path with filename of the currently selected song or movie in a container",
            "ListItem.FileExtension": "Shows the file extension (without leading dot) of the currently selected item in a container",
            "ListItem.Date": "Shows the file date of the currently selected song or movie in a container / Aired date of an episode / Day, start time and end time of current selected TV programme (PVR)",
            "ListItem.DateAdded": "Shows the date the currently selected item was added to the library / Date and time of an event in the EventLog window.",
            "ListItem.Size": "Shows the file size of the currently selected song or movie in a container",
            "ListItem.Rating": "Shows the scraped rating of the currently selected item in a container. Optionally you can specify the name of the scraper to retrieve a specific rating, for use in dialogvideoinfo.xml.",
            "ListItem.Set": "Shows the name of the set the movie is part of",
            "ListItem.SetId": "Shows the id of the set the movie is part of",
            "ListItem.UserRating": "Shows the user rating of the currently selected item in a container",
            "ListItem.Votes": "Shows the IMDB votes of the currently selected movie in a container. Optionally you can specify the name of the scraper to retrieve specific votes, for use in dialogvideoinfo.xml.",
            "ListItem.RatingAndVotes": "Shows the IMDB rating and votes of the currently selected movie in a container. Optionally you can specify the name of the scraper to retrieve a specific rating and votes, for use in dialogvideoinfo.xml.",
            "ListItem.Mpaa": "Show the MPAA rating of the currently selected movie in a container",
            "ListItem.ProgramCount": "Shows the number of times an xbe has been run from 'my programs'",
            "ListItem.Duration": "Shows the song or movie duration of the currently selected movie in a container. Optionally specify a time format, hours (hh), minutes (mm) or seconds (ss). When 12 hour clock is used (xx) will return AM/PM. Also supported: (hh:mm), (mm:ss), (hh:mm:ss), (hh:mm:ss).",
            "ListItem.DBTYPE": "Shows the database type of the ListItem.DBID for videos (video, movie, set, tvshow, season, episode, musicvideo) or for audio (music, song, album, artist). Beware with season, the '*all seasons' entry does give a DBTYPE 'season' and a DBID, but you can't get the details of that entry since it's a virtual entry in the Video Library.",
            "ListItem.DBID": "Shows the database id of the currently selected listitem in a container",
            "ListItem.Cast": "Shows a concatenated string of cast members of the currently selected movie, for use in dialogvideoinfo.xml",
            "ListItem.CastAndRole": "Shows a concatenated string of cast members and roles of the currently selected movie, for use in dialogvideoinfo.xml",
            "ListItem.Studio": "Studio of current selected Music Video in a container",
            "ListItem.Top250": "Shows the IMDb top250 position of the currently selected listitem in a container.",
            "ListItem.Trailer": "Shows the full trailer path with filename of the currently selected movie in a container",
            "ListItem.Writer": "Name of Writer of current Video in a container",
            "ListItem.Tagline": "Small Summary of current Video in a container",
            "ListItem.PlotOutline": "Small Summary of current Video in a container",
            "ListItem.Plot": "Complete Text Summary of Video in a container",
            "ListItem.IMDBNumber": "The IMDB iD of the selected Video in a container",
            "ListItem.EpisodeName": "(PVR only) The name of the episode if the selected EPG item is a TV Show",
            "ListItem.PercentPlayed": "Returns percentage value [0-100] of how far the selected video has been played",
            "ListItem.LastPlayed": "Last play date of Video in a container",
            "ListItem.PlayCount": "Playcount of Video in a container",
            "ListItem.StartTime": "Start time of current selected TV programme in a container",
            "ListItem.EndTime": "End time of current selected TV programme in a container",
            "ListItem.StartDate": "Start date of current selected TV programme in a container",
            "ListItem.ChannelName": "Name of current selected TV channel in a container",
            "ListItem.VideoCodec": "Shows the video codec of the currently selected video (common values: 3iv2, avc1, div2, div3, divx, divx 4, dx50, flv, h264, microsoft, mp42, mp43, mp4v, mpeg1video, mpeg2video, mpg4, rv40, svq1, svq3, theora, vp6f, wmv2, wmv3, wvc1, xvid)",
            "ListItem.VideoResolution": "Shows the resolution of the currently selected video (possible values: 480, 576, 540, 720, 1080, 4K, 8K [Note: v18 addition]). Note that 540 usually means a widescreen format (around 960x540) while 576 means PAL resolutions (normally 720x576), therefore 540 is actually better resolution than 576.",
            "ListItem.VideoAspect": "Shows the aspect ratio of the currently selected video (possible values: 1.33, 1.37, 1.66, 1.78, 1.85, 2.20, 2.35, 2.40, 2.55, 2.76, Note: Kodi v20: 1.00, 1.19, 2.00 )",
            "ListItem.AudioCodec": "Shows the audio codec of the currently selected video (common values: aac, ac3, cook, dca, dtshd_hra, dtshd_ma, eac3, mp1, mp2, mp3, pcm_s16be, pcm_s16le, pcm_u8, truehd, vorbis, wmapro, wmav2)",
            "ListItem.AudioChannels": "Shows the number of audio channels of the currently selected video (possible values: 1, 2, 4, 5, 6, 7, 8, 10)",
            "ListItem.AudioLanguage": "Shows the audio language of the currently selected video (returns an ISO 639-2 three character code, e.g. eng, epo, deu)",
            "ListItem.SubtitleLanguage": "Shows the subtitle language of the currently selected video (returns an ISO 639-2 three character code, e.g. eng, epo, deu)",
            "ListItem.Property(AudioCodec.0)": "Shows the audio codec of the currently selected video, 'n' defines the number of the audiostream (values: see ListItem.AudioCodec)",
            "ListItem.Property(AudioChannels.0)": "Shows the number of audio channels of the currently selected video, 'n' defines the number of the audiostream (values: see ListItem.AudioChannels)",
            "ListItem.Property(AudioLanguage.0)": "Shows the audio language of the currently selected video, 'n' defines the number of the audiostream (values: see ListItem.AudioLanguage)",
            "ListItem.Property(SubtitleLanguage.0)": "Shows the subtitle language of the currently selected video, 'n' defines the number of the subtitle (values: see ListItem.SubtitleLanguage)",
            "ListItem.AddonName": "Shows the name of the currently selected addon",
            "ListItem.AddonVersion": "Shows the version of the currently selected addon",
            "ListItem.AddonSummary": "Shows a short description of the currently selected addon",
            "ListItem.AddonDescription": "Shows the full description of the currently selected addon",
            "ListItem.AddonType": "Shows the type (screensaver, script, skin, etc...) of the currently selected addon",
            "ListItem.AddonCreator": "Shows the name of the author the currently selected addon",
            "ListItem.AddonDisclaimer": "Shows the disclaimer of the currently selected addon",
            "ListItem.AddonBroken": "Deprecated! use ListItem.AddonLifecycleDesc instead",
            "ListItem.Property(Addon.Changelog)": "Shows the changelog of the currently selected addon",
            "ListItem.Property(Addon.ID)": "Shows the identifier of the currently selected addon",
            "ListItem.Property(Addon.Status)": "Shows the status of the currently selected addon",
            "ListItem.Property(Addon.Path)": "Shows the path of the currently selected addon",
            "ListItem.StartTime": "Start time of the selected item (PVR).",
            "ListItem.EndTime": "End time of the selected item (PVR).",
            "ListItem.StartDate": "Start date of the selected item (PVR).",
            "ListItem.EndDate": "End date of the selected item (PVR).",
            "ListItem.NextTitle": "Title of the next item (PVR).",
            "ListItem.NextGenre": "Genre of the next item (PVR).",
            "ListItem.NextPlot": "Plot of the next item (PVR).",
            "ListItem.NextPlotOutline": "Plot outline of the next item (PVR).",
            "ListItem.NextStartTime": "Start time of the next item (PVR).",
            "ListItem.NextEndTime": "End of the next item (PVR).",
            "ListItem.NextStartDate": "Start date of the next item (PVR).",
            "ListItem.NextEndDate": "End date of the next item (PVR).",
            "Listitem.NextDuration": "Duration of the next item (PVR).",
            "ListItem.ChannelName": "Channelname of the selected item (PVR).",
            "ListItem.ChannelNumber": "Channel number of the selected item (PVR).",
            "ListItem.ChannelNumberLabel": "Channel and subchannel number of the currently selected channel that's currently playing (PVR).",
            "ListItem.Progress": "Part of the programme that's been played (PVR).",
            "ListItem.StereoscopicMode": "Returns the stereomode of the selected video (i.e. mono, split_vertical, split_horizontal, row_interleaved, anaglyph_cyan_red, anaglyph_green_magenta)",
            "ListItem.Comment": "Comment assigned to the item (PVR/MUSIC).",
            "ListItem.AddonInstallDate": "Date the addon was installed",
            "ListItem.AddonLastUpdated": "Date the addon was last updated",
            "ListItem.AddonLastUsed": "Date the addon was used last",
            "ListItem.AddonNews": "Returns a brief changelog, taken from the addons' addon.xml file",
            "ListItem.AddonSize": "Filesize of the addon",
            "ListItem.Contributors": "List of all people who've contributed to the selected song",
            "ListItem.ContributorAndRole": "List of all people and their role who've contributed to the selected song",
            "ListItem.EndTimeResume": "Returns the time a video will end if you resume it, instead of playing it from the beginning.",
            "ListItem.Mood": "Mood of the selected song",
            "ListItem.Status": "For use with tv shows. It can return one of the following: 'returning series','in production','planned','cancelled' or 'ended'",
            "ListItem.Tag": "Will return the name of the 'tag' this movie is part of.",
            "ListItem.Property(Role.Arranger)": "Returns the name of the person who arranged the selected song",
            "ListItem.Property(Role.Composer)": "Returns the name of the person who composed the selected song",
            "ListItem.Property(Role.Conductor)": "Returns the name of the person who conducted the selected song",
            "ListItem.Property(Role.DJMixer)": "Returns the name of the dj who remixed the selected song",
            "ListItem.Property(Role.Engineer)": "Returns the name of the person who was the engineer of the selected song",
            "ListItem.Property(Role.Lyricist)": "Returns the name of the person who wrote the lyrics of the selected song",
            "ListItem.Property(Role.Mixer)": "Returns the name of the person who mixed the selected song",
            "ListItem.Property(Role.Orchestra)": "Returns the name of the orchestra performing the selected song",
            "ListItem.Property(Role.Producer)": "Returns the name of the person who produced the selected song",
            "ListItem.Property(Role.Remixer)": "Returns the name of the person who remixed the selected song",
            "ListItem.Property(Album_Duration)": "Returns the duration of an album in HH:MM:SS",
            "ListItem.Appearances": "Returns the number of movies featuring the selected actor / directed by the selected director",
            "ListItem.PrivacyPolicy": "Returns the official Kodi privacy-policy",
            "Listitem.Property(game.videofilter)": "Name of the video filter (eg. Bilinear)",
            "Listitem.Property(game.stretchmode)": "Name of the stretch mode (eg. Stretch 4:3)",
            "Listitem.Property(game.videorotation)": "Angle of the rotation",
            "ListItem.CurrentItem": "will return the current index of the item in a container starting at 1.",
            "ListItem.DiscTitle": "The disc title of the currently selected album or song",
            "ListItem.TotalDiscs": "The total amount of discs belonging to an album",
            "ListItem.IsBoxset": "Returns true if the item is part of a boxset",
            "ListItem.ReleaseDate": "Returns the release date of the current item",
            "ListItem.OriginalDate": "Returns the original release date of the item",
            "ListItem.BPM": "Returns the Beats Per Minute for a song",
            "ListItem.BitRate": "Returns the bitrate of the current song (Actual rate for CBR, average rate for VBR)",
            "ListItem.SampleRate": "Returns the sample rate of a song / 1000.0 eg 44.1, 48, 96 etc",
            "ListItem.MusicChannels": "Returns the number of audio channels for a song",
            "ListItem.AlbumStatus": "Returns the Musicbrainz release status of the album (offical, bootleg, promotion etc)",
            "ListItem.UniqueID()": "Returns the UniqueID of the selected item in a container",
            "ListItem.TvShowDBID": "Returns the tv show DBID of the selected season or episode a container",
            "ListItem.AddonLifecycleType": "The Lifecycle type of the addon (returns a localized string: normal / broken / deprecated)",
            "ListItem.AddonLifecycleDesc": "Description of the Lifecycle type (example: broken due to website changes)",
            
            "Container(id).Row": "Returns the row number of the focused position in a panel container.",
            "Container(id).Position": "Returns the current focused position of the container / grouplist (id) as a numeric label.",
            "Container(id).NumPages": "Number of pages in the container with given id. If no id is specified it grabs the current container.",
            "Container(id).NumNonFolderItems": "Number of items in the container or grouplist with given id excluding all folder items.",
            "Container(id).NumItems": "Number of items in the container or grouplist with given id. If no id is specified it grabs the current container.",
            "Container(id).NumAllItems": "Number of all items in the container or grouplist with given id including parent folder item.",
            "Container(id).CurrentPage": "Current page in the container with given id. If no id is specified it grabs the current container.",
            "Container(id).CurrentItem": "Current absolute item in the container or grouplist with given id. If no id is specified it grabs the current container.",
            "Container(id).Column": "Returns the column number of the focused position in a panel container.",
            "Fanart.Color1": "Returns the first of three colors included in the currently selected Fanart theme for the parent TV Show. Colors are arranged Lightest to Darkest.",     
            "Fanart.Color2": "Returns the second of three colors included in the currently selected Fanart theme for the parent TV Show. Colors are arranged Lightest to Darkest.",     
            "Fanart.Color3": "Returns the third of three colors included in the currently selected Fanart theme for the parent TV Show. Colors are arranged Lightest to Darkest.", 
            
            "Game.Title": "Name of the game",
            "Game.Platform": "Platform the game runs on (eg. Atari 2600)",
            "Game.Genres": "Gerne of the game (eg. Action)",
            "Game.Publisher": "Publishing company of the game (eg. Nintendo)",
            "Game.Developer": "Developer of the game",
            "Game.Overview": "Game description",
            "Game.Year": "Year the game was released",
            "Game.GameClient": "Name of the used emulator",
        
            "MusicPartyMode.SongsPlayed": "Number of songs played during Party Mode",
            "MusicPartyMode.MatchingSongs": "Number of songs available to Party Mode",
            "MusicPartyMode.MatchingSongsPicked": "Number of songs picked already for Party Mode",
            "MusicPartyMode.MatchingSongsLeft": "Number of songs left to be picked from for Party Mode",
            "MusicPartyMode.RelaxedSongsPicked": "Not currently used",
            "MusicPartyMode.RandomSongsPicked": "Number of unique random songs picked during Party Mode",
        
        
            "Network.IsDHCP": "Network type is DHCP or FIXED",
            "Network.IPAddress": "The system's IP Address (<ipaddress> is returned as a string)",
            "Network.LinkState": "Network linkstate e.g. 10mbit/100mbit etc.",
            "Network.MacAddress": "The system's mac address",
            "Network.SubnetMask": "Network subnet mask",
            "Network.GatewayAddress": "Network gateway address",
            "Network.DNS1Address": "Network dns server 1 address",
            "Network.DNS2Address": "Network dns server 2 address",
            "Network.DHCPAddress": "DHCP server ip address",
        
        
            "Playlist.Length(video)": "Total size of the current playlist. optional parameter media is either video or music.",
            "Playlist.Position(video)": "Position of the current item in the current playlist. optional parameter media is either video or music.",
            "Playlist.Length(music)": "Total size of the current playlist. optional parameter media is either video or music.",
            "Playlist.Position(music)": "Position of the current item in the current playlist. optional parameter media is either video or music.",    
            "Playlist.Random": "Returns 'On' or 'Off'",
            "Playlist.Repeat": "Returns string ID's 592 (Repeat One), 593 (Repeat All), or 594 (Repeat Off)",
        
        
            "Skin.CurrentTheme": "Returns the current selected skin theme.",
            "Skin.CurrentColourTheme": "Returns the current selected colour theme of the skin.",
            "Skin.Font": "Returns the current fontset from Font.xml.",
            "Skin.String(name)": "Returns the user-set skin string, set via the Skin.SetString(name) List of Built In Functions. Allows skinners to have user-customisable labels.",
            "Skin.AspectRatio": "Returns the closest aspect ratio match using the resolution info from the skin's addon.xml file.",
        
        
            "System.Time": "Current time",
            "System.Time(hh:mm:ss)": "Shows hours (hh), minutes (mm) or seconds (ss). When 12 hour clock is used (xx) will return AM/PM. Also supported: (hh:mm), (mm:ss), (hh:mm:ss), (hh:mm:ss). (xx) option added after dharma",
            "System.Date": "Current date",
            'System.Date(mm dd yyyy)': "Show current date using format, available markings: d (day of month 1-31), dd (day of month 01-31), ddd (short day of the week Mon-Sun), DDD (long day of the week Monday-Sunday), m (month 1-12), mm (month 01-12), mmm (short month name Jan-Dec), MMM (long month name January-December), yy (2-digit year), yyyy (4-digit year). Added after dharma.",
            "System.AlarmPos": "Shutdown Timer position",
            "System.BatteryLevel": "Returns the remaining battery level in range 0-100",
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
            "System.FriendlyName": "Returns the Kodi instance name. It will auto append (%hostname%) in case the device name was not changed. eg. 'Kodi (htpc)'",
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
            
            "Visualisation.Preset": "Shows the current preset of the visualisation.",
            "Visualisation.Name": "Shows the name of the visualisation.",
            
            "Weather.Conditions": "Current weather conditions - this is looked up in a background process.",
            "Weather.Temperature": "Current weather temperature ",
            "Weather.Location": "City/town which the above two items are for",
            "Weather.fanartcode": "Current weather fanartcode.",
            "Weather.plugin": "Current weather plugin.",
            
            
            "Window().Property(key)": "Window property. (key can be any value, optional window can be id or name)",
            "Window.Property(xmlfile)": "Displays the name of the xml file currently shown",
            "Window.Property(IsRadio)": "Returns 'true' if the window is a radio window, empty string otherwise (for use in the PVR windows)",
            "Window(AddonBrowser).Property(Updated)": "Shows the date and time the addon repo was last checked for updates",
            "Window.Property(Addon.ID)": "Returns the id of the selected addon, in DialogAddonSettings.xml",
            "Window(Home).Property(Movies.Count)": "The home window has the following info labels.",
            "Window(Home).Property(Movies.Watched)": "The home window has the following info labels.",
            "Window(Home).Property(Movies.UnWatched)": "The home window has the following info labels.",
            "Window(Home).Property(TVShows.Count)": "The home window has the following info labels.",
            "Window(Home).Property(TVShows.Watched)": "The home window has the following info labels.",
            "Window(Home).Property(TVShows.UnWatched)": "The home window has the following info labels.",
            "Window(Home).Property(Episodes.Count)": "The home window has the following info labels.",
            "Window(Home).Property(Episodes.Watched)": "The home window has the following info labels.",
            "Window(Home).Property(Episodes.UnWatched)": "The home window has the following info labels.",
            "Window(Home).Property(MusicVideos.Count)": "The home window has the following info labels.",
            "Window(Home).Property(MusicVideos.Watched)": "The home window has the following info labels.",
            "Window(Home).Property(MusicVideos.UnWatched)": "The home window has the following info labels.",
            "Window(Home).Property(Music.SongsCount)": "The home window has the following info labels.",
            "Window(Home).Property(Music.AlbumsCount)": "The home window has the following info labels.",
            "Window(Home).Property(Music.ArtistsCount)": "The home window has the following info labels.",
        
            
            "Window(Weather).Property(Location)": "The weather window has the following info labels.",
            "Window(Weather).Property(Updated)": "The weather window has the following info labels.",
            "Window(Weather).Property(Current.Condition)": "The weather window has the following info labels.",
            "Window(Weather).Property(Current.Temperature)": "The weather window has the following info labels.",
            "Window(Weather).Property(Current.FeelsLike)": "The weather window has the following info labels.",
            "Window(Weather).Property(Current.UVIndex)": "The weather window has the following info labels.",
            "Window(Weather).Property(Current.Wind)": "(From <wind dir.> at <speed> <unit>)",
            "Window(Weather).Property(Current.WindSpeed)": "The weather window has the following info labels.",
            "Window(Weather).Property(Current.WindDirection)": "The weather window has the following info labels.",
            "Window(Weather).Property(Current.DewPoint)": "The weather window has the following info labels.",
            "Window(Weather).Property(Current.Humidity)": "The weather window has the following info labels.",
            "Window(Weather).Property(WeatherProvider)": "The weather window has the following info labels.",
            
            "ListItem.Art(poster)": "Artwork for the current listitem.",
            "ListItem.Art(fanart)": "Artwork for the current listitem.",
            "ListItem.Art(landscape)": "Artwork for the current listitem.",
            "ListItem.Art(thumb)": "Artwork for the current listitem.",
            "ListItem.Art(tvshow.clearlogo)": "Artwork for the current listitem.",
            "ListItem.Art(set.poster)": "Artwork for the current listitem.",
            "ListItem.Art(season.poster)": "Artwork for the current listitem.",
            "ListItem.Art(artist.fanart)": "Artwork for the current listitem.",
            "ListItem.Art(artist.clearlogo)": "Artwork for the current listitem.",
            
            "ListItem.Art(clearlogo)": "Artwork for the current listitem.",
            "ListItem.Art(tvshow.poster)": "Artwork for the current listitem.",
            "ListItem.Art(set.poster )": "Artwork for the current listitem.",
            "ListItem.Art(album.thumb)": "Artwork for the current listitem.",
            "ListItem.Art(album.thumb )": "Artwork for the current listitem.",
        
        
            "Fanart.Image": "Fanart image for the parent TV Show. Note: Deprecated, use ListItem.Art(tvshow.fanart) instead.",
            "ListItem.Thumb": "Shows the thumbnail (if it exists) of the currently selected item in a list or thumb control. Note: Deprecated but still available, returns the same as ListItem.Art(thumb).", 
            "ListItem.Icon": "Shows the thumbnail (if it exists) of the currently selected item in a list or thumb control. If no thumbnail image exists, it will show the default icon.",
            "ListItem.ActualIcon": "Shows the default icon of the currently selected item in a list or thumb control.",
            "ListItem.Overlay": "Shows the Overlay Icon status (compressed file [OverlayRAR.png], watched [OverlayWatched.png], unwatched [OverlayUnwatched.png], locked [OverlayLocked.png]) of the currently selected item in a list or thumb control.",
            "ListItem.EPGEventIcon": "Returns the icon of the EPG programme (if available).",
            "ListItem.Property(Fanart_Image)": "Fanart Image currently selected item or of the parent TV show. Note: Deprecated, use ListItem.Art(fanart) or ListItem.Art(tvshow.fanart) instead.",
            "MusicPlayer.Cover": "Cover of currently playing album",
            "MusicPlayer.Property(Fanart_Image)": "Fanart image of the currently playing artist",
            "Player.Art(type)": "Artwork for the currently playing item.",
            "Player.Icon": "Shows the thumbnail (if it exists) of the currently playing item. If no thumbnail image exists, it will show the icon.",
            "Player.StarRating": "Returns a value of 0 to 5 as a graphical display from images named rating0.png to rating5.png of the skin",
            "Pvr.NowRecordingChannelIcon": "Channel icon of the programme currently being recorded.",
            "Pvr.NextRecordingChannelIcon": "Channel icon of the programme that will be recorded next.",
            "Pvr.EPGEventIcon": "Returns the icon of the currently playing EPG programme (if available).",
            "Skin.String(name)": "Returns the image or image folder set by the user via a Skin.SetPath(name) or Skin.SetImage(name) List of Built In Functions. Allows skinners to have user-customisable images and multiimages.",
            "System.AddonIcon(id)": "Returns the Icon of the specified addon. Instead of specifying the id directly, one can also use an infolabel (eg. $INFO[Skin.String(Foo)])",
            "System.ProfileThumb": "Shows the Thumbnail image of the currently logged in Kodi user",
            "VideoPlayer.Cover": "Cover of currently playing movie. Note: Deprecated, use Player.Art(type) instead.",
            "Weather.ConditionsIcon": "Image of current weather conditions (NOTE: Can be used to load/refresh weather conditions)",


            "Window(Home).ListItem.Budget": "Budget",
            "Container(99950).Property(Budget)": "Budget",

        
            "ListItem.Property(TMDb_ID)": "TMDb ID",
            "ListItem.Property(IMDb_ID)": "IMDb ID",
            "ListItem.Property(TVDb_ID)": "TVDb ID",
            "ListItem.Property(Genre.X.Name)": "Name of Genre at X position",
            "ListItem.Property(Genre.X.TMDb_ID)": "TMDb_ID of Genre at X position",
            "ListItem.Property(Studio.X.Name)": "Name of Studio at X position. Note for TV Shows     'ListItem.Studio' combines Release Network + Production Studios. Studio.X properties only list Production Studios. Use Network.X properties to retrieve TV Networks",
            "ListItem.Property(Studio.X.Icon)": "Icon of Studio at X position",
            "ListItem.Property(Studio.X.TMDb_ID)": "TMDb_ID of Studio at X position",
            "ListItem.Property(Country.X.Name)": "Name of Country at X position",
            "ListItem.Property(Country.X.TMDb_ID)": "TMDb_ID of Country at X position",
            "ListItem.Property(Language.X.Name)": "Name of Language at X position",
            "ListItem.Property(Language.X.ISO)": "ISO of Language at X position",
            "ListItem.Property(Cast.X.Name)": "Name of Cast at X position",
            "ListItem.Property(Cast.X.Role)": "Role of Cast at X position",
            "ListItem.Property(Cast.X.Character)": "Character of Cast at X position",
            "ListItem.Property(Cast.X.Thumb)": "Thumb of Cast at X position",
            "ListItem.Property(Crew.X.Name)": "Name of Crew at X position",
            "ListItem.Property(Crew.X.Role)": "Role of Crew at X position",
            "ListItem.Property(Crew.X.Job)": "Job of Crew at X position",
            "ListItem.Property(Crew.X.Department)": "Department of Crew at X position",
            "ListItem.Property(Crew.X.Thumb)": "Thumb of Crew at X position",
            "ListItem.Property(Screenplay.X.Name)": "Name of Screenplay at X position",
            "ListItem.Property(Screenplay.X.Role)": "Role of Screenplay at X position",
            "ListItem.Property(Screenplay.X.Job)": "Job of Screenplay at X position",
            "ListItem.Property(Screenplay.X.Department)": "Department of Screenplay at X position",
            "ListItem.Property(Screenplay.X.Thumb)": "Thumb of Screenplay at X position",
            "ListItem.Property(Director.X.Name)": "Name of Director at X position",
            "ListItem.Property(Director.X.Role)": "Role of Director at X position",
            "ListItem.Property(Director.X.Job)": "Job of Director at X position",
            "ListItem.Property(Director.X.Department)": "Department of Director at X position",
            "ListItem.Property(Director.X.Thumb)": "Thumb of Director at X position",
            "ListItem.Property(Writer.X.Name)": "Name of Writer at X position",
            "ListItem.Property(Writer.X.Role)": "Role of Writer at X position",
            "ListItem.Property(Writer.X.Job)": "Job of Writer at X position",
            "ListItem.Property(Writer.X.Department)": "Department of Writer at X position",
            "ListItem.Property(Writer.X.Thumb)": "Thumb of Writer at X position",
            "ListItem.Property(Producer.X.Name)": "Name of Producer at X position",
            "ListItem.Property(Producer.X.Role)": "Role of Producer at X position",
            "ListItem.Property(Producer.X.Job)": "Job of Producer at X position",
            "ListItem.Property(Producer.X.Department)": "Department of Producer at X position",
            "ListItem.Property(Producer.X.Thumb)": "Thumb of Producer at X position",
            "ListItem.Property(Sound_Department.X.Name)": "Name of Sound_Department at X position",
            "ListItem.Property(Sound_Department.X.Role)": "Role of Sound_Department at X position",
            "ListItem.Property(Sound_Department.X.Job)": "Job of Sound_Department at X position",
            "ListItem.Property(Sound_Department.X.Department)": "Department of Sound_Department at X position",
            "ListItem.Property(Sound_Department.X.Thumb)": "Thumb of Sound_Department at X position",
            "ListItem.Property(Art_Department.X.Name)": "Name of Art_Department at X position",
            "ListItem.Property(Art_Department.X.Role)": "Role of Art_Department at X position",
            "ListItem.Property(Art_Department.X.Job)": "Job of Art_Department at X position",
            "ListItem.Property(Art_Department.X.Department)": "Department of Art_Department at X position",
            "ListItem.Property(Art_Department.X.Thumb)": "Thumb of Art_Department at X position",
            "ListItem.Property(Photography.X.Name)": "Name of Photography at X position",
            "ListItem.Property(Photography.X.Role)": "Role of Photography at X position",
            "ListItem.Property(Photography.X.Job)": "Job of Photography at X position",
            "ListItem.Property(Photography.X.Department)": "Department of Photography at X position",
            "ListItem.Property(Photography.X.Thumb)": "Thumb of Photography at X position",
            "ListItem.Property(Editor.X.Name)": "Name of Editor at X position",
            "ListItem.Property(Editor.X.Role)": "Role of Editor at X position",
            "ListItem.Property(Editor.X.Job)": "Job of Editor at X position",
            "ListItem.Property(Editor.X.Department)": "Department of Editor at X position",
            "ListItem.Property(Editor.X.Thumb)": "Thumb of Editor at X position",
            
            "ListItem.Property(Budget)": "Budget",
            "ListItem.Property(Revenue)": "Revenue",
            "ListItem.Property(Set.TMDb_ID)": "TMDb_ID of Set Movie Belongs To",
            "ListItem.Property(Set.Name)": "Name of Set Movie Belongs To",
            "ListItem.Property(Set.Poster)": "Poster of Set Movie Belongs To",
            "ListItem.Property(Set.Fanart)": "Fanart of Set Movie Belongs To",
            
            "ListItem.Property(Last_Aired)": "Last Aired Date in Kodi System Short Format",
            "ListItem.Property(Last_Aired.Day)": "Last Aired Day",
            "ListItem.Property(Last_Aired.Long)": "Last Aired Date in Kodi System Long Format",
            "ListItem.Property(Last_Aired.Short)": "Last Aired in %d %b format e.g. 6 May",
            "ListItem.Property(Last_Aired.Episode)": "Last Aired Episode",
            "ListItem.Property(Last_Aired.Name)": "Last Aired Name",
            "ListItem.Property(Last_Aired.TMDb_ID)": "Last Aired TMDb_ID",
            "ListItem.Property(Last_Aired.Plot)": "Last Aired Plot",
            "ListItem.Property(Last_Aired.Season)": "Last Aired Season",
            "ListItem.Property(Last_Aired.Rating)": "Last Aired Rating",
            "ListItem.Property(Last_Aired.Votes)": "Last Aired Votes",
            "ListItem.Property(Last_Aired.Thumb)": "Last Aired Thumb",
            "ListItem.Property(Next_Aired)": "Next Aired Date in Kodi System Short Format",
            "ListItem.Property(Next_Aired.Day)": "Next Aired Day",
            "ListItem.Property(Next_Aired.Long)": "Next Aired Date in Kodi System Long Format",
            "ListItem.Property(Next_Aired.Short)": "Next Aired Date in %d %b format e.g. 6 May",
            "ListItem.Property(Next_Aired.Episode)": "Next Aired Episode",
            "ListItem.Property(Next_Aired.Name)": "Next Aired Name",
            "ListItem.Property(Next_Aired.TMDb_ID)": "Next Aired TMDb_ID",
            "ListItem.Property(Next_Aired.Plot)": "Next Aired Plot",
            "ListItem.Property(Next_Aired.Season)": "Next Aired Season",
            "ListItem.Property(Next_Aired.Thumb)": "Next Aired Thumb",
            "ListItem.Property(Creator)": "List of TvShow Creators",
            "ListItem.Property(Creator.X.Name)": "Name of Creator at X Position",
            "ListItem.Property(Creator.X.TMDb_ID)": "TMDb ID of Creator at X Position",
            "ListItem.Property(Creator.X.Thumb)": "Thumb of Creator at X Position",
            "ListItem.Property(Network)": "List of Networks. Note for TV Shows ListItem.Studio combines Release Network + Production Studios. Use Network property to retrieve only TV Networks.",
            "ListItem.Property(Network.X.Name)": "Name of Network at X position. Note for TV Shows Studio.X properties contain only Production Studios. Use Network.X properties to retrieve TV Networks.",
            "ListItem.Property(Network.X.Icon)": "Icon of Network at X position",
            "ListItem.Property(Network.X.TMDb_ID)": "TMDb_ID of Network at X position",
            "ListItem.Property(Air_Time)": "Time Program Airs (Trakt)",
            "ListItem.Property(UnWatchedEpisodes)": "Number of Episodes Remaining (Trakt)",
        }
    
    # if intrest:
    # Window(Weather).Property(key) 
    # The weather window has the following info labels.
    # Day[0-6].Title, Day[0-6].HighTemp, Day[0-6].LowTemp, Day[0-6].Outlook, 
    
    
    
    # unsure how to get these, if possible at all.
    #    "System.AddonTitle(id)": "Returns the title of the addon with the given id",
    #    "System.AddonVersion(id)": "Returns the version of the addon with the given id",
    
    
    #    "Container.Viewmode": "Returns the current viewmode (list, icons etc.)",
    #    "Container.ViewCount": "The number of available skin view modes for the current container listing.",
    #    "Container.TotalWatched": "Returns the number of watched items in the current container",
    #    "Container.TotalUnWatched": "Returns the number of unwatched items in the current container",
    #    "Container.Totaltime": "Returns the total time of all items in the current container",
    #    "Container.SortOrder": "Returns the current sort order (Ascending/Descending)",
    #    "Container.SortMethod": "Returns the current sort method (returns the localized name of: title, year, rating, etc.)",
    #    "Container.ShowTitle": "Returns the TV Show title of the current container and can be used at season and episode level",
    #    "Container.ShowPlot": "Returns the TV Show plot of the current container and can be used at season and episode level",
    #    "Container.Property(reponame)": "Returns the current add-on repository name",
    #    "Container.Property(addoncategory)": "Returns the current add-on category",
    #    "Container.PluginName": "Returns the current plugins base folder name",
    #    "Container.PluginCategory": "Returns the current plugins category (set by the scripter)",
    #    "Container.FolderPath": "Shows complete path of currently displayed folder",
    #    "Container.FolderName": "Shows top most folder in currently displayed folder",
    #    "Container.Content": "Shows content of the current container",
    
    
    def gather_data(self):
        if xbmc.getCondVisibility("Window.IsActive(busydialog)"):
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            xbmc.sleep(800)
    #        xbmc.executebuiltin("Container.Refresh") 
    
    #    win = xbmcgui.Window(10000)
        windowID = xbmcgui.getCurrentWindowId()
        currwin = xbmcgui.Window(windowID)
        container = xbmc.getInfoLabel('System.CurrentControlID')
        
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
        
    
            z = videoInfoTag.getActors()
            content = content + "<tr><td>getActors()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getActors() :' + str(z) + "\n"
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
            z = videoInfoTag.getDirectors()
            content = content + "<tr><td>getDirectors()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getDirectors() :' + str(z) + "\n"
            z = videoInfoTag.getDuration()
            content = content + "<tr><td>getDuration()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getDuration() :' + str(z) + "\n"
            z = videoInfoTag.getEpisode()
            content = content + "<tr><td>getEpisode()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getEpisode() :' + str(z) + "\n"
            z = videoInfoTag.getFile()
            content = content + "<tr><td>getFile()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getFile() :' + str(z) + "\n"
            z = videoInfoTag.getFilenameAndPath()
            content = content + "<tr><td>getFilenameAndPath()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getFilenameAndPath() :' + str(z) + "\n"
            z = videoInfoTag.getFirstAired()
            content = content + "<tr><td>getFirstAired()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getFirstAired() :' + str(z) + "\n"
            z = videoInfoTag.getFirstAiredAsW3C()
            content = content + "<tr><td>getFirstAiredAsW3C()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getFirstAiredAsW3C() :' + str(z) + "\n"
            z = videoInfoTag.getGenre()
            content = content + "<tr><td>getGenre()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getGenre() :' + str(z) + "\n"
            z = videoInfoTag.getGenres()
            content = content + "<tr><td>getGenres()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getGenres() :' + str(z) + "\n"
            z = videoInfoTag.getIMDBNumber()
            content = content + "<tr><td>getIMDBNumber()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getIMDBNumber() :' + str(z) + "\n"
            z = videoInfoTag.getLastPlayed()
            content = content + "<tr><td>getLastPlayed()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getLastPlayed() :' + str(z) + "\n"
            z = videoInfoTag.getLastPlayedAsW3C()
            content = content + "<tr><td>getLastPlayedAsW3C()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getLastPlayedAsW3C() :' + str(z) + "\n"
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
            z = videoInfoTag.getPremieredAsW3C()
            content = content + "<tr><td>getPremieredAsW3C()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getPremieredAsW3C() :' + str(z) + "\n"
            z = videoInfoTag.getRating('imdb')
            content = content + "<tr><td>getRating('imdb')</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + "getRating(imdb') :" + str(z) + "\n"
            z = videoInfoTag.getRating('tvdb')
            content = content + "<tr><td>getRating('tvdb')</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + "getRating('tvdb') :" + str(z) + "\n"
            z = videoInfoTag.getRating('tmdb')
            content = content + "<tr><td>getRating('tmdb')</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + "getRating('tmdb') :" + str(z) + "\n"
            z = videoInfoTag.getRating('anidb')
            content = content + "<tr><td>getRating('anidb')</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + "getRating('anidb') :" + str(z) + "\n"
            z = videoInfoTag.getResumeTime()
            content = content + "<tr><td>getResumeTime()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getResumeTime() :' + str(z) + "\n"
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
            z = videoInfoTag.getTrailer()
            content = content + "<tr><td>getTrailer()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getTrailer() :' + str(z) + "\n"
            z = videoInfoTag.getTVShowTitle()
            content = content + "<tr><td>getTVShowTitle()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getTVShowTitle() :' + str(z) + "\n"
            z = videoInfoTag.getUniqueID('imdb')
            content = content + "<tr><td>getUniqueID('imdb')</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + "getUniqueID('imdb') :" + str(z) + "\n"
            z = videoInfoTag.getUniqueID('tvdb')
            content = content + "<tr><td>getUniqueID('tvdb')</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + "getUniqueID('tvdb') :" + str(z) + "\n"
            z = videoInfoTag.getUniqueID('tmdb')
            content = content + "<tr><td>getUniqueID('tmdb')</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + "getUniqueID('tmdb') :" + str(z) + "\n"
            z = videoInfoTag.getUniqueID('anidb')
            content = content + "<tr><td>getUniqueID('anidb')</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + "getUniqueID('anidb') :" + str(z) + "\n"
            z = videoInfoTag.getUserRating()
            content = content + "<tr><td>getUserRating()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getUserRating() :' + str(z) + "\n"
            z = videoInfoTag.getVotes()
            content = content + "<tr><td>getVotes()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getVotes() :' + str(z) + "\n"
            z = videoInfoTag.getVotesAsInt()
            content = content + "<tr><td>getVotesAsInt()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getVotesAsInt() :' + str(z) + "\n"
            z = videoInfoTag.getWriters()
            content = content + "<tr><td>getWriters()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getWriters() :' + str(z) + "\n"
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
            z = musicinfo.getLastPlayedAsW3C()
            content = content + "<tr><td>getLastPlayedAsW3C()</td><td>" + str(z) + '</td></tr>' + "\n"
            content_txt = content_txt + 'getLastPlayedAsW3C() :' + str(z) + "\n"
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
        
        content = content + divider + '<table border=1><tr><td colspan=2><h1>xbmc.getInfoLabel :</h1></td></tr>'  + "\n"
        content_txt = content_txt + divider_txt + 'xbmc.getInfoLabel :' + "\n"
        
        for key, value in outlist :
            
            key = re.sub(r"Container\(id\)", "Container(" + container + ")", key)
            
            lookup = xbmc.getInfoLabel(key)
            
            
            if lookup is not None and lookup != "" and lookup != key:
                xbmcresult = xbmc.getInfoLabel(key)
                xbmcresult_txt = xbmcresult
                x = re.search("^http", xbmcresult)
                if x and key != 'ListItem.Path' and key != 'ListItem.FileNameAndPath':
                    xbmcresult = xbmcresult + '<img src="' + xbmcresult + '" height=200>'     
                
                content = content + '<tr><td>' + key + '</td><td>' + xbmcresult + '</td>' + '<td>' + value + '</td></tr>' + "\n"
                content_txt = content_txt + key + ' : ' + xbmcresult_txt + ' : ' + value + "\n"
    
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



