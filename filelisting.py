#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, stat, time

import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from model import FileListModel


class GenericTreeModelExample:
    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()
        return False
 
    def __init__(self):
        # Create a new window
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
 
        self.window.set_size_request(300, 200)
 
        self.window.connect("delete_event", self.delete_event)
 
        self.listmodel = FileListModel()
 
        # create the TreeView
        self.treeview = Gtk.TreeView()
 
        # create the TreeViewColumns to display the data
        column_names = self.listmodel.get_column_names()
        self.tvcolumn = [None] * len(column_names)
        cellpb = Gtk.CellRendererPixbuf()
        self.tvcolumn[0] = Gtk.TreeViewColumn(column_names[0],
                                              cellpb, pixbuf=0)
        cell = Gtk.CellRendererText()
        self.tvcolumn[0].pack_start(cell, False)
        self.tvcolumn[0].add_attribute(cell, 'text', 1)
        self.treeview.append_column(self.tvcolumn[0])
        for n in range(1, len(column_names)):
            cell = Gtk.CellRendererText()
            if n == 1:
                cell.set_property('xalign', 1.0)
            self.tvcolumn[n] = Gtk.TreeViewColumn(column_names[n],
                                                  cell, text=n+1)
            self.treeview.append_column(self.tvcolumn[n])

        self.treeview.connect('row-activated', self.open_file)
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.add(self.treeview)
        self.window.add(self.scrolledwindow)
        self.treeview.set_model(self.listmodel)
        self.window.set_title(self.listmodel.dirname)
        self.window.show_all()

    def open_file(self, treeview, path, column):
        model = treeview.get_model()
        if model.is_folder(path):
            pathname = model.get_pathname(path)
            new_model = FileListModel(pathname)
            self.window.set_title(new_model.dirname)
            treeview.set_model(new_model)
        return
 
def main():
    Gtk.main()

if __name__ == "__main__":
    gtmexample = GenericTreeModelExample()
    main()
