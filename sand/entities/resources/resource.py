from sand.entities import RenderEntity
import shutil
import os


# A PlainResource is a file that is copied from one location to another. If the target location already exists
# then it will delete the target and replace it.
class PlainResource(RenderEntity):
    def __init__(self, site, target, source, **kwargs):
        super().__init__(site, target, source, **kwargs)

    def validate(self):
        return self.source is not None and self.target is not None

    def render(self, environment, **kwargs):
        self._debug()
        directory = os.path.split(self.target_path)[0]
        os.makedirs(directory, exist_ok=True)

        if os.path.isdir(self.source_path):
            shutil.rmtree(self.target_path, ignore_errors=True)
            shutil.copytree(self.source_path, self.target_path)
        elif os.path.isfile(self.source_path):
            if os.path.exists(self.target_path):
                os.remove(self.target_path)
            shutil.copy2(self.source_path, self.target_path)

