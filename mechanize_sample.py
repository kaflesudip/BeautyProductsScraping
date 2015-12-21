import mechanize

mb = mechanize.Browser()
mb.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 
mb.set_handle_robots(False)
url = "http://www.maccosmetics.com/bestsellers"
response = mb.open(url).read()
print response