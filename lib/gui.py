"""-----------------------------------------------------------------------------

	gui.py

	Controls the creation of the GUI.
	
-----------------------------------------------------------------------------"""

import wx
import re
import kijiji_scraper


"""-----------------------------------------------------------------------------

	Globals
	
-----------------------------------------------------------------------------"""

global GUI_ELEMENTS
global VALID_LOCATIONS
global AD_ENTRIES
global ACTIVE_VIEW
global UI_TO_LOCATION
global HARD_MAX_AD_NUMBER
global SET_VIEWED_AD_IDS
global SET_CURRENT_AD_IDS
GUI_ELEMENTS = {}
VALID_LOCATIONS = [
	'All of Toronto (GTA)',
	'City of Toronto'
]
AD_ENTRIES = []
ACTIVE_VIEW = None
UI_TO_LOCATION = {
	'All of Toronto (GTA)': 'all-of-toronto',
	'City of Toronto': 'city-of-toronto'
}
HARD_MAX_AD_NUMBER = 99
SET_VIEWED_AD_IDS = set()
SET_CURRENT_AD_IDS = set()

global DUMMY
DUMMY = {
	'title': 'Test',
	'price': 500.00,
	'description': 'Foo',
	'location': 'Here',
	'date_posted': '5 seconds ago',
	'url': 'http://website.org'
}
global OTHER_DUMMY
OTHER_DUMMY = {
	'title': 'Example',
	'price': 'this is the price',
	'description': 'Bar',
	'location': 'Not here',
	'date_posted': '5 years ago',
	'url': 'http://website.org'
}
AD_ENTRIES.append(DUMMY)
AD_ENTRIES.append(OTHER_DUMMY)

"""-----------------------------------------------------------------------------

	Checks
	
-----------------------------------------------------------------------------"""

def ads_to_display(show_top_ads, show_featured_ads, top_ads, featured_ads, normal_ads):
	if show_top_ads and show_featured_ads:
		return not len(top_ads) == len(featured_ads) == len(normal_ads) == 0
	elif show_top_ads:
		return not len(top_ads) == len(normal_ads) == 0
	elif show_featured_ads:
		return not len(featured_ads) == len(normal_ads) == 0
	else:
		return not len(normal_ads) == 0

# check for name made entirely of alphanumerics or spaces
alphanumeric_space_full = re.compile('^[\w ]+$')
def valid_product_name(arg):
	try:
		match = alphanumeric_space_full.match(arg)
		return match is not None
	except TypeError:
		return False

def get_max_ads(arg):
	try:
		max_ads = int(arg)
		return max_ads
	except ValueError:
		return False


"""-----------------------------------------------------------------------------

	Display conversions
	
-----------------------------------------------------------------------------"""

def convert_price_to_display(arg):
	try:
		nearest_cent = round(arg, 2)
		return '$' + str(nearest_cent)
	except TypeError:
		return arg


"""-----------------------------------------------------------------------------

	App creation
	
-----------------------------------------------------------------------------"""

def create_app():
	app = wx.App(False)
	return app


"""-----------------------------------------------------------------------------

	Views Options creation
	
-----------------------------------------------------------------------------"""

def create_views_sizer():
	sizer = wx.BoxSizer(wx.VERTICAL)
	return sizer

def create_views_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY)
	return panel

def create_views_label(parent):
	label = wx.StaticText(parent, wx.ID_ANY, "Change Views", style = wx.TE_READONLY|wx.TE_CENTRE|wx.BORDER_NONE)
	return label

def scrape_mode_button_callback(arg):
	change_view('scraping')

def create_scrape_mode_button(parent):
	button = wx.Button(parent, wx.ID_ANY, "Scraping View")
	button.Bind(wx.EVT_BUTTON, scrape_mode_button_callback)
	return button

def notifications_mode_button_callback(arg):
	change_view('notifications')

def create_notifications_mode_button(parent):
	button = wx.Button(parent, wx.ID_ANY, "Notifications View")
	button.Bind(wx.EVT_BUTTON, notifications_mode_button_callback)
	return button

def threads_mode_button_callback(arg):
	change_view('threads')

def create_threads_mode_button(parent):
	button = wx.Button(parent, wx.ID_ANY, "Threads View")
	button.Bind(wx.EVT_BUTTON, threads_mode_button_callback)
	return button

