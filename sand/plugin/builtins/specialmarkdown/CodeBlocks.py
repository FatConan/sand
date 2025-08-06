import re
import xml.etree.ElementTree as ET
from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.blockparser import BlockParser

class BoxBlockProcessor(BlockProcessor):
    RE_FENCE_START = r'^\s*(?P<start>==[=]*)(?P<type>[^ =\n]+)[^ =\n]*(?P<class_names>\.[^=\n]*)'
    RE_FENCE_END = r'[\n\s]*(?P<end>==[=]*)[\n\s]*$'
    RE_FENCE_END_SPECIFIC = r'[\n\s]*%s[\n\s]*$'
    KNOWN_TYPES = {
        "as": "aside",
        "ar": "article",
        "d": "div",
        "s": "section"
    }

    def __init__(self, parser: BlockParser):
        super().__init__(parser)
        self.closing_tags = []
        self.levels = []
        self.completed = False

    def test(self, parent, block):
        return self.is_start(block)[0]

    @staticmethod
    def render_element(parent, box_type, class_names):
        element = BoxBlockProcessor.KNOWN_TYPES.get(box_type, "div")
        e = ET.SubElement(parent, element)
        e.set('class', class_names)
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
        self.closing_tags.append(groups.get("start"))
        self.levels.append(new_element)

        active_block = re.sub(self.RE_FENCE_START, '', block)
        if active_block:
            self.parser.parseBlocks(new_element, [active_block])

        return new_element

    def close_block(self, parent, block, end_match):
        groups = end_match.groupdict()
        end_group = groups.get("end")
        restored_element = parent

        if self.closing_tags and end_group == self.closing_tags[-1]:
            self.closing_tags = self.closing_tags[:-1]
            self.levels = self.levels[:-1]

            if self.levels:
                restored_element = self.levels[-1]

        block = ""
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
                print("Start an element", counter)
                parent = self.open_block(parent, block, start[1])

            elif end[0]:
                print("end an element", counter)
                if continued:
                    self.parser.parseBlocks(parent, continued)
                    continued = []

                parent = self.close_block(parent, block, end[1])
                blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)

                if not self.closing_tags:
                    break
            else:
                print("Continue", counter)
                continued.append(block)

        for i in range(0, counter):
            blocks.pop(0)

        return False

    def run(self, parent, blocks):
        return self.process(parent, blocks)


class BoxExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(BoxBlockProcessor(md.parser), 'box', 175)
