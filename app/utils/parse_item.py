
def parse_item(item):
    def get(tag):
        el = item.find(tag)
        return el.text.strip() if el is not None and el.text else ""

    title = get("title")
    link = get("link")

    content = (
        get("description") or
        get("{http://purl.org/rss/1.0/modules/content/}encoded")
    )

    return title, link, content

