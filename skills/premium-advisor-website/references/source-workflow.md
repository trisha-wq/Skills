# Premium advisor source collection

## ClickUp intake

Open the supplied task and inspect description, custom fields, attachments, linked Drive folders, production tasks and relevant comments. Verify advisor and firm identity. Collect website/print biography labels as provided, logo, headshots, roster, mission, business contact details, calendar, social links, GHL form, desired routes, webinar registration, stress tool, planning platform/payment, probate calculator, Legacy Stories resources and video production records. MVP section numbers and bio placement do not apply automatically to the Premium page structure.

Discover linked records before asking the user to retype information. Distinguish a GHL contact record from a website location/subaccount. Do not infer account absence from a task status. If the task requests only particular pages, build those pages rather than automatically expanding to every reference page.

## Google Drive

Use connected Drive tools to read actual approved documents and select website-ready logos/headshots and media. Folder names alone are weaker evidence than approved brand files. Keep file IDs/source links in the current advisor manifest. Download assets to the task workspace when supported; retain the approved text exactly where required. For About image corrections, download the website roster and actual advisor headshot only; keep strategic partner images as supplied unless explicitly requested otherwise. Choose the portrait by inspecting the image, not by an Advisor_Image filename that may identify a framed graphic. Use a user-supplied verified GHL headshot directly. Kyle’s confirmed portrait is https://assets.cdn.filesafe.space/VxKKxOMXI106VzdhqbxH/media/6a329e966dd61c546af669a5.jpg; this example belongs only to Kyle and is not a default for other advisors. A Drive preview URL is not an image src. Upload selected website images to the verified advisor GHL Media Storage location using the asset-hosting workflow below, or record the specific unresolved upload blocker.

## WebPrez / smartmoney.talk

Verify the selected advisor in My Group or the active subaccount before retrieving links. For this Premium workflow, use Video Page Hypertext Link WITHOUT Viewing Notice, unless the user explicitly chooses another viewing mode. This differs from the MVP skill's WITH Viewing Notice convention.

Retrieve each full link from that advisor's exact video detail dialog. Do not synthesize advisor tokens, use another advisor's links, or substitute a generic embed/video URL. Match both video identity and detailed title; catalog labels may differ. Examples from Pinnacle: Annuities Are Pensions -> Guaranteed Lifetime Income Contract; FIA / ADL -> Asset Based Elder Care; Roth Conversion -> Tax Free Income from Your IRA; IUL vs Qualified Plan -> Retirement Plan Comparison; Safe Money Advisor -> Protect Your Retirement Accounts from Market Volatility.

Pinnacle's library contains 12 risk and 12 tax cards. Use those as reference inventory, verifying the new task's actual selection rather than inventing missing cards. Render each risk/tax card as a clickable GHL-hosted thumbnail that opens the complete advisor-specific viewing page in an on-page iframe popup. Keep the exact original href as a fallback and unload the iframe when closing. Reuse the matching approved shared GHL thumbnail from the Premium reference when supplied; keep its existing image URL while collecting the new advisor’s destination. Match by source video identity, not only title, especially for courses with identical labels. Capture card title, category, source video identity, thumbnail and complete advisor-specific viewing URL. Allow a newly selected catalog page to finish updating before extracting cards. Leave any temporary impersonation/subaccount mode appropriately when finished.

## Vimeo

Verify the account/folder and match each video to its intended slot. Use the exact signed 720p video file link from Video file links or an authoritative task record. Keep rendition, filename, query string and signature unchanged. HTML &amp; encoding is normal. A numeric video ID cannot reconstruct a signed playback URL. Do not replace file links with Vimeo page links or iframe URLs unless asked.

Prefer the existing Vimeo API integration when configured. Browser sign-in is a separate supported fallback, not an API credential; follow the available `vimeo-link-capture` skill. If the user has already signed in, inspect that session before asking for an integration path again. Copy from Video file links / Play the video / HD 720p and validate the copied URL against the exact source ID. Use only supported clipboard access; unrelated clipboard contents must not be returned or stored.

Honor account-only conversion when requested: keep original watch URLs, privacy hashes, query strings, and approved embeds for outside-account videos. Record these as user-approved retained originals separately from actual missing captures. Do not substitute an account-owned duplicate by title or repeatedly request another account after the user approves keeping the existing link. Store capture method and ID in task-local media data. A HEAD response of 200 with video/mp4 verifies file transport, not playback; retain the signed redirect, not its temporary CDN target.

Pinnacle has 14 Kai-Zen videos, plus advisor introduction and featured/estate videos. Its corrected title is Kai-Zen Mortgage Analogy; a title change does not alter the video URL. Download the thumbnail for each selected Vimeo video, upload it to the advisor’s GHL Media Storage, and render a clickable image using the returned GHL URL with a visible SVG play triangle. Clicking opens the independently scoped on-page video popup described in SKILL.md. Its native video source and fallback anchor destination use the exact signed HD 720p link from Video file links → Play the video, not the Download links panel, a Vimeo watch page, or an iframe. Associate each thumbnail, duration and playback link with the correct video. Signed links may expire; verify or recollect when needed and label playback checks accurately. The legacy resources use supplied BB video iframe embeds; preserve those when approved rather than forcing all media into Vimeo.

## GHL image hosting

Before final exports, collect the approved Drive images and the thumbnails/posters for selected Vimeo videos into the task workspace. Match each thumbnail to its source video ID and intended card before uploading. Preserve source quality, aspect ratio, and transparency; do not upload biographies/documents or whole Vimeo videos as part of this image-hosting step.

Confirm the advisor’s GHL location/subaccount from trusted task records and the active account. Use available supported GHL tools or authenticated browser Media Storage controls. With current-session authorization, upload the selected images there, reusing an existing verified hosted copy of the same asset in that location when available. Approved shared WebPrez thumbnails and existing strategic partner images may retain their supplied GHL URLs; this does not authorize copying advisor portraits or viewing links from another advisor. Do not upload to a different advisor’s account or change sharing/settings to work around access.

If the user chooses the skill/reference thumbnail links, preserve matching verified shared GHL URLs for all 42 standard cards, including Vimeo/Kai-Zen cards; do not reupload them just because destinations change. This explicit artwork choice overrides collecting replacement thumbnails for those slots only. Other new images still follow the normal hosting workflow.

Capture the actual public URL returned by GHL for each uploaded or reused asset; never construct a CDN URL from a filename. Record source Drive file ID/link or Vimeo video ID and thumbnail URL, local filename, GHL location, returned hosted URL, and the page/card/poster/background uses in the task-local asset manifest. Verify the returned URL loads the intended image without authentication.

Replace collection-source image URLs in generation data, HTML img sources, video poster attributes, CSS backgrounds, combined previews, and all affected Custom HTML blocks with the verified GHL URLs. Keep Vimeo playback URLs and approved third-party video embeds unchanged. For embedded third-party players whose internal thumbnail is controlled by that provider, record that limitation instead of claiming its internal artwork is GHL-hosted.

Check the final outputs for leftover Drive/Vimeo image sources and report any unresolved assets. Rebuild affected exports and the ZIP after URL replacement. Asset upload success does not imply the website was installed or published in GHL.

## Finish the manifest

Record exact destinations separately for booking, contact form, webinar, stress assessment, platform order, probate and Legacy Stories. Shared resources can be retained when confirmed by the task; advisor-specific URLs must come from the new advisor's records. Never use Pinnacle's booking, form, payment, stress tool or webinar links as defaults for another advisor. Credentials and browser sessions are not portable project assets.
