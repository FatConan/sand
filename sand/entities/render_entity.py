import os
import warnings

class RenderEntity(object):
    def __init__(self, site, source, target, **kwargs):
        self.site = site
        self.source = source
        self.target = target

        self.source_file = self.extract_filename(self.source)
        self.target_file = self.extract_filename(self.target)

        self.source_path = self.default_path(self.source)
        self.target_path = self.default_path(self.target, is_output=True)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.source, self.target)

    def validate(self):
        """
        Perform a check to see if there's sufficient information to render the entity. In the base class
        we'll simply check that a target is defined, which is about as cursory as we can get.

        :return: A boolean indicating whether the entity meets the requirements to be rendered
        """

        return self.target is not None and self.target != ""

    def as_dict(self):
        return {}

    def extract_filename(self, path):
        """
        Extract the filename form the provided path

        :param path: The file path
        :return: The truncated filename or None if the provided path is None
        """

        filename = None

        if path is not None:
            try:
                filename = os.path.split(path)[-1]
            except IndexError:
               filename = path

        return filename

    def default_path(self, path, is_output=False):
        root = self.site.root
        if is_output:
            root = self.site.output_root

        if path is not None:
            return os.path.abspath(os.path.join(root, path))
        return None

    def render(self, environment, **kwargs):
        warnings.warn("No-op renderer selected, please check your configuration")