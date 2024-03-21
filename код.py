import scrapy
from requests_html import HTMLSession
import csv
class Spider(scrapy.Spider):
    name = 'spider'
    def start_requests(self):
        text = getattr(self, 'text', 'football')
        link_list = make_URL_2(text)
        with open('links2.txt', 'w') as f:
            with open('text.txt', 'w') as f:
                with open('links.txt', 'w') as f:
                    numder =0
        number = 10
        link_list = find_correct_URL(link_list, number)
        print(link_list)
        for url in link_list:
            if "http" in url and "google.com" not in url:
                with open('text.txt', 'a') as f:
                    f.write(url + '\n')
                yield scrapy.Request(url, self.parse)
                with open('links2.txt', 'a') as file:
                    file.write(url + '\n')
        save_in_file()
        

    def parse(self, response):
        links = response.css('a::attr(href)').getall()
        with open('links.txt', 'a') as f:
            f.write('main link' + '\n')
            for link in links:
                f.write(response.urljoin(link) + '\n')
        title = response.css('title::text').get()
        paragraphs = response.css('p::text').getall()
        text = ' '.join(paragraphs)
        with open('text.txt', 'a') as f:
            f.write(f'Title: {title}\n\n')
            f.write(text)
        headers = response.css('body::text').getall()
        with open('text.txt', 'a') as f:
           f.write('\n'.join(headers) + '\n')

    

def make_URL(text):
    parts = text.split()
    yandex_text = "https://yandex.ru/search/?text="
    end = "&lr=2"
    words = "+".join(parts)
    return yandex_text+words+end

def make_URL_2(text):
    session = HTMLSession()
    r = session.get("https://www.google.com/search", params={"q": text})
    data = r.html.absolute_links
    return list(data)

def find_correct_URL(link_list, number):
        correct=[]
        string = "url="
        count = 0
        for link in link_list:
            if string in link:
                correct.append(link[link.find('url=')+4 :link.find('&ved')])
                if count==number:
                    return correct
                count +=1
        return correct
    
def save_in_file(): 
    with open('links2.txt', 'r') as in_file:
        parts = (line.strip() for line in in_file)
        lines = (line.split(",") for line in parts if line)
        with open('1.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            name = "links"
            writer.writerow([name])
            for line in lines:
                writer.writerow(line)