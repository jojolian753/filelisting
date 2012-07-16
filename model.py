# -*- coding: utf-8 -*-

import os, stat, time
from os import path

import gi; gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf


folderpb = GdkPixbuf.Pixbuf.new_from_file_at_size('folder.png', 16, 16)
filepb = GdkPixbuf.Pixbuf.new_from_file_at_size('note.png', 16, 16)


class FileListModel(GObject.Object, Gtk.TreeModel):
    column_types = (GdkPixbuf.Pixbuf, str, long, str, str)
    column_names = ['Name', 'Size', 'Mode', 'Last Changed']

    def __init__(self, dname=None):
        super(FileListModel, self).__init__()

        self.myiter = Gtk.TreeIter()
        self.myiter.stamp = 4

        if dname:
            self.dirname = os.path.abspath(dname)
        else:
            self.dirname = os.path.expanduser('~')

        self.files = os.listdir(self.dirname)
        self.files.sort()
        self.files.insert(0, '..')

    # code to refactor out
    def get_pathname(self, path):
        filename = self.files[list(path)[0]]
        return path.join(self.dirname, filename)

    def is_folder(self, path):
        filename = self.files[list(path)[0]]
        pathname = path.join(self.dirname, filename)

        return path.isdir(pathname)

    def get_column_names(self):
        return self.column_names[:]

    # Signals
    def do_row_changed(self, tree_path, tree_iter):
        pass

    def do_row_inserted(self, tree_path, tree_iter):
        pass

    def do_row_has_child_toggled(self, tree_path, tree_iter):
        pass

    def do_row_deleted(self, tree_path):
        pass

    def do_get_flags(self):
        return Gtk.TreeModelFlags.LIST_ONLY|Gtk.TreeModelFlags.ITERS_PERSIST

    def do_get_n_columns(self):
        return len(self.column_types)

    def do_get_column_type(self, n):
        return self.column_types[n]

    def do_get_iter(self, tree_path):
        idx = list(tree_path)[0]
        print("get_iter: idx is {0}".format(idx))

        stamp = hash(self.files[idx]) >> 24
        print("stamp is {0}".format(stamp))

        self.myiter.user_data = self.files[idx]
        self.myiter.stamp = stamp
        print("get_iter: user_data is {0}".format(self.myiter.user_data))

        return self.myiter

    def do_get_path(self, rowref):
        return self.files.index(rowref.user_data)

    def do_get_value(self, rowref, column):
        fname = os.path.join(self.dirname, rowref.user_data)
        try:
            filestat = os.stat(fname)
        except OSError:
            return None

        if column is 0:
            if path.isdir(fname):
                return folderpb
            else:
                return filepb
        elif column is 1:
            return rowref.user_data
        elif column is 2:
            return filestat.st_size
        elif column is 3:
            return oct(stat.S_IMODE(mode))
        return time.ctime(filestat.st_mtime)

    def do_iter_next(self, rowref):
        print
        print('stamp is:\n{0}'.format(rowref.stamp))
        print('user_data is:\n{0}'.format(rowref.user_data))
        print('user_data2 is:\n{0}'.format(rowref.user_data2))
        print('user_data3 is:\n{0}'.format(rowref.user_data3))
        print
        try:
            i = self.files.index(rowref.user_data)+1
        except (TypeError, IndexError, ValueError) as exc:
            print(exc)
            return None
        else:
            return (True, self.files[i])

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

