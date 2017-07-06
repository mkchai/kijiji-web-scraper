"""-----------------------------------------------------------------------------

	client_state.py

	Used to hold application state, accessible between modules.

-----------------------------------------------------------------------------"""

active_view = None


gui_elements = {}
valid_locations = [
	'All of Toronto (GTA)',
	'City of Toronto',
	'Markham / York Region',
	'Mississauga / Peel Region',
	'Oakville / Halton Region',
	'Oshawa / Durham Region'
]

ui_to_location = {
	'All of Toronto (GTA)': 'all-of-toronto',
	'Toronto (GTA)': 'all-of-toronto',
	'Canada': 'canada',
	'City of Toronto': 'city-of-toronto',
	'Markham / York Region': 'markham-york-region',
	'Mississauga / Peel Region': 'mississauga-peel-region',
	'Oakville / Halton Region': 'oakville-halton-region',
	'Oshawa / Durham Region': 'oshawa-durham-region'
}
location_to_ui = {
	'canada': 'Canada',
	'all-of-toronto': 'All of Toronto (GTA)',
	'city-of-toronto': 'City of Toronto',
	'markham-york-region': 'Markham / York Region',
	'mississauga-peel-region': 'Mississauga / Peel Region',
	'oakville-halton-region': 'Oakville / Halton Region',
	'oshawa-durham-region': 'Oshawa / Durham Region'
}

ad_entries = []
notification_entries = []
notification_gui_panels = []
num_notifications = 50
tracker_entries = []

viewed_ad_ids = set()

app_open = True