import scrapy
import re

class VerkkokauppaScraperSpider(scrapy.Spider):
    name = 'verkkokauppa_scraper'
    allowed_domains = ['verkkokauppa.com']
    start_urls = ['https://www.verkkokauppa.com/fi/product/332585/Plantronics-Voyager-5200-Bluetooth-kuuloke/reviews']
    
    def parse(self, response):
        
        #Review text saved into string
        review_texts = response.css('[class="review-content-wrapper"] > p::text').extract()

        #Review ratings saved into string
        review_ratings = response.css('[class="review-content__ratings"] > div > div').extract()
        
        #Parse review ratings with format "Arvosana x/x" from html code. Every text review includes four ratings
        for i in range(len(review_ratings)):
            review_ratings[i] = re.findall('[A-Za-z]{8}[ ][0-5][/][0-5]', review_ratings[i])

        #review texts and ratings saved into vector -> returned from function
        for i in range(len(review_texts)):
            review = {
                'text' : review_texts[i],
                'rating': review_ratings[i]
            }
            yield review
        
        #counter for pages
        counter = 1
        max_pages = 3
        
        if(counter <= max_pages): 
            #Moving to next page
            next_page_url = "https://www.verkkokauppa.com/fi/product/332585/Plantronics-Voyager-5200-Bluetooth-kuuloke/reviews?page=" + str(counter)
            counter += 1
            yield response.follow(next_page_url, self.parse)