import sys
import textwrap

import requests
import lxml.html


def pretty(block):
    wrapper = textwrap.TextWrapper(
        subsequent_indent="    ",
        initial_indent="     ",
        width=80,
    )
    return "\n".join(wrapper.wrap(block))


def lxmlize(path):
    response = requests.get(path)
    page = lxml.html.fromstring(response.text)
    page.make_links_absolute(path)
    return page


def page_to_jargon(page):
    doc = lxmlize(page)
    article ,= doc.xpath("//h1")
    article = article.text_content()
    lines = ":{}:\n".format(article) + "\n\n".join([
        pretty(x.text_content().strip()) for x in
        doc.xpath("//h1/following-sibling::p[following::hr]")
    ]) + "\n"
    return lines


def iterpages(page):
    doc = lxmlize(page)
    for href in doc.xpath("//a[contains(@href, '//HTML/')]/@href"):
        sys.stderr.write(href)
        sys.stderr.write("\n")
        sys.stderr.flush()

        yield page_to_jargon(href)



for page in iterpages("http://xlinux.nist.gov/dads//ui.html"):
    print(page)

