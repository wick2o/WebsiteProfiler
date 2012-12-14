#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib2
import random
import socket

halt = False

try:
	import argparse
except ImportError:
	print 'Missing needed module: easy_install argparse'
	halt = True


try:
	from BeautifulSoup import BeautifulSoup
except ImportError:
	print 'Missing needed module: easy_install beautifulsoup'
	halt = True

	
try:
	import fpdf
except ImportError:
	print 'Missing needed module: easy_install fpdf'
	halt = True

try:
	import pygeoip
except ImportError:
	print 'Missing needed module: easy_install pygeoip'
	halt = True

try:
	import dns.rdatatype
	import dns.message
	import dns.query
except ImportError:
	print 'Missing needed module: easy_install dnspython'
	halt = True
	
if halt == True:
	sys.exit()


js_functions = [ 'eval(', 'unescape(', 'alert(' ]	

profile = {}

			

def get_useragent():
	user_agents = [	'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'
					'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Avant Browser; Avant Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506; Tablet PC 2.0)',
					'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Avant Browser; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
					'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2; Avant Browser; Avant Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; InfoPath.2)',
					'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.14) Gecko/20080417 BonEcho/2.0.0.14',
					'Mozilla/5.0 (BeOS; U; Haiku BePC; en-US; rv:1.8.1.14) Gecko/20080429 BonEcho/2.0.0.14',
					'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
					'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
					'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24',
					'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00',
					'Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00',
					'Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00',
					'Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00',
					'Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0',
					'Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
					'Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
					'Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-FR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
					'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
					'Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27',
					'Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4',
					'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.0.9) Gecko/2009042410 Firefox/3.0.9 Wyzo/3.0.3',
					'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.9) Gecko/2009042410 Firefox/3.0.9 Wyzo/3.0.3',
					'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.0.9) Gecko/2009042410 Firefox/3.0.9 Wyzo/3.0.3',
				  ]
	return user_agents[random.randint(0, len(user_agents) - 1)]

def get_referer():
	referers = [ 'http://www.google.com',
 				 'http://www.msn.com',
				 'http://www.yahoo.com',
				 'http://www.bing.com',
				 'http://www.dailychanges.com',
			   ]
	return referers[random.randint(0,len(referers) - 1)]
	
def profile_meta(soup):

	profile['title'] = soup.title.string.strip()

	try:
		profile['description'] = soup.find('meta', {'name':'description'})['content'].encode('utf-8')
	except:
		profile['description'] = "None"
	try:
		profile['language'] = soup.find('meta', {'name':'language'})['content'].encode('utf_8')
	except:
		profile['language'] = "None"
	try:
		profile['copyright'] = soup.find('meta', {'name':'copyright'})['content'].encode('utf_8')
	except:
		profile['copyright'] = "None"
	try:
		profile['keywords'] = soup.find('meta', {'name':'keywords'})['content'].encode('utf_8')
	except:
		profile['keywords'] = "None"
	try:
		profile['author'] = soup.find('meta', {'name':'author'})['content'].encode('utf_8')
	except:
		profile['author'] = "None"
	
def profile_links(soup):
	internal_count = 0
	external_count = 0
	mailto_count = 0
	links = []
	
	for lnk in soup.findAll('a'):
		if lnk.has_key('href'):
			links.append(lnk['href'])
				
	for lnk in sorted(set(links)):
		if lnk == '/' or lnk == '#' or lnk == '/#':
			pass
		elif lnk.startswith('/'):
			internal_count += 1
		elif lnk.startswith('http') or lnk.startswith('www'):
			external_count += 1
		elif lnk.startswith('mailto:'):
			mailto_count += 1
		else:
			internal_count += 1
			
	profile['internal_links'] = internal_count
	profile['external_links'] = external_count
	profile['mailto_links'] = mailto_count

def profile_js(soup):
	js_links = []
	js_func_found = []
	js_code_blocks = 0

	for script in soup.findAll('script'):
		if script.has_key('src'):
			js_links.append(script['src'])
		else:
			js_code_blocks += 1
			for func in js_functions:
				if func in script.string:
					js_func_found.append(func)

			
	profile['js_external_links'] = ','.join(sorted(set(js_links)))
	profile['js_internal_blocks'] = js_code_blocks
	profile['js_fun_found'] = ','.join(sorted(set(js_func_found)))


def profile_css(soup):
	css_links = []
	
	for css in soup.findAll('link'):
		css_links.append('%s: %s' % (css['rel'], css['href']))

	profile['css_links'] = ','.join(sorted(set(css_links)))

