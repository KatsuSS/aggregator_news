from bs4 import BeautifulSoup
import aiohttp
import asyncio


class Requestor:
    def __init__(self, url):
        self.url = url # base_url = ["https://daily.afisha.ru/news/", "https://www.the-village.ru/news"]

    async def _get_page(self, session, url):
        try:
            async with session.get(url) as response:
                page_content = await response.text()
                return self._get_page_info(url, page_content)
        except aiohttp.ClientError as err:
            print(err)

    def _get_page_info(self, url, page_content):
        soup = BeautifulSoup(page_content, "lxml")
        if "the-village" in url:
            return self._get_info_village(soup)
        elif "afisha" in url:
            return self._get_info_afisha(soup)
        else:
            print("Empty")
            return []

    def _get_info_village(self, soup):
        url = "https://www.the-village.ru"
        data = {}
        ads = soup.find('div', class_="p-news").find('div', class_='block-justifier').find_all('div', class_="post-item")
        for key, ad in enumerate(ads):
            try:
                title = ad.find(["h2", "h3"], class_="post-title").getText().strip()
                link = ad.find("a", class_="post-link")['href']
                create_time = ad.find("li", class_="meta-time").getText().strip()
            except Exception as e:
                create_time = ad.find("span", class_="post-time").getText().strip()
                print(key)
                print(e)
            data[key] = {"title": title,
                         "name": "the-village",
                         "link": url + link,
                         "time": create_time}
        return data

    def _get_info_afisha(self, soup):
        url = "https://daily.afisha.ru"
        data = {}
        break_space = u'\xa0'
        ads = soup.find('div', class_="news-feed").find('div', attrs={"data-page-counter": "1"})\
            .find_all("div", class_="news-feed__item")
        for key, ad in enumerate(ads):
            try:
                title = ad.find("a", class_="news-feed__title").getText().strip().replace(break_space, ' ')
                create_time = ad.find("span", class_="news-feed__datetime").getText().strip()
                link = ad.find("a", class_="news-feed__title")['href']
            except Exception as e:
                print(e)
            data[key] = {"title": title,
                         "name": "afisha",
                         "link": url + link,
                         "time": create_time}
        return data

    async def _create_task(self, url):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for page in url:
                task = asyncio.ensure_future(self._get_page(session, page))
                tasks.append(task)
            result = await asyncio.gather(*tasks)
            return result

    def get_request(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # loop = asyncio.get_event_loop()
        data = loop.run_until_complete(self._create_task(self.url))
        return data
