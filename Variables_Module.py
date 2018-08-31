# This imports all that is listed in __init__.py of current directory:
from __init__ import *

# QSettings is a function of Qt that allows you to store the application's settings in the device's registry
# by the name of the company and software
settings = QtCore.QSettings("A.E.R.T", "EditOS")

# these are plain variables which store the default settings for find option
# but they are later used and changed accoring to user's choice by checkboxes and radio buttons.
case_sensitive = False
whole_words_only = False
direction = "Backward"