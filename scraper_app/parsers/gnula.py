from typing import Set

from bs4 import BeautifulSoup

from .base import BaseParser
from posting_app.database import Posting, PostingRepository


class GnulaParser(BaseParser):
    base_info_class = 'widget-content'
    base_info_tag = 'div'
    base_info_tag_2 = 'divd'
    link_regex = 'a'
    price_regex = 'img'

    def extract_data(self) -> Set[Posting]:
        '''Extracting data and returning list of postings'''
        postings = set()
        base_info_soaps_1 = self.soup.find_all(
            self.base_info_tag, class_=self.base_info_class)

        base_info_soaps_2 = self.soup.find_all(
            self.base_info_tag_2, class_=self.base_info_class)    

        base_info_soaps = base_info_soaps_1 + base_info_soaps_2    

        for base_info_soap in base_info_soaps:
            links_container = base_info_soap.find_all('a')
            #print(links_container)
            for link in links_container:
                try:
                    link_container = link
                    #print(link_container)
                    #print(link_container['href'])
                    price_container = link_container.select(self.price_regex)[0]
                    #print(price_container)
                    #price_container = base_info_soap.select(self.price_regex)[0]
                    description_container = price_container['title']
                    #print (description_container)
                    location_container = price_container['src']

                except Exception as e:
                    print('ERROR: the regex didnt work')
                    continue

                href = link_container['href']
                #print(href)
                title = price_container['alt'].replace('Poster pequeño de ','')     
                sha = self.get_id(href)
                price = ''
                description = description_container
                location = self.sanitize_text(location_container)

                posting_repository = PostingRepository()
                if posting_repository.get_posting_by_sha(sha):
                    continue

                new_posting = Posting(
                    sha=sha,
                    url=href,
                    title=title,
                    price=price,
                    description=description,
                    location=location,
                )
                postings.add(new_posting)

        return postings
