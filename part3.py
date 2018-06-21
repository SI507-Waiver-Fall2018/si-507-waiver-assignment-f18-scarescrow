# these should be the only imports you need

import requests
from bs4 import BeautifulSoup

# My full name is Sagnik Sinha Roy
# My UMich uniqname is sagniksr

# write your code here
# usage should be python3 part3.py

URL = "https://www.michigandaily.com"

if __name__ == "__main__":

	# First, use the HTTP GET method to get the HTML
	# of the website

	req = requests.get(URL)
	html = req.text
	req.close()

	# Now convert it to a soup object

	soup = BeautifulSoup(html, 'html.parser')

	# Find the div of most read stories with
	# a unique identifier

	class_to_find = 'view-most-read'
	most_read_div = soup.find('div', class_=class_to_find)

	# Parse the div to get the text and links
	# of the most read stories

	most_read_list = most_read_div.find('ol').findAll('li')
	most_read_stories = []

	for listItem in most_read_list:
		anchorTag = listItem.find('a')
		storyObject = {
			'link': anchorTag['href'],
			'title': anchorTag.getText()
		}
		most_read_stories.append(storyObject)

	# Iterate over the stories, and make an HTTP 
	# request for each link

	class_to_find = 'byline'

	for story in most_read_stories:

		req = requests.get(URL + story['link'])
		html = req.text
		req.close()

		soup = BeautifulSoup(html, 'html.parser')

		# Now parse the html to get the name of the author
		# print(story['link'])
		try:
			author_div = soup.find('div', class_=class_to_find)
			author = author_div.find('a').getText()
			story['author'] = author
		except:
			# Some articles under the news section do not have an author,
			# so marking the author of those as Daily Staff Writer
			story['author'] = 'Daily Staff Writer'
			pass

	# Finally, print result in the required format

	print("Michigan Daily -- MOST READ")
	for story in most_read_stories:
		print(story['title'])
		print('  by ' + story['author'])