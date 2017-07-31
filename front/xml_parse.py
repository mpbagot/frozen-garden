import re

class XMLParser:
    def __init__(self, text):
        self.text = text
        self.tree = []
        self.evaluate()

    def evaluate(self):
        '''
        Generate the tag tree from the text
        '''
        node = XMLNode(self.text)
        node.evaluate()
        self.tree = node.tags


class XMLNode:
    def __init__(self, raw_data):
        self.data = raw_data
        self.tags = []

    def evaluate(self):
        # Remove new lines from the svg file
        data = ' '.join(self.data.split('\n'))
        # Pull all of the XML tags from the SVG file
        tags = [a for a in re.findall('<.+?>', data) if not a.startswith('<?') and not a.startswith('<!')]

        # Pull the tag types out of the tags
        tag_types = [a[1:-1].split()[0] for a in tags]
        opening = None
        # Iterate all of the tags
        for i, tag in enumerate(tag_types):
            if opening == None and not tag.startswith('/'):
                # open the tag and begin recording data
                opening = (i, tag)
            if opening and (tag == '/'+opening[1] or tags[opening[0]].endswith('/>')):
                inner_text = ''
                if tag != opening[1]:
                    # Close the tag and pull all of the data in
                    inner_text = ''.join(tags[opening[0]+1:i])
                # If its a closing tag, then clip the tag type
                if tag.startswith('/'):
                    tag = tag[1:]
                # Add a top-level tag to the tag list
                self.tags.append(TagNode(tag, self.getAttributes(tags[opening[0]]), inner_text))
                opening = None
        # Iterate and parse each tag
        for tag in self.tags:
            tag.evaluate()

    def getAttributes(self, tag):
        tag = tag[1:-1]
        attrs = re.findall(r'[^ \t]+?=".+?"', tag)
        attr_dict = {}
        for a in attrs:
            a = a.strip().split('=')
            attr_dict[a[0]] = a[1][1:-1]
        return attr_dict

class TagNode:
    def __init__(self, name, attrs, inner_text):
        self.attributes = attrs
        self.name = name
        self.inner_text = inner_text
        self.children = []

    def __str__(self):
        return 'Tag(type={}, inner_text="{}", attributes="{}")'.format(self.name, self.inner_text, self.attributes)

    def evaluate(self):
        '''
        Parse the attributes of the tag and check for validity
        '''
        if self.inner_text:
            node = XMLNode(self.inner_text)
            node.evaluate()
            self.children = node.tags