def profile_robots(url):
	disallowed = []
	
	req = urllib2.Request('%s/robots.txt' % (args.url))
	req.add_header('User-Agent', get_useragent())
	req.add_header('Referer', get_referer())
	try:
		page = urllib2.urlopen(req)
	
		page_content = page.read()
	
		for line in page_content.split('\n'):
			if 'disallow' in line.strip().lower() and not line.startswith('#'):
				disallowed.append(line.split(':')[1].strip().replace('\n',''))

		page.close()

		profile['robots_disallowed'] = ','.join(sorted(set(disallowed)))
	
	except urllib2.URLError, e:
		if e.code == '404':
			profile['robots_disallowed'] = 'None'

def profile_whois(url):

	ns = []
	hosts = { 'abuse'   : 'whois.abuse.net',
			  'nic'     : 'whois.crsnic',
			  'inic'    : 'whois.networksolutions.com',
			  'dnic'    : 'whois.nic.mil',
			  'gnic'    : 'whois.nic.gov',
			  'anic'    : 'whois.arin.net',
			  'lnic'    : 'whois.lacnic.net',
			  'rnic'    : 'whois.ripe.net',
			  'mnic'    : 'whois.ra.net',
			  'qnic'    : '.whois-servers.net',
			  'snic'    : 'whois.6bone.net',
			  'bnic'    : 'whois.registro.br',
			  'norid'   : 'whois.norid.no',
			  'iana'    : 'whois.iana.org',
			  'germnic' : 'de.whois-servers.net',
			}
			
	if url.rfind('.') == url.find('.'):
		url = url.replace('http://','').replace('https://','')
	else:
		url = url[url.find('.')+1:]
		
	if url.endswith('-NORID'):
		lookup_host = hosts['norid']
	else:
		pos = url.rfind('.')
		if pos == -1:
			lookup_host = None
		else:
			tld = url[pos+1:]
			if tld[0].isdigit():
				lookup_host = hosts['anic']
			else:
				lookup_host = '%s%s' % (tld,hosts['qnic'])

	if lookup_host != None:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((lookup_host, 43))
		if lookup_host == hosts['germnic']:
			s.send('-T dn,ace -C US-ASCII %s \r\n' % (url))
		else:
			s.send('%s\r\n' % (url))
		res = ''
		while True:
			d = s.recv(4096)
			res += d
			if not d:
				break
		s.close()
		for line in res.split('\n'):
			c_line = line.replace('\n','').strip()
			if 'Registrar:' in c_line:
				profile['whois_registrar'] = c_line.split(':')[1].strip()
			elif 'Whois Server:' in c_line:
				profile['whois_server'] = c_line.split(':')[1].strip()
			elif 'Name Server:' in c_line:
				ns.append(c_line.split(':')[1].strip())
			elif 'Status:' in c_line:
				profile['whois_status'] = c_line.split(':')[1].strip()
			elif 'Updated Date:' in c_line:
				profile['whois_updated'] = c_line.split(':')[1].strip()
			elif 'Creation Date:' in c_line:
				profile['whois_creation'] = c_line.split(':')[1].strip()
			elif 'Expiration Date:' in c_line:
				profile['whois_expiration'] = c_line.split(':')[1].strip()
				
		profile['whois_nameserver'] = ','.join(ns)
		
	gic = pygeoip.GeoIP('GeoLiteCity.dat')
	data = gic.record_by_name(url)

	profile['geoip_city'] = data['city']
	profile['geoip_time_zone'] = data['time_zone']
	profile['geoip_metro_code'] = data['metro_code']
	profile['geoip_postal_code'] = data['postal_code']
	profile['geoip_lat'] = data['latitude']
	profile['geoip_long'] = data['longitude']
	profile['geoip_country_name'] = data['country_name']
	profile['geoip_area_code'] = data['area_code']
	
	message = dns.message.make_query(url, dns.rdatatype.ANY)
	response = dns.query.udp(message, '8.8.8.8')
	
	res = []

	for itm in response.answer:
		for i in itm.to_text().split('\n'):
			res.append(i)
			
	profile['dns_lookup'] = '\n'.join(res)

		
	
	
