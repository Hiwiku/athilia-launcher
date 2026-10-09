###
## Start web window and WebUI
###

from src.launcher.backend import backend
from src.launcher.web_view import webview

def start_ui():
    #Start backend
    backend.start_backend()
    #Start webview and open web page
    webview.start_webview()
