---
name: vimeo-link-capture
description: Capture advisor video links through the existing Vimeo API, including exact signed 720p file links from personal or team folders, for MVP and Premium GHL websites.
---

# Vimeo link capture

Use the user's existing Vimeo API credential (`VIMEO_ACCESS_TOKEN`) to find an advisor's folder and export its video links. This is a read-only capture workflow, usable by either advisor website skill. Browser sign-in is not API authentication.

## Existing integration

The source project is `GHLCustomValueFillInAutomation-main`, originally from https://github.com/ePIC-Max-ohohoh/GHLCustomValueFillInAutomation. Locate it in the workspace when available. Its `src/vimeo_folder_videos.py` implements folder traversal; `src/vimeo_connectivity.py` supports team-owner lookup. Reuse configured `VIMEO_ACCESS_TOKEN` and `VIMEO_TEAM_OWNER_USER_IDS`. Do not invoke GHL sync/apply commands to capture links: they write custom values and generate embed URLs rather than the requested file links.

The portable helper below uses the same API base, bearer variable, API version, and owner-scoped project-item endpoints. It requires only Python's standard library. Load credentials from the current process or the user's existing local env file using `--env-file`; never copy a token into this skill, output, website HTML, or chat. The env reader supports literal quoted or unquoted values, not variable interpolation. If no credential is available, ask only for the local configuration location or local setup, not the token text.

## Capture

1. Resolve the advisor name from the user's request or ClickUp task. Ask only if identity is ambiguous. A ClickUp URL alone does not identify a Vimeo folder; inspect the task using an available connector when needed.
2. Run `scripts/capture.py --advisor "Advisor Name" --output-dir "workspace/output/advisor"`, adding `--env-file "path/to/existing/.env"` when needed. The helper discovers personal and advertised team folders and configured team owners. `--owner-id` selects a known numeric team owner; `--folder-uri` disambiguates an exact API folder URI. Do not invent an owner ID or accept an unrelated advisor's folder.
3. Review `capture.json` and `capture.csv`. Folder selection must match the full name ignoring case and whitespace, or a user-specified folder URI. Duplicate matching folders require disambiguation; missing folders or inaccessible libraries require a precise status, not a guessed match. Nested folders are included with provenance.
4. Match video titles to the requested website cards using source titles and existing template mappings. Do not generalize Winston's pilot-specific mappings to other advisors. Duplicate or unclear video matches remain unresolved. Capture alone does not authorize changes to GHL.

## Link contract

- Default to **720p only**. Capture the actual API `files[].link` with `player.vimeo.com/progressive_redirect/playback/{video_id}/rendition/720p/` and a nonempty signature. Preserve its complete query and encoded filename exactly. Never build signatures, rewrite another resolution, strip parameters, or substitute an embed/share URL.
- Prefer `files` for static website links. Report `play.progressive` candidates separately when no matching `files` link is returned; those may expire and are not silently used as durable website values. `download` links may trigger downloads and are not playback replacements.
- If file links are missing, check account access and `public`, `private`, `video_files` scopes. Do not change permissions or generate a new credential without a request. Read [API notes](references/api-notes.md) when diagnosing links or library access.
- When inserting a captured URL into an HTML attribute, escape `&` as `&amp;` only at rendering. Keep raw URLs in JSON/CSV. Preserve existing thumbnails, layout, CSS, headings, and scripts unless the user requests changes.
- Return the output paths, advisor/folder identity, counts of captured and unresolved videos, and relevant access problems. Clearly distinguish API-returned captures from actual playback verification. Never claim a live capture when only fixtures were tested.
