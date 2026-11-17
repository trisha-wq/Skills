# Existing-site additions

Use this reference when an approved Premium rebuild must preserve source-site differences or add requested pages beyond the eight-page baseline. Extend task-local outputs after rendering the pinned baseline; do not change its hashes or make one advisor's extra pages, people, colors, counts, or URLs universal defaults.

## Scope and inventory

Compare the existing site's routes, navigation destinations, page sections, roster, biographies, video categories, forms, quizzes, and event resources with the selected template. Include verified additions within the approved scope using the same Premium layout and scoped block conventions. Record additions and exceptions in the task manifest. An optional original registration bar may reuse the supplied registration channel; do not invent event dates or countdowns.

Keep advisor-specific data in generation inputs. Distinguish direct advisor contact details from the firm office when both are verified. Team counts and profile routes come from approved sources, not a previous build. Give separate biographies their own blocks when the export requires independently editable sections. Reused headers, footers, and profile sections need distinct wrappers and IDs for each page.

## Legal pages

For a requested Privacy Policy or Terms of Service rebuild, read the advisor's published page or approved legal text. Preserve every substantive heading and paragraph in order, with links and verified business contact details. Resolve publicly encoded contact text from the source rather than shipping an "email protected" placeholder. Do not write new legal terms or copy another firm's policy.

Export a separate header, compact page hero, legal body, and footer using the Premium design. Use the confirmed route, such as `/privacy-policy`, in affected headers and footers, and localize that route in previews. Compare rendered text nodes with the stored approved legal content; report source access or completeness gaps rather than fabricating copy.

## Reviews page and navigation

Preserve all approved published review texts, author names, ratings, dates when available, and matching verified hosted images. Do not invent testimonials or replace real reviewer images with generated people. Keep the original write/read reviews CTA destination.

Building a local Reviews page does not automatically change the navbar. Store its page route separately from the navbar destination. If the user says to keep the existing navbar link, preserve the exact external URL in exports and previews; include the rebuilt page in the local preview index independently.

Use repeated review items in the Premium design, with keyboard-accessible Read More/Read Less controls for long text. Each control must use a unique target ID and correct `aria-controls` and `aria-expanded` states. Verify the published inventory and identities against task-local data, rather than fixing a global review count. Do not submit a review during testing.

## Added video collections

Preserve the standard 14 Risk, 14 Tax, and 14 Kai-Zen cards; add verified original-site collections without replacing those cards. Keep category buttons, selected heading, descriptions, search, counts, and empty results together in the single video-library block. Confirm expected counts for each added category from this advisor's source.

Match extra cards by exact source video identity, not title alone. Account-owned and outside-account uploads with the same title are not interchangeable. Retain approved third-party embeds where needed, recording provider-controlled internal artwork separately from GHL-hosted custom thumbnails. Respect account-only Vimeo migration and requested shared-thumbnail preservation as described in `SKILL.md`.

The baseline renderer accepts only its declared tokens and requires signed 720p URLs for Vimeo slots. Keep extra media slots and approved outside-account watch URLs in task-local extension data rather than passing unknown keys or non-file URLs to the renderer. For a retained original in a standard slot, leave its baseline URL unresolved, then resolve that exact disabled slot in the task-local adaptation using the approved original destination; verify the exception separately. Do not weaken the renderer's file-link validation or report the retained watch URL as a captured file link. Apply the approved unnumbered and Services resource policies to adapted blocks too.

## Deliverables and checks

Include every requested extra page in numbered inline sections, its individual preview, the combined preview/index, route checks, actual page/block totals, generation inputs, manifests, paste-order guide, and ZIP. Rebuilding must preserve corrections. Verify legal copy, review inventory and toggle targets, unchanged navbar destinations, media identities, category behavior, unique IDs, and matching shared image URLs. Never claim baseline checks validate added pages or that HTTP file checks establish video playback, visual rendering, or live installation.
