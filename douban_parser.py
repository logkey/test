import string
import re
import urllib.request

class DouBanSpider(object) :
    def __init__(self) :
        self.page = 1
        self.cur_url = "http://movie.douban.com/top250?start={page}&filter=&type="
        self.datas = []
        self._top_num = 1
    def get_page(self, cur_page) :
        url = self.cur_url.format(page = (cur_page - 1) * 25)
        my_page = urllib.request.urlopen(url).read().decode("utf-8")
        return my_page
    def find_title(self, my_page) :
        temp_data = []
        movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)
        for index, item in enumerate(movie_items) :
            if item.find("&nbsp") == -1 :
                temp_data.append( str(self._top_num) + "    " + item )
                self._top_num += 1
        self.datas.extend(temp_data)
    
    def start_spider(self) :
        while self.page <= 20 :
            my_page = self.get_page(self.page)
            self.find_title(my_page)
            self.page += 1
def main() :
    my_spider = DouBanSpider()
    my_spider.start_spider()
    for item in my_spider.datas :
        print (item)
main()
