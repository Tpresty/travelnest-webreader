#!/usr/bin/env python

from bs4 import BeautifulSoup
import httplib2
import collections


def site_reader(url):

    http = httplib2.Http()
    status, response = http.request(url)
    page = BeautifulSoup(response, 'html.parser')
    property_name = page.title.string.split(' - ')[0]
    summary = page.find_all('span', attrs={'class': '_y8ard79'})
    property_type = 'Flat'
    beds = None
    bedrooms = None
    bathrooms = None
    for tag in summary:
        if tag.string is not None:
            if 'bed' in tag.string and 'bedroom' not in tag.string:
                beds = int(tag.string.split(' ')[0])
            if 'bedroom' in tag.string:
                bedrooms = int(tag.string.split(' ')[0])
            if 'bath' in tag.string:
                bathrooms = int(tag.string.split(' ')[0])

    amenities = page.find('div', class_='amenities')
    amenities_list = [amenity.string for amenity in amenities.find_all('span') if amenity.string != 'Amenities']
    amenities_list = list(set(amenities_list))
    amenities_list = ', '.join(amenities_list)

    if bedrooms is None:
        bedrooms = beds

    results = collections.OrderedDict(property_name=property_name)
    results['property_type'] = property_type
    results['bedrooms'] = bedrooms
    results['bathrooms'] = bathrooms
    results['amenities'] = amenities_list

    return results


dict1 = site_reader('https://www.airbnb.co.uk/rooms/14531512?s=51')

dict2 = site_reader('https://www.airbnb.co.uk/rooms/19278160?s=51')

dict3 = site_reader('https://www.airbnb.co.uk/rooms/19292873?s=51')

for page_dict in [dict1, dict2, dict3]:
    for i in page_dict:
        print("{}\t{}".format(i, page_dict[i]))
    print '\n'
