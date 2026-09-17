# FUREVER — ANIME TEASER PACK

A **game announce teaser** for *FurEver: The Lost Starkeeper*, built as
**26 × 10-second anime shots** with timed background narration.

- **CORE CUT** — 16 shots — **2:40** ← build this one first
- **EXTENDED CUT** — 26 shots — **4:20**

## Files

| File | What it's for |
| --- | --- |
| [`style-bible.md`](style-bible.md) | The look, the character locks, the colour script, camera language, narrator direction |
| [`build_prompts.py`](build_prompts.py) | The shot list itself + the generator. Edit shots here, re-run |
| `out/character_refs.txt` | **Generate these 3 first.** Reference stills for Lumi, Noctra, the scarf |
| `out/core_cut_10s.txt` | 16 prompts, one per line — the 2:40 teaser |
| `out/bulk_prompts_10s.txt` | All 26 prompts, one per line |
| `out/narration_core.txt` | VO script, timecoded to the core cut |
| `out/narration_extended.txt` | VO script, timecoded to the extended cut |
| `out/shots.csv` | The whole edit as a spreadsheet, both timelines |

Regenerate after editing the shot list:

```bash
python3 furever/anime/build_prompts.py
```

## How to actually run this

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

## Structure of the teaser

| Act | Shots | What it does |
| --- | --- | --- |
| **I. The Full Sky** | 01–04 | Veylora, the ten living stars, a small cat who carries them. Warm, abundant, ordered. |
| **II. The Break** | 05–11 | The Vault. Noctra. The fight Lumi refuses to win. The scarf tears. **The Homing.** |
| **III. The Empty Sky** | 12–16 | The map burns. He wakes in a field with no name. One joke, to prove he's still himself. |
| **IV. Ten Regions** | 17–21 | The world the stars broke by going home. Gameplay-flavoured. |
| **V. The Pursuer** | 22–24 | Something has been following him. It has not attacked once. |
| **VI. Title** | 25–26 | *"— find me."* |

## The three things that make it not generic

**The narrator is Noctra.** Nothing signposts it. He spends the whole teaser
talking about Lumi in the third person, warmly, and on shot 24 his voice walks
into frame. Everything he said gets re-read in one beat.

**Colour is a currency.** Shots 01–04 have all ten hues. After the Homing the
world goes desaturated, and each region returns exactly one colour. Don't spend
a hue before its shot.

**Five shots are silent on purpose.** 04, 06, 09, 10, 13. Do not fill them. A
teaser narrated wall to wall has no teaser in it — the silence is where the
audience decides they want the game.
