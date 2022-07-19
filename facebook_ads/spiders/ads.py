# encoding: utf8
#from gc import callbacks
#from facebook_ads.facebook_ads.items import FacebookAdsItem
import scrapy
#import pymongo
#import servers
import os
import time
#import scrapyd_api
import json
#from scrapyd_api import ScrapydAPI
from facebook_ads.items import FacebookAdsItem
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#import couchdb


class ads(scrapy.Spider):
	name = "facebook_ads"
	project = "ads"

	tmstmp = int(time.time())

	default_api_version = "v14.0"

	access_token = "TEST_TOKEN"

	def start_requests(self):
		os.environ['TZ']='Europe/Berlin'
		time.tzset()

		# type = getattr(self, 'type','')
		fields  = getattr(self, 'fields',None)
		search_term  = getattr(self, 'search_term',None)
		if fields is None or search_term is None:
			self.log("Fields and Search Term are mandatory.")
			return
		country = getattr(self, 'country','CA')
		search_page_ids = getattr(self, 'search_page_ids','')
		ad_active_status = getattr(self, 'ad_active_status','ALL')
		after_date = getattr(self, 'after_date','1970-01-01')
		page_limit = getattr(self, 'page_limit','500')
		api_version = getattr(self, 'api_version',self.default_api_version)
		self.retry_limit = getattr(self, 'retry_limit','3')

		default_url_pattern = (
		"https://graph.facebook.com/{}/ads_archive?access_token={}&"
		+ "fields={}&search_terms={}&ad_reached_countries={}&search_page_ids={}&"
		+ "ad_active_status={}&limit={}"
		)

		next_page_url = self.default_url_pattern.format(
			api_version,
			self.access_token,
			fields,
			search_term,
			country,
			search_page_ids,
			ad_active_status,
			page_limit,
		)

		yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)

	def parse(self, response):

		result = json.loads(response.body)

		if "paging" in result:
			yield scrapy.Request(url=result["paging"]["next"])

		# possible to filter data here
		# 	
		yield FacebookAdsItem(data=result['data'])