"""Apply the approved compact NRI presentation without changing pinned assets."""
import re
import colorsys

POLICY = 'premium-nri-template-v1'
MARK = '/* Approved Premium NRI template v1 */'


def apply_approved_template(code, palette, hero_layout='compact', primary=None):
    if hero_layout not in {'compact', 'preserve'}:
        raise ValueError('hero_layout must be compact or preserve')
    if MARK in code:
        return code
    wrapper = re.search(r'<div class="premium-template (premium-[^"\s]+)', code)
    if not wrapper:
        return code
    name = wrapper[1]
    scope = 'div.premium-template.' + name + ' '
    # The pinned CSS contains fixed blue/gold shades as well as theme tokens.
    # Tint those CSS shades to the chosen logo hue; preserve exact supplied colors.
    primary = primary or palette.get('hover', palette['background'])
    brand_rgb = [int(primary[i:i+2],16)/255 for i in (1,3,5)]
    brand_hue = colorsys.rgb_to_hls(*brand_rgb)[0]
    protected = {color.lower() for color in [primary,*palette.values()]}
    def tint(match):
        color=match[0]
        if color.lower() in protected: return color
        rgb=[int(color[i:i+2],16)/255 for i in (1,3,5)]
        _,light,sat=colorsys.rgb_to_hls(*rgb)
        if sat < .07: return color
        if light < .60: light=max(.22,light)
        rgb=colorsys.hls_to_rgb(brand_hue,light,min(sat,.17 if light<.60 else .22))
        return '#'+''.join(f'{round(c*255):02x}' for c in rgb)
    def style(match):
        if 'premium-video-popup-' in match[0] or 'premium-webprez-popup-' in match[0]:
            return match[0]
        return re.sub(r'#[0-9a-fA-F]{6}\b',tint,match[0])
    code=re.sub(r'<style\b[^>]*>.*?</style>',style,code,flags=re.S)
    background = palette['background']
    rgb = [int(background[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [c/12.92 if c <= .04045 else ((c+.055)/1.055)**2.4 for c in rgb]
    luminance = sum(a*b for a,b in zip(linear, [.2126,.7152,.0722]))
    foreground = '#fff' if luminance < .179 else '#111'
    rules = [
        '.pfg-filter:before{display:none;content:none}',
        '.srs-partner-tab:before{display:none;content:none}',
        '.legacy-card:before{display:none;content:none}',
        '.pfg-filter{gap:0}',
        '.pfg-service-number.premium-service-icon{color:var(--ink);background:var(--ivory);border-color:var(--line)}'
    ]
    # Keep data-index attributes and all functional controls intact.
    code = re.sub(r'content\s*:\s*attr\(data-index\)', 'content:none', code)
    extra = ''
    if name.endswith('-01'):
        rules += ['.pfg-nav>a{font-size:17px;font-weight:600}',
                  '.pfg-nav .pfg-btn{font-size:15px}',
                  '.pfg-nav{gap:20px}', '.pfg-header-inner{gap:22px}']
        extra += '@media(max-width:1190px){' + ''.join(scope+r for r in [
            '.pfg-menu{display:inline-flex}',
            '.pfg-nav{display:none;position:absolute;top:100%;left:0;right:0;background:#fff;padding:24px 30px;border-bottom:1px solid var(--line);box-shadow:0 15px 20px #00000010;max-height:75vh;overflow:auto}',
            '.pfg-nav.pfg-open{display:flex;flex-direction:column;align-items:stretch;gap:9px}',
            '.pfg-nav>a{font-size:18px}']) + '}'
    if name == 'premium-home-03':
        rules += [f'.pfg-media-caption{{background:{background};color:{foreground};font-size:14px;line-height:1.5;letter-spacing:.06em;flex-wrap:wrap;gap:8px 24px;padding:18px 24px}}']
    if name == 'premium-home-10':
        rules += [f'.pfg-legacy-banner .pfg-eyebrow{{color:{foreground};background:{background};display:inline-block;width:fit-content;max-width:100%;padding:8px 12px;border-radius:4px;font-size:14px;line-height:1.5;letter-spacing:.06em}}']
    if name == 'premium-home-02' and hero_layout == 'compact':
        rules += [
            '.pfg-cinema{min-height:0!important;height:auto!important}',
            '.pfg-cinema-content{min-height:0!important;padding-block:48px 104px!important}',
            '.pfg-cinema-content h1{font-size:48px;line-height:1.03}',
            '.pfg-cinema-content>.pfg-eyebrow{margin-bottom:22px}',
            '.pfg-cinema-content>p{margin-top:26px;line-height:1.65}',
            '.pfg-cinema .pfg-actions{margin-top:28px}',
            'video.pfg-background-video{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;max-width:none!important;object-fit:cover!important}',
            '.pfg-cinema-bottom{bottom:18px;padding-top:14px}']
        extra += '@media(max-width:800px){'+scope+'.pfg-cinema-content h1{font-size:40px}}'
        extra += '@media(max-width:540px){'+scope+'.pfg-cinema-content{padding-block:38px 100px!important}'+scope+'.pfg-cinema-content h1{font-size:36px}'+scope+'.pfg-cinema-content>.pfg-eyebrow{font-size:14px}}'
    css = MARK+'\n'+'\n'.join(scope+r for r in rules)+'\n'+extra
    return code.replace('</style>', css+'\n</style>', 1)
