import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import sys, re, os
import socketserver
import json
from genreport import *

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ID = ADDON.getAddonInfo("id")

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
#        global thisreport
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        output = 'HTTP/1.0 200 OK\n'
        output = output + 'Content-Type: text/html\n'
        output = output + "\n"
        
#        thisreport = report()
#        thisreport.gather_data()
        
        
        
        profilePath = xbmcvfs.translatePath( ADDON.getAddonInfo('profile') )
        file = os.path.join(profilePath, 'index.html')
        with xbmcvfs.File(file) as data:
            content = data.read()

        output = output + content
        bytes = output.encode(encoding='UTF-8')
        self.request.sendall(bytes)


if __name__ == '__main__':
    monitor = xbmc.Monitor()
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()

        while not monitor.abortRequested():
             # Sleep/wait for abort for 10 seconds
             if monitor.waitForAbort(10):
                # Abort was requested while waiting. We should exit
                server.shutdown()
                break        
                
    

            