import time
import datetime
import os

# Set up logging
import logging.config

import request
import scraper
import word


logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def spent_time():
    global start_time
    sec_all = time.time() - start_time
    if sec_all > 60:
        minutes = sec_all // 60
        sec = sec_all % 60
        time_str = f'| {int(minutes)} min {round(sec, 1)} sec'
    else:
        time_str = f'| {round(sec_all, 1)} sec'
    start_time = time.time()
    return time_str


def get_html(url):
    # html = request.get_request(url)
    html = request.get_request_proxy(url)
    # html = scraper.prettify_html(html)
    return html


def get_blogpost_links():
    url = 'https://www.svpg.com/articles/'
    for i in range(1, 28):
        url_cat = url + 'page/' + str(i) + '/'
        logger.debug(f'url_cat: {url_cat}')
        html = get_html(url_cat)
        # logger.debug(f'html: {html}')
        scraper.parse_blogpost_links(html)
    return scraper.save_blogpost_links()


def get_blogpost(url):
    html = get_html(url)
    return html


if __name__ == '__main__':
    time_begin = start_time = time.time()
    #####################################
    # get blogpost links by requests
    #####################################
    # get_blogpost_links()
    # logger.debug(f'{spent_time()}')
    #####################################

    # TEST
    # url = 'https://www.svpg.com/the-foundation-of-product/'
    # data = get_html(url)
    # data = scraper.parse_blogpost(url, data)
    # # scraper.save_file(data, 'article.html')
    # word.save_html_to_word(data, 'article.docx')
    # TEST

    # Read blogpost links from file
    with open('blogpost_list.txt', 'r') as file:
        blogpost_links = []
        for line in file.readlines():
            blogpost_links.append(line.replace('\n', ''))
    logger.debug(f'blogpost_links: {len(blogpost_links)} | {blogpost_links}')


    # Save all articles in html for parsing
    # for link in blogpost_links:
    #     data = get_html(link)
    #     filename = f"articles/{link.replace('https://www.svpg.com/', '').replace('/', '')}.html"
    #     logger.debug(f'filename: {filename}')
    #     scraper.save_file(data, filename)

    # Read all files in directory and parse
    data_out = []
    for filename in os.listdir('articles'):
        logger.debug(f'filename: {filename}')

        url = f"https://www.svpg.com/{filename.split('.')[0]}/"
        logger.debug(f'url: {url}')

        path = os.path.join('articles', filename)
        logger.debug(f'path: {path}')

        data = scraper.read_file(path)

        data = scraper.parse_blogpost(url, data)
        data_out.append(data)
        # word.append_html_to_word(data, 'article.docx')

    data_out_sorted = sorted(data_out, key=lambda item: item[0], reverse=True)
    logger.debug(f'data_out_sorted: {data_out_sorted}')
    post_count = 0
    for data in data_out_sorted:
        post_count += 1
        write_data = f'<p>Post #{post_count}</p>' + data[1]
        word.append_html_to_word(write_data, 'article.docx')
    # word.save_html_to_word(data_out, 'article.docx')


    logger.debug(f'{spent_time()}')
