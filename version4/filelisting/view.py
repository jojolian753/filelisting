# -*- coding: utf-8 -*-

from gi.repository import GObject, Gtk

from model import FileListModel


class FileListView(Gtk.TreeView):

    __gsignals__ = {
        'dir-activated': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        'file-activated': (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }

    def __init__(self, list_model=None, column_idx=()):
        if list_model is None:
            list_model = FileListModel()
        super(FileListView, self).__init__(list_model)

        # create the TreeViewColumns to display the data
        column_names = list_model.get_column_names()
        tvcolumn = []

        cellpb = Gtk.CellRendererPixbuf()
        tvcolumn.append(Gtk.TreeViewColumn(column_names[0], cellpb, pixbuf=0))

        cell = Gtk.CellRendererText()
        tvcolumn[0].pack_start(cell, False)
        tvcolumn[0].add_attribute(cell, 'text', column_names.index("Name") + 1)

        self.append_column(tvcolumn[0])

        if not column_idx:
            column_idx = range(1, len(column_names))
        for n in column_idx:
            cell = Gtk.CellRendererText()
            if n == 1:
                cell.set_property('xalign', 1.0)

            tvcolumn.append(Gtk.TreeViewColumn(
                column_names[n],
                cell, text=n+1
            ))

            self.append_column(tvcolumn[-1])

    def do_row_activated(self, tree_path, column):
        model = self.get_model()
        pathname = model.get_pathname(tree_path)
        if model.is_folder(tree_path):
            new_model = FileListModel(pathname)
            self.set_model(new_model)
            self.emit("dir-activated", new_model.dirname)
        else:
            self.emit("file-activated", pathname)
