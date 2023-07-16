import datetime

import rfeed


class Plugin:
    def generate_feed(self, config, pages):
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
    def parse(self, site_data, site):
        rss_config = site_data.get("rss", {})
        base_url = site_data.get("domain", "")
        pages = [(r, p) for r, p in site.page_reference.get("/", []) if p.data("rss", False)]
        pages.sort(key=lambda x: x[1].data("created"))
        page_items = []
        for route, page in pages:
            item = rfeed.Item(
                title=page.data("title", ""),
                link="%s/%s" % (base_url, route,),
                description=page.data("description", ""),
                pubDate=datetime.datetime.strptime(page.data("created"), '%Y-%m-%d %H:%M:%S'),
                guid=rfeed.Guid("%s/%s" % (base_url, route,))
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
