# FUREVER — ANIME TEASER PACK

**Using Google Flow? → `out/FLOW_PROMPTS.txt`.** Flow is Veo, and it needs a
different build: 8-second clips, a separate negative field, one camera move per
shot, and explicit framing so subjects stop leaving the frame.

**9 clips × 8s = 1:12**, two drops, ending on a **FUREVER / PLAY NOW** end card.

| Clip | Time | Beat |
| --- | --- | --- |
| 1 | 0:00–0:08 | The world — Lumi running, ten lights lit |
| 2 | 0:08–0:16 | The lights die, the Vault, the build |
| 3 | 0:16–0:24 | **DROP ONE** — Noctra reveal |
| 4 | 0:24–0:32 | The scarf tears, the Homing |
| 5 | 0:32–0:40 | Half-time — the broken world, three regions |
| 6 | 0:40–0:48 | **DROP TWO** — Lumi's power moment |
| 7 | 0:48–0:56 | Stripped — the pursuer in the rain |
| 8 | 0:56–1:04 | Music cuts dead — he wakes with nothing |
| 9 | 1:04–1:12 | Clean plate → **FUREVER / PLAY NOW** |

```bash
python3 furever/anime/build_flow_teaser.py
```

**Anything else → `build_teaser_40.py`, the 40-second beat-synced teaser.**

Built the way anime edits are actually built: on a BPM grid, with a buildup, a
hard gap, and the character reveal landing **on the drop**.

```
150 BPM | 1 beat = 0.4s | 1 bar = 1.6s | 40s = 100 beats = 25 bars
36 cuts, every one of them on a beat
```

```bash
python3 furever/anime/build_teaser_40.py
```

**All eight prompts live in one file: `out/ALL_PROMPTS.txt`.** Each prompt is a
single line — triple-click selects the whole thing. Headers above each one say
which references to attach and what the narration is.

## The structure

Gojo's blindfold comes off on the drop. Gear 5 lands on the drop. The Dandadan
OP does the same thing. It's one shape, and it's the shape this uses:

| Bars | Time | Section | Cutting |
| --- | --- | --- | --- |
| 1–4 | 0:00–0:06.4 | Cold open | 3 cuts, long. Sub-bass only. |
| 5–8 | 0:06.4–0:12.8 | The world | 4 cuts, one per bar. Beat enters. |
| 9–12 | 0:12.8–0:19.2 | The build | 8 cuts, halving. Riser. |
| **13** | **0:19.2–0:20.8** | **THE GAP** | **Black. Total silence.** |
| 14–17 | 0:20.8–0:27.2 | **THE DROP** | 8 cuts. Noctra reveal on the downbeat. |
| 18–20 | 0:27.2–0:32.0 | The break | 6 cuts. The scarf tears. |
| 21–22 | 0:32.0–0:35.2 | The Homing | 1 cut, held long. Biggest hit. |
| 23–24 | 0:35.2–0:38.4 | The fall | 3 cuts. Music stops dead. |
| 25 | 0:38.4–0:40.0 | Title | Logo slams on the downbeat. |

Full 36-cut list, music brief and post recipe: `out/teaser40_edit.md`

## The music idea worth keeping

The four-note lullaby Noctra wrote for Lumi is stated clean and gentle on a lone
plucked instrument in bar 1 — and **the drop is the same four notes**, distorted,
pitched down, played as a riff.

The hype and the story are the same melody. That's what stops it feeling like a
generic edit with a cat in it.

## Getting references to actually stick

Gemini/Veo drifts off-model unless you outrank the text. Every prompt now opens
with a binding reference block that says, in terms:

> *If anything in the text below appears to conflict with an attached reference
> image, **THE REFERENCE IMAGE WINS**.*

Plus off-model terms in the negative (`redesigned character`, `generic cat`,
`wrong markings`, `character drift`). On top of that:

1. **Attach the references on every single generation**, not just the first. A
   reference from three prompts ago is not in context.
2. **Chain last frame → first frame** between clips. Text continuity alone won't
   hold four clips together.
3. If it still drifts, **attach fewer references** — one character per generation
   beats three at once, which is why clip 3 (Lumi *and* Noctra) is the one most
   likely to go off-model.
4. Regenerate rather than argue. A drifted take doesn't recover.

## Voice

Deep now, not warm:

> *Deep male, heavy chest resonance, gravel in the bottom end, close-mic'd with
> audible breath. Track it twice and pitch the second take a full octave down
> underneath the first at about −12dB, so there's a floor beneath the voice you
> feel more than hear. Stone-room reverb tail, dry signal forward. Slow and
> weighted — every word lands like something heavy being set down. Not a
> hype-man, not a trailer boom. He is remembering, not announcing. (It is
> Noctra. Do not play it that way yet.)*

