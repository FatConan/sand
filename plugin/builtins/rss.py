import datetime
import json

import rfeed


class Plugin:
    @staticmethod
    def generate_feed(config, pages):
        feed = rfeed.Feed(
            title=config.get("title", ""),
            link=config.get("link", ""),
            description=config.get("description", ""),
            language=config.get("language", "en-US"),
            lastBuildDate=datetime.datetime.now(),
            items=pages,
        )
        return feed.rss()

    def configure(self, site_data, site):
        pass

    # Called during the parsing phase of the processing
    @staticmethod
    def process_pages(page_reference):
        def bool_of(string):
            if not isinstance(string, str):
                return string
            return json.loads(string.lower())

        rss_pages = []
        for base_route, pages in page_reference.items():
            for route, page in pages:
                if page.data("rss", False, lambda v: bool_of(v)):
                    rss_pages.append((page.target_url, page))
        return rss_pages

    def parse(self, site_data, site):
        rss_config = site_data.get("rss", {})
        base_url = site_data.get("domain", "")
        if base_url[len(base_url) - 1] == "/":
            base_url = base_url[:-1]
        pages = self.process_pages(site.page_reference)
        pages.sort(key=lambda x: x[1].data("created", "1970-01-01 00:00:00"))
        page_items = []
        for route, page in pages:
            item = rfeed.Item(
                title=page.data("title", ""),
                link="%s%s" % (base_url, route,),
                description=page.data("description", ""),
                pubDate=datetime.datetime.strptime(page.data("created", "1970-01-01 00:00:00"), '%Y-%m-%d %H:%M:%S'),
                guid=rfeed.Guid("%s%s" % (base_url, route,))
            )
            page_items.append(item)

        rss_content = self.generate_feed(rss_config, page_items)
        out_path = "./rss.xml"
        page_dict = {'source': None, 'target': out_path, "page_type": "RAW"}
        page_dict["config"] = {
            "jinja_pass": False,
            "is_index": False,
            "static_content": rss_content
        }
        site.add_page(page_dict)

    def add_render_context(self, page, environment, data):
        pass
