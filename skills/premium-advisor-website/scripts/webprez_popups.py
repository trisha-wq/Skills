"""Embed original Risk/Tax WebPrez viewing pages in independently scoped dialogs."""
import re
from pathlib import Path
from video_popups import popup_palette

POLICY='webprez-popup-v1'
START='<!-- Premium WebPrez popup start -->'
END='<!-- Premium WebPrez popup end -->'


def with_webprez_popups(source,palette=None):
    if not re.search(r'href="https://smartmoney\.talk/',source) or not re.search(r'data-category="(?:risk|tax)"',source):
        return source
    root=re.search(r'<div class="(premium-template|ct-premium) ([^" ]+)',source)
    if not root or not re.fullmatch(r'[a-zA-Z0-9_-]+',root[2]):
        raise ValueError('WebPrez popup requires an independently scoped Premium section')
    source=re.sub(re.escape(START)+r'.*?'+re.escape(END),'',source,flags=re.S).rstrip()
    markup=(Path(__file__).parent/'webprez-popup.html').read_text(encoding='utf-8')
    markup=markup.replace('DIALOG_ID','premium-webprez-popup-'+root[2]).replace('ROOT_SELECTOR','.'+root[1]+'.'+root[2])
    palette=palette or popup_palette()
    # Replace only CSS colors; runtime links retain the exact original advisor URL.
    css,rest=markup.split('</style>',1)
    mapping={'#08335b':palette['background'],'#d8bba0':palette['accent'],'#ead0b7':palette['link'],'#062947':palette['hover']}
    css=re.sub('|'.join(re.escape(c) for c in mapping),lambda m:mapping[m[0]],css)
    return source+'\n'+START+'\n'+css+'</style>'+rest.rstrip()+'\n'+END+'\n'
