"""Approved restrained arrows, responsive spacing and service heading icons."""
import re

POLICY = 'restrained-arrows-responsive-v1'
SERVICE_ICON_POLICY = 'service-icons-v3'
ICONS = {'Estate Planning': '<path d="m3 10 9-7 9 7M5 9v12h14V9M9 21v-8h6v8"/>', 'Income Planning': '<ellipse cx="9" cy="6" rx="6" ry="3"/><path d="M3 6v5c0 1.7 2.7 3 6 3m-6-3v5c0 1.7 2.7 3 6 3M15 6v4"/><ellipse cx="16" cy="14" rx="5" ry="2.5"/><path d="M11 14v5c0 1.4 2.2 2.5 5 2.5s5-1.1 5-2.5v-5"/>', 'Asset Preservation': '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 15v2"/>', 'Tax Mitigation': '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9zM14 3v6h6M9 17l6-5"/><circle cx="9" cy="12" r=".8"/><circle cx="15" cy="17" r=".8"/>', 'Risk Mitigation': '<path d="m12 3 8 3v6c0 4.5-4 7.5-8 9-4-1.5-8-4.5-8-9V6zM8.5 12l2.5 2.5 4.5-5"/>', 'Business Planning': '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12a22 22 0 0 0 18 0M12 12v4"/>', 'Wealth Management': '<path d="M4 21h16M6 17v-4M12 17V9M18 17V5M5 8l5-3 4 1 5-3"/>', 'Charitable Remainder Trusts': '<path d="M12 11s-5-2.8-5-5.3a2.7 2.7 0 0 1 5-1.3 2.7 2.7 0 0 1 5 1.3C17 8.2 12 11 12 11zM3 16l4-3h5a2 2 0 0 1 0 4H9M12 17l6-4a2 2 0 0 1 3 2l-7 6H7l-4-3"/>'}
CTA_ARROW = '<svg class="premium-cta-arrow" aria-hidden="true" focusable="false" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18 18 6M6 6h12v12"/></svg>'
CSS = '\nSCOPE .premium-cta-arrow{display:inline-block;flex:0 0 18px;width:18px;height:18px;vertical-align:middle}\nSCOPE .premium-service-heading{display:flex;align-items:center;gap:14px;min-height:64px;margin-bottom:18px}\nSCOPE .pfg-service-number.premium-service-icon{display:flex;align-items:center;justify-content:center;flex:0 0 42px;width:42px;height:42px;min-height:42px;margin:0;border:1px solid #d7c5a6;border-radius:10px;background:#eee7da;color:#936827;line-height:1}\nSCOPE .premium-service-icon svg{display:block;width:24px;height:24px;flex-shrink:0}\nSCOPE .premium-service-heading h3{flex:1;min-width:0;min-height:0;margin:0;font-size:23px;line-height:1.2}\nSCOPE .pfg-btn{max-width:100%;white-space:normal;min-height:48px;text-align:center;justify-content:center}\nSCOPE .pfg-btn:focus-visible,SCOPE button:focus-visible,SCOPE a:focus-visible{outline:3px solid currentColor;outline-offset:4px}\nSCOPE .pfg-wrap>*,SCOPE .pfg-split>*,SCOPE .pfg-path-panel>*,SCOPE .pfg-contact-grid>*,SCOPE .pfg-footer-grid>*{min-width:0}\nSCOPE .pfg-footer a,SCOPE .pfg-contact-info a{overflow-wrap:anywhere}\n@media(max-width:380px){SCOPE h1,SCOPE h2{overflow-wrap:anywhere}}\n@media(max-width:1100px) and (min-width:701px){\nSCOPE .pfg-split,SCOPE .pfg-intro-grid{gap:36px}\nSCOPE .pfg-path-panel{gap:30px;padding:36px}\nSCOPE .pfg-path-panel h2{font-size:36px}\nSCOPE .pfg-assessment{gap:30px;padding:36px}\nSCOPE .pfg-cta .pfg-wrap{flex-wrap:wrap;gap:28px}\n}\n@media(max-width:700px){\nSCOPE .pfg-header-inner{gap:12px}\nSCOPE .pfg-brand{max-width:calc(100% - 60px)}\nSCOPE .pfg-brand img{max-width:100%;height:auto}\nSCOPE .pfg-menu{min-width:44px;min-height:44px;flex-shrink:0}\nSCOPE .pfg-path-tabs button,SCOPE .srs-partner-tab,SCOPE .pfg-filter{min-height:48px}\nSCOPE .pfg-path-panel{padding:28px 24px}\nSCOPE .pfg-cinema-actions{align-items:stretch}\nSCOPE .pfg-cinema-actions .pfg-btn{width:100%}\nSCOPE .pfg-footer-grid{gap:28px 20px}\n}\n@media(max-width:380px){SCOPE .pfg-footer-grid{grid-template-columns:1fr}SCOPE .pfg-footer-grid>div{grid-column:1}}\n'
ARROW = r'[↗→↓↑➜➡]\ufe0f?'
PROTECTED = r'(<style\b[^>]*>[\s\S]*?</style>|<script\b[^>]*>[\s\S]*?</script>)'


def service_heading(title):
    artwork = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + ICONS[title] + '</svg>'
    return '<div class="premium-service-heading"><div class="pfg-service-number premium-service-icon" aria-hidden="true">' + artwork + '</div><h3>' + title + '</h3></div>'


def apply_presentation(code):
    code = re.sub(r'<style data-premium-polish="[^"]+">[\s\S]*?</style>', '', code)
    def styles(match):
        scope = '.premium-template.' + match[1]
        return '<style data-premium-polish="' + match[1] + '">' + CSS.replace('SCOPE', scope) + '</style>' + match[0]
    code = re.sub(r'<div class="premium-template (premium-[^"\s]+)[^"]*"[^>]*>', styles, code)
    # Protect script literals while removing CSS-generated and markup arrows.
    parts, keep = re.split(PROTECTED, code), False
    for i, part in enumerate(parts):
        if part.startswith('<script'):
            continue
        if part.startswith('<style'):
            parts[i] = re.sub(r"content:\s*(['\"])" + ARROW + r'\1', 'content:none', part)
            continue
        owner = re.search(r'class="premium-template (premium-[^"\s]+)', part)
        if owner:
            keep = owner[1].endswith('-01') or owner[1] == 'premium-home-02' or bool(re.search(r'class="pfg-cta\b', part))
        part = re.sub(r'<span\b[^>]*>\s*' + ARROW + r'\s*</span>', CTA_ARROW if keep else '', part)
        part = re.sub(ARROW, '', part)
        part = re.sub(r'<div class="premium-service-heading">(<div class="pfg-service-number premium-service-icon"[^>]*>[\s\S]*?</div><h3>[^<]+</h3>)</div>', r'\1', part)
        part = re.sub(r'<div class="pfg-service-number(?: premium-service-icon)?"(?: aria-hidden="true")?>[\s\S]*?</div><h3>([^<]+)</h3>', lambda m: service_heading(m[1]) if m[1] in ICONS else m[0], part)
        parts[i] = part
    return ''.join(parts)