def generate_views_options(parent):
	global GUI_ELEMENTS
	# creating panel and setting sizer
	views_panel = create_views_panel(parent)
	views_sizer = create_views_sizer()
	views_panel.SetSizer(views_sizer)
	# creating elements
	views_label = create_views_label(views_panel)
	scrape_mode_button = create_scrape_mode_button(views_panel)
	notifications_mode_button = create_notifications_mode_button(views_panel)
	threads_mode_button = create_threads_mode_button(views_panel)
	# adding to sizer
	views_sizer.Add(views_label, 0, wx.ALL|wx.EXPAND)
	views_sizer.Add(scrape_mode_button, 0, wx.ALL|wx.EXPAND, 5)
	views_sizer.Add(notifications_mode_button, 0, wx.ALL|wx.EXPAND, 5)
	views_sizer.Add(threads_mode_button, 0, wx.ALL|wx.EXPAND, 5)
	GUI_ELEMENTS['views_options_panel'] = views_panel
	return views_panel


"""-----------------------------------------------------------------------------

	Scrape Options creation
	
-----------------------------------------------------------------------------"""

def create_scrape_options_sizer():
	sizer = wx.BoxSizer(wx.VERTICAL)
	return sizer

def create_scrape_options_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY)
	return panel

def create_sub_product_sizer():
	sizer = wx.BoxSizer(wx.HORIZONTAL)
	return sizer

def create_sub_product_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY)
	return panel

def create_sub_scrape_sizer():
	sizer = wx.BoxSizer(wx.HORIZONTAL)
	return sizer

def create_sub_scrape_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY)
	return panel

def create_scrape_label(parent):
	label = wx.StaticText(parent, wx.ID_ANY, "Scraping", style = wx.TE_READONLY|wx.TE_CENTRE|wx.BORDER_NONE)
	return label

def create_product_name_label(parent):
	label = wx.StaticText(parent, wx.ID_ANY, "Product Name:", style = wx.TE_READONLY|wx.BORDER_NONE)
	return label

def create_product_name_text_box(parent):
	global GUI_ELEMENTS
	text_box = wx.TextCtrl(parent, wx.ID_ANY)
	GUI_ELEMENTS['product_name_text_box'] = text_box
	return text_box

def only_new_checkbox_callback(arg):
	print("Checkbox event fired")

def create_only_new_checkbox(parent):
	checkbox = wx.CheckBox(parent, wx.ID_ANY, "Only scrape new ads")
	checkbox.Bind(wx.EVT_CHECKBOX, only_new_checkbox_callback)
	GUI_ELEMENTS['only_new_checkbox'] = checkbox
	return checkbox

def create_max_ads_label(parent):
	label = wx.StaticText(parent, wx.ID_ANY, "Max Ads:", style = wx.TE_READONLY|wx.TE_RIGHT|wx.BORDER_NONE)
	return label

def create_max_ads_text_box(parent):
	global GUI_ELEMENTS
	textbox = wx.TextCtrl(parent, wx.ID_ANY, str(HARD_MAX_AD_NUMBER))
	GUI_ELEMENTS['max_ads_text_box'] = textbox
	return textbox

def create_show_top_ads_checkbox(parent):
	global GUI_ELEMENTS
	checkbox = wx.CheckBox(parent, wx.ID_ANY, "Show Top Ads")
	GUI_ELEMENTS['show_top_ads_checkbox'] = checkbox
	return checkbox

def create_show_featured_ads_checkbox(parent):
	global GUI_ELEMENTS
	checkbox = wx.CheckBox(parent, wx.ID_ANY, "Show Featured Ads")
	GUI_ELEMENTS['show_featured_ads_checkbox'] = checkbox
	return checkbox

def create_location_choice(parent):
	global GUI_ELEMENTS
	choice = wx.Choice(parent, wx.ID_ANY, choices = VALID_LOCATIONS)
	GUI_ELEMENTS['location_choice'] = choice
	return choice

