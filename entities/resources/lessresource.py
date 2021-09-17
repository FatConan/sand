import os
import lesscpy
from entities.render_entity import RenderEntity


class LessResource(RenderEntity):
    def __init__(self, site, source, target):
        super().__init__(site, source, target)
        self.source_path = os.path.abspath(os.path.join(self.site.root, self.source))
        self.target_path = os.path.abspath(os.path.join(self.site.output_root, self.target))

    def render(self, environment):
        directory = os.path.split(self.target_path)[0]
        os.makedirs(directory, exist_ok=True)

        if os.path.isfile(self.source_path):
            if os.path.exists(self.target_path):
                os.remove(self.target_path)
            with open(self.source_path, "r") as pre:
                with open(self.target_path, "w") as compiled:
                    compiled.write(lesscpy.compile(pre, minify=True))