def generate_report():

	#title
	#description
	#language
	#copyright
	#keywords
	#author
	#internal_links
	#external_links
	#mailto_links
	#js_external_links
	#js_internal_blocks
	#js_fun_found
	#css_links
	#robots_disallowed
	#whois_registrar
	#whois_server
	#whois_referral
	#whois_nameserver
	#whois_status
	#whois_updated
	#whois_creation
	#whois_expiration
	#geoip_city
	#geoip_time_zone
	#geoip_metro_code
	#geoip_postal_code
	#geoip_lat
	#geoip_long
	#geo_country_name
	#geo_area_code
	#dns_lookup

	pdf = fpdf.FPDF('P','in','A4')
	pdf.add_page()
	pdf.set_font('Arial','B',8)
	pdf.cell(0,0.2,'URL: %s' % (args.url))
	pdf.ln()
	pdf.cell(0,0.2,'Title: %s' % (profile['title']))
	pdf.ln()
	pdf.cell(0,0.2,'Description: %s' % (profile['description']))
	pdf.ln()
	pdf.cell(0,0.2,'Keywords: %s' % (profile['keywords']))
	pdf.ln()
	pdf.cell(0,0.2,'Internal Link Count: %s' % (profile['internal_links']))
	pdf.ln()
	pdf.cell(0,0.2,'External Link Count: %s' % (profile['external_links']))
	pdf.ln()
	pdf.cell(0,0.2,'Mailto Link Count: %s' % (profile['mailto_links']))
	pdf.ln()
	pdf.cell(0,0.2,'Javascript External Links:')
	pdf.ln()
	for itm in profile['js_external_links'].split(','):
		pdf.cell(0.3)
		pdf.cell(0,0.2,itm.strip())
		pdf.ln()
	pdf.cell(0,0.2,'Javascript Code Blocks: %s' % (profile['js_internal_blocks']))
	pdf.ln()
	if ', '.join(profile['js_fun_found'].replace('{','')) == '':
		pdf.cell(0,0.2,'Javascript Functions Found: None')
	else:
		pdf.cell(0,0.2,'Javascript Functions Found: %s' % (', '.join(profile['js_fun_found'].replace('{',''))))
	pdf.ln()
	pdf.cell(0,0.2,'CSS Links Found:')
	pdf.ln()
	for itm in profile['css_links'].split(','):
		pdf.cell(0.3)
		pdf.cell(0,0.2,itm.strip())
		pdf.ln()
	pdf.cell(0,0.2,'Robots.txt Disallowed:')
	pdf.ln()
	for itm in profile['robots_disallowed'].split(','):
		pdf.cell(0.3)
		pdf.cell(0,0.2,itm.strip())
		pdf.ln()
	pdf.cell(0,0.2,'Whois Information:')
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Registrar: %s' % (profile['whois_registrar']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Whois Server: %s' % (profile['whois_server']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Name Servers: %s' % (profile['whois_nameserver'].replace(',',', ')))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Status: %s' % (profile['whois_status']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Updated Date: %s' % (profile['whois_updated']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Creation Date: %s' % (profile['whois_creation']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Expiration Date: %s' % (profile['whois_expiration']))
	pdf.ln()
	pdf.cell(0,0.2,'Geo Location Data:')
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'City: %s' % (profile['geoip_city']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'TimeZone: %s' % (profile['geoip_time_zone']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Metro Code: %s' % (profile['geoip_metro_code']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Postal Code: %s' % (profile['geoip_postal_code']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Latitude: %s' % (profile['geoip_lat']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Longitude: %s' % (profile['geoip_long']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Country Name: %s' % (profile['geoip_country_name']))
	pdf.ln()
	pdf.cell(0.3)
	pdf.cell(0,0.2,'Area Code: %s' % (profile['geoip_area_code']))
	pdf.ln()
	pdf.cell(0,0.2,'DIG ANY Results:')
	pdf.ln()
	for itm in profile['dns_lookup'].split('\n'):
		pdf.cell(0.3)
		pdf.cell(0,0.2,itm)
		pdf.ln()
		

		
	

	pdf.output('example_report.pdf', 'F')
	
def setup():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--url', action='store', dest='url', required=True, help='url ie: wwww.google.com')
	
	global args
	args = parser.parse_args()
	
def main():
	setup()
	
	req = urllib2.Request(args.url)
	req.add_header('User-Agent', get_useragent())
	req.add_header('Referer', get_referer())
	page = urllib2.urlopen(req)
	
	page_content = page.read()
	page_soup = BeautifulSoup(page_content)
	
	profile_meta(page_soup)
	profile_links(page_soup)
	profile_js(page_soup)
	profile_css(page_soup)
	profile_robots(args.url)
	profile_whois(args.url)
	

	generate_report()

	page.close()

if __name__ == "__main__":
	main()
	