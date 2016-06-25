#! /usr/bin/python

#import html parser
from bs4 import BeautifulSoup
#import http library
import urllib2
#import command line parser
import sys
# import regex
import re
import datetime


root_url = 'http://www.bbc.co.uk/learningenglish/english/features/the-english-we-speak/'

# Input a url and extract the download url
def extract_download_url(url):
	try:
		connection = urllib2.urlopen(url)
		if 200 == connection.getcode():
			soup = BeautifulSoup(connection.read())
			return soup.find('a', {'class':'download bbcle-download-extension-pdf'})['href']
		else:
			return ""
		connection.close()
	except urllib2.HTTPError, e:
		print e.getcode()
		raise

def download_file(url, path):
	try:
		connection = urllib2.urlopen(url)
		f = open(path, 'w')
		f.write(connection.read())
		f.close()
		print "download file finished"
	except urllib2.HTTPError, e:
		print e.getcode()
		raise

def is_valid_date(date):
	if re.match('\d{6}', date):
		return True
	else:
		return False


def get_file_by_url(sub_dir):
	try:
		url = root_url + sub_dir

		download_url = extract_download_url(url)

		if download_url:
        		print download_url
		else:
        		print 'Cannot extract download url'

		file_dir = '/home/cong/' + sub_dir + '.pdf'

		download_file(download_url, file_dir)
	except urllib2.HTTPError, e:
		raise


if 3 == len(sys.argv): 
	start_date = sys.argv[1]
	end_date = sys.argv[2]
	print start_date + ' ' + end_date
	if is_valid_date(start_date) and is_valid_date(end_date):
		try:
			start_date = datetime.datetime.strptime(start_date, '%d%m%y')
			end_date = datetime.datetime.strptime(end_date, '%d%m%y')
			print 'Dates are valid'
		except ValueError, e:
			print e;
			print 'Please check your date format!'
			sys.exit(1)
		# Get next Tuesday as "The English we speak" update every Tuesday
		nearest_Tuesday = start_date + datetime.timedelta(days=((7 - (start_date.weekday() - 1)) % 7))
		print('\n')
		while nearest_Tuesday <= end_date:
			print nearest_Tuesday
			sub_dir = 'ep-' + nearest_Tuesday.strftime('%y%m%d')
			print 'sub-dir: ' + sub_dir
			try:
				get_file_by_url(sub_dir)
			except urllib2.HTTPError, e:
				print 'Download file: ' + sub_dir + ' failed!'
			nearest_Tuesday =  nearest_Tuesday + datetime.timedelta(weeks=1)
			print '\n'
		print 'finished'
	else:
		print 'Dates are not valid'
		sys.exit(1)
else: 
        print 'Please input as following format' 
        print 'python filename.py ddmmyy(start date) ddmmyy(end date)'
	sys.exit(1)

