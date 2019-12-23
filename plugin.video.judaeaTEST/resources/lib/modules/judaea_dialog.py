# -*- coding: utf-8 -*-

import os

from resources.lib.modules import control

class Dialog(control.dialogWindow):

    def __init__(self):
        self.closed = False
        self.window_width = (1280 / 2)
        self.window_height = (720 / 2)
        logo_x = self.window_width - 40
        logo_y = self.window_height - 165
        logo_path = control.JUDAEA_LOGO_PATH
        self.list_item = None

        texture_path = os.path.join(control.IMAGES_PATH, 'texture.png')

        background = control.imageControl(0, 0, 1280, 720, texture_path)
        self.addControl(background)
        background_diffuse = '0x0FFFFFFF'
        background.setColorDiffuse(background_diffuse)

        texture = control.imageControl((self.window_width / 2) + 10, self.window_height / 2 ,
                                     self.window_width, self.window_height, texture_path)
        self.addControl(texture)

        logo = control.imageControl(logo_x, logo_y, 50, 80 / 2, logo_path)
        self.addControl(logo)

    def onAction(self, action):

        id = action.getId()
        if id == 92 or id == 10:
            self.close_dialog()
            self.close_dialog()

        if id == 7:
            self.close_dialog()

        if id == 0:
            pass

    def close_dialog(self):
        control.closeBusyDialog()
        self.closed = True
        self.close()
