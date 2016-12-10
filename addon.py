#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 2015 techdealer

##############LIBRARIES TO IMPORT AND SETTINGS####################
import sys,urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,httplib

addon_id = 'script.teletextopt'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'

###################################################################################

###################################################################################
#TELETEXT WINDOW

class TeletextWindow(xbmcgui.WindowDialog):
	def __init__(self,channel,page):
		self.page = page
		self.channel = channel
		self.Open_page()

	def onControl(self, control):
		if control == self.anterior: #previous sub_page
			if len(self.txt_array)>1:
				if self.sub_page == 1: self.sub_page = len(self.txt_array)
				else: self.sub_page -= 1
				self.Change_sub_page()
		elif control == self.proximo: #next sub_page
			if len(self.txt_array)>1:
				if self.sub_page == len(self.txt_array): self.sub_page = 1
				else: self.sub_page += 1
				self.Change_sub_page()
		elif control == self.page_input: #go to page
			self.page = Page_Search()
			self.Open_page()
		elif control == self.addon_exit: #exit
			self.close()
		elif len(channel_list) > 1 and control == self.switch_channel: #switch channel
			tmp_channel = Choose_channel()
			if tmp_channel > 0:
				self.channel = tmp_channel
				self.page = 100
				self.Open_page()
		
	def onAction(self, action):
		action_id = action.getId()
		if action_id == 1: #previous sub_page
			if len(self.txt_array)>1:
				if self.sub_page == 1: self.sub_page = len(self.txt_array)
				else: self.sub_page -= 1
				self.Change_sub_page()
		elif action_id == 2: #next sub_page
			if len(self.txt_array)>1:
				if self.sub_page == len(self.txt_array): self.sub_page = 1
				else: self.sub_page += 1
				self.Change_sub_page()
		elif action_id == 4: #previous page
			if self.page == 100: self.page = 888
			else: self.page -= 1
			self.Open_page()
		elif action_id == 3: #next page
			if self.page == 888: self.page = 100
			else: self.page += 1
			self.Open_page()
		elif action_id == 7: #enter
			self.page = Page_Search()
			self.Open_page()
		elif action_id == 10 or action_id == 92: #esc or backspace
			self.close()
		elif len(channel_list) > 1 and action_id == 12: #spacebar
			tmp_channel = Choose_channel()
			if tmp_channel > 0:
				self.channel = tmp_channel
				self.page = 100
				self.Open_page()
		
	def Open_page(self):
		self.sub_page = 1
		
		if self.channel == 1: self.txt_array = RTP_resolver(self.page)
		elif self.channel == 2: self.txt_array = SIC_resolver(self.page)
		
		if len(self.txt_array)>0:
			self.background = xbmcgui.ControlImage(0,0,1280,720,self.txt_array[self.sub_page-1])
			self.addControl(self.background)
		else:
			self.background = xbmcgui.ControlImage(0,0,1280,720,addonfolder+artfolder+'notfound.jpg')
			self.addControl(self.background)
		if len(self.txt_array)>1:
			self.pagelabel = xbmcgui.ControlLabel(38,5,500,500,'Página '+str(self.page)+' - '+str(self.sub_page)+'/'+str(len(self.txt_array)), font='font24_title', angle=-90)
			self.addControl(self.pagelabel)
		else:
			self.pagelabel = xbmcgui.ControlLabel(38,5,500,500,'Página '+str(self.page), font='font24_title', angle=-90)
			self.addControl(self.pagelabel)
		if len(channel_list) > 1:
			self.switch_channel = xbmcgui.ControlButton(1202,0,80,70,'', focusTexture=addonfolder+artfolder+'switch.png', noFocusTexture=addonfolder+artfolder+'switch.png')
			self.addControl(self.switch_channel)
		self.page_input = xbmcgui.ControlButton(0,240,80,70,'', focusTexture=addonfolder+artfolder+'comando.png', noFocusTexture=addonfolder+artfolder+'comando.png')
		self.addControl(self.page_input)
		self.addon_exit = xbmcgui.ControlButton(1202,240,80,70,'', focusTexture=addonfolder+artfolder+'sair.png', noFocusTexture=addonfolder+artfolder+'sair.png')
		self.addControl(self.addon_exit)
		self.anterior = xbmcgui.ControlButton(0,652,80,70,'', focusTexture=addonfolder+artfolder+'anterior.png', noFocusTexture=addonfolder+artfolder+'anterior.png')
		self.addControl(self.anterior)
		self.proximo = xbmcgui.ControlButton(1202,652,80,70,'',focusTexture=addonfolder+artfolder+'proximo.png', noFocusTexture=addonfolder+artfolder+'proximo.png')
		self.addControl(self.proximo)
		
	def Change_sub_page(self):
		self.background = xbmcgui.ControlImage(0,0,1280,720,self.txt_array[self.sub_page-1])
		self.addControl(self.background)
		self.pagelabel = xbmcgui.ControlLabel(38,5,500,500,'Página '+str(self.page)+' - '+str(self.sub_page)+'/'+str(len(self.txt_array)), font='font24_title', angle=-90)
		self.addControl(self.pagelabel)
		if len(channel_list) > 1:
			self.switch_channel = xbmcgui.ControlButton(1202,0,80,70,'', focusTexture=addonfolder+artfolder+'switch.png', noFocusTexture=addonfolder+artfolder+'switch.png')
			self.addControl(self.switch_channel)
		self.page_input = xbmcgui.ControlButton(0,240,80,70,'', focusTexture=addonfolder+artfolder+'comando.png', noFocusTexture=addonfolder+artfolder+'comando.png')
		self.addControl(self.page_input)
		self.addon_exit = xbmcgui.ControlButton(1202,240,80,70,'', focusTexture=addonfolder+artfolder+'sair.png', noFocusTexture=addonfolder+artfolder+'sair.png')
		self.addControl(self.addon_exit)
		self.anterior = xbmcgui.ControlButton(0,652,80,70,'', focusTexture=addonfolder+artfolder+'anterior.png', noFocusTexture=addonfolder+artfolder+'anterior.png')
		self.addControl(self.anterior)
		self.proximo = xbmcgui.ControlButton(1202,652,80,70,'',focusTexture=addonfolder+artfolder+'proximo.png', noFocusTexture=addonfolder+artfolder+'proximo.png')
		self.addControl(self.proximo)

