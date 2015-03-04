import sublime, sublime_plugin
import webbrowser

class HelpCommand(sublime_plugin.WindowCommand):
	settings 		= None
	lang			= None
	defaultSettings 	= None
	helpList		= []

	def __init__(self,*args,**kwargs):
		super(HelpCommand,self).__init__(*args,**kwargs)
		defaultSettings={'PHP':'http://php.net/%s','jQuery':'http://api.jquery.com/?s=%s','Google':'http://google.com/#newwindow=1&q=%s','Yandex':'http://yandex.ru/yandsearch?text=%s'}
		settings = sublime.load_settings('Help.sublime-settings') 
		if not settings.has('urls'):
			settings.set('urls',defaultSettings)

		sublime.save_settings('Help.sublime-settings')

	def run(self):
		self.settings = sublime.load_settings('Help.sublime-settings')
		if not self.settings.has('urls'):
			self.settings.set('urls',defaultSettings)
			sublime.save_settings('Help.sublime-settings')
		self.list_urls();

	def list_urls(self):
		self.helpList=[]
		for host, url in sorted(self.settings.get('urls').items()):
			self.helpList.append([host,url])

		self.window.show_quick_panel(self.helpList,self.get_help)

	def get_help(self,index):
		if(index >-1):
			url = self.helpList[index][1]
			self.window.active_view().run_command("help_get",{"url":url})


class HelpGetCommand(sublime_plugin.TextCommand):
	selection 	= None
	url 		= None

	def run(self,edit,url):
		self.url = url
		self.selection = ""

		self.get_selection()

	def get_selection(self):
		for sel in self.view.sel():
			self.selection += self.view.substr(sel)

		if not self.selection:
			sublime.error_message('You have to highlight a word on which you want some help.')
			sublime.status_message('Aborting')
		else:
			self.get_help()

	def get_help(self):
		url = self.url.replace('%s',self.selection)
		sublime.status_message('Opening a new tab in your favorite browser (%s)' %  url)
		webbrowser.open(url,2)
