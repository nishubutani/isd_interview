import scrapy
from scrapy.cmdline import execute
import pandas as pd
import xlsxwriter
import csv
class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['quotes.toscrape.com']

    def start_requests(self):
        self.list = []
        self.file_name = "isd_data.xlsx"

        link = 'https://isd110.org/our-schools/laketown-elementary/staff-directory'
        yield scrapy.FormRequest(url=link,callback=self.parse,dont_filter=True)

    def parse(self, response):
        try:
            addres = " ".join(response.xpath('//p[@class="address"]/text()').extract()).strip()
            print(addres)
        except Exception as e:
            print(e)
            addres = ''

        try:
            state = response.xpath('//p[@class="address"]/text()[2]').extract_first('')
            state = state.split(",")[1].strip()
            state = state.split(" ")[0]
            print(state)
        except Exception as e:
            print(e)
            state = ''

        try:
            Zip = response.xpath('//p[@class="address"]/text()[2]').extract_first('')
            Zip = Zip.split(",")[1].strip()
            Zip = Zip.split(" ")[1]
            print(Zip)
        except Exception as e:
            print(e)
            Zip = ''


        divs = response.xpath('//div[@class="paragraph staff default"]//div[@class="views-row"]')
        for div1 in divs:
            try:
                title = div1.xpath('.//div[@class="field job-title"]/text()').extract_first('').strip()
                print(title)
            except Exception as e:
                print(e)
                title = ''

            try:
                last_name = div1.xpath('.//h2/text()').extract_first('')
                last_name = last_name.split(",")[1].strip()
                print(last_name)
            except Exception as e:
                print(e)
                last_name = ''

            try:
                first_name = div1.xpath('.//h2/text()').extract_first('')
                first_name = first_name.split(",")[0].strip()
                print(first_name)
            except Exception as e:
                print(e)
                first_name = ''

            try:
                phone = div1.xpath('.//div[@class="field phone"]/a/text()').extract_first('')
                print(phone)
            except Exception as e:
                print(e)
                phone = ''

            try:
                email = div1.xpath('.//div[@class="field email"]/a/text()').extract_first('')
                print(email)
            except Exception as e:
                print(e)
                email = ''

            item = {}
            item['Title'] = title
            item['Last Name'] = last_name
            item['First Name'] = first_name
            item['phone'] = phone
            item['email'] = email
            item['Address'] = addres
            item['State'] = state
            item['Zip'] = Zip
            item['url'] = response.url

            self.list.append(item)


        try:
            next_page = response.xpath('//a[@rel="next"]/@href').extract_first('')
            if next_page:
                next_page = 'https://isd110.org/our-schools/laketown-elementary/staff-directory' + next_page
                yield scrapy.FormRequest(url=next_page,dont_filter=True,callback=self.parse)
            else:
                df = pd.DataFrame(self.list)
                df.to_csv('test.csv')
        except Exception as e:
            print(e)

execute("scrapy crawl test".split())