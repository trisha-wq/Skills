"""Remove decorative Premium numbering without rewriting other HTML."""
import html
import re
from html.parser import HTMLParser

POLICY = 'unnumbered-v1'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class NumberingParser(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.source = source
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer('\n', source))
        self.stack, self.edits, self.kinds = [], [], set()
        self.scope = None
        self.feed(source)

    def source_position(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set(attrs.get('class', '').split())
        if self.scope is None and 'premium-template' in classes:
            self.scope = next(c for c in attrs['class'].split() if c != 'premium-template')
        if tag not in VOID:
            self.stack.append((tag, attrs, self.source_position(), self.source_position() + len(self.get_starttag_text())))

    def handle_endtag(self, tag):
        index = next((i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i][0] == tag), None)
        if index is None:
            return
        _, attrs, start, inner_start = self.stack[index]
        inner = self.source[inner_start:self.source_position()]
        ancestors = self.stack[:index]
        classes = set(attrs.get('class', '').split())
        ancestor_classes = {c for _, a, _, _ in ancestors for c in a.get('class', '').split()}
        kind = None
        if tag == 'span' and re.fullmatch(r'\s*\d+\s*', html.unescape(inner)):
            if 'pfg-resource-number' in classes:
                kind = 'resource'
            elif 'srs-partner-index' in classes:
                kind = 'partner'
            elif 'pfg-service-number' in ancestor_classes:
                kind = 'service'
            elif 'pfg-path-tabs' in ancestor_classes:
                kind = 'tab'
            elif 'pfg-event-topics' in ancestor_classes:
                kind = 'event'
            if kind:
                self.edits.append((start, self.source_position() + len('</span>'), ''))
        elif tag == 'span' and 'pfg-step' in ancestor_classes:
            label = re.fullmatch(r'\s*\d+\s*/\s*([^<]+)', inner)
            if label:
                kind = 'step'
                self.edits.append((inner_start, self.source_position(), label[1]))
        if kind:
            self.kinds.add(kind)
        del self.stack[index:]


def without_numbering(source):
    parser = NumberingParser(source)
    for start, end, replacement in reversed(parser.edits):
        source = source[:start] + replacement + source[end:]
    if not parser.edits or not parser.scope:
        return source
    root = '.premium-template.' + parser.scope
    css = []
    if 'service' in parser.kinds:
        css.append(f'{root} .pfg-service-number{{justify-content:flex-end}}{root} .pfg-service-number span[aria-hidden]{{font-family:Manrope,sans-serif;font-size:18px;color:var(--ink,#24342e)}}')
    if 'tab' in parser.kinds:
        css.append(f'{root} .pfg-path-tabs button span[aria-hidden]{{font-family:inherit;font-size:inherit;font-style:normal;opacity:1}}')
    if 'resource' in parser.kinds:
        css.append(f'{root} .pfg-resource-panel{{grid-template-columns:minmax(0,1fr) auto}}{root} .pfg-resource-action{{grid-column:auto}}@media(max-width:1100px){{{root} .pfg-resource-panel{{grid-template-columns:1fr}}}}')
    if css:
        source = source.replace('</style>', '\n/* Approved unnumbered output policy. */\n' + ''.join(css) + '\n</style>', 1)
    return source
