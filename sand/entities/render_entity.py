import os


class RenderEntity(object):
    def __init__(self, site, source, target, **kwargs):
        self.site = site
        self.source = source
        self.target = target

        if self.source is not None:
            try:
                self.source_file = os.path.split(self.source)[-1]
            except IndexError:
                self.source_file = source
        else:
            self.source_file = None

        try:
            self.target_file = os.path.split(self.target)[-1]
        except IndexError:
            self.target_file = target

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.source, self.target)

    def as_dict(self):
        return {}

    def render(self, environment, **kwargs):
        print("No-op renderer selected, please check your configuration")