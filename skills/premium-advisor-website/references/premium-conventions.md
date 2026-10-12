# Premium design and reference structure

## Default template

The current default is `premium-ardie-tbfgp-v1`, based on the verified Ardie Baxter reference at https://tbfgp.com/. All 56 numbered, self-contained Custom HTML sections are bundled in `assets/template/`. `assets/design-contract.json` lists page order, section files, content tokens, card counts, and pinned SHA-256 hashes. `assets/video-card-map.json` identifies video slots without copying advisor playback links.

Default inventory: Home 12; About 8; Services 7; Videos 5; Events 5; Legacy Stories 7; Contact 4; Stress Test 8. About section 3 contains the roster and section 4 the biography. Videos has 14 Risk, 14 Tax, and 14 Kai-Zen cards; Home keeps four Legacy Collection cards. Retain the Mission Statement and Order Here footer areas. A content gap does not change this inventory.

Each block owns its CSS, IDs, and script initialization. Preserve the wrapper and inner markup. Set the first GHL outer section to Sticky Top when using the sticky header, and set surrounding GHL padding/margins to zero. Do not add global historical CSS on top. Change only documented content/color placeholders with the renderer; theme colors do not change geometry.

For the roster, select the original high-resolution advisor artwork, inspect its natural dimensions, and upload that original to the verified advisor GHL account. Record its width/height and returned CDN URL. Do not stretch a low-resolution website preview to desktop width or use the GHL media grid's transformed thumbnail URL. At the template's roughly 1240-pixel maximum content width, prefer an original at least 2480 pixels wide when available. Report a source-quality limitation instead of inventing detail.

## Historical Pinnacle reference

This skill carries the conventions of the Pinnacle Financial Group project in:
C:/Users/Mochi/Documents/ChatGPT/Premium Sites/pinnacle-ghl

This old path is historical context, not a required location, portable dependency, or the default design. For a continuation of that specific project, use its actual current files. For another advisor use explicitly supplied Premium code first, otherwise the portable Ardie templates. The map below documents the older Pinnacle variant and must not override the default contract.

Do not run Pinnacle's build.py for a new advisor unchanged: it contains advisor-specific content and URLs. For the existing project, trace generation sources before updating outputs so rebuilds preserve corrections. Include inline section directories in any deliverable package intended to contain them; the original package.py only packages selected folders.

## Historical styling

Final Premium style: Manrope sans-serif headings/body with Playfair Display italic emphasis; teal/navy #123238/#103438, cream #f5f3ed, gold #d8bba0. Rounded pill calls to action, restrained borders, numbered cream cards and teal gradient active buttons. Base stylesheet precedes Premium overrides. User-provided advisor branding wins.

Preserve reduced-motion handling and keyboard-accessible interactions. Use full-width GHL wrappers with internal constrained content. Do not prune cascade rules blindly or copy the same root ID into every block. Scoped full CSS in each block is acceptable and matches the user's requested export format.

## Historical page map

Reference order; adapt to approved scope and content.

- Home: header; cinematic autoplay video hero with pause and reduced-motion behavior; advisor introduction immediately after hero; trust bar; three planning-priority tabs; services; featured legacy videos; stress-test CTA linking internally; event invitation linking internally; Legacy Stories banner; consultation; footer; optional page progress/back-to-top utility.
- About: header; hero; personal relationships introduction; advisor biographies; education/integrity; strategic partner tabs and profiles; consultation; footer. Pinnacle has two advisors and nine partners; do not assign those counts or people to every firm.
- Services: header; hero; expandable service cards; planning process; planning opportunities; consultation; footer.
- Videos: header; hero; one video library block; consultation; footer. Three categories Risk Mitigation Strategies, Tax Mitigation Strategies, Kai-Zen. Library has search, selected category heading/description, live count and empty state. Reference totals 12/12/14. Risk/tax thumbnails omit the overlaid play icon; Kai-Zen retains it.
- Events: header; hero; educational session card and Learn/Ask/Explore steps; consultation; footer. Maintain 16:9 thumbnail with captions beneath it; avoid empty media padding. Use actual session registration link.
- Legacy Stories: header; hero; guidebook video/CTA/features and Teach/Inspire content; story prompts; legacy access/logo/buttons/video; consultation; footer. Supplied original has 12 native accordion categories, 211 prompts, ten features and two BB video embeds. These are original content inventory checks, not values to invent for new projects. Retain approved source copy and supplied product price/link.
- Contact: header; hero; contact details and embedded GHL inquiry form together; footer. Test rendering without submitting a lead.
- Stress Test: header; hero; resource introduction; estate assessment; estate planning platform; probate cost estimator; closing note; footer. Three resource cards are independent blocks, with a continuous cream background across section boundaries. Prevent margin-collapse gaps (for example scoped flow-root wrappers). Keep separate verified assessment, payment and calculator URLs.
- Order/payment page: include only if the task requires it and verified source content is available.

Pinnacle removed breadcrumbs on About, Services, Videos, Events, Stress Test and Legacy Stories; Contact retained its breadcrumb. Preserve the current project or requested reference rather than applying this to unrelated layouts.

## Shared footer

Actual advisor logo in a cream plaque, contact/social/navigation, and approved mission statement below the main grid. Preserve mission text exactly when supplied. Compact responsive headshots avoid unnecessary padding; strategic partner tabs use numbered cards, visible selected state and arrow-key/Home/End keyboard navigation.

## Historical export inventory

Home 13 blocks; About 9; Services 7; Videos 5; Events 5; Legacy Stories 7; Contact 4; Stress Test 8. Existing folders are ghl-<page>-sections-inline; combined previews are review/<page>-sections-inline.html. Export block numbering reflects the page order above. Reuse relevant current blocks for Pinnacle changes; for another advisor map new content into this structure and verify all substitutions.
