import os
import re
import pdb

def is_chinese(c):
    return '\u4e00' <= c <= '\u9fff'

def parse(text):
    """
        Read in poem and parse it to standard format
    """
    text = text.strip()
    poems = []
    lines = re.sub(r'^\s*', '', text).split('\n')
    if len(lines) <= 1:
        return None
    hline = lines[0].replace('【', ' ').replace('】', ' ').strip()
    headers = re.sub(r'\s+', ' ', hline).split(' ')
    volume = headers[0]
    if len(headers) >= 2:
        # only volume
        title = headers[1]
    else:
        title = None
    if len(headers) >= 3:
        author = headers[2]
    else:
        author = None
    # try:
    #     headers[1]
    # except:
    #     pdb.set_trace()
    content = ''
    for line in lines[1:]:
        if line != '':
            content += line
        else:
            if content == '':
                continue
            else:
                poem = {}
                poem['title'] = title
                poem['author'] = author
                poem['content'] = content
                poem['volume'] = volume
                poems.append(poem)
                content = ''
    poem = {}
    poem['title'] = title
    poem['author'] = author
    poem['content'] = content
    poem['volume'] = volume
    poems.append(poem)
    return poems