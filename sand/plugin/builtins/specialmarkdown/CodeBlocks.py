import re
import xml.etree.ElementTree as ET
from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.blockparser import BlockParser

class BoxBlockProcessor(BlockProcessor):
    RE_DEFAULT_OPEN = "{% "
    RE_DEFAULT_CLOSE = "%}"
    RE_FENCE_START_TEMPLATE = r'^\s*(?P<start>%s)(?P<type>[^\. \n]+)[^\. \n]*(?P<class_names>\.{0,1}[^\n]*)'
    RE_FENCE_END_TEMPLATE = r'[\n\s]*(?P<end>%s)[\n\s]*$'

    KNOWN_TYPES = {
        "as": {"tag": "aside", "classes":""},
        "ar": {"tag": "article", "classes":""},
        "d":  {"tag": "div", "classes":""},
        "s":  {"tag": "section", "classes":""},
    }

    def __init__(self, parser: BlockParser, config_options):
        self.debug = config_options.get("debug", False)

        if "types" in config_options:
            if self.debug:
                print("Introducing new types:", config_options.get("types"))
            self.KNOWN_TYPES |= config_options.get("types", {})

        self.open_tag = self.RE_DEFAULT_OPEN
        self.close_tag = self.RE_DEFAULT_CLOSE

        if "tags" in config_options:
            tags = config_options.get("tags")
            if self.debug:
                print("Configuring new tags:", tags)

            self.open_tag = tags.get("open", self.RE_DEFAULT_OPEN)
            self.close_tag = tags.get("close", self.RE_DEFAULT_CLOSE)


        self.RE_FENCE_START = self.RE_FENCE_START_TEMPLATE % self.open_tag
        self.RE_FENCE_END = self.RE_FENCE_END_TEMPLATE % self.close_tag

        self.depth = 0
        self.element_tree = []
        self.completed = False

        super().__init__(parser)

    def test(self, parent, block):
        return self.is_start(block)[0]

    def render_element(self, parent, box_type, class_names):
        element = self.KNOWN_TYPES.get(box_type, {"tag":"div", "classes":""})
        if self.debug:
            print("Selected Element", element)
        e = ET.SubElement(parent, element.get("tag", "div"))
        classes = "%s %s" % (element.get("classes", ""), class_names)
        if classes:
            e.set('class', classes)
        return e

    def render(self, parent, groups):
        box_type = groups.get("type", "")
        class_names = groups.get("class_names", "").strip()[1:]
        return self.render_element(parent, box_type, class_names)

    def is_start(self, block):
        start_match = re.match(self.RE_FENCE_START, block)
        return (start_match is not None, start_match)

    def is_end(self, block):
        end_match = re.match(self.RE_FENCE_END, block)
        return (end_match is not None, end_match)

    def open_block(self, parent, block, start_match):
        groups = start_match.groupdict()
        new_element = self.render(parent, groups)
        self.depth += 1
        self.element_tree.append(new_element)

        active_block = re.sub(self.RE_FENCE_START, '', block)
        if active_block:
            self.parser.parseBlocks(new_element, [active_block])
        return new_element

    def close_block(self, parent):
        restored_element = parent

        if self.depth:
            self.depth -= 1
            self.element_tree = self.element_tree[:-1]

            if self.element_tree:
                restored_element = self.element_tree[-1]
        return restored_element

    def process(self, parent, blocks):
        counter = 0
        continued = []

        for block_num, block in enumerate(blocks):
            start = self.is_start(block)
            end = self.is_end(block)
            counter = block_num

            if start[0]:
                if continued:
                    self.parser.parseBlocks(parent, continued)
                    continued = []
                if self.debug:
                    print("Start an element", counter, start[1].groupdict().get("type"))
                parent = self.open_block(parent, block, start[1])

            elif end[0]:
                if self.debug:
                    print("end an element", counter)
                if continued:
                    self.parser.parseBlocks(parent, continued)
                    continued = []

                parent = self.close_block(parent)
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)

                if not self.depth:
                    break
            else:
                if self.debug:
                    print("Continue", counter)
                continued.append(block)

        for i in range(0, counter):
            blocks.pop(0)

        return False

    def run(self, parent, blocks):
        return self.process(parent, blocks)


class BoxExtension(Extension):
    def __init__(self, config_options):
        super().__init__()
        self.config_options = config_options

    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(BoxBlockProcessor(md.parser, self.config_options), 'box', 175)
