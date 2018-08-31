# This imports all that is listed in __init__.py of current directory:
from __init__ import *

#-------------------------------------------------------------------------------------- MAIN WINDOW CLASS ----------------------------------------------------------------------------------#
class Window(QtGui.QMainWindow):                    # defines a subclass of QMainWindow named Window
    
    # This method defines everything that is to be executed automatically when the class is initialized:
    def __init__(self):
        super(Window, self).__init__() # This makes the class inherit functions from its upper class (Here, QMainWindow Class).
        
        #---------------------------------- RESTORING THE LAST SETTINGS --------------------------------#
        # Note: settings is an imported variable (see Variables_Module.py)

        if settings.value("Runs").isNull():             # if a value named Runs does not exist in settings (this is the first time the code is run)
            # then, set these custom values as the x, y positions and height, width of the Window class:
            # Note: QRect converts integer values into a rectangle form which can be used to visualize a window:
            self.setGeometry(QtCore.QRect(50, 50, 800, 450))
        else:
            self.restore_last_settings_MWindow()                     # restore the last settings...
        
        self.setWindowTitle("EditOS")
        self.setWindowIcon(QtGui.QIcon("Icons/Icon.ico")) # sets the icon to the icon present in icons folder of current directory...
        self.initialize_editor() # (for initialize_editor, see __init__ RELATED FUNCTIONS in Objects_Module.py)
        
        #--------------------------------- MENU BAR CONFIGURATION ---------------------------------------#
        # Here, we add a menubar using the built-in .menuBar() function of QMainWindow class in PyQt and store it in self.main_menu variable for future use:
        self.main_menu = self.menuBar()
        self.file_menu = self.main_menu.addMenu("&File")
        self.edit_menu = self.main_menu.addMenu("&Edit")
        self.view_menu = self.main_menu.addMenu("&View")
        self.help_menu = self.main_menu.addMenu("&Help")
        # Here, we add a statusbar using the built-in .statusBar() function of QMainWindow class in PyQt and store it in self.statusbar variable for future use:
        self.statusbar = self.statusBar()
        self.statusbar.hide() # we hide it currently so that it can be invoked by our statusbar option in view menu (see Functions_Modules.py for details)
        
        #------------------------------- FINAL TOUCHES TO THE WINDOW --------------------------------------#
        # Here, we add a style named cleanlooks using QStyleFactory and set that style to our QApplication:
        # Note: Qt has a number of built-in styles with names such as plastique, cleanlooks, motif, windows vista, cde etc.
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
        self.show()
    
    #-------------------------------------------------------------- __init__ RELATED FUNCTIONS ------------------------------------------------------------------------#
    def restore_last_settings_MWindow(self):
        if (settings.value("Runs").toInt()) >= 1:                           # check if the number of runs is equal to or greater than 1:
            
            if (settings.value("State").toString()) == "Maximized": # if yes, check the settings if the last time window was maximized
                # then, set these custom values as the x, y positions and height, width of the Window class and maximize the window:
                # Note: QRect converts integer values into a rectangle form which can be used to visualize a window:
                self.setGeometry(QtCore.QRect(50, 50, 800, 450))
                self.showMaximized()
            else:
                # if no, last time the window was not maximized,
                # then set the position and size of the window according to the last values present in the settings named Geometry:
                # Note: .toSize and .toPoint converts the values in settings to QSize and QPoint
                # Which are compatible values to be used for moving and resizing the main window.
                self.resize(settings.value("Main_Size").toSize())
                self.move(settings.value("Main_Position").toPoint())

        else:   # the else command is just a safety measure for any unexpected exceptions or falts...
            self.setGeometry(QtCore.QRect(50, 50, 800, 450))
    
    
    
    
    def initialize_editor(self):
        #-------------------------------- SETTING THE DEFAULT SETTINGS (EDITOR WINDOW) ---------------------------------------#
        self.text_editor = QtGui.QPlainTextEdit() # QPlainTextEdit gives us that big bald white space we call editor.
        tmr = QtGui.QFont("times new roman")
        tmr.setPointSize(16) # set font size to 16pt
        self.text_editor.setFont(tmr)
        # self.back_color and self.font_color hold the background and font colors of our editor
        # They are defaulted to none but we will allow the user to change them later:
        self.back_color = "none"
        self.font_color = "none"
        # sets the default stylesheet of our editor using css. it has no border, no  background and no font color currently.
        self.text_editor.setStyleSheet("border: none;background: %s;color: %s;" %(self.back_color, self.font_color))
        
        #-------------------------------- RESTORING THE LAST SETTINGS (EDITOR WINDOW) -------------------------------------------#
        # Note: settings is an imported variable (see Variables_Module.py)
        if settings.value("Runs").isNull():             # if a value named Runs does not exist in settings (this is the first time the code is run)
            pass                                             # do nothing.
        else:                                           # else, if a value named Runs does exist (this is not the first time the code is run)
            # (for restore_last_settings_editor, see SUPPORT FUNCTIONS in Objects_Module.py)
            self.restore_last_settings_editor()                   # restore the last settings of the text editor's window...
        
        #-------------------------------- FINAL TOUCHES TO THE WINDOW (EDITOR WINDOW) -------------------------------------------#
        self.text_editor.cursorPositionChanged.connect(self.position_print) # (for position_print, see SUPPORT FUNCTIONS in Objects_Module.py)
        self.setCentralWidget(self.text_editor) # makes our window a text editor.


    
    #-------------------------------------------------------------- FUNCTIONS FOR MENUBAR OPTIONS-------------------------------------------------------------------------------#
    def new_file(self):
        warning = QtGui.QMessageBox.question(self, "Warning!!!", "Are you sure?\nplease save all work first....", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if warning == QtGui.QMessageBox.Yes:
            self.text_editor.clear()
        else:
            pass
    
    def open_file(self):
        # note: File_Dialog_Window is a team created class (see OTHER WINDOW CLASSES in Objects_Module.py)
        # get the name and location of the file to be opened:
        self.open_file_name = QtGui.QFileDialog.getOpenFileName(File_Dialog_Window(), "Open File", "", ("Text Files (*.txt);;Any File (*.*)"))
        with open(self.open_file_name, "r") as self.current_file:            # open the file in read only mode and as variable self.current_file
            text = self.current_file.read()                        
            self.text_editor.setPlainText(text)                              # set the text in the file as the text in the editor window
        
        self.current_file = open(self.open_file_name, "r+")                  # open file for future purposes
    
    def save_file(self):
        try:                                             # try checking if there is a variable named self.current_file
            self.current_file
        except AttributeError:                           # except, if there is an attribute error (no file was opened).
            self.save_as_file()                          # (for save_as_file function, see below)
        else:                                            # else if everything goes ok (there is a self.current_file variable), then:
            if self.current_file.closed == True:
                self.save_as_file()                      # (for save_as_file function, see below)
            elif self.current_file.closed == False:
                text = self.text_editor.toPlainText()    # get the text currently in the editor...
                try:                                     # try saving the file:
                    self.current_file.write(text)
                except IOError:                          # except, if there is an input output error
                    self.save_as_file()                  # (for save_as_file function, see below)
    
    def save_as_file(self):
        # note: File_Dialog_Window is a team created class (see OTHER WINDOW CLASSES in Objects_Module.py)
        # get the name and location of the file to be saved:
        self.save_file_name = QtGui.QFileDialog.getSaveFileName(File_Dialog_Window(), "Save As File", "Document", ("Text Files (*.txt);;Any File (*.*)"))
        with open(self.save_file_name, "w") as self.current_file:
            text = self.text_editor.toPlainText()                           # get the text currently in the editor...
            self.current_file.write(text)                                   # write the text in the editor to the file
        self.current_file = open(self.save_file_name, "r+")                 # open file for future purposes
    
    def print_preview(self):
        # note: paint_page_view is a team created function, see SUPPORT FUNCTIONS in Objects_Module.py
        print_preview_dialog = QtGui.QPrintPreviewDialog()
        print_preview_dialog.paintRequested.connect(self.paint_page_view)    # whenever print_preview_dialog is created supply current page_view via paint_page_view method...
        print_preview_dialog.exec_()
    
    def print_doc(self):
        print_dialog = QtGui.QPrintDialog()
        print_dialog.exec_()
        if print_dialog.Accepted:                               # if a printer is selected successfully,
            self.text_editor.print_(print_dialog.printer())     # print everything in the text_editor by the printer selected by user in print_dialog
    
    def exit_app(self):
        # note: save_current_settings() is a team created function, see SUPPORT FUNCTIONS in Objects_Module.py
        self.save_current_settings()
        warning = QtGui.QMessageBox.question(self, "Warning!!!", "Are you sure you want to quit?\nplease save all work before closing....", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if warning == QtGui.QMessageBox.Yes:
            try:                                            # try closing the current file:
                self.current_file.close()
            except AttributeError:                          # except, if there is an attribute error (no file was opened).
                QtCore.QCoreApplication.instance().quit()
            else:                                           # else, if self.current_file is sucessfully closed:
                QtCore.QCoreApplication.instance().quit()
        
        else:      # if, No button is clicked:
            pass   # do, nothing.

    def find(self):
        editor = self.text_editor                # allows us to access editor window through a variable named editor
        # note: File_Dialog is a team created class (see OTHER WINDOW CLASSES in Objects_Module.py)
        find_dialog = Find_Dialog(self)
        self.find_dialog = find_dialog           # allows us to access Find_Dialog class through a variable named self.find_dialog
        text = self.text_editor.toPlainText()    # gets the text currently in the editor and stores it in text variable

        def find_text(self):
            # gets the word to be found from the find dialog and stores it in find_word:
            find_word = find_dialog.find_input.text()
            
            # Note: case_sensitive, whole_words_only and direction are all imported variables (see Variables_Module.py)
            # These variables are manipulated from the check boxes in the find dialog window
            # flag contains the settings which makes the find function work.
            if case_sensitive == False and whole_words_only == False and direction == "Backward":
                flag = QtGui.QTextDocument.FindBackward 
            
            elif case_sensitive == True and whole_words_only == False and direction == "Backward":
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively
            
            elif case_sensitive == True and whole_words_only == True and direction == "Backward":
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindCaseSensitively and QtGui.QTextDocument.FindWholeWords
            
            elif case_sensitive == False and whole_words_only == True and direction == "Backward":
                flag = QtGui.QTextDocument.FindBackward and QtGui.QTextDocument.FindWholeWords
            
            elif case_sensitive == False and whole_words_only == False and direction == "Forward":
                flag = QtGui.QTextDocument.FindCaseSensitively
            
            elif case_sensitive == True and whole_words_only == False and direction == "Forward":
                flag = QtGui.QTextDocument.FindCaseSensitively
            
            elif case_sensitive == True and whole_words_only == True and direction == "Forward":
                flag = QtGui.QTextDocument.FindCaseSensitively and QtGui.QTextDocument.FindWholeWords
            
            elif case_sensitive == False and whole_words_only == True and direction == "Forward":
                flag = QtGui.QTextDocument.FindWholeWords
            
            else:
                flag = QtGui.QTextDocument.FindBackward
            
            editor.find(find_word, flag)
        
        def replace_text(self):
            # gets the word to be found from the find dialog and stores it in replace_word:
            replace_word = find_dialog.replace_input.text()
            
            #-------------------------------------------------------------------------#
            #-- when the find button is clicked in the find dialog, if a word is    --#
            #-- found. Then, it is selected automatically and thus, the cursor      --#
            #-- has a selection. However, if no matching word is found the cursor   --#
            #-- will have no selection                                              --#
            #-------------------------------------------------------------------------#
            
            if editor.textCursor().hasSelection():
                editor.insertPlainText(replace_word)         # replace the selection with the word to be replaced with
            else:
                # show a message:
                message = QtGui.QMessageBox(QtGui.QMessageBox.Information, "Error!!!", "No text was found to be replaced, \nTry finding the word again then replace it!", QtGui.QMessageBox.Ok)
                message.setWindowIcon(QtGui.QIcon("Icons/Icon.ico"))
                message.exec_()

        
        def replace_all(self):
            # get the words to be found and replaced from the find dialog:
            find_word = find_dialog.find_input.text()
            replace_word = find_dialog.replace_input.text()

            new_text = text.replace(find_word, replace_word)
            editor.clear()
            editor.insertPlainText(new_text)                # add the new text to the editor window
        
        self.find_dialog.find_btn.clicked.connect(find_text)
        self.find_dialog.find_next_btn.clicked.connect(find_text)
        self.find_dialog.replace_btn.clicked.connect(replace_text)
        self.find_dialog.replace_all_btn.clicked.connect(replace_all)
        return self.find_dialog
    
    def get_font_choice(self):
        font, valid = QtGui.QFontDialog.getFont()
        if valid:
            self.text_editor.setFont(font)
            # add a value named "Editor_Font" to settings and set that value to the font chosen by user in QFontDialog:
            settings.setValue("Editor_Font", font)
    
    def get_font_color(self):
        color_dialog = QtGui.QColorDialog.getColor()
        # change the value of self.font_color to the name of the color chosen by user:
        self.font_color = color_dialog.name()
        # set the stylesheet of the text editor with the same background color but new font color:
        self.text_editor.setStyleSheet("border: none;background: %s;color: %s;" %(self.back_color, self.font_color))
    
    def get_back_color(self):
        bgcolor_dialog = QtGui.QColorDialog.getColor()
        # change the value of self.back_color to the name of the color chosen by user:
        self.back_color = bgcolor_dialog.name()
        # set the stylesheet of the text editor with the same font color but new background color:
        self.text_editor.setStyleSheet("border: none;background: %s;color: %s;" %(self.back_color, self.font_color))
    
    def set_night_theme(self, isChecked):
        #----------------------------------------------------------#
        #-- This function is called by the checkbox of view menu --#
        #-- named "Night Theme" and this function acts according --#
        #-- to the current state of that checkbox. For more info --#
        #-- see add_night_theme_option_view_menu() function in   --#
        #-- Functions_Module.py                                  --#
        #----------------------------------------------------------#

        # Note: isChecked is a property of checkboxes that returns true if it is checked or false otherwise:
        if isChecked:
            # change the values of self.back_color and self.font_color variables to black and white respectively:
            self.back_color = "black"   
            self.font_color = "white"
            # set the stylesheet of the text editor according to the changed values of self.back_color and self.font_color:
            self.text_editor.setStyleSheet("border: none;background: %s;color: %s;" %(self.back_color, self.font_color))
            # add a value named "Night_Btn" to settings and set that value to the current status of the checkbox that is "checked":
            settings.setValue("Night_Btn", "checked")
        else:
            # set the stylesheet of the text editor back to default :
            self.text_editor.setStyleSheet("border: none;background: none;color: none;")
            # add a value named "Night_Btn" to settings and set that value to the current status of the checkbox that is "unchecked":
            settings.setValue("Night_Btn", "unchecked")
    
    def add_statusbar(self, isChecked):
        #----------------------------------------------------------#
        #-- This function is called by the checkbox of view menu --#
        #-- named "Statusbar" and this function acts according   --#
        #-- to the current state of that checkbox. For more info --#
        #-- see add_statusbar_checkbox_view_menu() function in   --#
        #-- Functions_Module.py                                  --#
        #----------------------------------------------------------#
        
        # Note: isChecked is a property of checkboxes that returns true if it is checked or false otherwise:
        if isChecked:
            self.statusbar.show()
            # add a value named "Status_Btn" to settings and set that value to the current status of the checkbox that is "checked":
            settings.setValue("Status_Btn", "checked")
        else:
            self.statusbar.hide()
            # add a value named "Status_Btn" to settings and set that value to the current status of the checkbox that is "unchecked":
            settings.setValue("Status_Btn", "unchecked")
    
    def about(self):
        # note: About_Window is a team created class (see OTHER WINDOW CLASSES in Objects_Module.py)
        self.about = About_Window()
        return self.about
    
    #------------------------------------------------------------- SUPPORT FUNCTIONS ---------------------------------------------------------------------#
    def save_current_settings(self):
        # Note: settings is an imported variable (see Variables_Module.py)
        settings.setValue("Main_Size", self.size())  # add a value named "Main_Size" to settings and set that value to the current size of the main window.
        settings.setValue("Main_Position", self.pos())  # add a value named "Main_Position" to settings and set that value to the current position of the main window.
        settings.setValue("StyleSheet", self.text_editor.styleSheet()) # add a value named "StyleSheet" to settings and set that value to the current stylesheet of the editor
        
        if settings.value("Runs").isNull():                        # if a value named Runs does not exist in settings (this is the first time the code is run)
            settings.setValue("Runs", int(1))                          # create a value named Runs in settings and set its value to integer 1 (the current no. of runs)
        elif (settings.value("Runs").toInt()) >= 1:                # else if a value named "Runs" does exist in settings, check if its value is greater than 1.
            runs, can_convert = (settings.value("Runs").toInt())       # can_convert is a property of integer setting values that returns true if it can be converted
            if can_convert == True:
                settings.setValue("Runs", int(runs + 1))               # add 1 to the number of runs before closing the app.
        else:
            settings.setValue("Runs", int(1))                      # the else command is just a safety measure for any unexpected exceptions or falts...
        
        if self.isMaximized():                                     # if self (here, our Window Class) is maximized:
            settings.setValue("State", "Maximized")                     # create a value named State in settings and set its value to "Maximized"
        else:
            settings.setValue("State", "False")
    
    def paint_page_view(self, printer):
        self.text_editor.print_(printer)                           # print current page view using the given printer
    
    def restore_last_settings_editor(self):
        if (settings.value("Runs").toInt()) >= 1:                  # check if the number of runs is equal to or greater than 1,
            self.text_editor.setStyleSheet(settings.value("StyleSheet").toString())
            if settings.value("Editor_Font").isValid():
                self.text_editor.setFont(QtGui.QFont(settings.value("Editor_Font")))
        else:
            pass                                                   # do nothing...
    
    def position_print(self):
        line = self.text_editor.textCursor().blockNumber()
        col = self.text_editor.textCursor().columnNumber()
        cursor_position = ("Line: %s | Column: %s" %(str(line), str(col)))
        self.statusbar.showMessage(cursor_position)                # shows the cursor position on statusbar
    
    def closeEvent(self, event):                                   # if user tries to close self (here, our Window class) this function is executed.
        event.ignore()
        self.exit_app()                                            # note: exit_app() is a team created function, see FUNCTIONS FOR MENUBAR OPTIONS in Objects_Module.py

#------------------------------------------------------------------------------------- OTHER WINDOW CLASSES --------------------------------------------------------------------------#
class File_Dialog_Window(QtGui.QWidget):                  # defines a subclass of QWidget named File_Dialog_Window
    
    # This method defines everything that is to be executed automatically when the class is initialized:
    def __init__(self):
        super(File_Dialog_Window, self).__init__()  # This makes the class inherit functions from its upper class (Here, QWidget Class):
        self.move(50, 50)
        self.setWindowIcon(QtGui.QIcon("Icons/Icon.ico"))
        self.show()

class About_Window(QtGui.QWidget):                        # defines a subclass of QWidget named About_Window
    
    # This method defines everything that is to be executed automatically when the class is initialized:
    def __init__(self):
        super(About_Window, self).__init__()        # This makes the class inherit functions from its upper class (Here, QWidget Class):
        
        if settings.value("Runs").isNull():             # if a value named Runs does not exist in settings (this is the first time the code is run)
            # then, set these custom values as the x, y positions and height, width of the Window class:
            # Note: QRect converts integer values into a rectangle form which can be used to visualize a window:
            self.setGeometry(QtCore.QRect(50, 50, 350, 110))
        else:
            self.restore_last_settings_AbWindow()                     # restore the last settings of About_Window...
            pass
        
        self.setWindowTitle("About")
        self.setWindowIcon(QtGui.QIcon("Icons/Icon.ico"))
        self.interface()
        self.show()
    
    def restore_last_settings_AbWindow(self):
        if (settings.value("Runs").toInt()) >= 1:                           # check if the number of runs is equal to or greater than 1:
            # If yes, then set the position of the window according to the last values present in the settings named About_Position:
            # Note: .toPoint converts the values in settings to a QPoint which can be used to move the window.
            self.move(settings.value("About_Position").toPoint())
            self.resize(350, 110)

        else:   # the else command is just a safety measure for any unexpected exceptions or falts...
            self.setGeometry(QtCore.QRect(50, 50, 350, 110))

    def interface(self):
        para = "An open source project by A.E.R.T team. \nIts a fully functional text editor coded in python \nand licensed under unlicense."
        name = QtGui.QLabel(self)
        about_text = QtGui.QLabel(self)

        name.setStyleSheet("font-family: georgia;color: blue;font: 18pt")
        about_text.setStyleSheet("font-family: georgia;font: 12pt")

        name.setText("EditOS")
        about_text.setText(para)

        name.resize(name.sizeHint())
        about_text.resize(about_text.sizeHint())

        name.move(40, 7)
        about_text.move(5, 45)

        logo = QtGui.QLabel(self)
        logo.setPixmap(QtGui.QPixmap("Icons/Large_Icon.ico"))
        logo.move(5, 5)
        logo.resize(logo.sizeHint())
        logo.show()
    
    # this saves the current settings in registry and then, closes the window:
    def close_window(self):
        # Note: settings is an imported variable (see Variables_Module.py)
        settings.setValue("About_Position", self.pos())     # add a value named "About_Position" to settings and set that value to the current position of the window
        self.hide()
    
    def closeEvent(self, event):                                   # if user tries to close self (here, our About_Window class) this function is executed.
        event.ignore()
        self.close_window()



class Find_Dialog(QtGui.QDialog):                                       # defines a subclass of QDailog named Find_Dialog
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)                            # This makes the class inherit functions from its upper class (Here, QDialog Class):
        
        if settings.value("Runs").isNull():             # if a value named Runs does not exist in settings (this is the first time the code is run)
            # then, set these custom values as the x, y positions and height, width of the Window class:
            # Note: QRect converts integer values into a rectangle form which can be used to visualize a window:
            self.setGeometry(QtCore.QRect(50, 50, 400, 220))
        else:
            self.restore_last_settings_FdWindow()                     # restore the last settings of Find_Dialog...
            pass
        
        self.setWindowTitle("Find")
        self.setWindowIcon(QtGui.QIcon("Icons/Icon.ico"))
        self.add_find_interface()
        self.show()
    
    def restore_last_settings_FdWindow(self):
        if (settings.value("Runs").toInt()) >= 1:                           # check if the number of runs is equal to or greater than 1:
            # If yes, then set the position of the window according to the last values present in the settings named Find_Position:
            # Note: .toPoint converts the values in settings to a QPoint which can be used to move the window.
            self.move(settings.value("Find_Position").toPoint())
            self.resize(400, 220)

        else:   # the else command is just a safety measure for any unexpected exceptions or falts...
            self.setGeometry(QtCore.QRect(50, 50, 400, 220))
    
    def width(self):
        return float(self.frameGeometry().width())
    
    def height(self):
        return float(self.frameGeometry().height())
    
    def paintEvent(self, event):                                        # creates the line for direction option
        painter = QtGui.QPainter()
        painter.begin(self)
        pen = QtGui.QPen(QtGui.QColor(211, 211, 211))
        painter.setPen(pen)
        painter.drawLine(QtCore.QPoint(int(self.width() / 40.0), int(self.height() /3.5)), QtCore.QPoint(int(self.width() / 20.0), int(self.height() /3.5)))
        painter.drawLine(QtCore.QPoint(int(self.width() / 5.7), int(self.height() /3.5)), QtCore.QPoint(int(self.width() / 1.16), int(self.height() /3.5)))
        painter.drawLine(QtCore.QPoint(int(self.width() / 40.0), int(self.height() /3.5)), QtCore.QPoint(int(self.width() / 40.0), int(self.height() / 2.15)))
        painter.drawLine(QtCore.QPoint(int(self.width() / 40.0), int(self.height() / 2.15)), QtCore.QPoint(int(self.width() / 1.16), int(self.height() / 2.15)))
        painter.drawLine(QtCore.QPoint(int(self.width() / 1.16), int(self.height() /3.5)), QtCore.QPoint(int(self.width() / 1.16), int(self.height() / 2.15)))
        painter.end()
 
    def add_find_interface(self):
        find_label = QtGui.QLabel("Search For: ", self)
        self.find_label = find_label
        self.find_label.move(int(self.width() / 20.0), int(self.height() / 15.5))
        self.find_label.resize(self.find_label.sizeHint())
 
        find_input = QtGui.QLineEdit(self)
        self.find_input = find_input
        self.find_input.setGeometry(int(self.width() / 4.0), int(self.height() / 20.0), int(self.width() / 1.6), int(self.height() / 8.8))
 
        find_btn = QtGui.QPushButton("Find", self)
        self.find_btn = find_btn
        self.find_btn.move(int(self.width() / 2.9), int(self.height() / 5.0))
        self.find_btn.resize(self.find_btn.sizeHint())

        find_next_btn = QtGui.QPushButton("Find Next", self)
        self.find_next_btn = find_next_btn
        self.find_next_btn.move(int(self.width() / 1.7), int(self.height() / 5.0))
        self.find_next_btn.resize(self.find_next_btn.sizeHint())

        direction_label = QtGui.QLabel("Direction: ", self)
        self.direction_label = direction_label
        self.direction_label.move(int(self.width() / 17.0), int(self.height() / 3.2))
        self.direction_label.resize(self.direction_label.sizeHint())

        backwards_radio_btn = QtGui.QRadioButton("Backward", self)
        self.backwards_radio_btn = backwards_radio_btn
        self.backwards_radio_btn.move(int(self.width() / 4.5), int(self.width() / 4.4))
        self.backwards_radio_btn.resize(self.backwards_radio_btn.sizeHint())
        self.backwards_radio_btn.toggle()
        self.backwards_radio_btn.toggled.connect(self.set_direction)

        forwards_radio_btn = QtGui.QRadioButton("Forward", self)
        self.forwards_radio_btn = forwards_radio_btn
        self.forwards_radio_btn.move(int(self.width() / 2.0), int(self.width() / 4.4))
        self.forwards_radio_btn.resize(self.forwards_radio_btn.sizeHint())
        self.forwards_radio_btn.toggled.connect(self.set_direction)

        replace_label = QtGui.QLabel("Replace By: ", self)
        self.replace_label = replace_label
        self.replace_label.move(int(self.width() / 20.0), int(self.height() / 1.65))
        self.replace_label.resize(self.replace_label.sizeHint())
        
        replace_input = QtGui.QLineEdit(self)
        self.replace_input = replace_input
        self.replace_input.setGeometry(int(self.width() / 4.0), int(self.height() / 1.7), int(self.width() / 1.6), int(self.height() / 8.8))

        replace_btn = QtGui.QPushButton("Replace", self)
        self.replace_btn = replace_btn
        self.replace_btn.move(int(self.width() / 2.9), int(self.height() / 1.34))
        self.replace_btn.resize(self.replace_btn.sizeHint())

        replace_all_btn = QtGui.QPushButton("Replace All", self)
        self.replace_all_btn = replace_all_btn
        self.replace_all_btn.move(int(self.width() / 1.7), int(self.height() / 1.34))
        self.replace_all_btn.resize(self.replace_all_btn.sizeHint())
        
        case_check = QtGui.QCheckBox("Case sensitive", self)
        self.case_check = case_check
        self.case_check.move(int(self.width() / 40.0), int(self.height() / 1.1))
        self.case_check.stateChanged.connect(self.case_sense)
         
        whole_word_opt = QtGui.QCheckBox("Whole words only",self)
        self.whole_word_opt = whole_word_opt
        self.whole_word_opt.move(int(self.width() / 3.7), int(self.height() / 1.1))
        self.whole_word_opt.stateChanged.connect(self.whole_word_sense)
    
    def set_direction(self, isChecked):
        #--------------------------------------------------#
        #-- This function is called by either            --#   
        #-- backwards_radio_btn or forwards_radio_btn    --#
        #-- and this function acts according             --#
        #-- to the current state of those radio buttons. --#
        #-- For the coding of these buttons, see up      --#
        #-- In add_find_interface of Find_Dialog         --#
        #--------------------------------------------------#

        # Note: isChecked is a property of radio buttons that returns true if it is checked or false otherwise:

        global direction                   # Note: direction is an imported variable (see Variables_Module.py)
        if isChecked:
            if direction == "Forward":
                direction = "Backward"
            
            elif direction == "Backward":
                direction = "Forward"
            
            else:
                direction = "Backward"
        
        else:
            pass

    
    def case_sense(self, state):
        #--------------------------------------------------------#
        #-- This function is called by whole_word_opt checkbox --#
        #-- and this function acts according to                --#
        #-- the current state of that checkbox.                --#
        #-- For the coding of this checkbox,                   --#
        #-- See up in add_find_interface of Find_Dialog        --#
        #--------------------------------------------------------#

        # Note: state is a property of checkboxes that equals QtCore.Qt.Checked if checkbox is checked or false otherwise:

        global case_sensitive               # Note: case_sensitive is an imported variable (see Variables_Module.py)

        if state == QtCore.Qt.Checked:
            case_sensitive = True
        else:
            case_sensitive = False
    
    def whole_word_sense(self, state):
        #----------------------------------------------------#
        #-- This function is called by case_check checkbox --#
        #-- and this function acts according to            --#
        #-- the current state of that checkbox.            --#
        #-- For the coding of this checkbox,               --#
        #-- See up in add_find_interface of Find_Dialog    --#
        #----------------------------------------------------#

        # Note: state is a property of checkboxes that equals QtCore.Qt.Checked if checkbox is checked or false otherwise:

        global whole_words_only             # Note: whole_words_only is an imported variable (see Variables_Module.py)

        if state == QtCore.Qt.Checked:
            whole_words_only = True
        else:
            whole_words_only = False
    
    # this saves the current settings in registry and then, closes the window:
    def close_window(self):
        # Note: settings is an imported variable (see Variables_Module.py)
        settings.setValue("Find_Position", self.pos())     # add a value named "Find_Position" to settings and set that value to the current position of the window
        self.hide()
    
    def closeEvent(self, event):                                   # if user tries to close self (here, our Find_Dialog class) this function is executed.
        event.ignore()
        self.close_window()

#-------x-----------------------x-------------------------x--------------------------THE END--------------------x---------------------x-----------------------------------x---------------------x------------------x------------#