import re
import json
import streamlit as st

from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup, ResultSet, PageElement


class WikiCrawler:

    def __init__(self):
        self.documents = {}
        self.links = []
        self.tags_start = re.compile(r"<[^<]+>")
        self.tags_end = re.compile(r"<[^<]+>")
        self.references = re.compile(r"\[\d+\]")

    def get_random_page(self):
        '''
        Obtains a random page from the wiki smaller web page
        '''
        return 'https://en.m.wikipedia.org/wiki/Special:Random'

    def get_title(self, page):
        '''
        Gets page title
        '''
        try:
            return page.find('h1', {'id': 'section_0'}).text
        except:
            return page.find('h1', {'id': 'firstHeading'}).text

    def get_links_in_paragraph(self, paragraph):
        '''
        Gets links from a paragraph
        '''
        links = paragraph.find_all('a')

        return [link['href'] for link in links if 'href' in links and link['href'].startswith('https://en.m.wikipedia.org/wiki/')]

    def go_to_link(self, url):
        '''
        Go to page specified in url
        '''
        req = urlopen(url)
        soup = BeautifulSoup(req, 'html.parser')
        return soup

    def get_links(self, page):
        '''
        Get all links in page and adds it to self.links
        '''
        # get the main body text
        body = page.find('div', {'id': 'mw-content-text'})

        paragraphs = body.findChildren(['p', 'ul', 'li'])
        for p in paragraphs:
            self.links.extend(self.get_links_in_paragraph(p))

    def get_document_info(self, page):
        '''
        Gets the document information of the wiki article for 
        simplicity, only the summary of the article is stored
        '''
        title = self.get_title(page)
        summary = page.find('section', {'class': 'mf-section-0'})

        paragraphs: ResultSet = summary.findChildren(['p'])
        paragraphs_list = []
        for p in paragraphs:
            p: PageElement
            text = str(p)
            text = self.tags_start.sub('', text)
            text = self.tags_end.sub('', text)
            text = self.references.sub('', text)
            text = text.replace('\n', '')
            paragraphs_list.append(text)

        summary_text = '\n'.join(paragraphs_list)
        self.documents[title] = summary_text

    def crawl(self, n=20):
        try:
            for _ in range(n):
                if len(self.links) == 0:
                    self.links.append(self.get_random_page())
                link = self.links.pop()
                page = self.go_to_link(link)
                self.get_document_info(page)
                self.get_links(page)

            self.save_documents()
            st.write(self.documents)
            return True
        except:
            st.write('Error de conexión')
            return False

    def save_documents(self):
        try:
            json.dump(self.documents, open(Path(
                '../collections/wiki_docs.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        except FileNotFoundError:
            json.dump(self.documents, open(Path(
                '../collections/wiki_docs.json'), 'x', encoding='utf-8'), ensure_ascii=False)


if __name__ == '__main__':
    WikiCrawler().crawl(10)
