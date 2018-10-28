from render_entity import RenderEntity
import shutil
import os


class PlainResource(RenderEntity):
    def __init__(self, site_root, source, target, resource_type=None):
        super().__init__(site_root, source, target)
        self.source_path = os.path.abspath(os.path.join(self.site_root, self.source))
        self.target_path = os.path.abspath(os.path.join(self.site_root, self.target))

    def render(self, environment):
        directory = os.path.split(self.target_path)[0]
        os.makedirs(directory, exist_ok=True)

        if os.path.isdir(self.source_path):
            shutil.rmtree(self.target_path, ignore_errors=True)
            shutil.copytree(self.source_path, self.target_path)
        elif os.path.isfile(self.source_path):
            if os.path.exists(self.target_path):
                os.remove(self.target_path)
            shutil.copy2(self.source_path, self.target_path)
