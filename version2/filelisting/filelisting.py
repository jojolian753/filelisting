#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, stat, time

import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

from view import FileListView


class FileListApp(Gtk.Application):
    def __init__(self):
        super(FileListApp, self).__init__(
            application_id="apps.nassimian.filelisting",
            flags=Gio.ApplicationFlags.FLAGS_NONE
        )

        self.connect("activate", self.on_activate)


    def on_activate(self, data=None):
        self.treeview = FileListView(column_idx=(1, 3, 2))
        self.treeview.connect('dir-changed', self.on_dir_changed)

        # Create a new window
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_size_request(300, 200)
        window.connect("destroy", Gtk.main_quit)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.add(self.treeview)
        window.add(scrolledwindow)
        window.set_title(self.treeview.get_model().dirname)
        window.set_application(self)
        window.show_all()


    def on_dir_changed(self, treeview, dirname):
        self.get_windows()[0].set_title(dirname)


def main(*args):
    app = FileListApp()
    app.run(args)


if __name__ == "__main__":
    sys.exit(main(*sys.argv))
