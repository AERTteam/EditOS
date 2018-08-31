# This imports all that is listed in __init__.py of current directory:
from __init__ import *

# Note: here self is our Window Class (See Objects_Module.py) as this function is invoked by that class
# ie; this function is used in Window Class so here self refers to that class. 
# This Function is used to build up the interface of our Main Window:
def interface(self):
    add_new_option_file_menu(self)
    add_open_option_file_menu(self)
    add_save_option_file_menu(self)
    add_save_as_option_file_menu(self)
    add_print_preview_option_file_menu(self)
    add_print_option_file_menu(self)
    add_exit_option_file_menu(self)
    add_find_option_edit_menu(self)
    add_font_option_view_menu(self)
    add_font_color_option_view_menu(self)
    add_bgcolor_option_view_menu(self)
    add_night_theme_option_view_menu(self)
    add_statusbar_checkbox_view_menu(self)
    add_about_option_help_menu(self)

def add_new_option_file_menu(self):
    new_action = QtGui.QAction("&New", self)
    new_action.setShortcut("Ctrl+N")
    new_action.triggered.connect(self.new_file)               # (for new_file function, see MAIN WINDOW Class in Objects_Module.py)
    new_action.setStatusTip("create a new file")
    self.file_menu.addAction(new_action)

def add_open_option_file_menu(self):
    open_action = QtGui.QAction("&Open", self)
    open_action.setShortcut("Ctrl+O")
    open_action.triggered.connect(self.open_file)               # (for open_file function, see MAIN WINDOW Class in Objects_Module.py)
    open_action.setStatusTip("open a file")
    self.file_menu.addAction(open_action)

def add_save_option_file_menu(self):
    save_action = QtGui.QAction("&Save", self)
    save_action.setShortcut("Ctrl+S")
    save_action.triggered.connect(self.save_file)               # (for save_file function, see MAIN WINDOW Class in Objects_Module.py)
    save_action.setStatusTip("save currently opened file")
    self.file_menu.addAction(save_action)

def add_save_as_option_file_menu(self):
    save_as_action = QtGui.QAction("&Save As", self)
    save_as_action.setShortcut("Ctrl+Shift+S")
    save_as_action.triggered.connect(self.save_as_file)               # (for save_as_file function, see MAIN WINDOW Class in Objects_Module.py)
    save_as_action.setStatusTip("save a file with any extension")
    self.file_menu.addAction(save_as_action)

def add_print_preview_option_file_menu(self):
    print_preview_action = QtGui.QAction("&Print Preview", self)
    print_preview_action.setShortcut("Ctrl+Shift+P")
    print_preview_action.triggered.connect(self.print_preview)               # (for print_preview function, see MAIN WINDOW Class in Objects_Module.py)
    print_preview_action.setStatusTip("preview document before printing")
    self.file_menu.addAction(print_preview_action)

def add_print_option_file_menu(self):
    print_action = QtGui.QAction("&Print", self)
    print_action.setShortcut("Ctrl+P")
    print_action.triggered.connect(self.print_doc)               # (for print_doc function, see MAIN WINDOW Class in Objects_Module.py)
    print_action.setStatusTip("print document")
    self.file_menu.addAction(print_action)

def add_exit_option_file_menu(self):
    exit_action = QtGui.QAction("&Exit", self)
    exit_action.setShortcut("Ctrl+Q")
    exit_action.triggered.connect(self.exit_app)               # (for exit_app function, see MAIN WINDOW Class in Objects_Module.py)
    exit_action.setStatusTip("exit the app")
    self.file_menu.addAction(exit_action)

def add_find_option_edit_menu(self):
    find_action = QtGui.QAction("&Find", self)
    find_action.setShortcut("Ctrl+F")
    find_action.triggered.connect(self.find)               # (for find function, see MAIN WINDOW Class in Objects_Module.py)
    find_action.setStatusTip("find or replace text")
    self.edit_menu.addAction(find_action)

def add_font_option_view_menu(self):
    font_action = QtGui.QAction("&Font", self)
    font_action.triggered.connect(self.get_font_choice)         # (for get_font_choice function, see MAIN WINDOW Class in Objects_Module.py)
    font_action.setStatusTip("customize font")
    self.view_menu.addAction(font_action)

def add_font_color_option_view_menu(self):
    color_action = QtGui.QAction("&Font Color", self)
    color_action.triggered.connect(self.get_font_color)         # (for get_font_color function, see MAIN WINDOW Class in Objects_Module.py)
    color_action.setStatusTip("customize font color")
    self.view_menu.addAction(color_action)

def add_bgcolor_option_view_menu(self):
    bgcolor_action = QtGui.QAction("&Background Color", self)
    bgcolor_action.triggered.connect(self.get_back_color)         # (for get_back_color function, see MAIN WINDOW Class in Objects_Module.py)
    bgcolor_action.setStatusTip("customize background color")
    self.view_menu.addAction(bgcolor_action)

def add_night_theme_option_view_menu(self):
    theme_action = QtGui.QAction("&Night Theme", self, checkable=True)
    theme_action.triggered.connect(self.set_night_theme)         # (for set_night_theme function, see MAIN WINDOW Class in Objects_Module.py)
    theme_action.setStatusTip("apply night theme")
    self.view_menu.addAction(theme_action)
    # Note: settings is an imported variable (see Variables_Module.py)
    if (settings.value("Night_Btn").toString()) == "checked":          # check if this checkbox was toggled last time the window was executed
        theme_action.toggle()                                          # if yes, toggle it.
    else:
        pass

def add_statusbar_checkbox_view_menu(self):
    status_action = QtGui.QAction("&Statusbar", self, checkable=True)
    status_action.triggered.connect(self.add_statusbar)         # (for add_statusbar function, see MAIN WINDOW Class in Objects_Module.py)
    self.view_menu.addAction(status_action)
    # check if this checkbox was toggled last time the window was executed:
    if (settings.value("Status_Btn").toString()) == "unchecked":
        pass
    elif (settings.value("Status_Btn").toString()) == "checked":
        # if yes, then, show the statusbar and toggle it:
        self.statusbar.show() 
        status_action.toggle()
    else:                               # This is just a safety measure for unexpected faults 
        self.statusbar.show()
        status_action.toggle()

def add_about_option_help_menu(self):
    about_action = QtGui.QAction("&About Us", self)
    about_action.triggered.connect(self.about)         # (for about function, see MAIN WINDOW Class in Objects_Module.py)
    self.help_menu.addAction(about_action)