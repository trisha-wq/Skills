# Renderer values

The JSON has three top-level fields: `values` (string keys and values), `bios` (home and about paragraph arrays), and optional `sources` (current advisor provenance). Unknown/missing values stay as GHL Custom Value placeholders and are listed in missing-values.csv.

Text keys: advisor_name, advisor_first_name, advisor_firm_name, advisor_title, advisor_location. advisor_name is required to identify the output. Do not assume advisor_first_name from a multi-part name when unclear.

URL keys: advisor_booking_url, advisor_contact_form_url, advisor_headshot_url, advisor_roster_image_url, advisor_events_page_url, event_registration_url, advisor_stress_test_url, advisor_estateplan_order_url.

Vimeo URL keys: video_advisor_intro, video_not_just_for_millionaires, video_21st_century_trust, video_neverstop, video_insurance_blp, video_estate_planning_overview. Advisor introduction and estate-planning overview each have a corresponding `_thumbnail` URL key. Section 4 uses retained original generic thumbnails.

WebPrez keys: webprez_risk_01 through webprez_risk_14 and webprez_tax_01 through webprez_tax_14, following assets/webprez-card-map.json. Section 5 uses retained original images.

bios.home contains Website Bio paragraphs. bios.about contains Print Bio paragraphs. The renderer escapes these as text and wraps them in p tags; do not supply raw HTML. Preserve exact approved wording.

Optional values theme_primary, theme_hover and theme_light are six-digit hex colors. Defaults: #8e9897, #a3adac, #d4dcdb. The primary color also controls matching translucent accent RGB values. Geometry and breakpoints remain unchanged.

Each section uses the existing structure: 1 hero, 2 advisor profile/form, 3 services, 4 four featured videos, 5 risk/tax library, 6 about/team, 7 events/overview, 8 estate tools. Optional section 9 is Legacy Stories + Guidebook and keeps its shared source media/action links.