**17 words in 40 seconds**, and none at all across the drop. The music carries
it — every line is a stab landing in a gap, not a sentence flowing over a
section.

| Time | Speaker | Line |
| --- | --- | --- |
| 0:02.4 | Narrator | *"Ten stars."* |
| 0:09.6 | Narrator | *"One keeper."* |
| 0:13.6 | Narrator | *"They all left him."* |
| 0:35.2 | Noctra | *"Find them."* |
| 0:38.4 | Noctra | *"And when you remember — find me."* |

## Prompt vs. post

**In the prompt** (the generator can do these): whip pans, crash zooms, speed
ramps, motion blur, smear frames, impact poses, debris past the lens.

**In the edit only** (never prompt for these — they bake in badly and you lose
control of which frame they land on): beat-synced shake, impact frames, RGB
split, glow pump, zoom punches, the title.

## Clips

**4 core** — chained, continuous, cover the whole 40s.
**4 optional hero inserts** — `out/teaser40_inserts.txt`. Four clips can carry
this; eight makes it look like the reference edits, because the drop wants hero
shots it doesn't have to share with a continuous take.

## Files

| File | What it's for |
| --- | --- |
| `out/FLOW_PROMPTS.txt` | **Google Flow / Veo build — 9 clips, negative field, end-card spec** |
| [`build_flow_teaser.py`](build_flow_teaser.py) | The Flow builder |
| `out/ALL_PROMPTS.txt` | All 8 prompts for other generators, plus workflow and VO |
| [`build_teaser_40.py`](build_teaser_40.py) | The 40s beat-synced teaser builder |
| `out/teaser40_prompts.txt` | Just the 4 core prompts, if you want them separate |
| `out/teaser40_inserts.txt` | Just the 4 optional hero inserts |
| `out/teaser40_edit.md` | 36-cut beat grid, music brief, post recipe |
| `out/teaser40_narration.txt` | VO script |
| [`style-bible.md`](style-bible.md) | Look, character locks, colour script, camera |
| [`build_prompts.py`](build_prompts.py) | The long-form 26-shot trailer pack |
| `out/core_cut_10s.txt` / `bulk_prompts_10s.txt` | Trailer prompts, 2:40 and 4:20 |
| `out/narration_core.txt` / `narration_extended.txt` | Trailer VO |
| `out/character_refs.txt` | Reference stills for Lumi, Noctra, the scarf |
| `out/shots.csv` | The trailer edit as a spreadsheet |

## The long-form trailer

Only if you want the 2:40 or 4:20 cut rather than the teaser.

```bash
python3 furever/anime/build_prompts.py
```

### How to run it

1. **Generate the three character references first.** Everything else depends on
   them. Pick the best Lumi, the best Noctra, the best scarf, and keep them.
2. **Feed those back in as reference / first-frame images** for every shot the
   character appears in. This does more for consistency than any amount of
   prompt wording.
3. **Lock a seed per character** and reuse it across all their shots.
4. Paste `out/core_cut_10s.txt` into your batch queue — each line is one
   complete, self-contained 10-second prompt.
5. **Render 3–4 takes of every shot.** Ten-second AI clips fail on motion, not
   composition. You are fishing for the one where the face holds.
6. Cut to the narration script. Record VO first and cut picture to it.

### Structure of the trailer

| Act | Shots | What it does |
| --- | --- | --- |
| **I. The Full Sky** | 01–04 | Veylora, the ten living stars, a small cat who carries them. Warm, abundant, ordered. |
| **II. The Break** | 05–11 | The Vault. Noctra. The fight Lumi refuses to win. The scarf tears. **The Homing.** |
| **III. The Empty Sky** | 12–16 | The map burns. He wakes in a field with no name. One joke, to prove he's still himself. |
| **IV. Ten Regions** | 17–21 | The world the stars broke by going home. Gameplay-flavoured. |
| **V. The Pursuer** | 22–24 | Something has been following him. It has not attacked once. |
| **VI. Title** | 25–26 | *"— find me."* |

### What makes it not generic

**The narrator is Noctra.** Nothing signposts it. He spends the whole teaser
talking about Lumi in the third person, warmly, and on shot 24 his voice walks
into frame. Everything he said gets re-read in one beat.

**Colour is a currency.** Shots 01–04 have all ten hues. After the Homing the
world goes desaturated, and each region returns exactly one colour. Don't spend
a hue before its shot.

**Five shots are silent on purpose.** 04, 06, 09, 10, 13. Do not fill them. A
teaser narrated wall to wall has no teaser in it — the silence is where the
audience decides they want the game.
