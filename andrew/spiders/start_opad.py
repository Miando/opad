from scrapy.spiders import CrawlSpider, Rule
from scrapy import Selector, Request
from scrapy.linkextractors import LinkExtractor
from andrew.items import AndrewItem
import sys

class MySpider(CrawlSpider):
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    name = "opad"
    allowed_domains = ["opad.com"]

    urls = open("2.csv").readlines()
    start=[]
    for url in urls:
        start.append("http://www.opad.com/%s.html" % url[:-1])

    #start_urls =start
    start_urls= ["http://www.opad.com/brands.html"]
    '''
    rules = (
        Rule(LinkExtractor(restrict_xpaths=("")), callback='parse_item5'),

        Rule(LinkExtractor(restrict_xpaths=("//div[@class='contentsItems']/div")), follow=True),

        Rule(LinkExtractor(restrict_xpaths=("//div[@class='pageNums controlBlock']")), follow=True),
    )
    '''

    def parse(self, response):
        #hxs = HtmlXPathSelector(response)
        hxs = Selector(response)

        urls1 = hxs.xpath("//div[@class='contentsItems']/div//a/@href").extract()

        for i in urls1:
            url = "http://www.opad.com/"+str(i)+"?ps=1000000#pagingContents"
            yield Request(url, callback=self.parse2)

    def parse1(self, response):
        #hxs = HtmlXPathSelector(response)
        hxs = Selector(response)
        urls2 = hxs.xpath("//div[@class='pageNums controlBlock']/a/@href").extract()[:-1]
        urls2.append(response.url)
        print urls2
        for j in urls2:
            url = "http://www.opad.com/"+str(j)
            yield Request(url, callback=self.parse2)

    def parse2(self, response):
        #hxs = HtmlXPathSelector(response)
        hxs = Selector(response)
        urls3 = []
        page = response.body

        start_link = 1
        end_quote=0
        while start_link >0:
            start_link = page.find('data-url="',end_quote)
            print start_link
            start_quote = page.find('"', start_link)
            print start_quote
            if start_quote == -1:
                break
            end_quote = page.find('"', start_quote+1)
            print end_quote
            url = page[start_quote+1:end_quote]

            urls3.append(url)

        for k in urls3:
            #url = "http://www.opad.com/"+str(k)
            yield Request(k,callback= self.parse5)

    def generate_item_dict(self):
        list1 = open("1.csv").readlines()
        list2=list1[0].split(",")
        dicti={}
        dicti["title"]=""
        dicti["file_urls"]=""
        dicti["image_urls"]=""

        for i in list2:
            dicti[i]=""
        return dicti

    def parse5(self, response):
        hxs = Selector(response)
        print "--------------------------------"
        items = []
        item= self.generate_item_dict()
        #yura:

        item["file_urls"]=[]
        item["title"] = hxs.select("//div[@class='breadcrumbs']/b/text()").extract_first()
        print item["title"]
        item["image_urls"] = hxs.select("//div[@class='scroller-view']/div/div/a/@href").extract()

        try:
            z = hxs.select("//div[@class='itemPDF']/div/a/@onclick").extract()
            for i in range(len(z)):
                x = ((z[i]).split("('")[1]).split("','")[0]
                item["file_urls"].append(x)
            print item["file_urls"]
        except:
            item["file_urls"] = ""
            print "No PDF there"

        #----------------------------------
        item["name"] = hxs.xpath("//h1[@id='itemName']/text()").extract()[0]
        item["price"] = hxs.xpath("//div[@id='mss-top-price']/em/text()").extract()[0]
        aaa="hhhh"
        try:

            a= hxs.xpath("//div[@class='ytInfoTab']/text()").extract()
            aa=[]
            for i in a:

                i=i.lower()
                a=i.split(" ")

                if "info" in a:
                    aaa=i.capitalize()[:-5]
                    item["pbrand"]= i.capitalize()[:-5]
            if aaa=="" or aaa==" ":
                item["pbrand"]=hxs.xpath("//div[@class='viewMoreLinks']/a/text()").extract()[-1]
        except:
            print "Brand not found"
        category =hxs.xpath("//div[@id='breadcrumbs']//a/text()").extract()[-1]
        items.append(item)
        return items
