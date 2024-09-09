import json

from sand.plugin import SandPlugin


class JavaScriptExtensions:
    def __init__(self):
        self.CDNs = {}
        self.CDN_details = {}
        self.CSSs = []
        self.scripts = []

        self.base_link = """<link rel="stylesheet" href="%s" />"""
        self.base_tag = """<script type="module" src="%(url)s" 
            integrity="%(integrity)s" 
            crossorigin="%(crossorigin)s"
            referrerpolicy="%(referrerpolicy)s"></script>"""
        self.base_importmap = """<script type="importmap">%s</script>"""

    def script_details(self, url, integrity="", crossorigin="", referrerpolicy=""):
        return  {
            "url": url,
            "integrity": integrity,
            "crossorigin": crossorigin,
            "referrerpolicy": referrerpolicy
        }

    def add_CDN(self, name, url, integrity="", crossorigin="", referrerpolicy=""):
        self.CDN_details[name] = self.script_details(url, integrity, crossorigin, referrerpolicy)
        self.CDNs[name] = url

    def add_css(self, url):
        self.CSSs.append(url)

    def add_script(self, url):
        self.scripts.append(url)

    def headers(self):
        headers = []

        for url in self.CSSs:
            headers.append(self.base_link % url)

        headers.append(self.base_importmap % json.dumps({"imports": self.CDNs}))

        for name, details in self.CDN_details.items():
            headers.append(self.base_tag % details)

        for url in self.scripts:
            headers.append(self.base_tag % self.script_details(url))

        return "\n".join(headers)


class Plugin(SandPlugin):
    def __init__(self):
        self.es6css = JavaScriptExtensions()

    def configure(self, site_data, site):
        es6css_config = site_data.get("es6css")
        for css in es6css_config.get("CSS", []):
            self.es6css.add_css(css)

        for cdn in es6css_config.get("CDN", []):
            self.es6css.add_CDN(cdn.get("alias"), cdn.get("src"),
                                cdn.get("integrity", ""),
                                cdn.get("crossorigin", ""),
                                cdn.get("referrerpolicy", ""))

        for script in es6css_config.get("scripts", []):
            self.es6css.add_script(script)

    def add_render_context(self, page, environment, data):
        data["ES6CSS"] = self.es6css
