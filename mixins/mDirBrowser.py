#   Programmer: limodou
#   E-mail:     limodou@gmail.coms
#
#   Copyleft 2006 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   NewEdit is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   $Id: mDirBrowser.py 475 2006-01-16 09:50:28Z limodou $

import wx
from modules import Mixin
from modules import common
from modules import Globals

def add_mainframe_menu(menulist):
    menulist.extend([('IDM_FILE',
        [
            (138, 'IDM_WINDOW_DIRBROWSER', tr('Directory Browser')+'\tF2', wx.ITEM_NORMAL, 'OnWindowDirBrowser', tr('Opens directory browser window.'))
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_mainframe_menu', add_mainframe_menu)

def add_notebook_menu(popmenulist):
    popmenulist.extend([(None,
        [
            (170, 'IDPM_DIRBROWSERWINDOW', tr('Directory Browser'), wx.ITEM_NORMAL, 'OnDirBrowserWindow', tr('Opens directory browser window.')),
        ]),
    ])
Mixin.setPlugin('notebook', 'add_notebook_menu', add_notebook_menu)

dirbrowser_imagelist = {
    'close':common.unicode_abspath('images/folderclose.gif'),
    'open':common.unicode_abspath('images/folderopen.gif'),
    'item':common.unicode_abspath('images/file.gif'),
}

def afterinit(win):
    win.dirbrowser_imagelist = {
        'close':'images/folderclose.gif',
        'open':'images/folderopen.gif',
        'item':'images/file.gif',
    }
    if win.pref.open_last_dir_as_startup and win.pref.last_dir_paths:
        wx.CallAfter(win.createDirBrowserWindow, win.pref.last_dir_paths)
        wx.CallAfter(win.panel.showPage, tr('Dir Browser'))
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

#toollist = [
#   (550, 'dirbrowser'),
#]
#Mixin.setMixin('mainframe', 'toollist', toollist)
#
##order, IDname, imagefile, short text, long text, func
#toolbaritems = {
#   'dirbrowser':(wx.ITEM_NORMAL, 'IDM_WINDOW_DIRBROWSER', images.getWizardBitmap(), tr('dir browser'), tr('Opens directory browser window.'), 'OnWindowDirBrowser'),
#}
#Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def createDirBrowserWindow(win, dirs=None):
    if not win.panel.getPage(tr('Dir Browser')):
        from DirBrowser import DirBrowser

        page = DirBrowser(win.panel.createNotebook('left'), win, dirs)
        win.panel.addPage('left', page, tr('Dir Browser'))
Mixin.setMixin('mainframe', 'createDirBrowserWindow', createDirBrowserWindow)

def OnWindowDirBrowser(win, event):
    win.createDirBrowserWindow()
    win.panel.showPage(tr('Dir Browser'))
Mixin.setMixin('mainframe', 'OnWindowDirBrowser', OnWindowDirBrowser)

def OnDirBrowserWindow(win, event):
    win.mainframe.createDirBrowserWindow()
    win.panel.showPage(tr('Dir Browser'))
Mixin.setMixin('notebook', 'OnDirBrowserWindow', OnDirBrowserWindow)

def pref_init(pref):
    pref.recent_dir_paths = []
    pref.recent_dir_paths_num = 10
    pref.last_dir_paths = []
    pref.open_last_dir_as_startup = True
Mixin.setPlugin('preference', 'init', pref_init)

def add_pref(preflist):
    preflist.extend([
        (tr('General'), 115, 'num', 'recent_dir_paths_num', tr('Max number of recent browse directories:'), None),
        (tr('General'), 240, 'check', 'open_last_dir_as_startup', tr('Open last directory browser as startup'), None),
    ])
Mixin.setPlugin('preference', 'add_pref', add_pref)

def after_addpath(dirbrowser):
    Globals.mainframe.pref.last_dir_paths = dirbrowser.getTopDirs()
    Globals.mainframe.pref.save()
Mixin.setPlugin('dirbrowser', 'after_addpath', after_addpath)

def after_closepath(dirbrowser, path):
    Globals.mainframe.pref.last_dir_paths = dirbrowser.getTopDirs()
    Globals.mainframe.pref.save()
Mixin.setPlugin('dirbrowser', 'after_closepath', after_closepath)
