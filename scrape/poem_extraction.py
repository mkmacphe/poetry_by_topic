import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import string

printable = set(string.printable)

# Returns a list of pages that will contain
# poetry we care about
def get_all_pages_poetry_foundation(url):
	# Assuming poetryfoundation
	prefix = "https://www.poetryfoundation.org"
	pageList = list()
	response = urlopen(url).read()
	soup = bs(response, "lxml")
	numbers = soup.find_all("ol", class_="c-pagination-list")
	for li in numbers[-1].find_all("li"):
		for a in li.find_all("a", href=True):
			pageList.append(prefix + a["href"])
	return pageList

# Finds all poems in a url, and calls
# print_poem on them
def get_all_poems(url):
	poemsToTraverse = list()
	poems_to_text = list()
	response = urlopen(url).read()
	soup = bs(response, "lxml")
	poems = soup.find_all("div", class_="c-feature-hd")
	for poem in poems:
		for link in poem.find_all("a", href=True):
			if link != None:
				poemsToTraverse.append(link["href"])

	for poem in poemsToTraverse:
		poems_to_text.append(return_poem(poem))

	return(poems_to_text)

# Return a poem via url as raw text
def return_poem(url):
	response = urlopen(url).read()
	soup = bs(response, "lxml")
	poems = soup.find_all("div", class_="o-poem")
	for poem in poems:
		return(''.join(filter( lambda x: x in printable, poem.get_text().strip())))

# Dump a bunch of poems from a poetry foundation link
def dump_poems(url):
	pages_of_poems = list()
	for page in get_all_pages_poetry_foundation(url):
		pages_of_poems.append(get_all_poems(page))

	return(pages_of_poems)


	

if __name__ == "__main__":
	url = "https://www.poetryfoundation.org/search?query=front%20seat&refinement=poems"
	print(dump_poems(url))
