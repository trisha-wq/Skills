"""Native on-page Vimeo playback and visible play-icon output policy."""
import re
from pathlib import Path

POLICY = "vimeo-popup-v1"
START = '<!-- Premium Vimeo popup start -->'
END = '<!-- Premium Vimeo popup end -->'
PLAY_ICON = '<svg data-ct-play-icon="true" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M8 5v14l11-7z"></path></svg>'


def popup_palette(values=None, overrides=None):
    values=values or {}
    palette={'background':values.get('theme_deep','#062947'),'accent':'#d8bba0','link':'#ead0b7','hover':values.get('theme_primary','#08335b')}
    overrides=overrides or {}
    if not isinstance(overrides,dict) or set(overrides)-set(palette):
        raise ValueError('popup_theme supports background, accent, link and hover colors')
    palette.update(overrides)
    if any(not isinstance(color,str) or not re.fullmatch(r'#[0-9a-fA-F]{6}',color) for color in palette.values()):
        raise ValueError('Popup colors must be six-digit hex colors')
    return palette


def with_play_icons(text):
    def thumbnail(match):
        anchor=match[0]
        if '<img ' not in anchor:return anchor
        anchor,count=re.subn(r'(<span class="ab-play"[^>]*>).*?(</span>)',
            lambda m:m[1]+PLAY_ICON+m[2],anchor,flags=re.S)
        assert count==1, 'Expected one play overlay per Vimeo thumbnail'
        return anchor
    return re.sub(r'<a\b[^>]*href="https://player\.vimeo\.com/progressive_redirect/[^\"]+"[^>]*>.*?</a>',thumbnail,text,flags=re.S)


def add_popup(text, scope, root_selector, palette=None):
    text = re.sub(re.escape(START)+r'.*?'+re.escape(END),'',text,flags=re.S).rstrip()
    text = with_play_icons(text)
    popup_id = 'premium-video-popup-'+scope
    title_id = popup_id+'-title'
    css = '''dialog#ID{box-sizing:border-box;width:min(1080px,calc(100vw - 32px));max-width:calc(100vw - 32px);max-height:calc(100dvh - 32px);padding:0;border:1px solid #d8bba0;border-radius:14px;background:#062947;color:#fff;overflow:auto;box-shadow:0 20px 100px #0008;font-family:Manrope,Arial,sans-serif}dialog#ID::backdrop{background:#000c}#ID .ct-popup-bar{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:16px 20px}#ID h2{margin:0;font:600 18px/1.4 Manrope,Arial,sans-serif}#ID button{flex-shrink:0;min-width:44px;min-height:44px;border:1px solid #d8bba0;border-radius:8px;background:transparent;color:#fff;font:inherit;cursor:pointer;padding:8px 12px}#ID button:focus-visible,#ID a:focus-visible{outline:3px solid #d8bba0;outline-offset:3px}#ID video{display:block;width:100%;max-height:calc(100dvh - 160px);aspect-ratio:16/9;background:#000;object-fit:contain}#ID [data-video-error]{margin:0;padding:16px 20px;font-size:14px}#ID a{color:#ead0b7}#ID [hidden]{display:none!important}@media(max-width:600px){#ID .ct-popup-bar{padding:10px 12px;gap:10px}#ID h2{font-size:15px}}'''.replace('ID',popup_id)
    js=(Path(__file__).parent/'video-popup.js').read_text(encoding='utf-8').replace('ROOT_SELECTOR',root_selector).replace('DIALOG_ID',popup_id)
    css += root_selector+' .ab-play svg{display:block;width:24px;height:24px;pointer-events:none}'
    if palette:
        css=css.replace('#062947',palette['background']).replace('#d8bba0',palette['accent']).replace('#ead0b7',palette['link'])
        css+='#'+popup_id+' button:hover{background:'+palette['hover']+'}'
    return (text+'\n'+START+'\n<style>'+css+'</style>\n'
        '<dialog id="'+popup_id+'" aria-labelledby="'+title_id+'">'
        '<div class="ct-popup-bar"><h2 id="'+title_id+'">Watch video</h2>'
        '<button type="button" aria-label="Close video">Close ×</button></div>'
        '<video controls playsinline preload="metadata"></video>'
        '<p data-video-error role="status" hidden>This video could not be loaded. '
        '<a target="_blank" rel="noopener noreferrer">Open the video directly</a>.</p>'
        '</dialog>\n<script>'+js+'</script>\n'+END+'\n')


def with_video_popups(source, palette=None):
    if not re.search(r'href="https://player\.vimeo\.com/progressive_redirect/',source):
        return source
    root=re.search(r'<div class="(premium-template|ct-premium) ([^" ]+)',source)
    if not root:
        raise ValueError('Vimeo popup requires an independently scoped Premium section')
    scope=root[2]
    if not re.fullmatch(r'[a-zA-Z0-9_-]+',scope):
        raise ValueError('Invalid Premium popup scope')
    return add_popup(source,scope,'.'+root[1]+'.'+scope,palette)
