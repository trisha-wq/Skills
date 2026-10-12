---
name: mvp-advisor-website
description: Build or update MVP advisor GHL sections using the portable Winston pilot templates and approved advisor sources, preserving the chosen design. Distinct from the Ardie-based Premium eight-page template.
---

# MVP advisor website

Use this workflow for the user's MVP advisor websites. A ClickUp task link is the starting input; discover linked source folders and accounts before asking the user to manually supply individual fields. This skill carries the website conventions from the Winston Bramwell pilot, not his personal data or authenticated sessions.

## Website conventions

Use the user's explicitly selected current code/reference first; otherwise use the packaged `mvp-winston-v1` design in `assets/template/`. MVP is the eight-section Winston pilot, not the Ardie/Premium eight-page site. Record the chosen design ID/reference and any explicitly approved departures. Do not reconstruct the layout from screenshots, prose, or memory when the template exists. Do not use Premium CSS or sections as MVP defaults.

- Preserve the user's section layout, classes, IDs, responsive breakpoints, animations, and scripts. Change content, approved URLs, and requested colors. Do not redesign or switch the deliverable to a new website platform.
- The default primary color for this MVP template is `#8e9897`, hover `#a3adac`, and light accent `#d4dcdb`. Honor a new advisor's requested branding when provided.
- Section 2 uses the source labeled **Website Bio**. Section 6 uses the advisor's **Print Bio**. Preserve the approved text rather than inventing or rewriting facts, licenses, or credentials.
- Section 2's introduction thumbnail is advisor-specific. Section 4 and 5 retain the original template image URLs unless the user requests replacements.
- Vimeo buttons use the exact signed **720p video file link**, including its complete signature. Obtain the URL from Vimeo's **Video file links** option or an authoritative ClickUp project record. Do not turn an MP4 URL into a Vimeo iframe URL, change rendition text on a signed URL, or assign one video to every card.
- Section 5 uses the selected advisor's WebPrez **Video Page Hypertext Link WITH Viewing Notice**. Never construct URLs by replacing advisor tokens or copying another advisor's signature.
- Section 8 contains the stress test, eStatePlan order link, and shared probate calculator. Legacy Stories + Guidebook is an optional separate block. Ask about replacement versus addition if placement is ambiguous; do not silently remove the stress test.

## Source collection

Read [references/source-workflow.md](references/source-workflow.md) when collecting advisor data. Prefer available authenticated connectors; use the supported browser tools for ClickUp, Vimeo and WebPrez when connectors cannot perform the task. A new session must inspect its own connections and browser state. Ask the user to sign in only when actually blocked. Do not ask for passwords or tokens in chat, or export browser cookies into this skill.

Keep a source manifest for the current advisor: values, source task/file/video pages, selected account identity, and unresolved fields. ClickUp task status is a clue, not proof that a linked service account exists or does not exist. Downloading a photo does not provide a public GHL image URL.

## Generate and verify

Read [references/fields.md](references/fields.md) before filling the template. Prefer the user's current code if supplied; otherwise use the neutral HTML files in `assets/template/`. They preserve the pilot layout with advisor-specific values removed. `assets/webprez-card-map.json` records section 5 card order and original video identities; it contains no advisor viewing URLs.

For the bundled template, write an advisor values JSON using the documented schema and run:

```text
python scripts/render.py --values /absolute/path/advisor-values.json --output /absolute/path/advisor-output
```

Paths in this example are arguments to replace, not fixed output locations. Use an available Python runtime. Add `--include-legacy` only when the user wants the Legacy Stories block appended after section 8. The renderer verifies the pinned template hashes in `assets/design-contract.json`, then writes section snippets, combined HTML, a local preview, unresolved-field CSV, and source-level verification. It never writes to GHL or publishes. Preserve the original source files and keep all current advisor values in the task workspace, outside the installed skill. Do not update template hashes merely to bypass a failing check.

Run `python scripts/verify_design.py --output /absolute/path/advisor-output` after generation and after changes; include `--include-legacy` when applicable. This verifies the section inventory, DOM layout, CSS geometry, and scripts against the bundled pilot. For an explicitly supplied different layout, preserve that task-local source and record the override instead of claiming the default contract applies.

Verify that every discovered link is assigned to the correct card and advisor. For WebPrez, check video identity as well as title, especially duplicate course titles. For Vimeo, distinguish website page links from video files, and preserve complete signed URLs. Missing content does not authorize removing sections/cards or replacing the design. For new builds, render the complete page at desktop and mobile widths, confirm the actual viewport sizes, and visually compare section order, typography, spacing, images, and interactions with the selected MVP template/reference. CSS/script checks alone do not prove visual fidelity. Report source checks separately from browser rendering, playback, or live GHL checks.

Deliver clickable absolute paths to the updated snippets and a ZIP of the output. List only material missing values and the next access step. Leave unresolved values visibly marked instead of guessing. Creating local code does not by itself authorize publishing a GHL page, changing cloud Custom Values, creating accounts, or changing sharing permissions; follow the user's current requested scope.
