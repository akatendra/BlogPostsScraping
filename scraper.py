import datetime

import os



from bs4 import BeautifulSoup

# Set up logging
import logging.config

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

blogpost_list = []
post_count = 0


def prettify_html(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.prettify()


def parse_blogpost_links(data):
    global blogpost_list
    soup = BeautifulSoup(data, 'lxml')
    items = soup.select('a[class="read--more"]')
    # logger.debug(f'items: {items}')
    for item in items:
        blogpost_list.append(item['href'])
    logger.debug('###############################################')
    logger.debug(
        f'Number of items founded on page: {len(items)}')
    logger.debug('###############################################')


def remove_file(file):
    if os.path.isfile(file):
        # os.remove() function to remove the file
        os.remove(file)
        # Printing the confirmation message of deletion
        print("File Deleted successfully")
    else:
        print("File does not exist")


def read_file(path):
    with open(path, "r") as file:
        return file.read()


def save_file(data, filename):
    with open(filename, 'a') as file:
        file.write(data)


def save_blogpost_links():
    remove_file('blogpost_list.txt')
    logger.debug(
        f'blogpost_links_list: {len(blogpost_list)} |  {blogpost_list}')
    with open('blogpost_list.txt', 'a') as file:
        for link in blogpost_list:
            file.write(link + '\n')

    remove_file('blogpost_links.txt')
    blogpost_links = set(blogpost_list)
    logger.debug(
        f'blogpost_links set: {len(blogpost_links)} | {blogpost_links}')
    with open('blogpost_links.txt', 'a') as file:
        for link in blogpost_links:
            file.write(link + '\n')
    return blogpost_links


def parse_blogpost(url, data):
    global post_count
    soup = BeautifulSoup(data, 'lxml')

    category_html = soup.select_one('span[class*="category cat--"]')
    logger.debug(f'category_html: {category_html}')
    category = None
    if category_html:
        category = category_html.text.strip()
    logger.debug(f'category: {category}')

    publish_date_html = soup.select_one('time')
    logger.debug(f'publish_date_html: {publish_date_html}')
    publish_date = None
    publish_date_obj = datetime.datetime(1981, 8, 17)
    if publish_date_html:
        publish_date = publish_date_html.text.strip()

        # Convert publish date into datetime object
        publish_date_parse = publish_date.split(',')
        publish_date_month_day = publish_date_parse[0].split()
        publish_date_month = publish_date_month_day[0].strip()
        publish_date_month = datetime.datetime.strptime(publish_date_month,
                                                        "%B").month
        publish_date_day = int(publish_date_month_day[1])
        publish_date_year = int(publish_date_parse[1])
        publish_date_obj = datetime.datetime(publish_date_year,
                                             publish_date_month,
                                             publish_date_day)
    logger.debug(f'publish_date: {publish_date}')
    logger.debug(f'publish_date_obj: {publish_date_obj}')

    author_html = soup.select_one('span[class="author"]')
    logger.debug(f'author_html: {author_html}')
    author = None
    if author_html:
        author = author_html.text.strip()
    logger.debug(f'author: {author}')

    title_html = soup.select_one('h1')
    logger.debug(f'title_html: {title_html}')
    title = None
    if title_html:
        title = title_html.text.strip()
    logger.debug(f'title: {title}')

    # article_body = soup.select_one('article')
    article = soup.select_one('div[class="col-md-8 offset-md-1"]')
    logger.debug(f'article: {article}')

    aside_p = soup.select('aside p')
    logger.debug(f'aside_p: {aside_p}')
    aside = ''
    for p in aside_p:
        aside += str(p) + '\n'
    # article += aside
    logger.debug(f'aside: {aside}')

    html_out = f'''<p><a href="{url}">{url}</a></p>
                   <p>Topic: {category}</p>
                   <p>Publish date: {publish_date}</p>
                   <p>Author: {author}</p>
                   {article}<br>
                   {aside}
                   <hr>
                '''

    logger.debug(f'html_out: {html_out}')

    return publish_date_obj, html_out


def reduce_white_spaces(string):
    string = string.replace('\n', '')
    while '  ' in string:
        string = string.replace('  ', ' ')
    return string
