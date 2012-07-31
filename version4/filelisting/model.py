# -*- coding: utf-8 -*-

import os, stat, time
from os import path

import gi; gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GdkPixbuf


folderpb = GdkPixbuf.Pixbuf.new_from_file_at_size('res/folder.png', 16, 16)
filepb = GdkPixbuf.Pixbuf.new_from_file_at_size('res/note.png', 16, 16)


class ListingOptions(object):
    DEFAULT = 0
    SHOW_PARENT = 1
    HIDE_FILES = 2
    MIX_FOLDERS_FILES = 4
    NO_SORT = 8


class FileListModel(GObject.Object, Gtk.TreeModel):
    __gsignals__ = {
        "filelist-mode-set": (GObject.SignalFlags.RUN_FIRST, None, (int,)),
    }

    column_types = (GdkPixbuf.Pixbuf, str, long, str, str)
    column_names = ['Name', 'Size', 'Mode', 'Last Changed']

    def __init__(self, dname=None, mode_code=0):
        super(FileListModel, self).__init__()

        if dname:
            self.dirname = os.path.abspath(dname)
        else:
            self.dirname = os.path.expanduser('~')

        self.fs_iter = os.walk(self.dirname)
        self.walk_res = self.fs_iter.next()
        self.set_filelist_mode(mode_code)
        self.files = None
        self.set_filelist_mode(mode_code)

    def get_pathname(self, tree_path):
        filename = self.files[tree_path.get_indices()[0]]
        res = path.join(self.dirname, filename)

        return res

    def is_folder(self, tree_path):
        filename = self.files[tree_path.get_indices()[0]]
        pathname = path.join(self.dirname, filename)

        return path.isdir(pathname)

    def get_column_names(self):
        return self.column_names[:]

    def set_filelist_mode(self, mode_code=0):
        def sort(list1, list2, mixed):
            if mixed:
                return sorted(list1 + list2)
            else:
                return sorted(list1) + sorted(list2)

        list1 = self.walk_res[1]

        if ListingOptions.HIDE_FILES & mode_code:
            list2 = []
        else:
            list2 = self.walk_res[2]

        if ListingOptions.NO_SORT & mode_code:
            self.files = list1 + list2
        else:
            self.files = sort(
                list1, list2,
                ListingOptions.MIX_FOLDERS_FILES & mode_code
            )

        if ListingOptions.SHOW_PARENT & mode_code:
            self.files.insert(0, '..')

        self.emit("filelist-mode-set", mode_code)

    # -------------------------------------------------------------------------
    # Interface implementation
    def do_get_flags(self):
        return Gtk.TreeModelFlags.LIST_ONLY|Gtk.TreeModelFlags.ITERS_PERSIST

    def do_get_n_columns(self):
        return len(self.column_types)

    def do_get_column_type(self, n):
        return self.column_types[n]

    def do_get_iter(self, tree_path):
        idx = tree_path.get_indices()[0]

        aiter = Gtk.TreeIter()
        stamp = 4

        aiter.user_data = self.files[idx]
        aiter.stamp = stamp

        return (True, aiter)

    def do_get_path(self, rowref):
#        try:
        res = Gtk.TreePath((self.files.index(rowref.user_data),))
#        except ValueError:
#            res = Gtk.TreePath((0,))
        return res

    def do_get_value(self, rowref, column):
        bname = rowref.user_data
        fname = path.join(self.dirname, bname)
        try:
            filestat = os.stat(fname)
        except OSError as exc:
            print("get_value: file not found!\n\n{0}".format(exc))

            return None
        mode = filestat.st_mode
        if column is 0:
            if stat.S_ISDIR(mode):
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
        i = self.files.index(rowref.user_data)+1
        try:
            rowref.user_data = self.files[i]
        except IndexError:
            rowref.stamp = -1
            return (False, rowref)
        except (TypeError, ValueError) as exc:
            print(exc)
            rowref.stamp = -1
            return (False, rowref)
        else:
            return (True, rowref)

    def do_iter_children(self, rowref, parent_iter):
        print("iter_children: function")
        if rowref.user_data:
            rowref.user_data = None
            return (False, rowref)
        else:
            rowref.user_data = self.files[0]
            return (True, rowref)

    def do_iter_has_child(self, rowref):
        print("iter_has_child: function")
        return False

    def do_iter_n_children(self, rowref):
        print("iter_n_children: function")
        if rowref.user_data:
            return 0
        return len(self.files)

    def do_iter_nth_child(self, parent_iter, n):
        print("iter_nth_child: function")
        if parent_iter:
            return (False, None)
        try:
            rowref = Gtk.TreeIter()
            rowref.user_data = self.files[n]
            return (True, rowref)
        except IndexError:
            return (False, rowref)

    def do_iter_parent(child):
        print("iter_parent: function")

        return (False, Gtk.TreeIter())
