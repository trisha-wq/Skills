"""Approved Premium footer mission and development credit output policy."""
import html
import re

POLICY = 'epic-footer-v1'
MISSION_PARAGRAPHS = [
    'Our mission is to create a firm like no other in the industry. Working together with the clients and our multidisciplinary team approach of specialists, we will create an elevated client experience. Families and small businesses are demanding ever-increasing assistance with support and guidance for smart estate and financial planning for building wealth.',
    'Continuous training and support for company management and employees, combined with the strictest standards of protocols, ethics, and integrity will be expected and implemented.'
]
CREDIT = 'Built, powered & developed by ePIC Services Company.'


def apply_footer_policy(source):
    """Change footer copy only; keep company copyright, links and styles."""
    if 'class="pfg-footer-mission"' not in source:
        return source
    body = ''.join('<p>'+html.escape(p)+'</p>' for p in MISSION_PARAGRAPHS)
    source, missions = re.subn(
        r'(<section class="pfg-footer-mission"[^>]*><h3\b[^>]*>Mission Statement</h3><div>).*?(</div></section>)',
        lambda m:m[1]+body+m[2], source, flags=re.S)
    source, credits = re.subn(
        r'(<div class="pfg-copyright"><span>.*?</span><span>).*?(</span></div>)',
        lambda m:m[1]+html.escape(CREDIT)+m[2], source, flags=re.S)
    if missions != 1 or credits != 1:
        raise ValueError('Expected one mission section and one development credit in a footer block')
    return source
