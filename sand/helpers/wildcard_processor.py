import glob
import re
import os
import warnings


WILDCARD_RE = re.compile(r"([^\*]*)\*([\.]{0,1}.*)")

class ProcessedWildcard:
    def __init__(self, source, target, wildcard_filename=None):
        self.source = source
        self.target = target
        self.wildcard_filename = wildcard_filename

    def is_wild(self):
        return self.wildcard_filename is not None


def process_wildcards(source, target, site):
    source_match = WILDCARD_RE.match(source)
    target_match = WILDCARD_RE.match(target)
    replacements = []

    if source_match and target_match:
        listed_sources = glob.glob(os.path.abspath(os.path.join(site.root, source)))
        for list_source in listed_sources:
            pre, post = source_match.groups()
            filename = os.path.split(list_source)[-1].replace(post, "")

            replace_target = target.replace("*", filename)
            replace_source = source.replace("*", filename)
            replacements.append(ProcessedWildcard(replace_source, replace_target, filename))
        return replacements
    elif source_match or target_match:
        warnings.warn("Badly formed source and target pairing, %s and %s", (source, target))
    else:
        return [ProcessedWildcard(source, target)]