def scrape_button_callback(arg):
	global GUI_ELEMENTS
	global AD_ENTRIES
	global SET_CURRENT_AD_IDS
	global SET_VIEWED_AD_IDS
	product_name_text_box = GUI_ELEMENTS['product_name_text_box']
	location_choice = GUI_ELEMENTS['location_choice']
	scrape_message = GUI_ELEMENTS['scrape_message']
	max_ads_text_box = GUI_ELEMENTS['max_ads_text_box']
	only_new_checkbox = GUI_ELEMENTS['only_new_checkbox']
	show_top_ads_checkbox = GUI_ELEMENTS['show_top_ads_checkbox']
	show_featured_ads_checkbox = GUI_ELEMENTS['show_featured_ads_checkbox']
	scrape_message.SetValue('')
	given_product_name = product_name_text_box.GetLineText(lineNo = 0)
	given_max_ads = get_max_ads(max_ads_text_box.GetLineText(lineNo = 0))
	given_location = location_choice.GetSelection()
	location = UI_TO_LOCATION.get(location_choice.GetString(given_location))
	if not valid_product_name(given_product_name):
		scrape_message.SetValue('Invalid product name. Only alphabetical and numeric characters are supported.')
		return
	if not given_max_ads or not 0 <= given_max_ads <= HARD_MAX_AD_NUMBER:
		scrape_message.SetValue('Invalid maximum ad number. Must be between 0 and ' + str(HARD_MAX_AD_NUMBER) + '.')
		return
	if not location:
		scrape_message.SetValue('Invalid location.')
		return
	current_page_num = 1
	only_new_ads = only_new_checkbox.GetValue()
	show_top_ads = show_top_ads_checkbox.GetValue()
	show_featured_ads = show_featured_ads_checkbox.GetValue()
	AD_ENTRIES = []
	SET_CURRENT_AD_IDS = set()
	no_more_new_ads = False
	while True:
		# get all ads for current page
		ads = kijiji_scraper.get_ads(
			name = given_product_name,
			location = location,
			page_num = current_page_num
		)
		normal_ads = ads.get('normal_ads')
		featured_ads = ads.get('featured_ads')
		top_ads = ads.get('top_ads')
		# breaks if there are no ads to display
		if not ads_to_display(
			show_top_ads = show_top_ads,
			show_featured_ads = show_featured_ads,
			top_ads = top_ads,
			featured_ads = featured_ads,
			normal_ads = normal_ads
		):
			break
		# adds top ads in, breaking if total ads are more than given max
		if show_top_ads:
			for ad in top_ads:
				ad_id = ad.get('ad_id')
				if len(AD_ENTRIES) >= given_max_ads:
					break
				if (ad_id not in SET_CURRENT_AD_IDS):
					AD_ENTRIES.append(ad)
					SET_CURRENT_AD_IDS.add(ad_id)
					SET_VIEWED_AD_IDS.add(ad_id)
		# breaks if current num of entries exceeds max entries
		if len(AD_ENTRIES) >= given_max_ads:
			break
		# adds featured ads in, breaking if total ads are more than given max
		if show_featured_ads:
			for ad in featured_ads:
				ad_id = ad.get('ad_id')
				if len(AD_ENTRIES) >= given_max_ads:
					break
				if (ad_id not in SET_CURRENT_AD_IDS):
					AD_ENTRIES.append(ad)
					SET_CURRENT_AD_IDS.add(ad_id)
					SET_VIEWED_AD_IDS.add(ad_id)
		# breaks if current num of entries exceeds max entries
		if len(AD_ENTRIES) >= given_max_ads:
			break
		# adds normal ads in, breaking if total ads are more than given max, or
		# if only new ads are to be displayed and a previous id is reached
		for ad in normal_ads:
			ad_id = ad.get('ad_id')
			if len(AD_ENTRIES) >= given_max_ads:
				break
			if ad_id in SET_VIEWED_AD_IDS:
				no_more_new_ads = True
				if only_new_ads:
					break
			if (ad_id not in SET_CURRENT_AD_IDS) and ((not only_new_ads) or (ad_id not in SET_VIEWED_AD_IDS)):
				AD_ENTRIES.append(ad)
				SET_CURRENT_AD_IDS.add(ad_id)
				SET_VIEWED_AD_IDS.add(ad_id)
		# breaks if current num of entries exceeds max entries
		if len(AD_ENTRIES) >= given_max_ads:
			break
		# breaks if a previous normal ad has been found
		if only_new_ads and no_more_new_ads:
			break
		current_page_num += 1

	update_scrape_view()

def create_scrape_button(parent):
	global GUI_ELEMENTS
	button = wx.Button(parent, wx.ID_ANY, "Scrape")
	button.Bind(wx.EVT_BUTTON, scrape_button_callback)
	GUI_ELEMENTS['scrape_button'] = button
	return button

