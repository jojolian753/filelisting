# -*- coding: utf-8 -*-

import os, stat, time

import gi; gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf


folderpb = GdkPixbuf.Pixbuf.new_from_file_at_size('folder.png', 16, 16)
filepb = GdkPixbuf.Pixbuf.new_from_file_at_size('note.png', 16, 16)


class FileListModel(GObject.Object, Gtk.TreeModel):
    column_types = (GdkPixbuf.Pixbuf, str, long, str, str)
    column_names = ['Name', 'Size', 'Mode', 'Last Changed']

    def __init__(self, dname=None):
        super(FileListModel, self).__init__()
        if not dname:
            self.dirname = os.path.expanduser('~')
        else:
            self.dirname = os.path.abspath(dname)
        self.files = [f for f in os.listdir(self.dirname) if f[0] <> '.']
        self.files.sort()
        self.files = ['..'] + self.files
        return

    def get_pathname(self, path):
        filename = self.files[path[0]]
        return os.path.join(self.dirname, filename)

    def is_folder(self, path):
        filename = self.files[path[0]]
        pathname = os.path.join(self.dirname, filename)
        filestat = os.stat(pathname)
        if stat.S_ISDIR(filestat.st_mode):
            return True
        return False

    def get_column_names(self):
        return self.column_names[:]

    def do_get_flags(self):
        return Gtk.TreeModelFlags.LIST_ONLY|Gtk.TreeModelFlags.ITERS_PERSIST

    def do_get_n_columns(self):
        return len(self.column_types)

    def do_get_column_type(self, n):
        return self.column_types[n]

    def do_get_iter(self, path):
        idx = list(path)[0]
        print("get_iter works")
        return self.files[idx]

    def do_get_path(self, rowref):
        return self.files.index(rowref)

    def do_get_value(self, rowref, column):
        fname = os.path.join(self.dirname, rowref)
        try:
            filestat = os.stat(fname)
        except OSError:
            return None
        mode = filestat.st_mode
        if column is 0:
            if stat.S_ISDIR(mode):
                return folderpb
            else:
                return filepb
        elif column is 1:
            return rowref
        elif column is 2:
            return filestat.st_size
        elif column is 3:
            return oct(stat.S_IMODE(mode))
        return time.ctime(filestat.st_mtime)

    def do_iter_next(self, rowref):
        try:
            i = self.files.index(rowref)+1
            return self.files[i]
        except IndexError:
            return None
        except ValueError as exc:
            print(exc)
            Gtk.main_quit()

    def do_iter_children(self, rowref, parent_iter):
        if rowref:
            return None
        return self.files[0]

    def do_iter_has_child(self, rowref):
        return False

    def do_iter_n_children(self, rowref):
        if rowref:
            return 0
        return len(self.files)

    def do_iter_nth_child(self, rowref, parent_iter, n):
        if rowref:
            return None
        try:
            return self.files[n]
        except IndexError:
            return None

    def do_iter_parent(child):
        return None

