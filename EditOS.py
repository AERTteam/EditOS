#-----------------------------------------------------------------------------------------------------------------------------------#
#-- A.E.R.T ------------------------------------------------------------------------------------------------------------------------#
#-- presents EditOS. A fully functional open source text editor coded in python 2.7 with pyqt4 module ------------------------------#
#-- Note: Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form -----#
#-- or as a compiled binary, for any purpose, commercial or non-commercial, and by any means. --------------------------------------#
#-- see LISCENSE.txt and NOTICE.txt for further details ----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------------#

# This imports all that is listed in __init__.py of current directory:
from __init__ import *

app = QtGui.QApplication(sys.argv) # sys.argv command returns the name and arguments of the file on which it is called.

# if this file is executed as the main file. then execute the indented code: 
if __name__ == "__main__":
    Main_Window = Window()
    interface(Main_Window) # calls our team created interface function on our window class.
    sys.exit(app.exec_())  # executes our QApplication.

#x---------------x---------------x---------------x---------------x---------------x---------------x---------------x---------------x---------------x