def create_scrape_message(parent):
	global GUI_ELEMENTS
	label = wx.TextCtrl(parent, wx.ID_ANY, "", style = wx.TE_READONLY|wx.BORDER_NONE|wx.TE_MULTILINE|wx.TE_NO_VSCROLL)
	label.SetBackgroundColour(wx.Colour(240,240,240))
	GUI_ELEMENTS['scrape_message'] = label
	return label

def generate_scrape_options(parent):
	global GUI_ELEMENTS
	# creating panels and setting sizers
	scrape_options_panel = create_scrape_options_panel(parent)
	scrape_options_sizer = create_scrape_options_sizer()
	scrape_options_panel.SetSizer(scrape_options_sizer)
	sub_product_panel = create_sub_product_panel(scrape_options_panel)
	sub_product_sizer = create_sub_product_sizer()
	sub_product_panel.SetSizer(sub_product_sizer)
	sub_scrape_panel = create_sub_scrape_panel(scrape_options_panel)
	sub_scrape_sizer = create_sub_scrape_sizer()
	sub_scrape_panel.SetSizer(sub_scrape_sizer)
	# creating parts
	scrape_label = create_scrape_label(scrape_options_panel)
	product_name_label = create_product_name_label(sub_product_panel)
	product_name_text_box = create_product_name_text_box(sub_product_panel)
	only_new_checkbox = create_only_new_checkbox(sub_scrape_panel)
	max_ads_label = create_max_ads_label(sub_scrape_panel)
	max_ads_text_box = create_max_ads_text_box(sub_scrape_panel)
	show_top_ads_checkbox = create_show_top_ads_checkbox(scrape_options_panel)
	show_featured_ads_checkbox = create_show_featured_ads_checkbox(scrape_options_panel)
	location_choice = create_location_choice(scrape_options_panel)
	scrape_button = create_scrape_button(scrape_options_panel)
	scrape_message = create_scrape_message(scrape_options_panel)
	# putting in sizers
	sub_product_sizer.Add(product_name_label, 0, wx.TOP|wx.EXPAND, 4)
	sub_product_sizer.Add(product_name_text_box, 1, wx.LEFT|wx.EXPAND, 5)
	sub_scrape_sizer.Add(only_new_checkbox, 2, wx.ALL|wx.EXPAND, 1)
	sub_scrape_sizer.Add(max_ads_label, 0, wx.TOP|wx.EXPAND, 4)
	sub_scrape_sizer.Add(max_ads_text_box, 1, wx.LEFT|wx.EXPAND, 5)
	scrape_options_sizer.Add(scrape_label, 0, wx.ALL|wx.EXPAND)
	scrape_options_sizer.Add(sub_product_panel, 0, wx.ALL|wx.EXPAND, 5)
	scrape_options_sizer.Add(sub_scrape_panel, 0, wx.ALL|wx.EXPAND, 5)
	scrape_options_sizer.Add(show_top_ads_checkbox, 0, wx.ALL|wx.EXPAND, 5)
	scrape_options_sizer.Add(show_featured_ads_checkbox, 0, wx.ALL|wx.EXPAND, 5)
	scrape_options_sizer.Add(location_choice, 0, wx.ALL|wx.EXPAND, 5)
	scrape_options_sizer.Add(scrape_button, 0, wx.ALL|wx.EXPAND, 5)
	scrape_options_sizer.Add(scrape_message, 0, wx.ALL|wx.EXPAND, 5)
	GUI_ELEMENTS['scrape_options_panel'] = scrape_options_panel
	return scrape_options_panel

"""-----------------------------------------------------------------------------

	Scrape Options actions
	
-----------------------------------------------------------------------------"""

def enable_scraping_options():
	global GUI_ELEMENTS
	GUI_ELEMENTS['product_name_text_box'].Enable()
	GUI_ELEMENTS['only_new_checkbox'].Enable()
	GUI_ELEMENTS['max_ads_text_box'].Enable()
	GUI_ELEMENTS['show_top_ads_checkbox'].Enable()
	GUI_ELEMENTS['show_featured_ads_checkbox'].Enable()
	GUI_ELEMENTS['location_choice'].Enable()
	GUI_ELEMENTS['scrape_button'].Enable()

def disable_scraping_options():
	global GUI_ELEMENTS
	GUI_ELEMENTS['product_name_text_box'].Disable()
	GUI_ELEMENTS['only_new_checkbox'].Disable()
	GUI_ELEMENTS['max_ads_text_box'].Disable()
	GUI_ELEMENTS['show_top_ads_checkbox'].Disable()
	GUI_ELEMENTS['show_featured_ads_checkbox'].Disable()
	GUI_ELEMENTS['location_choice'].Disable()
	GUI_ELEMENTS['scrape_button'].Disable()
	

