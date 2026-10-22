# Topic gaps: Kurzgesagt and close competitors

_Checked 2026-10-22 against every video and Short title on 9 channels (~9,100 titles):
Kurzgesagt, MinuteEarth, MinutePhysics, TED-Ed, Veritasium, SciShow, SciShow Psych, Real Science, melodysheep._

Each topic below had **zero title matches** on any of these channels, including broader keyword variants.
The check uses titles only, so a topic could still appear briefly inside a video.

| # | Topic | Angle idea | Keywords checked |
|---|---|---|---|
| 1 | Brain-computer interfaces | People with implants are already typing with their thoughts. What comes next? | neuralink, brain-computer, brain chip/implant/interface |
| 2 | The glymphatic system | Your brain power-washes itself every night, and skipping sleep skips the cleaning | glymph, brain clean/wash |
| 3 | Senolytics and "zombie cells" | Cells that refuse to die drive aging, and drugs that kill them | senolytic, senescence, zombie cell |
| 4 | "Dark oxygen" on the sea floor | Metal nodules making oxygen without light, and the deep-sea mining fight over them | dark oxygen, nodule |
| 5 | Peak phosphorus | The element every farm needs, which can't be replaced and is mined in only a few countries | phosphor, fertilizer |
| 6 | Time crystals | Matter that repeats in time instead of space | time crystal |
| 7 | Lucid dreaming | Can you learn to control your dreams, and what is the brain doing when you do? | lucid |
| 8 | Wet-bulb temperature | The heat-plus-humidity level the human body cannot survive | wet-bulb, heat dome, heatwave |
| 9 | Vertical farming | Why most indoor farms went bankrupt, and whether they can work | vertical farm |
| 10 | Wolbachia mosquitoes | Releasing millions of bacteria-infected mosquitoes to stop dengue | wolbachia |

Near-gaps (covered once by SciShow or TED-Ed, never by Kurzgesagt): magnetars, sleep paralysis, tinnitus,
Long COVID, Boltzmann brains, zombie fires, direct-air carbon capture.

Re-run: `python tools/fetch_titles.py @kurzgesagt @MinuteEarth ...` then `python tools/topic_gaps.py titles.json`
(edit the candidate list in `tools/topic_gaps.py`).
