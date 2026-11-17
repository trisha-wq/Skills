"""Apply the approved modest type increase without changing pinned templates."""
import re

POLICY='readability-v1'
MARK='/* Premium readability policy: small text +2px */'


def with_readable_type(source):
    def style(match):
        css=match[1]
        if MARK in css:return match[0]
        def size(m):
            n=int(m[2])
            return m[1]+str(n+2 if n<=18 else n)+'px'
        css=re.sub(r'(font-size:\s*)(\d+)px',size,css)
        def shorthand(m):
            return re.sub(r'(?<![\d.])(\d+)px',lambda n:str(int(n[1])+2 if int(n[1])<=18 else int(n[1]))+'px',m[0],count=1)
        css=re.sub(r'font\s*:[^;{}]+',shorthand,css)
        return '<style>'+MARK+'\n'+css+'</style>'
    return re.sub(r'<style>(.*?)</style>',style,source,flags=re.S)