"""-----------------------------------------------------------------------------

	Notifications Options creation
	
-----------------------------------------------------------------------------"""

def create_notifications_options_sizer():
	sizer = wx.BoxSizer(wx.VERTICAL)
	return sizer

def create_notifications_options_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY)
	return panel

def create_notifications_label(parent):
	label = wx.StaticText(parent, wx.ID_ANY, "Notifications", style = wx.TE_READONLY|wx.TE_CENTRE|wx.BORDER_NONE)
	return label

def clear_all_notifications_button_callback(arg):
	print("Clear all notifications button pressed")

def create_clear_all_notifications_button(parent):
	global GUI_ELEMENTS
	button = wx.Button(parent, wx.ID_ANY, "Clear All Notifications")
	button.Bind(wx.EVT_BUTTON, clear_all_notifications_button_callback)
	GUI_ELEMENTS['clear_all_notifications_button'] = button
	return button

def generate_notifications_options(parent):
	global GUI_ELEMENTS
	# creating panel and setting sizer
	notifications_options_panel = create_notifications_options_panel(parent)
	notifications_options_sizer = create_notifications_options_sizer()
	notifications_options_panel.SetSizer(notifications_options_sizer)
	# creating elements
	notifications_label = create_notifications_label(notifications_options_panel)
	clear_all_notifications_button = create_clear_all_notifications_button(notifications_options_panel)
	# putting in sizers
	notifications_options_sizer.Add(notifications_label, 0, wx.ALL|wx.EXPAND)
	notifications_options_sizer.Add(clear_all_notifications_button, 0, wx.ALL|wx.EXPAND, 5)
	GUI_ELEMENTS['notifications_options_panel'] = notifications_options_panel
	return notifications_options_panel


"""-----------------------------------------------------------------------------

	Notifications Options actions
	
-----------------------------------------------------------------------------"""

def enable_notifications_options():
	global GUI_ELEMENTS
	GUI_ELEMENTS['clear_all_notifications_button'].Enable()

def disable_notifications_options():
	global GUI_ELEMENTS
	GUI_ELEMENTS['clear_all_notifications_button'].Disable()


"""-----------------------------------------------------------------------------

	Threads Options creation
	
-----------------------------------------------------------------------------"""

def create_threads_options_sizer():
	sizer = wx.BoxSizer(wx.VERTICAL)
	return sizer

def create_threads_options_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY)
	return panel

def create_threads_label(parent):
	label = wx.StaticText(parent, wx.ID_ANY, "Threads", style = wx.TE_READONLY|wx.TE_CENTRE|wx.BORDER_NONE)
	return label

def send_all_notifications_callback(arg):
	print("Send all notifications button pressed")

def create_send_all_notifications_button(parent):
	global GUI_ELEMENTS
	button = wx.Button(parent, wx.ID_ANY, "Send All Tray Notifications")
	button.Bind(wx.EVT_BUTTON, send_all_notifications_callback)
	GUI_ELEMENTS['send_all_notifications_button'] = button
	return button

def stop_all_notifications_callback(parent):
	print("Stop all notifications button pressed")

def create_stop_all_notifications_button(parent):
	global GUI_ELEMENTS
	button = wx.Button(parent, wx.ID_ANY, "Stop All Tray Notifications")
	button.Bind(wx.EVT_BUTTON, stop_all_notifications_callback)
	GUI_ELEMENTS['stop_all_notifications_button'] = button
	return button 

def kill_all_threads_button_callback(arg):
	print("Kill all threads button pressed")

def create_kill_all_threads_button(parent):
	global GUI_ELEMENTS
	button = wx.Button(parent, wx.ID_ANY, "Kill All Threads")
	button.Bind(wx.EVT_BUTTON, kill_all_threads_button_callback)
	GUI_ELEMENTS['kill_all_threads_button'] = button
	return button

