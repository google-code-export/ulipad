#	Programmer:	limodou
#	E-mail:		chatme@263.net
#
#	Copyleft 2004 limodou
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
#	$Id: mSearch.py 176 2005-11-22 02:46:37Z limodou $

"""Search process"""

import wx
from modules import Mixin
import os.path
from modules import common

menulist = [ (None, #parent menu id
	[
		(400, 'IDM_SEARCH', tr('Search'), wx.ITEM_NORMAL, None, ''),
	]),
	('IDM_SEARCH', #parent menu id
	[
		(100, 'IDM_SEARCH_FIND', tr('Find...') + '\tE=Ctrl+F', wx.ITEM_NORMAL, 'OnSearchFind', tr('Find text')),
		(110, 'IDM_SEARCH_DIRECTFIND', tr('Direct Find') + '\tF4', wx.ITEM_NORMAL, 'OnSearchDirectFind', tr('Direct find selected text')),
		(120, 'IDM_SEARCH_REPLACE', tr('Replace...') + '\tE=Ctrl+H', wx.ITEM_NORMAL, 'OnSearchReplace', tr('Find and replace text')),
		(130, 'IDM_SEARCH_FIND_NEXT', tr('Find Next') + '\tF3', wx.ITEM_NORMAL, 'OnSearchFindNext', tr('Find next occurance of text')),
		(140, 'IDM_SEARCH_FIND_PREVIOUS', tr('Find Previous') + '\tShift+F3', wx.ITEM_NORMAL, 'OnSearchFindPrev', tr('Find previous occurance of text')),
		(150, '', '-', wx.ITEM_SEPARATOR, None, ''),
		(160, 'IDM_SEARCH_GOTO_LINE', tr('Go to Line...') + '\tE=Ctrl+G', wx.ITEM_NORMAL, 'OnSearchGotoLine', tr('Goes to specified line in the active document')),
		(170, 'IDM_SEARCH_LAST_MODIFY', tr('Go to Last Modify') + '\tE=Ctrl+B', wx.ITEM_NORMAL, 'OnSearchLastModify', tr('Goes to the last modify position')),

	]),
]
Mixin.setMixin('mainframe', 'menulist', menulist)

imagelist = {
	'IDM_SEARCH_FIND':common.unicode_abspath('images/find.gif'),
	'IDM_SEARCH_REPLACE':common.unicode_abspath('images/replace.gif'),
	'IDM_SEARCH_FIND_NEXT':common.unicode_abspath('images/findnext.gif'),
}
Mixin.setMixin('mainframe', 'imagelist', imagelist)

toollist = [
	(220, 'find'),
	(230, 'replace'),
	(240, '|'),
]
Mixin.setMixin('mainframe', 'toollist', toollist)

toolbaritems = {
	'find':(wx.ITEM_NORMAL, 'IDM_SEARCH_FIND', common.unicode_abspath('images/find.gif'), tr('find'), tr('Find text'), 'OnSearchFind'),
	'replace':(wx.ITEM_NORMAL, 'IDM_SEARCH_REPLACE', common.unicode_abspath('images/replace.gif'), tr('replace'), tr('Find and replace text'), 'OnSearchReplace'),
}
Mixin.setMixin('mainframe', 'toolbaritems', toolbaritems)

def afterinit(win):
	import FindReplaceDialog

	win.finder = FindReplaceDialog.Finder()
Mixin.setPlugin('mainframe', 'afterinit', afterinit)

def on_document_enter(win, document):
	win.mainframe.finder.setWindow(document)
Mixin.setPlugin('editctrl', 'on_document_enter', on_document_enter)

findresfile = common.unicode_abspath('resources/finddialog.xrc')

def OnSearchFind(win, event):
	from modules import Resource
	from modules import i18n
	import FindReplaceDialog

	filename = i18n.makefilename(findresfile, win.app.i18n.lang)
	dlg = Resource.loadfromresfile(filename, win, FindReplaceDialog.FindDialog, 'FindDialog', win.finder)
	dlg.Show()
Mixin.setMixin('mainframe', 'OnSearchFind', OnSearchFind)

def OnSearchDirectFind(win, event):
	text = win.document.GetSelectedText()
	if len(text) > 0:
		win.finder.findtext = text
		win.finder.find(0)
Mixin.setMixin('mainframe', 'OnSearchDirectFind', OnSearchDirectFind)

def OnSearchReplace(win, event):
	from modules import Resource
	from modules import i18n
	import FindReplaceDialog

	filename = i18n.makefilename(findresfile, win.app.i18n.lang)
	filename = i18n.makefilename(findresfile, win.app.i18n.lang)
	dlg = Resource.loadfromresfile(filename, win, FindReplaceDialog.FindReplaceDialog, 'FindReplaceDialog', win.finder)
	dlg.Show()
Mixin.setMixin('mainframe', 'OnSearchReplace', OnSearchReplace)

def OnSearchFindNext(win, event):
	win.finder.find(0)
Mixin.setMixin('mainframe', 'OnSearchFindNext', OnSearchFindNext)

def OnSearchFindPrev(win, event):
	win.finder.find(1)
Mixin.setMixin('mainframe', 'OnSearchFindPrev', OnSearchFindPrev)

preflist = [
	(tr('General'), 120, 'num', 'max_number', tr('Max number of saved items:'), None)
]
Mixin.setMixin('preference', 'preflist', preflist)

def init(pref):
	pref.max_number  = 20
	pref.findtexts = []
	pref.replacetexts = []
Mixin.setPlugin('preference', 'init', init)

def OnSearchGotoLine(win, event):
	from modules import Entry

	line = win.document.GetCurrentLine() + 1
	dlg = Entry.MyTextEntry(win, tr("Go to Line..."), tr("Enter the Line Number:"), str(line))
	answer = dlg.ShowModal()
	if answer == wx.ID_OK:
		try:
			line = int(dlg.GetValue())
		except:
			return
		else:
			win.document.GotoLine(line-1)
Mixin.setMixin('mainframe', 'OnSearchGotoLine', OnSearchGotoLine)

def init(win):
	win.lastmodify = -1
Mixin.setPlugin('editor', 'init', init, Mixin.HIGH)

def OnSearchLastModify(win, event):
	if win.document.lastmodify > -1:
		win.document.GotoPos(win.document.lastmodify)
Mixin.setMixin('mainframe', 'OnSearchLastModify', OnSearchLastModify)

def OnModified(win, event):
	for flag in (wx.stc.STC_MOD_INSERTTEXT, wx.stc.STC_MOD_DELETETEXT,
		wx.stc.STC_PERFORMED_UNDO,
		wx.stc.STC_PERFORMED_REDO):
		if event.GetModificationType() & flag:
			win.lastmodify = event.GetPosition()
			return
Mixin.setPlugin('editor', 'on_modified', OnModified)