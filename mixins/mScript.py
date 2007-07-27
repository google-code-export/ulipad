#	Programmer:	limodou
#	E-mail:		limodou@gmail.com
#
#	Copyleft 2006 limodou
#
#	Distributed under the terms of the GPL (GNU Public License)
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
#	$Id: mScript.py 475 2006-01-16 09:50:28Z limodou $

import wx
import sys
from modules import Mixin
from modules import makemenu

def pref_init(pref):
	pref.scripts = []
	pref.last_script_dir = ''
Mixin.setPlugin('preference', 'init', pref_init)

def add_mainframe_menu(menulist):
    menulist.extend([(None,
        [
            (570, 'IDM_SCRIPT', tr('Script'), wx.ITEM_NORMAL, None, ''),
        ]),
        ('IDM_SCRIPT', #parent menu id
        [
            (100, 'IDM_SCRIPT_MANAGE', tr('Script Manage...'), wx.ITEM_NORMAL, 'OnScriptManage', tr('Script manage')),
            (110, '', '-', wx.ITEM_SEPARATOR, None, ''),
            (120, 'IDM_SCRIPT_ITEMS', tr('(empty)'), wx.ITEM_NORMAL, 'OnScriptItems', tr('Execute an script')),
        ]),
    ])
Mixin.setPlugin('mainframe', 'add_menu', add_mainframe_menu)

def OnScriptManage(win, event):
	from ScriptDialog import ScriptDialog

	dlg = ScriptDialog(win, win.pref)
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		makescriptmenu(win, win.pref)
Mixin.setMixin('mainframe', 'OnScriptManage', OnScriptManage)

def beforeinit(win):
	win.scriptmenu_ids=[win.IDM_SCRIPT_ITEMS]
	makescriptmenu(win, win.pref)
Mixin.setPlugin('mainframe', 'beforeinit', beforeinit)

def makescriptmenu(win, pref):
	menu = makemenu.findmenu(win.menuitems, 'IDM_SCRIPT')

	for id in win.scriptmenu_ids:
		menu.Delete(id)

	win.scriptmenu_ids = []
	if len(win.pref.scripts) == 0:
		id = win.IDM_SCRIPT_ITEMS
		menu.Append(id, tr('(empty)'))
		menu.Enable(id, False)
		win.scriptmenu_ids=[id]
	else:
		for description, filename in win.pref.scripts:
			id = wx.NewId()
			win.scriptmenu_ids.append(id)
			menu.Append(id, description)
			wx.EVT_MENU(win, id, win.OnScriptItems)

def OnScriptItems(win, event):
	import wx.lib.dialogs
	import traceback

	eid = event.GetId()
	index = win.scriptmenu_ids.index(eid)
	filename = win.pref.scripts[index][1]

	try:
		scripttext = open(filename, 'r').read()
	except:
		dlg = wx.MessageDialog(win, tr("Can't open the file [%s]!") % filename, tr("Running Script"), wx.OK | wx.ICON_INFORMATION)
		dlg.ShowModal()
		return

	try:
		code = compile((scripttext + '\n'), filename, 'exec')
	except:
		d = wx.lib.dialogs.ScrolledMessageDialog(win, (tr("Error compiling script.\n\nTraceback:\n\n") +
			''.join(traceback.format_exception(*sys.exc_info()))), tr("Error"), wx.DefaultPosition, wx.Size(400,300))
		d.ShowModal()
		d.Destroy()
		return

	try:
		namespace = locals()
		exec code in namespace
	except:
		d = wx.lib.dialogs.ScrolledMessageDialog(win, (tr("Error running script.\n\nTraceback:\n\n") +
			''.join(traceback.format_exception(*sys.exc_info()))), tr("Error"), wx.DefaultPosition, wx.Size(400,300))
		d.ShowModal()
		d.Destroy()
		return
Mixin.setMixin('mainframe', 'OnScriptItems', OnScriptItems)