def generate_threads_options(parent):
	global GUI_ELEMENTS
	# creating panel and setting sizer
	threads_options_panel = create_threads_options_panel(parent)
	threads_options_sizer = create_threads_options_sizer()
	threads_options_panel.SetSizer(threads_options_sizer)
	# creating elements
	threads_label = create_threads_label(threads_options_panel)
	send_all_notifications_button = create_send_all_notifications_button(threads_options_panel)
	stop_all_notifications_button = create_stop_all_notifications_button(threads_options_panel)
	kill_all_threads_button = create_kill_all_threads_button(threads_options_panel)
	# putting in sizers
	threads_options_sizer.Add(threads_label, 0, wx.ALL|wx.EXPAND)
	threads_options_sizer.Add(send_all_notifications_button, 0, wx.ALL|wx.EXPAND, 5)
	threads_options_sizer.Add(stop_all_notifications_button, 0, wx.ALL|wx.EXPAND, 5)
	threads_options_sizer.Add(kill_all_threads_button, 0, wx.ALL|wx.EXPAND, 5)
	GUI_ELEMENTS['threads_options_panel'] = threads_options_panel
	return threads_options_panel


"""-----------------------------------------------------------------------------

	Threads Options actions
	
-----------------------------------------------------------------------------"""

def enable_threads_options():
	global GUI_ELEMENTS
	GUI_ELEMENTS['send_all_notifications_button'].Enable()
	GUI_ELEMENTS['stop_all_notifications_button'].Enable()
	GUI_ELEMENTS['kill_all_threads_button'].Enable()

def disable_threads_options():
	global GUI_ELEMENTS
	GUI_ELEMENTS['send_all_notifications_button'].Disable()
	GUI_ELEMENTS['stop_all_notifications_button'].Disable()
	GUI_ELEMENTS['kill_all_threads_button'].Disable()


"""-----------------------------------------------------------------------------

	Options Panel creation
	
-----------------------------------------------------------------------------"""

def create_options_panel_sizer():
	sizer = wx.BoxSizer(wx.VERTICAL)
	return sizer

def create_options_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY, size = (300, 10000))
	return panel

def generate_options_panel(parent):
	global GUI_ELEMENTS
	# setting up panel and sizer
	options_panel = create_options_panel(parent)
	options_sizer = create_options_panel_sizer()
	options_panel.SetSizer(options_sizer)
	GUI_ELEMENTS['options_panel'] = options_panel
	GUI_ELEMENTS['options_panel_sizer'] = options_sizer
	return options_panel


"""-----------------------------------------------------------------------------

	Options Panel actions
	
-----------------------------------------------------------------------------"""

def change_options_panel_state(new_view):
	global GUI_ELEMENTS
	options_panel = GUI_ELEMENTS['options_panel']
	options_sizer = GUI_ELEMENTS['options_panel_sizer']
	options_sizer.Clear(delete_windows = True)
	views_options = generate_views_options(options_panel)
	options_sizer.Add(views_options, 0, wx.ALL|wx.EXPAND)
	options_sizer.AddSpacer(20)
	if new_view == 'scraping':
		scraping_options = generate_scrape_options(options_panel)
		options_sizer.Add(scraping_options, 0, wx.ALL|wx.EXPAND)
	elif new_view == 'notifications':
		notifications_options = generate_notifications_options(options_panel)
		options_sizer.Add(notifications_options, 0, wx.ALL|wx.EXPAND)
	elif new_view == 'threads':
		threads_options = generate_threads_options(options_panel)
		options_sizer.Add(threads_options, 0, wx.ALL|wx.EXPAND)


"""-----------------------------------------------------------------------------

	Scrolling Panel creation
	
-----------------------------------------------------------------------------"""

def create_scrolling_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY)
	return panel

def create_scrolling_panel_sizer():
	sizer = wx.BoxSizer(wx.VERTICAL)
	return sizer

def create_scroll_bar(parent):
	scrollbar = wx.ScrollBar(parent, wx.ID_ANY, style = wx.SB_VERTICAL, size = (20, 10000))
	scrollbar.SetScrollbar(0, 5, 10, 4, True)
	return scrollbar

def generate_scrolling_panel(parent):
	scrolling_panel = create_scrolling_panel(parent)
	scrollbar = create_scroll_bar(scrolling_panel)
	sizer = create_scrolling_panel_sizer()
	scrolling_panel.SetSizer(sizer)
	sizer.Add(scrollbar, 0, wx.ALL|wx.EXPAND)
	return scrolling_panel


"""-----------------------------------------------------------------------------

	Scrape View creation

-----------------------------------------------------------------------------"""

def create_scrape_view_sizer():
	sizer = wx.BoxSizer(wx.VERTICAL)
	return sizer

