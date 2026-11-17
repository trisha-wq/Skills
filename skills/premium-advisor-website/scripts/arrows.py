"""Reduce decorative arrows; retain vector arrows on top and closing CTAs."""
import html
import re
from html.parser import HTMLParser

POLICY = 'restrained-arrows-v1'
ARROWS = '\u2197\u2192\u2193\u27a1\u2794\u279c'
SVG = ('<svg class="premium-cta-arrow" aria-hidden="true" focusable="false" '
       'width="18" height="18" viewBox="0 0 24 24" fill="none" '
       'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
       'stroke-linejoin="round" style="display:inline-block;flex-shrink:0;vertical-align:middle">'
       '<path d="M6 18 18 6M6 6h12v12"/></svg>')
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class ArrowParser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source, self.stack, self.edits = source, [], []
        self.lines = [0] + [m.end() for m in re.finditer('\n', source)]
        self.feed(source)

    def position(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, dict(attrs), self.position()))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        index = next((i for i in range(len(self.stack)-1, -1, -1) if self.stack[i][0] == tag), None)
        if index is not None:
            del self.stack[index:]

    def process_text(self, raw):
        if not self.stack or self.stack[-1][0] in {'script', 'style'}:
            return
        if not any('premium-template' in a.get('class', '').split() for _, a, _ in self.stack):
            return
        decoded = html.unescape(raw)
        if not any(c in decoded for c in ARROWS):
            return
        classes = {c for _, a, _ in self.stack for c in a.get('class', '').split()}
        linked = any(tag == 'a' for tag, _, _ in self.stack)
        keep = linked and bool(classes & {'pfg-nav', 'pfg-actions', 'pfg-cta'})
        replacement = SVG if keep else ''
        start, end = self.position(), self.position() + len(raw)
        # Remove the complete decorative span to avoid empty flex items/gaps.
        if decoded.strip().strip('\ufe0e\ufe0f') in ARROWS and self.stack[-1][0] == 'span':
            closing = self.source.find('</span>', end)
            if closing == end:
                self.edits.append((self.stack[-1][2], closing + 7, replacement))
                return
        value = re.sub('[' + ARROWS + '][\ufe0e\ufe0f]?', replacement, decoded)
        self.edits.append((start, end, value))

    handle_data = process_text

    def handle_entityref(self, name):
        self.process_text('&' + name + ';')

    def handle_charref(self, name):
        self.process_text('&#' + name + ';')


def with_restrained_arrows(source):
    parser = ArrowParser(source)
    for start, end, value in sorted(parser.edits, reverse=True):
        source = source[:start] + value + source[end:]
    # Disable generated decorative arrows, including partner tabs and filters.
    def css(match):
        return 'content:none' if any(c in html.unescape(match[2]) for c in ARROWS) else match[0]
    def style(match):
        return re.sub(r'content\s*:\s*([\'\"])(.*?)\1', css, match[0])
    source = re.sub(r'<style\b[^>]*>.*?</style>', style, source, flags=re.S)
    # unnumbered-v1 previously left an arrow-only row above service titles.
    source = re.sub(r'<div class="pfg-service-number">\s*</div>', '', source)
    return source
