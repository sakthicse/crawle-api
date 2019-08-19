from django.shortcuts import render
from rest_framework.response import Response
import requests
from parsel import Selector
import time
from urllib.parse import urlparse
import copy
# Create your views here.

# from .models import Test
# from .serializer import TestSerializer
from rest_framework.views import APIView
class CrawleView(APIView):
	def get(self,request):
		data = request.GET
		print("****")
		datas = {"results": "res"}
		return Response(datas)

	def post(self,request):
		print("..... In view ..........")
		data = request.data
		url = data.get('url')
		level = data.get('level')
		print(level)
		href_links = []
		image_urls = []
		search_domain = urlparse(url).hostname
		print(search_domain)


		## Setup for scrapping tool
		# "response.txt" contain all web page content
		response = requests.get(url)
		selector = Selector(response.text)
		
		href_link_total = selector.xpath('//a/@href').getall()
		# image_links = selector.xpath('//img/@src').getall()
		for link in href_link_total:
			if not (urlparse(link).hostname):
				href_links.append(url+link)
			elif search_domain in link:
				href_links.append(link)
			else:
				print(link)
		if level == '2':
			# selector = Selector(response.text)
			# submenu_menu_links = selector.xpath('//*[@id="navbar-collapse"]/ul/li/a/@href').getall()
			# for i in submenu_menu_links:
			sub_menu_response = requests.get(href_links[0])
			sub_menu_selector = Selector(sub_menu_response.text)
			href_link_total = selector.xpath('//a/@href').getall()
			image_links = selector.xpath('//img/@src').getall()
			for link in href_link_total:
				if not (urlparse(link).hostname):
					href_links.append(url+link)
				elif search_domain in link:
					href_links.append(link)
				else:
					print(link)
			for im in image_links:
				if not (urlparse(im).hostname):
					if str(im[0]) != '/':
						image_urls.append(url+'/'+im)
					else:
						image_urls.append(url+im)
				elif search_domain in im:
					image_urls.append(im)
		elif level =='3':
			href_link = copy.deepcopy(href_links)
			for i in href_link:
				sub_menu_response = requests.get(i)
				sub_menu_selector = Selector(sub_menu_response.text)
				href_link_total = selector.xpath('//a/@href').getall()
				image_links = selector.xpath('//img/@src').getall()
				for link in href_link_total:
					if not (urlparse(link).hostname):
						href_links.append(url+link)
					elif search_domain in link:
						href_links.append(link)
					else:
						print(link)
				for im in image_links:
					if not (urlparse(im).hostname):
						if str(im[0]) != '/':
							image_urls.append(url+'/'+im)
						else:
							image_urls.append(url+im)
					elif search_domain in im:
						image_urls.append(im)
			# print(href_menu_link_total)
		# print('*****************************href_links************************************')
		# print(href_links)
		# print('*****************************/href_links************************************')
		# print('*****************************image_links************************************')
		# print(image_links)
		# print('*****************************/image_links************************************')
		datas = {"href_links": href_links,"image_urls":image_urls}
		return Response(datas)
