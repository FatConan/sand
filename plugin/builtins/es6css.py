import json


class JavaScriptExtensions:
    def __init__(self):
        self.CDNs = {}
        self.CSSs = []

        self.base_link = """<link rel="stylesheet" href="%s" />"""
        self.base_tag = """<script type="module" src="%s"></script>"""
        self.base_importmap = """<script type="importmap">%s</script>"""

    def add_CDN(self, name, url):
        self.CDNs[name] = url

    def add_css(self, url):
        self.CSSs.append(url)

    def headers(self):
        headers = []

        for url in self.CSSs:
            headers.append(self.base_link % url)

        headers.append(self.base_importmap % json.dumps({"imports": self.CDNs}))

        for name, url in self.CDNs.items():
            headers.append(self.base_tag % url)

        return "\n".join(headers)


class Plugin:
    def __init__(self):
        self.es6css = JavaScriptExtensions()

    def configure(self, site_data, site):
        es6css_config = site_data.get("es6css")
        for css in es6css_config.get("CSS", []):
            self.es6css.add_css(css)

        for cdn in es6css_config.get("CDN", []):
            self.es6css.add_CDN(cdn.get("alias"), cdn.get("src"))

    def parse(self, site_data, site):
        pass

    def add_render_context(self, page, environment, data):
        data["ES6CSS"] = self.es6css