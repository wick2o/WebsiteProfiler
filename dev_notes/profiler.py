#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib2
from datetime import date


nameservers = [ 'DOMAINCONTROL.COM', '1AND1.COM',           'REGISTRAR-SERVERS.COM', 'HICHINA.COM',        'WORLDNIC.COM',
				'NAME-SERVICES.COM', 'HOSTGATOR.COM',       'REGISTER.COM',          'ONAMAE.COM',         'BLUEHOST.COM',
				'CRAZYDOMAINS.COM',  'EXPIRINGMONITOR.COM', 'VALUE-DOMAIN.COM',      'DNSPOD.NET',         'DSREDIRECTION.COM',
				'OVH.NET',           'RENEWYOURNAME.NET',   'XINCACHE.COM',          'WEBSITEWELCOME.COM', 'DREAMHOST.COM',
				'NAME.COM',          'SEDOPARKING.COM',     'MDNSSERVICE.COM',       'WIX.COM',            'WORDPRESS.COM',
				'NDOVERDRIVE.COM',   'YOVOLE.COM',          'CASHPARKING.COM',       '1AND1.ES',           'IPAGE.COM',
				'ABOVE.COM',         'VPWEB.COM',           'YAHOO.COM',             '1UND1.DE',           'MYHOSTADMIN.NET',
				'GANDI.NET',         'NETFIRMS.COM',        '123-REG.CO.UK',         '1AND1.FR',           '22.CN',
				'FASTPARK.NET',      'MONIKERDNS.NET',      'HOSTMONSTER.COM',       'BODIS.COM',          '1AND1.CO.UK',
				'JUSTHOST.COM',      'DNSV.JP',             'STABLETRANSIT.COM',     'DOMAIN.COM',         '4CUN.COM',
			 ]


def main():
	t_day = date.today()
	
	# http://www.dailychanges.com/export/domaincontrol.com/2012-12-12/export.csv
	for n_server in nameservers:
		print 'Attempting %s...' % (n_server)
		try:
			url = 'http://www.dailychanges.com/export/%s/%s/export.csv' % (n_server, t_day)
			req = urllib2.Request(url)
			req.add_header('User-Agent', 'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1')
			req.add_header('Referer', 'http://www.dailychanges.com')
			
			page = urllib2.urlopen(req)
			
			f_name = page.info()['Content-Disposition'].split('filename=')[1].replace('"','')
			f_content = page.read()
	
			f = open(f_name, 'wb')
			f.write(f_content)
			f.close()
			
			page.close()
		except:
			print 'Too Many Downloads...'
			sys.exit()
		
if __name__ == "__main__":
	main()
	