# Faceless YouTube Channel — Project Guide

This file gives Claude the context for this project. Read it at the start of every session.

## Project overview

We are building a **faceless YouTube channel**: videos made without the creator on camera. They are built from voiceover, stock footage or B-roll, motion graphics, AI-generated visuals, and on-screen text.

- **Channel name:** _TBD_
- **Niche / topic:** science adventures with a space focus: Episodes 1–2 cover topic gaps (time crystals, dark oxygen), then well-known space topics (supernovae, black holes, dark matter...). See `ideas/backlog.md`.
- **Target audience:** _TBD (age, interests, what they want from the channel)_
- **Video formats:** YouTube Shorts only (vertical 9:16). Natural speaking pace matters more than a 60 s cap: aim for ~55–75 s (Shorts can be up to 3 minutes).
- **Publishing cadence:** _TBD (e.g. 2 long-form + 5 Shorts per week)_
- **Tone & voice:** warm, playful, awe-struck science storytelling, narrated by our host Atlas (look approved). See `channel/character.md` and `channel/voice.md`.
- **Story format:** stand-alone, thriller-style mini-adventures packed with verified wow facts (one common thread, cold open in danger, twist, fact pops, loop ending; no cross-episode cliffhangers). See `channel/format.md`.
- **Visual style:** cozy cinematic storybook illustration (lantern light, starry mountain nights, detailed fur and textures). See `channel/style-guide.md` and the master reference `channel/reference/atlas-reference.webp`.

> Fill in the TBD fields as decisions are made. They steer every sub-agent.

## Workflow: the three-stage pipeline

Every video moves through three stages. Each stage has a dedicated sub-agent, and the output of each one is the input to the next.

```
1. RESEARCH  ──►  2. SCRIPTING  ──►  3. CONTENT CREATION
   (research/)       (scripts/)          (production/)
```

### 1. Research agent
- Finds and checks video ideas: trending topics, search demand, competitor gaps.
- Gathers facts, sources, statistics, and story angles for a chosen topic.
- **Output:** a research brief in `research/<video-slug>.md` with sources linked.
- **Rule:** every factual claim needs a source. Mark anything unverified as such.

### 2. Scripting agent (`.claude/agents/scriptwriter.md`)
- Follows `channel/format.md`; model script: `scripts/dark-oxygen.md`.
- Turns a research brief into a script for narration.
- Structure: **common thread → question chain (each answered right away) → 5–7 wow facts with fact pops → loop ending**.
- Writes for the ear: short sentences, plain words, no tongue-twisters.
- Includes visual cues in brackets, e.g. `[B-ROLL: city skyline at night]`, `[TEXT: "73%"]`.
- Proposes 3–5 title options and a thumbnail concept.
- **Output:** `scripts/<video-slug>.md`.

### 3. Content creation agent (`.claude/agents/content-creator.md`)
- **Phase 1:** makes a **first-frame preview** (`production/<slug>/preview/first-frame-vN.png`) and STOPS.
- **Approval gate:** show the preview to the creator. Only when they explicitly approve, write `Preview approved: yes` in `production/<slug>/STATUS.md`. If they give feedback, write `Preview approved: no` plus the feedback and run Phase 1 again.
- **Phase 2:** turns the script into a production kit: scene images, voiceover script, shot list, captions, upload text, and a rights log.
- **Output:** a folder at `production/<video-slug>/`.

## Folder structure

```
.
├── CLAUDE.md              # This file
├── .claude/
│   └── agents/            # Sub-agent definitions (researcher, scriptwriter, creator)
├── channel/               # Brand guide, style guide, audience notes, niche research
├── ideas/                 # Backlog of video ideas (ideas/backlog.md)
├── research/              # Research briefs, one per video
├── scripts/               # Finished scripts, one per video
├── production/            # Per-video production assets
└── published/             # Notes and performance data on published videos
```

## Naming conventions

- Use a **video slug** for each video: lowercase, hyphenated, and short, e.g. `why-rome-fell`.
- The same slug is used across `research/`, `scripts/`, and `production/` so files for one video are easy to find.
- Prefix the slug with a date when helpful: `2026-10-22-why-rome-fell`.

## Content standards

- **Accuracy first.** Do not invent facts, quotes, or statistics. Cite sources in research briefs.
- **Originality.** Do not copy competitor scripts. Add our own analysis and angle, because YouTube penalizes reused or mass-produced content.
- **Retention-focused.** Open with a strong hook, avoid long intros, and add a pattern interrupt every 30–60s.
- **Brand-safe.** Keep content advertiser-friendly unless the channel's niche decides otherwise.
- **Rights.** Use only royalty-free or properly licensed music, footage, and images. Note the source and license in the production folder.
- **AI disclosure.** Follow YouTube's rules for labelling realistic altered or synthetic content.

## Tools & stack

- Image and video generation: **Higgsfield** (connector). Fallback: layout sketches only, rendered with `tools/render_frame.py`
- Voiceover: **Higgsfield text-to-speech** (Eleven v4 / Text to Speech V2 with the ElevenLabs engine; on the website, no separate ElevenLabs plan needed). See `channel/voice.md`.
- Editing: _TBD (e.g. CapCut)_
- Channel analysis: `tools/channel_analysis.py`, `tools/fetch_titles.py`, `tools/topic_gaps.py` (yt-dlp)

## How Claude should work in this project

- Follow the pipeline in order. Don't write a script without a research brief, and don't make production assets without an approved script.
- **Never produce a video kit without an approved first-frame preview.** Always show the preview image to the creator and wait for an explicit yes.
- Save every output to the right folder using the video slug.
- When a decision belongs to the creator (niche, tone, title choice), offer options with a recommendation and ask.
- Keep `ideas/backlog.md` updated as new ideas come up.
- Update this file when channel-wide decisions change.
