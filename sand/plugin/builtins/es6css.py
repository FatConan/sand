import json
from urllib.parse import urljoin

from sand.plugin import SandPlugin

SCRIPT_ATTRS = ["alias", "src",  "async", "crossorigin",  "defer", "integrity",  "nomodule", "referrerpolicy", "data"]

class JavaScriptExtensions:
    def __init__(self, base_url, force_base_url=False):
        self.base_url = base_url
        self.force_base_url = force_base_url
        self.CDNs = {}
        self.CDN_details = {}
        self.CSSs = []
        self.scripts = []

        self.base_link = """<link rel="stylesheet" href="{src}" />"""
        self.base_tag = """<script {extras}>{content}</script>"""
        self.base_importmap = """<script type="importmap">{map}</script>"""
        self.base_style = """<style>{content}</style>"""


    def script_details(self, src,  _type, _async="", crossorigin="",  defer="", integrity="",  nomodule="", referrerpolicy="", data=None):
        details = {
            "src": self.rebased_url(src),
            "type": _type,
            "async": _async,
            "crossorigin": crossorigin,
            "defer": defer,
            "integrity": integrity,
            "nomodule": nomodule,
            "referrerpolicy": referrerpolicy
        }

        if data is not None:
            for key, value in data.items():
                details["data-%s" % key] = value

        return details

    def rebased_url(self, url):
        url = url.strip()

        #if there's nothing to prepend, just return the original
        if not self.base_url:
            return url
        # if it looks fully qualified, just return it
        elif url.startswith("https://") or url.startswith("http://") or url.startswith("//"):
            return url
        #If we're forcing a base url
        elif self.force_base_url:
            relative_url = url
            if url.startswith("/"):
                relative_url = "." + url
            return urljoin(self.base_url, relative_url)
        else:
            #Otherwise leave it alone
            return url

    def add_CDN(self, alias="", src="", _async="", crossorigin="",  defer="", integrity="",  nomodule="", referrerpolicy="", data=None):
        self.CDN_details[alias] = self.script_details(src, "module", _async, crossorigin, defer, integrity, nomodule, referrerpolicy)
        self.CDNs[alias] = src

    def add_css(self, url):
        self.CSSs.append(self.rebased_url(url))

    def add_script(self, src="",  _async="", crossorigin="",  defer="defer", integrity="",  nomodule="", referrerpolicy="", data=None):
        self.scripts.append(self.script_details(src, "module", _async, crossorigin, defer, integrity, nomodule, referrerpolicy))

    def tag(self, details_dict):
        return self.base_tag.format(extras=" ".join(['%s="%s"' % (key, value) for key, value in details_dict.items() if value]), content="")

    def fouc_css(self):
        return self.base_style.format(content="html.hidden{display: none;}")

    def fouc_script(self):
        load_function = """
        const htmlEl = document.getElementsByTagName("html")[0];
        let classes = htmlEl.getAttribute("class") + " hidden";
        htmlEl.setAttribute("class", classes);
        document.addEventListener("DOMContentLoaded", () => {
            let classes = htmlEl.getAttribute("class");
            htmlEl.setAttribute("class", classes.replace("hidden", "")); 
        });
        """
        return self.base_tag.format(extras="", content=load_function)

    def headers(self, libraries_only=False):
        headers = []

        for url in self.CSSs:
            headers.append(self.base_link.format(src=url))

        headers.append(self.base_importmap.format(map=json.dumps({"imports": self.CDNs})))

        for name, details in self.CDN_details.items():
            headers.append(self.tag(details))

        if not libraries_only:
            for details in self.scripts:
                headers.append(self.tag(details))

        return "\n".join(headers)

    def script_footer(self):
        footers = []
        for details in self.scripts:
            footers.append(self.tag(details))

        return "\n".join(footers)

class Plugin(SandPlugin):
    def __init__(self):
        self.es6css = None

    def configure(self, site_data, site):
        es6css_config = site_data.get("es6css", {})
        self.es6css = JavaScriptExtensions(site.base_url, es6css_config.get("force_base_url", False))

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
