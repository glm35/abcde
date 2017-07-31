#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
import tkinter as tk
import tkinter.messagebox as tk_messagebox

import file
import ui.edit_zone
import ui.theme


class RootWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self._theme = ui.theme.Theme()
        self._edit_zone = ui.edit_zone.EditZone(self, self._theme)
        self._file = file.File(self, self._edit_zone._edit_zone)  # TODO: revoir les accesseurs
        self._file.set_root_title()
        self._edit_zone.set_check_text_change_since_last_save_cb(self._file.check_text_change_since_last_save)

        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='New', underline=0, accelerator='Ctrl + N', command=self._file.new)
        file_menu.add_command(label='Open...', underline=0, accelerator='Ctrl + O', command=self._file.open)
        file_menu.add_command(label='Save', underline=0, accelerator='Ctrl + S', command=self._file.save)
        file_menu.add_command(label='Save as...', underline=3, command=self._file.save_as)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', underline=0, accelerator='Alt + F4', command=self.exit)
        menu_bar.add_cascade(label='File', underline=0, menu=file_menu)

        self.config(menu=menu_bar)

        self.bind('<Control-N>', self._file.new)
        self.bind('<Control-n>', self._file.new)
        self.bind('<Control-O>', self._file.open)
        self.bind('<Control-o>', self._file.open)
        self.bind('<Control-S>', self._file.save)
        self.bind('<Control-s>', self._file.save)
        self.bind('Alt-Keypress-F4', self.exit)

        self.protocol('WM_DELETE_WINDOW', self.exit)

    def maximize(self):
        """Maximize the root window"""
        root_w, root_h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (root_w, root_h))

    def exit(self, event=None):
        log.debug('RootWindow.exit()')
        # TODO: proposer d'enregistrer le fichier si modifié
        if tk_messagebox.askokcancel('Quit?', 'Really quit?'):
            self.destroy()