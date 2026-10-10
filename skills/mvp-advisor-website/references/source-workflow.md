# Source collection for MVP advisors

## ClickUp first

Open the supplied task, verify the advisor's name, and inspect custom fields, description, attachments, linked project/list, and relevant project task descriptions. Record firm, professional title, location, business contact info, calendar, Drive folders, form, stress test, eStatePlan payment, webinar/event pages, Vimeo production links, and GHL subaccount if present. Project production tasks may contain media URLs absent from the account record.

A GHL agency contact-record URL is not the advisor's website subaccount. Do not use its location ID for website writes. Do not reuse the last advisor's URLs or fill blank credentials from memory. A failed marketing path does not justify guessed form or event paths.

## Google Drive

Use the connected Google Drive workflow to inspect the advisor folder and Bio, Photos, Roster and Logo subfolders. Prefer website-ready files when variants exist. Read the actual bio document to identify Website Bio and Print Bio. A folder name is weaker company-name evidence than the approved logo or explicit company field; record any inference.

Download approved assets to the current output bundle. Keep Drive file IDs and source links in the current manifest. Use public hosted asset URLs only when known; do not paste Drive preview pages or expiring authenticated download URLs into image src attributes. GHL upload/sharing is a separate externally mutating step within the current user's authorization.

## Vimeo

If library access is needed, inspect the signed-in account and find the folder named for the current advisor. Match the video title to the template slot. Use the visible video menu's **Video file links**, and select **720p**. Preserve the returned URL exactly; HTML encoding of `&` to `&amp;` is normal.

ClickUp production URLs can fill clearly identified slots without Vimeo login, but mark playback untested. The pilot explicitly mapped an eState Plan Intro video to the first featured card by user instruction; that mapping is not a universal rule. For new advisors, verify this slot rather than assuming all similarly named estate videos are interchangeable. Missing signed links cannot be recreated from a video ID alone.

## WebPrez

Find **My Group** and the exact advisor subaccount. If the dashboard is already inside that subaccount, verify the profile/sidebar identity and work there. If ambiguous, ask which group/account to use. The pilot dashboard exposed Winston Bramwell and his firm email; this is an example of identity evidence, not a login to reuse.

Open Videos / Done-For-You Videos. Catalog titles may differ from detailed page titles: for example, Annuities Are Pensions -> Guaranteed Lifetime Income Contract, FIA / ADL -> Asset Based Elder Care, Roth Conversion -> Tax Free Income from Your IRA, IUL vs Qualified Plan -> Retirement Plan Comparison, and Safe Money Advisor -> Protect Your Retirement Accounts from Market Volatility. Use detail titles and the card map to confirm the intended video.

On each matching video detail page, expand **Video Page Hypertext Links**, choose **Video Page Hypertext Link WITH Viewing Notice**, verify that exact dialog heading, and read the link from that dialog. The WITHOUT and WITH Lead Capture options are different. Do not take a hidden/background link or the generic Video URL in its place.

WebPrez pages can briefly show old card content after the page number changes. Check that visible cards have updated before collecting the next page. Ground browser locators in the observed DOM. If an action opens the wrong option or does nothing, inspect fresh state and use the currently observed control instead of repeating blindly.

The four Free Video Course cards represent distinct videos: risk 13 Estate Planning Campaign, risk 14 Retirement Savings Campaign, tax 13 Senior Market Campaign, tax 14 Family Life Campaign. Confirm these through video identity; do not collapse them by title.

The template's smartmoney.talk URLs identify the video separately from the advisor and signed viewing mode. The card map retains original video identities for matching only. Collect each advisor's full signed URL from their own dialog; do not synthesize a link from the map.

## Form and final assets

Use the actual advisor's GHL form iframe/embed URL; a contact record, calendar, or ordinary contact page is not a substitute. If absent, report the missing form/subaccount access. Maintain verified booking, stress test and order destinations separately. Generic shared resource links may stay as provided. Do not add invented advisor-specific redirects.
