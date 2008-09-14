import pygtk
pygtk.require('2.0')
import gtk

class GUI(object):
    def __init__(self, app):
        self.app = app

        self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.main_window.connect('delete_event', self.delete_event)
        self.main_window.connect('destroy', self.destroy)
        self.main_window.set_default_size(640, 480)
        self.main_window.set_title(u'Chavier')

        vbox = gtk.VBox()
        self.main_window.add(vbox)
        vbox.show()

        menubar, toolbar = self._create_ui_manager()

        vbox.pack_start(menubar, False, False)
        menubar.show()

        vbox.pack_start(toolbar, False, False)
        toolbar.show()

        hpaned = gtk.HPaned()
        vbox.pack_start(hpaned, True, True)
        hpaned.show()

        vpaned = gtk.VPaned()
        hpaned.add1(vpaned)
        vpaned.show()

        block1 = self._create_sidebar_block(u'Data sets',
                                            self._datasets_notebook_creator)
        hbuttons = self._create_datasets_buttons()
        block1.pack_start(hbuttons, False, False)
        hbuttons.show()

        vpaned.add1(block1)
        block1.show()

        block2 = self._create_sidebar_block(u'Options',
                                            self._options_treeview_creator)
        vpaned.add2(block2)
        block2.show()

        drawing_area = gtk.DrawingArea()
        hpaned.add2(drawing_area)
        drawing_area.show()

        self.main_window.show()

    def _create_ui_manager(self):
        uimanager = gtk.UIManager()
        accel_group = uimanager.get_accel_group()
        self.main_window.add_accel_group(accel_group)

        action_group = gtk.ActionGroup('default')
        action_group.add_actions([
                ('file', None, '_File', None, 'File', None),
                ('quit', gtk.STOCK_QUIT, '_Quit', None, 'Quit the program',
                 self.quit),
                ('view', None, '_View', None, 'View', None),
                ('refresh', gtk.STOCK_REFRESH, '_Refresh', None, 'Update the chart',
                 self.refresh),
                ])
        uimanager.insert_action_group(action_group, -1)

        ui = """<ui>
  <menubar name="MenuBar">
    <menu action="file">
      <menuitem action="quit"/>
    </menu>
    <menu action="view">
      <menuitem action="refresh"/>
    </menu>
  </menubar>
  <toolbar name="ToolBar">
    <toolitem action="refresh"/>
  </toolbar>
</ui>
"""
        uimanager.add_ui_from_string(ui)
        uimanager.ensure_update()
        menubar = uimanager.get_widget('/MenuBar')
        toolbar = uimanager.get_widget('/ToolBar')

        return menubar, toolbar

    def _create_sidebar_block(self, title, child_widget_creator):
        box = gtk.VBox(spacing=6)
        box.set_border_width(6)
        label = gtk.Label()
        label.set_markup(u'<span size="large" weight="bold">%s</span>' % title)
        label.set_alignment(0.0, 0.5)
        box.pack_start(label, False, False)
        label.show()

        child_widget = child_widget_creator()
        box.pack_start(child_widget, True, True)
        child_widget.show()

        return box

    def _datasets_notebook_creator(self):
        self.datasets_notebook = gtk.Notebook()
        self.datasets_notebook.set_scrollable(True)
        return self.datasets_notebook

    def _create_datasets_buttons(self):
        hbuttons = gtk.HButtonBox()
        hbuttons.set_layout(gtk.BUTTONBOX_END)

        add_button = gtk.Button(stock=gtk.STOCK_ADD)
        add_button.connect('clicked', self.add_dataset)
        hbuttons.pack_start(add_button, False, False)
        add_button.show()

        remove_button = gtk.Button(stock=gtk.STOCK_REMOVE)
        hbuttons.pack_start(remove_button, False, False)
        remove_button.show()
        remove_button.set_sensitive(False)

        return hbuttons

    def _dataset_treeview_creator(self):
        store = gtk.ListStore(float, float)
        treeview = gtk.TreeView(store)

        column1 = gtk.TreeViewColumn('x', gtk.CellRendererText(), text=0)
        treeview.append_column(column1)

        column2 = gtk.TreeViewColumn('y', gtk.CellRendererText(), text=1)
        treeview.append_column(column2)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrolled_window.add(treeview)
        treeview.show()

        return scrolled_window

    def _options_treeview_creator(self):
        self.options_store = gtk.TreeStore(str, str)
        options = self.app.get_default_options()
        self._fill_options_store(options, None)

        treeview = gtk.TreeView(self.options_store)

        column1 = gtk.TreeViewColumn('Name', gtk.CellRendererText(), text=0)
        treeview.append_column(column1)

        column2 = gtk.TreeViewColumn('Value', gtk.CellRendererText(), text=1)
        treeview.append_column(column2)

        treeview.expand_all()

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrolled_window.add(treeview)
        treeview.show()

        return scrolled_window

    def _fill_options_store(self, options, parent_node):
        for name, value in options.items():
            if isinstance(value, dict):
                current_parent = self.options_store.append(parent_node, (name, None))
                self._fill_options_store(value, current_parent)

            else:
                if value is not None:
                    value = str(value)
                self.options_store.append(parent_node, (name, value))

    def run(self):
        gtk.main()

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def quit(self, action):
        self.main_window.destroy()

    def add_dataset(self, button, data=None):
        n_pages = self.datasets_notebook.get_n_pages()
        suggested_name = u'Dataset %d' % (n_pages + 1)
        dialog = TextInputDialog(self.main_window, suggested_name)
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            name = dialog.get_name()
            scrolled_window = self._dataset_treeview_creator()
            scrolled_window.show()
            label = gtk.Label(name)
            self.datasets_notebook.append_page(scrolled_window, label)
        dialog.destroy()

    def refresh(self, action):
        pass

class TextInputDialog(gtk.Dialog):

    def __init__(self, toplevel_window, suggested_name):
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                   gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
        super(TextInputDialog, self).__init__(u'Enter a name for the dataset',
                                              toplevel_window, flags, buttons)
        self.set_default_size(300, -1)

        hbox = gtk.HBox(spacing=6)
        hbox.set_border_width(12)

        label = gtk.Label(u'Name')
        hbox.pack_start(label, False, False)

        self.entry = gtk.Entry()
        self.entry.set_text(suggested_name)
        self.entry.set_activates_default(True)
        hbox.pack_start(self.entry, True, True)

        self.vbox.pack_start(hbox, False, False)

        self.vbox.show_all()

        self.set_default_response(gtk.RESPONSE_ACCEPT)

    def get_name(self):
        return self.entry.get_text()
