class RenderEntity(object):
    def __init__(self, site, source, target):
        self.site = site
        self.source = source
        self.target = target

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.source, self.target)

    def as_dict(self):
        return {}

    def render(self, environment):
        pass