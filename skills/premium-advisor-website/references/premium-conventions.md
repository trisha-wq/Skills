# Premium design and reference structure

## Original project

This skill carries the conventions of the Pinnacle Financial Group project in:
C:/Users/Mochi/Documents/ChatGPT/Premium Sites/pinnacle-ghl

For continuation on this device, read the relevant current page/inline folder and build.py, premium.py, styles.css, premium.css or site.js as needed. Current code is more authoritative than this snapshot. This path is a reference, not a required output location or a portable dependency. For another advisor use supplied Premium code first; if none is available, use the bundled styling baseline and the structures below. Ask for a specific missing layout reference only when exact replication requires it.

Do not run Pinnacle's build.py for a new advisor unchanged: it contains advisor-specific content and URLs. For the existing project, trace generation sources before updating outputs so rebuilds preserve corrections. Include inline section directories in any deliverable package intended to contain them; the original package.py only packages selected folders.

## Design baseline

Final Premium style: Manrope sans-serif headings/body with Playfair Display italic emphasis; teal/navy #123238/#103438, cream #f5f3ed, gold #d8bba0. Rounded pill calls to action, restrained borders, numbered cream cards and teal gradient active buttons. Base stylesheet precedes Premium overrides. User-provided advisor branding wins.

Preserve reduced-motion handling and keyboard-accessible interactions. Use full-width GHL wrappers with internal constrained content. Do not prune cascade rules blindly or copy the same root ID into every block. Scoped full CSS in each block is acceptable and matches the user's requested export format.

## Page and section map

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

## Original export inventory

Home 13 blocks; About 9; Services 7; Videos 5; Events 5; Legacy Stories 7; Contact 4; Stress Test 8. Existing folders are ghl-<page>-sections-inline; combined previews are review/<page>-sections-inline.html. Export block numbering reflects the page order above. Reuse relevant current blocks for Pinnacle changes; for another advisor map new content into this structure and verify all substitutions.
