import bs4
import requests
import hashlib

'''
  File name: MD4Life.py
    Author: Hvts3rk
    Date created: 03/2020
    Python Version: 2.7
    Usage: change row 13 with your port's istance
'''

url="http://docker.hackthebox.eu:PORT/"

r = requests.session()
out= r.get(url)
soup = bs4.BeautifulSoup(out.text, 'lxml')
for x in soup.findAll("h3"):
    print "RECUPERATO: {}".format(x.get_text())
    val = x.get_text()

    new = hashlib.md5(val.encode('utf-8')).hexdigest()

    print "SPEDISCO: {}".format(new)

    data = {'hash': new}
    out = r.post(url, data=data)

    soup2 = bs4.BeautifulSoup(out.text, 'lxml')
    for y in soup2.findAll('p'):

        print "FLAG: {}".format(y.get_text())
