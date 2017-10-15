#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
import pathlib
import tkinter as tk
import tkinter.messagebox as tk_messagebox

import file
import ui.edit_zone
import ui.theme


class RootWindow():
    def __init__(self, filename=None):
        self.tk_root = tk.Tk()

        self._theme = ui.theme.Theme()

        self._edit_zone = ui.edit_zone.EditZone(self.tk_root, self._theme)

        self._file = file.File(self, self._edit_zone.get_buffer())
        self._file.set_root_window_title()
        self._edit_zone.set_check_text_change_since_last_save_cb(self._file.check_text_change_since_last_save)
        if filename:
            self._file.open(str(pathlib.Path(filename).absolute()))  # Make sure filename is absolute

        menu_bar = tk.Menu(self.tk_root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='New', underline=0, accelerator='Ctrl + N', command=self._file.on_file_new)
        file_menu.add_command(label='Open...', underline=0, accelerator='Ctrl + O', command=self._file.on_file_open)
        file_menu.add_command(label='Save', underline=0, accelerator='Ctrl + S', command=self._file.on_file_save)
        file_menu.add_command(label='Save as...', underline=3, command=self._file.on_file_save_as)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', underline=0, accelerator='Alt + F4', command=self.exit)
        menu_bar.add_cascade(label='File', underline=0, menu=file_menu)

        self.tk_root.config(menu=menu_bar)

        self.tk_root.bind('<Control-N>', self._file.on_file_new)
        self.tk_root.bind('<Control-n>', self._file.on_file_new)
        self.tk_root.bind('<Control-O>', self._file.on_file_open)
        self.tk_root.bind('<Control-o>', self._file.on_file_open)
        self.tk_root.bind('<Control-S>', self._file.on_file_save)
        self.tk_root.bind('<Control-s>', self._file.on_file_save)
        self.tk_root.bind('Alt-Keypress-F4', self.exit)

        self.tk_root.protocol('WM_DELETE_WINDOW', self.exit)

    def maximize(self):
        """Maximize the root window"""
        root_w, root_h = self.tk_root.winfo_screenwidth(), self.tk_root.winfo_screenheight()
        self.tk_root.geometry("%dx%d+0+0" % (root_w, root_h))

    def exit(self, event=None):
        log.debug('RootWindow.exit()')

        if self._file.ask_save_changes() == 'cancel':
            log.debug('RootWindow.exit(): ask save changes cancelled/failed, aborting')
            return 'break'
        elif tk_messagebox.askokcancel('Quit?', 'Really quit?'):
            self.tk_root.destroy()

    def set_title(self, filename, modified_flag):
        """Set the title of the root window

        The title shows the name of the file being edited, and a star '*'
        if the file has been modified in the editor since its last save on disk.

        Args:
            filename (str): string representation of the filename
            modified_flag (bool): whether the file has been modified

        Returns:
            None
        """

        modified_flag_str = '* ' if modified_flag else ''
        self.tk_root.title(modified_flag_str + filename)
