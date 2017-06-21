import lxml
import lxml.html
import requests

# class names of ads
# since Kijiji is weird, it uses a lot of whitespace in the class names
NORMAL_AD_CLASS = '''"
            search-item
             regular-ad
        "'''
TOP_AD_CLASS = " search-item top-feature "
FEATURED_AD_CLASS = " search-item highlight top-feature "

# lookup table of valid locations
location_lookup = {
	'all-of-toronto': {
		'name': 'b-gta-greater-toronto-area',
		'code': 'k0l1700272'
	}
}


def convert_price_text_to_float(text):
	try:
		# takes the dollar sign off and casts to float
		return float(text[1::])
	except ValueError:
		# for text like 'Free', 'Swap / Trade' and the like
		return text


def generate_url_elements_from_name_and_location(name, location):
	location_entry = location_lookup.get(location)
	if location_entry is not None:
		stripped_name = name.strip().lower()
		product_name = stripped_name.replace(" ", "-")
		location_name = location_entry.get('name')
		location_code = location_entry.get('code')
		return {
			'product_name': product_name,
			'location_name': location_name,
			'location_code': location_code
		}
	else:
		raise KeyError("Given location is not a valid location.")


def generate_page_url_from_url_elements(url_elements, page_num):
	product_name = url_elements.get('product_name')
	location_name = url_elements.get('location_name')
	location_code = url_elements.get('location_code')
	if page_num == 1:
		return 'http://kijiji.ca/' + location_name + '/' + product_name + '/' + location_code
	elif page_num > 1:
		page_number = 'page-' + str(page_num)
		return 'http://kijiji.ca/' + location_name + '/' + product_name + '/' + page_number + '/' + location_code
	else:
		raise IndexError("Page number must be a positive integer.")


def get_root_element_from_url(url):
	page = requests.get(url)
	return lxml.html.fromstring(page.content)


def get_ads_from_page(tree, class_name):
	normal_ads = tree.findall('.//div[@class=' + class_name + ']')
	dicts = []
	for ad in normal_ads:
		# reading raw string values from html
		info_container = ad.find('.//div[@class="info-container"]')
		raw_title = info_container.find('.//a[@class="title enable-search-navigation-flag "]').text
		raw_price = info_container.find('.//div[@class="price"]').text
		raw_description = info_container.find('.//div[@class="description"]').text
		raw_location = info_container.find('.//div[@class="location"]').text
		raw_date_posted = info_container.find('.//span[@class="date-posted"]').text
		raw_url = info_container.find('.//a[@class="title enable-search-navigation-flag "]').get('href')
		raw_ad_id = ad.get('data-ad-id')
		# converting raw values into appropriate formats / types
		title = raw_title.strip()
		price = convert_price_text_to_float(raw_price.strip())
		description = raw_description.strip()
		location = raw_location.strip()
		date_posted = raw_date_posted.strip()
		url = 'http://kijiji.ca' + raw_url
		ad_id = int(raw_ad_id)
		dicts.append({
			'title': title,
			'price': price,
			'description': description,
			'location': location,
			'date_posted': date_posted,
			'url': url,
			'ad_id': ad_id
		})

	return dicts


def get_normal_ads_from_page(tree):
	return get_ads_from_page(tree, NORMAL_AD_CLASS)


def get_featured_ads_from_page(tree):
	return get_ads_from_page(tree, FEATURED_AD_CLASS)


def get_top_ads_from_page(tree):
	return get_ads_from_page(tree, TOP_AD_CLASS)



def main():
	elements = generate_url_elements_from_name_and_location('Playstation 4', 'all-of-toronto')
	url = generate_page_url_from_url_elements(elements, 1)
	root = get_root_element_from_url(url)
	normal_ads = get_normal_ads_from_page(root)
	for ad in normal_ads:
		print(ad['ad_id'])



if __name__ == "__main__":
	main()