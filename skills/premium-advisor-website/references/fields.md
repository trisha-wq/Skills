# Portable Premium values

Input JSON contains `values` (string fields), `bios.about` (approved biography paragraph array), and optional `sources` (task-local provenance). The complete supported field inventory is `assets/design-contract.json` -> `tokens`; unknown fields are rejected. Never put passwords, cookies, API credentials, or authenticated download URLs here.

Identity: advisor_name (required), advisor_full_name, advisor_first_name, advisor_title, advisor_credentials, firm_name, license_number, phone, email, location_label, address_line_1, address_line_2, copyright_year. Uppercase variants of name/title/credentials/firm are derived if their corresponding source value is present. Supply intro_text, mission_text, and event_description from approved sources. Supply `bios.about` as paragraphs, not raw HTML.

Destinations: booking_url, linkedin_url, map_url, contact_form_url, stress_test_url, estateplan_invite_url, payment_url, bridge_url, instant_quote_url, registration_url. Keep these actions separate; do not substitute a booking/contact form for event registration or copy reference-advisor IDs. Internal page routes stay in the template; adapt final slugs only when confirmed and record that explicit change.

Images: logo_url, headshot_url, roster_url use verified original `https://assets.cdn.filesafe.space/` URLs. roster_width and roster_height are positive integer strings from the actual original image metadata. Use the high-resolution original, not a transformed media grid preview.

Vimeo slots: video_advisor_intro_url/title/thumbnail, video_registration_url/title/thumbnail, video_webinar_url/title/thumbnail. Home has home_video_01_url/thumbnail through home_video_04_url/thumbnail. Library Kai-Zen slots use library_kai_zen_01_url/thumbnail through 14. Playback URLs must be the complete signed Vimeo 720p file link; thumbnails must be verified GHL-hosted images. Source identity checks are still required; URL-shape validation alone does not prove a correct video.

WebPrez slots: library_risk_01_url/thumbnail through 14 and library_tax_01_url/thumbnail through 14. Match each slot to `assets/video-card-map.json` by source identity and title. Use this advisor's exact WITHOUT Viewing Notice link, unlike MVP's WITH Viewing Notice convention. Catalog names can differ; IUL vs Qualified Plan corresponds to Retirement Plan Comparison. All library slots take independent image fields so an approved supplied thumbnail can be retained without changing its identity.

Branding: theme_primary and theme_deep are six-digit hex colors; defaults #123238 and #0d292f. Explicit client branding takes precedence. Do not change CSS sizes, layout tracks, breakpoints, or fonts as part of a color substitution.

Missing content remains a token and is listed in missing-values.csv. Missing action URLs are rendered in place as disabled anchors, not broken navigable links. Missing image/bio fields mean the build is not ready for installation; do not claim otherwise. Registration, Home cards, and library cards remain present. The source report preserves the distinction between integrity checks, browser rendering, playback, and publication.
