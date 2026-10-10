# API and compatibility notes

Existing integration: `VIMEO_ACCESS_TOKEN`, optional comma-separated numeric `VIMEO_TEAM_OWNER_USER_IDS`; bearer requests to `https://api.vimeo.com`, Accept `application/vnd.vimeo.*+json;version=3.4`.

Capture calls GET `/me`, advertised folder/team connections, optional `/me/team`, `/users/{owner}/folders`, `/users/{owner}/projects/{folder}/items`, and `/videos/{id}`. Follow API paging links on the same API origin. An empty personal library does not prove the team library is empty. If advertised team enumeration fails, retain the error and use a configured owner ID when available. Never guess an owner from an unrelated account.

The helper exports only 720p signed progressive file links as `url_720p`. Other valid 720p links remain candidates for review; no fallback becomes a captured URL without an explicit change to the link contract. Repeated video IDs are captured once, retaining all folder paths. A partial capture returns exit code 2 while preserving successful records and diagnostics. Fatal identity/authentication problems return code 1.

Official references (checked 2026-10-09):
- https://developer.vimeo.com/api/files/video-links
- https://help.vimeo.com/hc/en-us/articles/12427806914577-About-video-file-download-links-from-the-API
- https://developer.vimeo.com/api/reference/response/video-file

Vimeo documents `public`, `private`, and `video_files` scopes for direct file access. `files` links do not expire; `play` and `download` links expire after 24 hours. Retain redirect links rather than the temporary CDN URL reached after following a redirect. Account eligibility and permissions can still prevent file access; consult current official documentation when troubleshooting.