###################################################################################
#TELETEXT FUNCTIONS
	
def Page_Search():
    page = xbmcgui.Dialog().numeric(0,'Abrir a página...')
    page=int(page)
    if page>888 or page<100:
        Page_Search()
    else:
		return page
		
def Choose_channel():
	channel = xbmcgui.Dialog().select('Escolha um canal...', channel_list)+1
	return channel
    
def Open_Teletext(channel,page):
	window = TeletextWindow(channel,page)
	window.doModal()
	
###################################################################################
#TELETEXT RESOLVERS

def RTP_resolver(page):
	txt_array = []
	if page_exists('http://www.rtp.pt/wportal/fab-txt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_0001.png')==True:
		codigo_fonte = abrir_url('http://www.rtp.pt/wportal/fab-txt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_0001.htm')
		total_pages = re.search('">([0-9]+)</A>&nbsp;&nbsp;<A HREF="', codigo_fonte)
		if total_pages==None:
				txt_array.append('http://www.rtp.pt/wportal/fab-txt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_0001.png')
		else:
			total_pages = total_pages.group(1)
			for i in range(1,int(total_pages)+1):
				txt_array.append('http://www.rtp.pt/wportal/fab-txt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_' + str(i).rjust(4, '0') + '.png')
	return txt_array

def SIC_resolver(page):
	txt_array = []
	if page_exists('http://teletexto.sic.aeiou.pt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_0001.htm')==True:
		codigo_fonte = abrir_url('http://teletexto.sic.aeiou.pt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_0001.htm')
		total_pages = re.search('([0-9]+)(</a>)?&nbsp;&nbsp;|&nbsp;&nbsp;(<a href=".">)?&gt;&gt;(</a>)?', codigo_fonte)
		if total_pages != None:
			if total_pages.group(1)=="1":
				txt_array.append('http://teletexto.sic.aeiou.pt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_0001.png')
			else:
				total_pages = total_pages.group(1)
				for i in range(1,int(total_pages)+1):
					txt_array.append('http://teletexto.sic.aeiou.pt/'+ str(page - int(str(page)[-2:])) +'/' + str(page) + '_' + str(i).rjust(4, '0') + '.png')
	return txt_array

###################################################################################
#OTHER FUNCTIONS

def page_exists(url):
	request = urllib2.Request(url)
	request.get_method = lambda : 'HEAD'
	try:
		response = urllib2.urlopen(request)
		return True
	except urllib2.HTTPError:
		return False

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:33.0) Gecko/20100101 Firefox/33.0')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

###################################################################################
#ADDON STARTUP CODE

channel_list = ['RTP']

if len(channel_list) > 1: channel = Choose_channel()
else: channel = 1

if channel == 0:
	sys.exit(0)
Open_Teletext(channel,100)