def create_scrape_view_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY)
	return panel

def create_ad_panel_sizer():
	sizer = wx.BoxSizer(wx.VERTICAL)
	return sizer

def create_ad_horizontal_sizer():
	sizer = wx.BoxSizer(wx.HORIZONTAL)
	return sizer

def create_scrape_header_text(parent):
	global AD_ENTRIES
	num_ads = len(AD_ENTRIES)
	displayed = str(num_ads) + ' ads found.'
	text = wx.TextCtrl(parent, wx.ID_ANY, displayed, style = wx.BORDER_NONE|wx.TE_READONLY)
	return text

def create_ad_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY, style = wx.BORDER_SIMPLE, size = (0, 100))
	return panel

def create_ad_sub_panel(parent):
	panel = wx.Panel(parent, wx.ID_ANY)
	return panel

def create_ad_title(parent, ad_title):
	textbox = wx.TextCtrl(parent, wx.ID_ANY, ad_title, style = wx.TE_READONLY|wx.BORDER_NONE)
	return textbox

def create_ad_price(parent, ad_price):
	textbox = wx.TextCtrl(parent, wx.ID_ANY, ad_price, style = wx.TE_READONLY|wx.BORDER_NONE)
	return textbox

def create_ad_date_posted(parent, ad_date_posted):
	textbox = wx.TextCtrl(parent, wx.ID_ANY, ad_date_posted, style = wx.TE_READONLY|wx.BORDER_NONE)
	return textbox

def create_ad_location(parent, ad_location):
	textbox = wx.TextCtrl(parent, wx.ID_ANY, ad_location, style = wx.TE_READONLY|wx.BORDER_NONE)
	return textbox

def create_ad_url(parent, ad_url):
	textbox = wx.TextCtrl(parent, wx.ID_ANY, ad_url, style = wx.TE_READONLY|wx.BORDER_NONE|wx.ALIGN_RIGHT)
	return textbox

def create_ad_description(parent, ad_description):
	textbox = wx.TextCtrl(parent, wx.ID_ANY, ad_description, style = wx.TE_READONLY|wx.BORDER_NONE|wx.TE_MULTILINE|wx.TE_NO_VSCROLL)
	textbox.SetBackgroundColour(wx.Colour(240,240,240))
	return textbox

def generate_ad_panel(parent, ad_dict):
	# converting dict entries to strings
	title = ad_dict.get('title')
	price = convert_price_to_display(ad_dict.get('price'))
	date_posted = ad_dict.get('date_posted')
	location = ad_dict.get('location')
	url = ad_dict.get('url')
	description = ad_dict.get('description')
	# setting up panel, sub-panels, and sizers
	ad_sizer = create_ad_panel_sizer()
	horiz_sizer_1 = create_ad_horizontal_sizer()
	horiz_sizer_2 = create_ad_horizontal_sizer()
	panel = create_ad_panel(parent)
	subpanel_1 = create_ad_sub_panel(panel)
	subpanel_2 = create_ad_sub_panel(panel)
	panel.SetSizer(ad_sizer)
	subpanel_1.SetSizer(horiz_sizer_1)
	subpanel_2.SetSizer(horiz_sizer_2)
	# adding price and title
	ad_title = create_ad_title(subpanel_1, title)
	ad_price = create_ad_price(subpanel_1, price)
	horiz_sizer_1.Add(ad_price, 1, wx.ALL|wx.EXPAND)
	horiz_sizer_1.Add(ad_title, 1, wx.ALL|wx.EXPAND)
	# adding date posted, location, and url
	ad_date_posted = create_ad_date_posted(subpanel_2, date_posted)
	ad_location = create_ad_location(subpanel_2, location)
	ad_url = create_ad_url(subpanel_2, url)
	horiz_sizer_2.Add(ad_date_posted, 1, wx.ALL|wx.EXPAND)
	horiz_sizer_2.Add(ad_location, 1, wx.ALL|wx.EXPAND)
	horiz_sizer_2.Add(ad_url, 5, wx.ALL|wx.EXPAND)
	# adding description
	ad_description = create_ad_description(panel, description)
	# adding all to main sizer
	ad_sizer.Add(subpanel_1, 0, wx.ALL|wx.EXPAND, 5)
	ad_sizer.Add(subpanel_2, 0, wx.ALL|wx.EXPAND, 5)
	ad_sizer.Add(ad_description, 0, wx.ALL|wx.EXPAND, 5)
	return panel

