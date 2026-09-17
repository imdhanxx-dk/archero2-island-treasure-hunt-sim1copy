# FUREVER — ANIME TEASER PACK

Two builds of the same material.

**→ `build_teaser_40.py` — the 40-second teaser. 4 chained clips. Start here.**
Each clip continues seamlessly from the last, so you generate four and lay them
end to end. No cutting required. Narration and the no-lip-sync lock are baked
into every prompt.

`build_prompts.py` — the long-form pack: 26 shots, a 2:40 core cut and a 4:20
extended cut, for when you want an actual trailer rather than a teaser.

## The 40-second teaser

| Clip | Time | Beat | Narration |
| --- | --- | --- | --- |
| 1 | 0:00–0:10 | **The Full Sky** — the scarf, ten lights, pull back to Lumi small in an enormous warm world | *"Ten stars. And one small cat, who carried every single one of them — for exactly as long as they wished to stay."* |
| 2 | 0:10–0:20 | **The Break** — lights stutter and die, a beat of pure black, Noctra walks out of it | *"Then something came up out of the dark that the world had spent four hundred years agreeing had never existed."* |
| 3 | 0:20–0:30 | **The Homing** — the scarf tears, ten lights blow past the lens and streak across the whole sky | *"They did not leave because they were afraid of him. They left because they were tired of being carried."* |
| 4 | 0:30–0:40 | **The Empty Sky** — dawn, he wakes with nothing, touches an empty ring, black, one gold point | NOCTRA: *"Find them. And when you remember — find me."* |

Run it:

```bash
python3 furever/anime/build_teaser_40.py
```

Then paste `out/teaser40_prompts.txt` — four lines, four clips.

### Three things that make it work

**The narrator is Noctra.** He talks about Lumi in third person for thirty
seconds, then in clip 4 the same voice speaks *to* him. Nothing signposts it.
Don't perform the reveal — the shift from description to imperative does it.

**Colour is spent, not used.** Clip 1 carries all ten hues. From the moment the
lights blow past the lens in clip 3 there is no saturated colour left until the
single gold point at the end. Don't grade warmth back into clip 4.

**The beat of black in clip 2 is not dead air.** Total silence, no room tone.
Everything before it is warm and everything after it is not, and the audience
needs one beat in the dark to feel the floor go.

### Chaining

Feed the **last frame of each clip in as the first frame of the next**. Every
prompt opens with the continuity instruction, but image conditioning is what
actually holds it together — wording alone won't.

Every prompt also carries an explicit **NO LIP SYNC** block in both the positive
and the negative, so nobody's mouth moves to the voice-over. The narration is
off-screen; it doesn't belong to anyone in frame.

## Files

| File | What it's for |
| --- | --- |
| [`build_teaser_40.py`](build_teaser_40.py) | **The 40s teaser.** 4 chained clips, narration and lip-sync lock built in |
| `out/teaser40_prompts.txt` | The 4 prompts, one per line — paste straight into your queue |
| `out/teaser40_prompts.md` | The same 4, readable, with per-clip sound and grading notes |
| `out/teaser40_narration.txt` | VO script for the voice session |
| [`style-bible.md`](style-bible.md) | The look, character locks, colour script, camera language |
| [`build_prompts.py`](build_prompts.py) | The long-form 26-shot trailer pack |
| `out/core_cut_10s.txt` | 16 prompts — the 2:40 trailer cut |
| `out/bulk_prompts_10s.txt` | All 26 trailer prompts |
| `out/narration_core.txt` / `narration_extended.txt` | Trailer VO, timecoded per cut |
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
