# Voice Guide: Atlas (narrator)

**Status: proposal. Awaiting creator approval.**

## The brief

The creator's reference is the *style* of a famous astrophysicist-presenter: warm, playful, awe-struck science storytelling.
We aim for that **style of delivery**, not that person's voice.

**Rules (legal and platform safety):**
- Never clone, imitate or name a real person in a voice tool, prompt, title or description.
- The voice must not be recognisable as any specific real person. If listeners say "that's X", change it.
- Use a voice designed from attributes (below), or an original voice actor.

## Voice attributes

- **Timbre:** warm, rich **baritone**, slightly gravelly, mid-50s male. American English, neutral accent.
- **Energy:** conversational and *delighted*, like explaining something amazing to a friend across a kitchen table.
- **Rhythm:** big contrasts. He speeds up with excitement, then **slows right down** for the key idea.
  He likes dramatic pauses ("...and that's... impossible.").
- **Emphasis:** leans hard on single words ("It. Doesn't. Stop."). He smiles audibly on the punchlines.
- **Pace:** about 150–160 words per minute on average. That's fast for the hook and slow for the reveal.
- **Avoid:** announcer voice, a breathy ASMR whisper, robotic flatness, or a sarcastic tone.

## Where to make it: Higgsfield (no extra subscription)

Higgsfield's audio models include **Eleven v4** (ElevenLabs), **Text to Speech V2** (engines: ElevenLabs, MiniMax,
Seed Speech, Vibe Voice, Cozy Voice), **Qwen Audio 3.0 TTS** and **Seed Audio 1.0**. They run on the Higgsfield
website. The public API docs (2026-10-23) list no speech models, so the voiceover is made on the website for now.

1. Open a text-to-speech model (start with Eleven v4 or Text to Speech V2 → ElevenLabs engine).
2. Browse the **preset** voices and pick a warm, deep, mature male voice that fits the attributes below.
3. Paste the voiceover text from `scripts/<slug>.md` and generate. Note the voice ID here so every episode uses the same voice.
4. Never use the "reference element" (voice cloning) option with a recording of a real person.

## ElevenLabs "Voice Design" prompt (only if you later use ElevenLabs directly)

> A warm, rich, slightly gravelly baritone voice of a man in his mid-fifties with a neutral American accent.
> He sounds like an enthusiastic science storyteller: friendly, playful and full of wonder, with an audible smile.
> He speaks conversationally with lively pacing, dramatic pauses before big reveals, and strong emphasis on key words.
> Clear studio-quality recording, close microphone, no background noise.

Generate 3 options, pick the one that best fits Atlas, and save its voice ID here.

- **Chosen voice ID:** _TBD_
- **Settings:** stability ~40% (expressive), similarity ~75%, style exaggeration ~30%. Tune by ear.

## Script markup for the voiceover

- `...` = a short dramatic pause
- `*word*` = strong emphasis
- `[whisper]`, `[excited]`, `[slow]` = delivery cues (remove them, or turn them into tool tags, before generating)
