import webview
from glob import glob
import importlib
import os
import json
import tensorflow
import pygame

from ctypes import windll
SetWindowPos = windll.user32.SetWindowPos
user32 = windll.user32

screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
foobar = None

class Api:
    def init(self):
        response = []
        for folder in glob("repos/*"):
            meta_file = folder + "/info.json"
            if not os.path.isfile(meta_file):
                continue

            meta = json.loads(
                open(meta_file, "r").read()
            )
            meta["path"] = folder

            entry = folder + "." + meta["entry"].replace(".py", "")
            meta["entry"] = entry.replace("\\", ".")

            response.append(
                meta
            )
        return response

    def callback(self, foobar):
        pos_x = screen_width // 2 - foobar.WIN_WIDTH // 2
        pos_y = screen_height //2 - foobar.WIN_HEIGHT // 2

        # Pin Window to the top
        SetWindowPos(
            foobar.pygame.display.get_wm_info()['window'], -1, pos_x, pos_y, 0, 0, 0x0001
        )


    def run(self, module):
        foobar = importlib.import_module(module)
        foobar.main(
            lambda: self.callback(foobar)
        )

api = Api()
window = webview.create_window('PoseCamera - Launcher', 'templates/index.html', js_api = api)
webview.start(debug=False)

