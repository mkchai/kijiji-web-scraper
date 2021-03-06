"""-----------------------------------------------------------------------------

	test_main.py

	Identical to main.py, except that the program state and UI is populated with 
	dummy entries.

-----------------------------------------------------------------------------"""

import time

import lib.gui
import lib.client_state
import lib.trackers


def main():
	# adding in test ads
	for i in range(0, 50):
		lib.client_state.ad_entries.append({
			'title': 'foo',
			'price': 500,
			'date_posted': '5 minutes ago',
			'location': 'canada',
			'url': 'http://website.com',
			'description': 'bar',
			'html_class': 'normal'
		})
	# adding in test notifications
	for i in range(0, 100):
		lib.client_state.notification_entries.appendleft({
			'notification_type': 'newad',
			'front_text': 'New Ad',
			'notification_title': 'foo',
			'ad_price': 'no price given',
			'ad_title': 'bar',
			'ad_url': 'http://website.com',
			'start_time': time.perf_counter()
		})
	# adding in test trackers
	for i in range(0, 2):
		lib.trackers.add_tracker_entry({
			'product_name': 'foo',
			'location': 'city-of-toronto',
			'max_price': 20,
			'cycle_time': 1800
		})
	lib.gui.instantiate()

if __name__ == "__main__":
	main()