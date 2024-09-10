import json

from sand.plugin import SandPlugin

SCRIPT_ATTRS = ["alias", "src",  "async", "crossorigin",  "defer", "integrity",  "nomodule", "referrerpolicy"]

class JavaScriptExtensions:
    def __init__(self):
        self.CDNs = {}
        self.CDN_details = {}
        self.CSSs = []
        self.scripts = []

        self.base_link = """<link rel="stylesheet" href="%s" />"""
        self.base_tag = """<script type="module" %s></script>"""
        self.base_importmap = """<script type="importmap">%s</script>"""

    def script_details(self, src,  _async="", crossorigin="",  defer="", integrity="",  nomodule="", referrerpolicy=""):
        return  {
            "src": src,
            "async": _async,
            "crossorigin": crossorigin,
            "defer": defer,
            "integrity": integrity,
            "nomodule": nomodule,
            "referrerpolicy": referrerpolicy
        }

    def add_CDN(self, alias="", src="", _async="async", crossorigin="",  defer="", integrity="",  nomodule="", referrerpolicy=""):
        self.CDN_details[alias] = self.script_details(src, _async, crossorigin, defer, integrity, nomodule, referrerpolicy)
        self.CDNs[alias] = src

    def add_css(self, url):
        self.CSSs.append(url)

    def add_script(self, src="",  _async="", crossorigin="",  defer="defer", integrity="",  nomodule="", referrerpolicy=""):
        self.scripts.append(self.script_details(src, _async, crossorigin, defer, integrity, nomodule, referrerpolicy))

    def tag(self, details_dict):
        return self.base_tag % " ".join(['%s="%s"' % (key, value) for key, value in details_dict.items() if value])

    def headers(self):
        headers = []

        for url in self.CSSs:
            headers.append(self.base_link % url)

        headers.append(self.base_importmap % json.dumps({"imports": self.CDNs}))

        for name, details in self.CDN_details.items():
            headers.append(self.tag(details))

        for details in self.scripts:
            headers.append(self.tag(details))

        return "\n".join(headers)


class Plugin(SandPlugin):
    def __init__(self):
        self.es6css = JavaScriptExtensions()

    def configure(self, site_data, site):
        es6css_config = site_data.get("es6css")
        for css in es6css_config.get("CSS", []):
            self.es6css.add_css(css)

        for cdn in es6css_config.get("CDN", []):
            self.es6css.add_CDN(**self.grab_script_details(cdn))

        for script in es6css_config.get("scripts", []):
            self.es6css.add_script(**self.grab_script_details(script))

    def grab_script_details(self, script):
        if isinstance(script, str):
            return {"src": script}

        script_attrs = {}
        if isinstance(script, dict):
            for attr in SCRIPT_ATTRS:
                if script.get(attr, None) is not None:
                    script_attrs[attr] = script.get(attr)
        return script_attrs

    def add_render_context(self, page, environment, data):
        data["ES6CSS"] = self.es6css
