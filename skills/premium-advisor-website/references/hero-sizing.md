# Compact hero with roomier spacing

This is the default for new Premium builds, implemented by `scripts/approved_template.py` as `premium-nri-template-v1`. Set top-level `hero_layout` to `preserve` only when retaining an existing site’s hero for a narrow edit. Apply this preset when the user requests the approved compact hero treatment. It is a scoped output adaptation for the bundled Home hero (`premium-home-02`), not a replacement of baseline template files. Preserve an explicitly chosen different layout and any later spacing preference.

Remove viewport-based minimum height from both the hero and its content. Increasing padding must not reintroduce `100vh` or `100svh` sizing. Keep the background video absolutely contained by the hero so GHL's global video rules cannot enlarge the section. Let text and controls determine the height; do not use a fixed maximum height that can clip mobile content.

Append this CSS after existing hero rules inside the same section's `<style>` block. Keep it in the task's generation source and apply it during every regeneration, including combined previews. For a different wrapper, scope it to that section's actual unique wrapper.

```css
/* Content-sized hero with roomier spacing. */
.premium-template.premium-home-02 .pfg-cinema{min-height:0!important;height:auto!important}
.premium-template.premium-home-02 .pfg-cinema-content{min-height:0!important;padding-block:48px 104px!important}
.premium-template.premium-home-02 .pfg-cinema-content h1{font-size:48px;line-height:1.03}
.premium-template.premium-home-02 .pfg-cinema-content>.pfg-eyebrow{margin-bottom:22px}
.premium-template.premium-home-02 .pfg-cinema-content>p{margin-top:26px;line-height:1.65}
.premium-template.premium-home-02 .pfg-cinema .pfg-actions{margin-top:28px}
.premium-template.premium-home-02 video.pfg-background-video{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;max-width:none!important;object-fit:cover!important}
.premium-template.premium-home-02 .pfg-cinema-bottom{bottom:18px;padding-top:14px}
@media(max-width:800px){.premium-template.premium-home-02 .pfg-cinema-content h1{font-size:40px}}
@media(max-width:540px){.premium-template.premium-home-02 .pfg-cinema-content{padding-block:38px 100px!important}.premium-template.premium-home-02 .pfg-cinema-content h1{font-size:36px}.premium-template.premium-home-02 .pfg-cinema-content>.pfg-eyebrow{font-size:14px}}

```

The approved spacing is 48px above and 104px below desktop content, with 38px/100px on mobile. At 1440px wide, the Justin version is about 583px tall; the height can vary with fonts and copy. Check desktop, tall desktop, and mobile: the hero must not grow just because the viewport is taller, actions must stay clear of bottom controls, and text must not overflow. Preserve pause/play and reduced-motion behavior.

For a requested GHL push, read the exact advisor location and page, back up the hero code through the supported editor, compare the existing block, and change only that block. Do not repaste identical code or overwrite other sections. Save and verify the returned preview. Distinguish a saved GHL edit from live publication; publish only within the user's authorized scope.
