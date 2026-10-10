# Advisor Website Skills

Three reusable Codex skills, with their instructions, templates, references, and Python helpers.

| Skill | Purpose |
| --- | --- |
| `mvp-advisor-website` | Build or update MVP advisor GHL website sections while preserving the supplied layout. |
| `premium-advisor-website` | Build or update Premium advisor GHL websites and export separate HTML sections with CSS. |
| `vimeo-link-capture` | Capture exact signed 720p Vimeo file links for the selected advisor. |

## Install on another device

Open Codex on your new device and paste this prompt:

```text
Use $skill-installer to install all three skills from https://github.com/trisha-wq/Skills:
- skills/mvp-advisor-website
- skills/premium-advisor-website
- skills/vimeo-link-capture
Install them in the user-level skills location supported by this Codex version so they are available across projects.
```

If a skill does not appear, restart Codex. Invoke it using the skill selector or `$mvp-advisor-website`, `$premium-advisor-website`, or `$vimeo-link-capture`.

Alternatively, download this repository and copy the three complete skill folders into your project's `.agents/skills/` directory, or your personal `~/.agents/skills/` directory. Do not copy only `SKILL.md`; supporting resources are required.

Official discovery and installation guidance: https://learn.chatgpt.com/docs/build-skills

## Connections and runtime

- Sign in to the required ClickUp, Google Drive, Vimeo, WebPrez, and GHL accounts on each device when the workflow requires them. GitHub stores the skills, not those connections.
- The bundled Python helpers require Python 3 and use the standard library.
- Vimeo API capture requires your locally configured `VIMEO_ACCESS_TOKEN`. Optional team-owner configuration is described in the Vimeo skill. Credentials remain on your device and must not be committed.
- The Premium reference's original Windows project path is historical context, not a required dependency. Use supplied Premium code or the bundled styling baseline on another device.

## Updates

This is a versioned backup, not automatic synchronization of local edits. Commit and push future skill changes to this repository, then update the installed copies on your other devices.

Generated advisor websites and advisor-specific output are kept outside these skill folders.