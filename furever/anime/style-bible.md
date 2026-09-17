# FUREVER — ANIME TEASER: ART DIRECTION & PROMPT SYSTEM

Everything here is built for **10-second shots** in an AI video generator, cut
together into a **game announce teaser** for *FurEver: The Lost Starkeeper*.

---

## 1. THE STYLE ANCHOR

Paste this verbatim at the head of **every** prompt. Consistency comes from
repetition, not from cleverness.

```
STYLE: 2D cel-shaded Japanese anime, theatrical feature-film quality, hand-drawn
key-animation look, crisp confident ink linework with varied line weight, flat
cel shading with hard-edged shadow terminators, warm rim light separating
subject from background, lush hand-painted gouache backgrounds in the classic
Japanese anime background-art tradition, rich cinematic color script, volumetric
god-rays, floating dust and pollen particulate, subtle 35mm film grain,
anamorphic lens flare, shallow depth of field, 2.39:1 cinemascope, 24fps,
no on-screen text, no subtitles, no watermark, no logo
```

## 2. THE NEGATIVE PROMPT

```
NEGATIVE: 3D render, CGI, Pixar style, photorealistic, live action, plastic
sheen, western cartoon, chibi, deformed anatomy, extra limbs, extra tails,
melting faces, morphing features, flickering, warped eyes, mismatched eye color,
human faces on animals, text, letters, captions, subtitles, watermark,
signature, UI overlay, low contrast mush, oversaturated neon clipping, jerky
motion, frame blending, duplicated characters, crowd of cats
```

---

## 3. CHARACTER LOCKS

Paste the relevant lock **verbatim, every time the character appears.** Do not
paraphrase. Do not abbreviate. Drift in these three blocks is the number one
cause of a teaser that looks like four different films.

### LUMI_LOCK
```
LUMI: a small white cat, true feline proportions on four legs, fluffy fur with a
faint cream undertone at ears and tail-tip, large round pale-gold eyes with
vertical pupils, thin delicate gold filigree markings tracing his forelegs and
across his brow, wearing a long dark indigo-navy scarf of woven-night fabric
with ten small circular silver fastenings stitched along it, scarf ends frayed
and trailing behind him
```

### NOCTRA_LOCK
```
NOCTRA: an enormous black cat, four to five times Lumi's size, fur so absolutely
black it reads as a hole cut in the frame and absorbs surrounding light, pale
violet eyes with slit pupils that emit a faint glow, thin violet fracture-lines
crawling across his body like lightning trapped beneath stone, black smoke
drifting continuously off his silhouette, a large cracked violet gem set in his
chest with a single hairline gold fracture across it
```

### SCARF_LOCK *(for close-ups where the scarf is the subject)*
```
THE NIGHTWEAVE: a long dark indigo scarf of impossibly black woven fabric that
light falls into rather than off, ten small circular silver fastenings stitched
along its length in an irregular constellation pattern, each fastening empty and
dark, frayed trailing ends
```

---

## 4. THE COLOR SCRIPT

The teaser runs a deliberate three-stage color journey. Say the stage in the
prompt.

| Stage | Shots | Palette | Feeling |
| --- | --- | --- | --- |
| **THE FULL SKY** | 01–04 | warm gold, deep teal, ten distinct saturated accent hues all present at once | abundance, order |
| **THE BREAK** | 05–11 | violet and near-black, all other hues draining out, single gold accent | violation, loss |
| **THE EMPTY SKY** | 12–19 | desaturated daylight, pale green-gold, colour returning one hue at a time | tenderness, slow return |
| **THE PURSUER** | 20–23 | indigo night, violet, a single warm lantern | dread turning to something else |
| **TITLE** | 24–26 | black, with one point of gold | promise |

**The single most important visual rule in the whole teaser:**
after shot 09, **colour is a currency.** The world goes grey-ish and each Star's
hue returns one at a time. Do not spend a colour before its shot.

---

## 5. CAMERA LANGUAGE

Because every clip is ten seconds, every clip is **one continuous move**. Never
describe a cut inside a shot — generators will either ignore it or produce a
morph.

| Character | Camera behaviour |
| --- | --- |
| **Lumi** | Low angle, near the ground, at his eye height. Handheld micro-drift. The camera is *with* him. |
| **Noctra** | Locked off, slow, geometrically precise push-ins. The camera is *afraid* of him and will not move quickly. |
| **The Stars** | Wide, static, reverent. Let them cross the frame. |
| **Veylora** | Slow lateral dolly and crane reveals. The world is bigger than the story. |

---

## 6. HOW TO WRITE A TEN-SECOND SHOT

Every shot in this pack has a **three-beat arc** baked into the prompt. This is
what makes a clip feel like ten seconds of film instead of ten seconds of a
looping gif.

```
0–3s   establish — the frame settles, one element already in motion
3–7s   develop — the action or the camera move commits
7–10s  land     — a change of state: a light dies, eyes open, a head turns
```

Write it as one flowing sentence of continuous action. **One** subject. **One**
camera move. **One** change of state.

---

## 7. AUDIO / NARRATION

Every shot carries a **background narration line (VO)** timed to fit ten seconds
at a measured trailer pace — roughly **22–26 words**, or fewer.

Shots marked `VO: —` are **deliberately silent.** Do not fill them. A teaser
with wall-to-wall narration has no teaser in it; the silence is where the
audience decides they want the game.

**Narrator voice direction:** low, unhurried, warm, close-mic'd. Not a
movie-trailer boom. The register of somebody telling you something true late at
night. Slight roughness. He is remembering, not announcing.

*(In the final game this narration is revealed to be Noctra. Do not signpost
this in the teaser. The last two lines should retroactively give it away.)*

---

## 8. TECHNICAL SETTINGS

- **Aspect:** 2.39:1 (or 16:9 and letterbox in the edit)
- **Duration:** 10s per clip
- **Resolution:** highest the model offers; upscale after, not during
- **Seed:** lock one seed per character and reuse it across all their shots
- **Consistency:** if your generator supports image conditioning, render the
  three **character-lock reference stills first**, then use them as the first
  frame / reference image for every shot that character is in. This matters far
  more than prompt wording.
- **Generate 3–4 takes per shot.** Ten-second AI clips fail on motion, not on
  composition; you are fishing for the one where the face holds.

---

## 9. THE CUT

- **CORE TEASER CUT** — 16 shots, **2 minutes 40**. Marked `[CORE]`.
- **EXTENDED CUT** — all 26 shots, **4 minutes 20**.

Build the core first. Add from the extended pack only where the core feels thin.