def generate_scrape_view(parent):
	global AD_ENTRIES
	global GUI_ELEMENTS
	scrape_view_sizer = create_scrape_view_sizer()
	scrape_view_panel = create_scrape_view_panel(parent)
	scrape_view_panel.SetSizer(scrape_view_sizer)
	scrape_header_text = create_scrape_header_text(scrape_view_panel)
	scrape_view_sizer.Add(scrape_header_text, 0, wx.ALL|wx.EXPAND, 5)
	GUI_ELEMENTS['scrape_view_panel'] = scrape_view_panel
	for ad in AD_ENTRIES:
		ad_panel = generate_ad_panel(scrape_view_panel, ad)
		scrape_view_sizer.Add(ad_panel, 0, wx.ALL|wx.EXPAND, 5)
	return scrape_view_panel

def destroy_scrape_view():
	global GUI_ELEMENTS
	GUI_ELEMENTS['scrape_view_panel'].Destroy()

def update_scrape_view():
	global GUI_ELEMENTS
	main_frame = GUI_ELEMENTS['main_frame']
	main_frame_sizer = GUI_ELEMENTS['main_frame_sizer']
	destroy_scrape_view()
	scrape_view = generate_scrape_view(main_frame)
	main_frame_sizer.Add(scrape_view, 1, wx.ALL|wx.EXPAND)
	main_frame.Layout()

"""-----------------------------------------------------------------------------

	Notifications View creation

-----------------------------------------------------------------------------"""

def generate_notifications_view(parent):
	pass

def destroy_notifications_view():
	pass


"""-----------------------------------------------------------------------------

	Threads View creation

-----------------------------------------------------------------------------"""

def generate_threads_view(parent):
	pass

def destroy_threads_view():
	pass

"""-----------------------------------------------------------------------------

	Main Frame creation
	
-----------------------------------------------------------------------------"""

def create_main_frame():
	frame = wx.Frame(None, wx.ID_ANY, "Kijiji Scraper")
	frame.Show()
	frame.Centre()
	frame.Maximize()
	return frame

def create_main_frame_sizer():
	sizer = wx.BoxSizer(wx.HORIZONTAL)
	return sizer

def generate_main_frame():
	global GUI_ELEMENTS
	main_frame = create_main_frame()
	options_panel = generate_options_panel(main_frame)
	scrolling_panel = generate_scrolling_panel(main_frame)
	sizer = create_main_frame_sizer()
	sizer.Add(options_panel, 0, wx.ALL|wx.EXPAND)
	sizer.Add(scrolling_panel, 0, wx.ALL|wx.EXPAND)
	main_frame.SetSizer(sizer)
	GUI_ELEMENTS['main_frame'] = main_frame
	GUI_ELEMENTS['main_frame_sizer'] = sizer
	return main_frame


"""-----------------------------------------------------------------------------

	State changes
	
-----------------------------------------------------------------------------"""

def change_view(new_view):
	global ACTIVE_VIEW
	if new_view != ACTIVE_VIEW:
		if ACTIVE_VIEW == 'scraping':
			destroy_scrape_view()
		elif ACTIVE_VIEW == 'notifications':
			destroy_notifications_view()
		elif ACTIVE_VIEW == 'threads':
			destroy_threads_view()
		# create new view and display relevant options
		main_frame = GUI_ELEMENTS['main_frame']
		main_frame_sizer = GUI_ELEMENTS['main_frame_sizer']
		change_options_panel_state(new_view)
		if new_view == 'scraping':
			scrape_view = generate_scrape_view(main_frame)
			main_frame_sizer.Add(scrape_view, 1, wx.ALL|wx.EXPAND)
			ACTIVE_VIEW = 'scraping'
		elif new_view == 'notifications':
			notifications_view = generate_notifications_view(main_frame)
			# main_frame_sizer.Add(notifications_view, 1, wx.ALL|wx.EXPAND)
			ACTIVE_VIEW = 'notifications'
		elif new_view == 'threads':
			threads_view = generate_threads_view(main_frame)
			# main_frame_sizer.Add(threads_view, 1, wx.ALL|wx.EXPAND)
			ACTIVE_VIEW	 = 'threads'
		main_frame.Layout()


def main():
	app = create_app()
	main_frame = generate_main_frame()
	change_view('scraping')
	app.MainLoop()


if __name__ == "__main__":
	main()
	