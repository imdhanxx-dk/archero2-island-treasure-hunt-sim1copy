#!/usr/bin/env python3
"""
FurEver - 40-SECOND ANIME TEASER, BEAT-SYNCED.

Built the way anime edits are actually built: on a BPM grid, with a buildup,
a hard gap, and the character reveal landing ON the drop.

    150 BPM | 1 beat = 0.4s | 1 bar = 1.6s | 40s = 100 beats = 25 bars
    36 cuts, every one of them on a beat.

Four core clips are generated at 10s each and shredded into 36 cuts in the
edit. Four optional hero-shot inserts are included - they are what the drop
actually needs, and eight clips gets materially closer to the reference edits
than four does.

    python3 build_teaser_40.py

Outputs into ./out/ :
    teaser40_prompts.txt           the 4 core clips, one prompt per line
    teaser40_inserts.txt           4 optional hero-shot inserts
    teaser40_edit.md               beat grid, 36-cut list, music brief, post recipe
    ALL_PROMPTS.txt                EVERYTHING in one file - start here
    teaser40_narration.txt         VO only
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_prompts import STYLE, NEGATIVE, LOCKS, REFERENCE, OFF_MODEL_NEG  # noqa: E402

CLIP_SECONDS = 10
BPM = 150
BEAT = 60.0 / BPM          # 0.4s
BAR = BEAT * 4             # 1.6s

CONTINUITY = (
    "Continue the video seamlessly from the last scene of the previous clip. "
    "Keep the same characters, appearance, clothing, environment, camera style, "
    "lighting, and overall visual consistency. The new scene must naturally begin "
    "exactly where the previous scene cut ended."
)

# Deep, not warm. This replaces the earlier softer read.
VOICE_DIRECTION = (
    "Voice: deep male, heavy chest resonance, gravel in the bottom end, close-mic'd "
    "with audible breath. Track it twice and pitch the second take a full octave "
    "down underneath the first at about -12dB, so there is a floor beneath the voice "
    "you feel more than hear. Stone-room reverb tail, dry signal kept forward. Slow "
    "and weighted - every word lands like something heavy being set down. Not a "
    "hype-man, not a trailer boom. He is remembering, not announcing. (It is Noctra. "
    "Do not play it that way yet.)"
)

NO_LIPSYNC = (
    "NO LIP SYNC: the narration is off-screen voice-over only. No character in "
    "frame is speaking. Every character's mouth stays closed and still throughout "
    "the entire shot. Do not animate mouths, jaws, muzzles or whiskers to match the "
    "narration. Do not sync any facial movement to the audio. The voice does not "
    "belong to anyone visible in the frame."
)

KINETIC = (
    "ENERGY: high-velocity anime action cinematography. Fast whip pans, crash "
    "zooms, snap rack-focus, hard speed ramps between slow motion and full speed, "
    "dynamic motion blur, anime smear frames on fast movement, speed lines, debris "
    "and particulate blasting past the lens, the camera physically jolting on "
    "impacts. Every frame is in motion. Nothing in this shot is slow or "
    "contemplative."
)

# Post-only effects. Asking a generator for these corrupts the image.
NO_POST = (
    "chromatic aberration, RGB split, glitch art, datamosh, VHS artifacts, film "
    "scratches, lens dirt overlay, light leak overlay, baked-in text, title cards, "
    "letterboxing bars, vignette overlay, social media UI, progress bar"
)

# ---------------------------------------------------------------------------
# THE FOUR CORE CLIPS
# ---------------------------------------------------------------------------

CLIPS = [
    dict(
        n=1, tin="0:00", tout="0:10", title="HOOK + THE WORLD",
        stage="THE FULL SKY - all ten hues blazing at once, saturated warm gold and deep teal, maximum abundance",
        locks=["lumi", "scarf"],
        vo="Ten stars. One keeper.",
        body=(
            "Open in extreme macro hurtling along the length of the black scarf at "
            "speed, the camera whipping past silver fastenings so fast that each living "
            "star inside them streaks across the lens as a bar of pure colour - "
            "green-gold, silver, ice blue, ember red - strobing past in motion blur. A "
            "hard snap rack-focus lands on the final fastening, which is empty. Dark. "
            "Then an immediate crash zoom outward and the frame rips open to reveal "
            "LUMI running flat out along a high ridge at golden hour, the camera racing "
            "alongside him low to the ground, grass and flowers whipping past the lens "
            "in heavy motion blur, the ten coloured lights trailing behind him like a "
            "comet tail. The camera pulls up and back hard into an enormous crane "
            "reveal of the whole of Veylora spread out below - forest, glass coastline, "
            "far mountains under a vast dusk sky. He skids to a stop on the ridge "
            "edge, scarf snapping forward past him, and his head comes up."
        ),
        note=("This is the only clip with warmth and speed together. Everything after "
              "takes it away. END FRAME: Lumi stopped on the ridge, head up, ten lights "
              "lit. Clip 2 continues from exactly this."),
    ),
    dict(
        n=2, tin="0:10", tout="0:20", title="THE BUILD + THE GAP",
        stage="THE BREAK - colour violently draining, violet and near-black flooding in",
        locks=["lumi", "noctra"],
        vo="They all left him.",
        body=(
            "Continue on LUMI stopped on the ridge. The ten coloured lights along his "
            "scarf strobe violently and snap out one after another in a hard stutter, "
            "the warm light draining out of the entire landscape with them. A fast whip "
            "pan smears the environment sideways and it resolves into the vast "
            "underground Star Vault - black pillars, gold mosaic floor, carved "
            "constellation dome. Darkness floods across the mosaic like spilled liquid, "
            "swallowing the gold. Lumi spins on the spot. Crash zoom into the black "
            "behind him where two pale violet eyes snap open, far higher than they "
            "should be. Then NOCTRA slams down into frame from above, an impact dust "
            "ring blasting outward across the floor and the camera physically jolting "
            "on the hit. Snap zoom onto his face as his head lowers toward the lens, "
            "and the cracked violet gem in his chest detonates with light."
        ),
        note=("The eyes-open beat is the reveal. Hold the last frame stable - the edit "
              "puts a hard black gap in front of the slam and that gap only works if "
              "the frames around it are clean. END FRAME: Noctra huge, gem blazing."),
    ),
    dict(
        n=3, tin="0:20", tout="0:30", title="THE DROP + THE HOMING",
        stage="THE BREAK into total desaturation - this clip spends the last colour in the teaser",
        locks=["lumi", "noctra"],
        vo="",
        body=(
            "Continue from NOCTRA close in the dark and go straight into explosive "
            "action. A sheet of living shadow tears across the mosaic floor; LUMI "
            "leaps through frame in heavy motion blur, the gold filigree on his "
            "forelegs igniting mid-air, and a curved golden barrier slams up between "
            "them on a hard flash of light. The shadow smashes into it and breaks "
            "around it in violent arcs, pillars exploding, gold mosaic blasting up into "
            "the air. He skids backward across the floor, barrier held, never striking "
            "outward. The claw of darkness rises and comes down - and the shot ramps "
            "hard into extreme slow motion as it strikes the scarf, the fabric tearing "
            "open and all ten fastenings bursting apart in sequence, the ten coloured "
            "lights blowing outward past the lens in long trailing streaks. Then the "
            "speed ramps back to full and the camera rockets straight upward through "
            "the collapsing roof into the open night sky, where the ten beams climb, "
            "split apart, and tear away over ten different horizons."
        ),
        note=("The busiest clip - the edit pulls nine cuts out of it. Generate this one "
              "the most times. The slow-motion tear and the ramp back out are what sell "
              "it. END FRAME: ten trails fading across a black sky."),
    ),
    dict(
        n=4, tin="0:30", tout="0:40", title="THE FALL + TITLE",
        stage="THE EMPTY SKY - pale washed-out desaturated daylight, no saturated colour anywhere until one gold point",
        locks=["lumi", "scarf"],
        vo="NOCTRA (V.O.): \"Find them. And when you remember - find me.\"",
        body=(
            "Hard transition from the emptied night sky into pale washed-out dawn at "
            "ground level in tall meadow grass, lens almost touching the soil. LUMI's "
            "eyes snap open in the foreground. He pushes himself up fast and "
            "disoriented, head whipping left and right across a landscape he plainly "
            "does not recognise, breathing hard. He looks down and grabs at the torn "
            "indigo scarf, touching one empty silver fastening - nothing - then the "
            "next, then the next, faster and faster along the row, and then he stops "
            "dead. His ears flatten. The camera crash zooms into the empty fastening "
            "until the frame falls entirely to black. Hold on black. Then one small "
            "point of warm gold light ignites at the exact centre and blooms outward, "
            "faintly revealing the black weave and the ghosts of ten empty silver rings "
            "arranged around it."
        ),
        note=("The tonal whiplash out of the Homing into daylight and silence is the "
              "whole trick - it is the equivalent of the beat dropping out. Keep it "
              "pale, do not grade warmth back in. Last 2s is a clean title plate; "
              "composite the logo in the edit, never in the prompt."),
    ),
]

# ---------------------------------------------------------------------------
# OPTIONAL HERO-SHOT INSERTS
# These are the shots the drop actually wants. Four core clips can carry the
# teaser; eight makes it look like the reference edits.
# ---------------------------------------------------------------------------

INSERTS = [
    dict(
        n="I1", title="LUMI HERO - the barrier at full power",
        stage="THE BREAK - gold against near-black, one hue only",
        locks=["lumi"],
        body=(
            "Low hero angle looking up at LUMI braced on the shattered mosaic floor, "
            "the camera slowly orbiting him. The gold filigree on his forelegs and brow "
            "is blazing at full power and a huge curved golden barrier of light stands "
            "above and around him, taking a continuous battering of shadow that breaks "
            "across it in arcs. His scarf snaps violently in the pressure wave. Debris "
            "and fragments of gold mosaic hang and tumble in the air around him. He is "
            "tiny and he is not moving back."
        ),
        use="The drop. Lands on the bar where his power beat should hit.",
    ),
    dict(
        n="I2", title="NOCTRA HERO - full height, head turn",
        stage="THE BREAK - violet and absolute black",
        locks=["noctra"],
        body=(
            "Extreme low hero angle looking steeply up at NOCTRA standing at full "
            "height, filling the entire frame against pure black, the camera pushing "
            "in slowly and steadily. Black smoke pours off his silhouette and rises "
            "past the lens. The violet fracture-lines across his body pulse brighter "
            "and brighter. In the last beats of the shot his head turns down and "
            "toward the camera and his pale violet eyes lock directly onto the lens."
        ),
        use="The reveal shot. This is the one that goes on the downbeat of the drop.",
    ),
    dict(
        n="I3", title="THE GOLD FRACTURE",
        stage="THE BREAK - violet, with a single warm gold intrusion",
        locks=["noctra"],
        body=(
            "Extreme macro on the cracked violet gem set in NOCTRA's chest, filling the "
            "entire frame, lit from within. The violet light pulses hard, twice. Then a "
            "single hairline fracture of warm gold splits across the surface of the gem "
            "from one edge to the other, glowing far brighter than the violet around "
            "it, and something pale and starlike moves once behind the crack. The "
            "violet pulse stutters out of rhythm."
        ),
        use="One-beat flash cut. Nobody understands it yet. That is the point.",
    ),
    dict(
        n="I4", title="A STAR CROSSING THE WORLD",
        stage="THE BREAK - one saturated hue tearing through a desaturated world",
        locks=[],
        body=(
            "Fast low aerial shot racing just above a black ocean at night toward a "
            "distant coastline, the camera moving at enormous speed. A single beam of "
            "brilliant ice-blue light screams into frame from behind the camera, "
            "overtakes it, and tears away toward the horizon, throwing hard moving "
            "highlights across the water below and leaving a long trail of colour "
            "hanging in the air behind it. The water churns in its wake."
        ),
        use="Cut between Homing shots to make the ten stars feel like they crossed a world.",
    ),
]

# ---------------------------------------------------------------------------
# THE 36-CUT BEAT GRID
# (start_beat, length_beats, source, slice, technique, description)
# ---------------------------------------------------------------------------

CUTS = [
    # --- COLD OPEN | bars 1-4 | sub-bass only, no drums ---
    (0,  6, "C1", "0.0-2.4", "-",                     "Ten lights streaking past the lens"),
    (6,  4, "C1", "2.4-4.0", "-",                     "Snap focus: the EMPTY tenth ring"),
    (10, 6, "C1", "4.0-6.4", "-",                     "Crash zoom out, Lumi running revealed"),
    # --- THE WORLD | bars 5-8 | beat enters, 4-beat cuts ---
    (16, 4, "C1", "6.4-8.0", "-",                     "Racing alongside him, comet tail of colour"),
    (20, 4, "C1", "8.0-9.0", "ramp 80%",              "Crane reveal, the whole of Veylora"),
    (24, 4, "I4", "2.0-3.6", "optional",              "A star crossing an ocean"),
    (28, 4, "C1", "9.0-10.0", "punch-in 140%",        "He skids to a stop, head comes up"),
    # --- THE BUILD | bars 9-12 | riser, cuts halving ---
    (32, 4, "C2", "0.0-1.6", "-",                     "The ten lights strobe and start dying"),
    (36, 4, "C2", "1.6-3.2", "-",                     "Whip pan, the world smears into the Vault"),
    (40, 2, "C2", "3.2-4.0", "-",                     "Darkness floods the mosaic floor"),
    (42, 2, "C2", "4.0-4.8", "-",                     "Lumi spins"),
    (44, 1, "C2", "4.8-5.2", "FLASH",                 "Violet eyes snap open"),
    (45, 1, "C1", "7.2-7.6", "FLASH, punch-in 200%",  "Lumi's eye, wide"),
    (46, 1, "I3", "3.0-3.4", "FLASH, optional",       "The gem"),
    (47, 1, "C2", "5.6-6.0", "FLASH",                 "The claw rising"),
    # --- THE GAP | bar 13 | EVERYTHING STOPS ---
    (48, 2, "BLACK", "-", "SILENCE",                  "Hard black. Kill every channel. No room tone."),
    (50, 2, "C2", "6.0-6.8", "hold",                  "Only the violet eyes, in black, growing"),
    # --- THE DROP | bars 14-17 | reveal on the downbeat ---
    (52, 4, "C2", "6.8-8.4", "SHAKE on hit",          "NOCTRA SLAMS DOWN. This is the drop."),
    (56, 2, "I2", "6.0-6.8", "optional",              "Hero shot: full height, head turns to lens"),
    (58, 2, "C2", "8.4-9.2", "-",                     "Snap zoom to his face"),
    (60, 1, "C2", "9.2-9.6", "FLASH",                 "The gem detonates"),
    (61, 1, "C3", "0.0-0.4", "-",                     "Shadow sheet tears across the floor"),
    (62, 2, "C3", "0.4-1.2", "-",                     "Lumi leaps through frame, motion blur"),
    (64, 2, "C3", "1.2-2.0", "IMPACT FRAME",          "THE BARRIER IGNITES"),
    (66, 2, "I1", "3.0-3.8", "optional",              "Hero shot: Lumi holding, not moving back"),
    # --- THE BREAK | bars 18-19 ---
    (68, 2, "C3", "2.0-2.8", "SHAKE",                 "Shadow smashes the barrier, pillars explode"),
    (70, 1, "C3", "2.8-3.2", "-",                     "He skids backward"),
    (71, 1, "C3", "3.2-3.6", "-",                     "The claw comes down"),
    (72, 4, "C3", "3.6-5.2", "ramp to 25%",           "SLOW MO: the scarf tears open"),
    (76, 2, "C3", "5.2-6.0", "ramp back to 100%",     "Ten lights blow past the lens"),
    (78, 2, "C3", "6.0-6.8", "-",                     "Camera rockets up through the roof"),
    # --- THE HOMING | bars 21-22 | biggest hit, longest hold ---
    (80, 8, "C3", "6.8-10.0", "hold, ramp 90%",       "THE HOMING. Ten beams across the whole sky."),
    # --- THE FALL | bars 23-24 | beat cuts out entirely ---
    (88, 4, "C4", "1.0-3.0", "no music",              "Daylight. Silence. His eyes open."),
    (92, 3, "C4", "4.0-5.5", "no music",              "Touching empty rings, faster, nothing"),
    (95, 1, "C4", "7.0-7.4", "crash zoom",            "Into the empty ring. To black."),
    # --- TITLE | bar 25 ---
    (96, 4, "C4", "8.0-10.0", "TITLE SLAM",           "Gold point ignites. Logo hits on the downbeat."),
]

NARRATION = [
    (6,  "NARRATOR", "Ten stars."),
    (24, "NARRATOR", "One keeper."),
    (34, "NARRATOR", "They all left him."),
    (88, "NOCTRA",   "Find them."),
    (96, "NOCTRA",   "And when you remember - find me."),
]

MUSIC = [
    ("1-4",   "0:00-0:06.4", "COLD OPEN",
     "Sub-bass drone only. No drums. State the four-note lullaby motif clean and "
     "exposed on a single plucked instrument - koto, shamisen or a muted guitar. "
     "This melody is the hook and it must be recognisable here."),
    ("5-8",   "0:06.4-0:12.8", "THE WORLD",
     "Beat enters. 808 sub on the downbeats, sparse syncopated hi-hats. The "
     "lullaby motif repeats underneath, now with a counter-rhythm. Warm."),
    ("9-12",  "0:12.8-0:19.2", "THE BUILD",
     "Riser. Hi-hats go to triplet rolls and accelerate. Taiko hits enter on "
     "beats 1 and 3, getting louder each bar. The lullaby motif starts detuning "
     "and going minor. Snare roll across bar 12."),
    ("13",    "0:19.2-0:20.8", "THE GAP",
     "TOTAL SILENCE for two beats. Every channel muted, no reverb tail, no room "
     "tone. Then two beats of a single sub-bass swell rising into the drop. This "
     "gap is the most important 0.8 seconds in the track."),
    ("14-17", "0:20.8-0:27.2", "THE DROP",
     "Full drop on the downbeat of bar 14. Distorted 808s, hard-hitting taiko, "
     "aggressive syncopation that refuses to sit square. The lead is the SAME "
     "four-note lullaby motif, now distorted, pitched down and played as a "
     "brutal riff. That is the whole trick - the lullaby is the drop."),
    ("18-20", "0:27.2-0:32.0", "THE BREAK",
     "Drums stutter and gate in half-time. Bass holds. Keep the riff but strip "
     "layers out so the Homing has air to land in."),
    ("21-22", "0:32.0-0:35.2", "THE HOMING",
     "Biggest hit in the track on the downbeat of bar 21, then a long sustained "
     "orchestral swell over the top of the beat while the ten beams cross the "
     "sky. Let it ring."),
    ("23-24", "0:35.2-0:38.4", "THE FALL",
     "Everything cuts out. No drums, no bass, no music at all. Wind and birdsong "
     "only. The silence after that much low end is what sells the loss."),
    ("25",    "0:38.4-0:40.0", "TITLE",
     "The four-note lullaby, played once, clean and complete, on the lone "
     "instrument from bar 1. One low title stinger underneath it on the downbeat."),
]

POST = [
    ("Beat-synced shake", "2-4 frame position shake on every bass hit during the drop "
     "(bars 14-21). Scale it to the hit - biggest on the Noctra slam at bar 14 and "
     "the Homing at bar 21. None at all before the drop or after bar 22."),
    ("Impact frames", "One to two frames of pure white or full-luminance-inverted "
     "frame on the hardest hits: the barrier igniting, the slam, the scarf tearing. "
     "Single frames only - two reads as a mistake."),
    ("RGB split", "2-6px chromatic split, only on the flash cuts in the build "
     "(beats 44-47) and on the drop hit. Ramp it off completely by bar 22. Never "
     "prompt for this - add it in post where you control the frame."),
    ("Speed ramps", "Ramp into the scarf tear down to 25% and back up to 100% over "
     "the following two beats. Ramp the crane reveal in bar 6 to 80%. Everything "
     "else plays at 100%."),
    ("Glow pump", "Bloom on the gold and the star colours, keyed to the kick during "
     "the drop. Subtle - 10-15% swing. It should feel like the light is breathing "
     "with the bass."),
    ("Zoom punches", "5-15% scale punch on single-beat cuts. Alternate direction "
     "between consecutive cuts so it never feels like one continuous move."),
    ("Grade", "Bars 1-8 warm and saturated. Bars 9-13 desaturating hard. Bars 14-21 "
     "violet and black with gold as the only warm accent. Bars 22-25 pale and "
     "almost colourless until the single gold point. Do not grade warmth back "
     "into the tail."),
    ("Title", "FUREVER slams on the downbeat of bar 25, THE LOST STARKEEPER fades "
     "up under it half a bar later. Composite it - never let the generator render "
     "text."),
]


def t(beats):
    s = beats * BEAT
    return f"{int(s) // 60:01d}:{s % 60:04.1f}"


def build_prompt(c, insert=False):
    parts = [REFERENCE]
    if not insert:
        parts.append(CONTINUITY)
    label = (f"{CLIP_SECONDS}-SECOND ANIME SHOT - CLIP {c['n']} OF 4 "
             f"({c['tin']}-{c['tout']})." if not insert
             else f"{CLIP_SECONDS}-SECOND ANIME INSERT SHOT - {c['n']}.")
    parts += [label, STYLE, KINETIC, f"COLOR STAGE: {c['stage']}."]
    parts += [LOCKS[k] for k in c["locks"]]
    parts += [f"SHOT: {c['body']}"]
    if not insert:
        if c["vo"]:
            parts.append("BACKGROUND NARRATION (off-screen voice-over, spoken over "
                         f"this clip): \"{c['vo']}\"")
        else:
            parts.append("BACKGROUND NARRATION: none - this clip carries no voice-over. "
                         "It plays on music alone.")
        parts.append(VOICE_DIRECTION)
    parts.append(NO_LIPSYNC)
    parts.append(
        "TIMING: one single continuous take at high energy, no cuts inside the shot. "
        "The final frame must be a clean, stable hold that the next clip can continue "
        "directly from.")
    parts.append(f"{NEGATIVE} {NO_POST}, {OFF_MODEL_NEG}, slow motion throughout, "
                 "static camera, contemplative pacing, empty frames, nothing happening.")
    return " ".join(" ".join(p.split()) for p in parts)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "out")
    os.makedirs(out, exist_ok=True)

    with open(os.path.join(out, "teaser40_prompts.txt"), "w") as f:
        for c in CLIPS:
            f.write(build_prompt(c) + "\n")

    with open(os.path.join(out, "teaser40_inserts.txt"), "w") as f:
        for c in INSERTS:
            f.write(build_prompt(c, insert=True) + "\n")

    # --- ONE merged file with everything in it, so nothing needs opening twice
    rule = "#" * 78
    attach = {1: "Lumi + scarf", 2: "Lumi + Noctra", 3: "Lumi + Noctra", 4: "Lumi + scarf"}
    with open(os.path.join(out, "ALL_PROMPTS.txt"), "w") as f:
        f.write(rule + "\n")
        f.write("#  FUREVER - 40 SECOND ANIME TEASER - ALL PROMPTS\n")
        f.write(f"#  {BPM} BPM | 4 core clips + {len(INSERTS)} optional inserts | "
                "10s each\n")
        f.write(rule + "\n")
        f.write("""
EACH PROMPT IS ONE SINGLE LINE. Triple-click it to select the whole thing.

HOW TO RUN IT
  1. Attach the character references on EVERY generation, not just the first.
     A reference from three prompts ago is not in context any more.
  2. Generate the 4 core clips in order: 1, 2, 3, 4.
  3. Feed the LAST FRAME of each clip in as the FIRST FRAME of the next.
     Text continuity alone will not hold four clips together.
  4. The 4 inserts are standalone - no chaining, generate them any time.
  5. Render 3-4 takes of everything. A drifted take does not recover, so
     regenerate rather than trying to correct it.
  6. Cut on the beat grid in teaser40_edit.md. Add shake, RGB split, impact
     frames and the title in the EDIT - never in the prompt.

IF IT GOES OFF-MODEL
  Attach fewer references per generation. One character beats three at once,
  which is why clips 2 and 3 drift most - they carry both cats.

""")
        f.write(rule + "\n#  CORE CLIPS - generate these four, in this order\n" + rule + "\n\n")
        for c in CLIPS:
            f.write(rule + "\n")
            f.write(f"#  CLIP {c['n']} OF 4   |   {c['tin']}-{c['tout']}   |   {c['title']}\n")
            f.write(f"#  ATTACH: {attach[c['n']]} reference\n")
            vo = c["vo"] if c["vo"] else "(none - this clip plays on music alone)"
            f.write(f"#  NARRATION: {vo}\n")
            f.write(f"#  NOTE: {' '.join(c['note'].split())}\n")
            f.write(rule + "\n\n")
            f.write(build_prompt(c) + "\n\n\n")

        f.write(rule + "\n#  OPTIONAL HERO INSERTS - the drop wants these\n")
        f.write("#  Four clips can carry the teaser. Eight makes it look like the\n")
        f.write("#  reference edits. No chaining - generate these standalone.\n")
        f.write(rule + "\n\n")
        for c in INSERTS:
            f.write(rule + "\n")
            f.write(f"#  INSERT {c['n']}   |   {c['title']}\n")
            f.write(f"#  FOR: {c['use']}\n")
            f.write(rule + "\n\n")
            f.write(build_prompt(c, insert=True) + "\n\n\n")

        f.write(rule + "\n#  NARRATION - record separately, 17 words total\n" + rule + "\n\n")
        f.write(VOICE_DIRECTION + "\n\n")
        f.write("No narration at all across the drop (0:20.8-0:34.4). Music only.\n\n")
        for beat, who, line in NARRATION:
            f.write(f"  {t(beat)}   {who:<9}  \"{line}\"\n")
        f.write("\n")

    with open(os.path.join(out, "teaser40_narration.txt"), "w") as f:
        f.write("FUREVER - 40s TEASER - NARRATION\n" + "=" * 70 + "\n\n")
        f.write(VOICE_DIRECTION + "\n\n")
        f.write("Fourteen words in forty seconds. The music carries this, not the\n")
        f.write("voice. Every line is a stab that lands in a gap, never a sentence\n")
        f.write("that flows over a section. There is NO narration at all across the\n")
        f.write("drop (0:20.8-0:34.4) - that passage is music and picture only.\n\n")
        f.write("THE TRICK: the narrator is Noctra. He talks about Lumi in the third\n")
        f.write("person, and then at 0:35.2 the same voice speaks TO him. Same read -\n")
        f.write("do not perform the reveal.\n\n" + "=" * 70 + "\n\n")
        for beat, who, line in NARRATION:
            f.write(f"{t(beat)}  (beat {beat})  {who}\n    \"{line}\"\n\n")

    with open(os.path.join(out, "teaser40_edit.md"), "w") as f:
        f.write("# FUREVER - 40s TEASER - BEAT-SYNCED EDIT\n\n")
        f.write(f"**{BPM} BPM | 1 beat = {BEAT}s | 1 bar = {BAR}s | "
                f"40s = 100 beats = 25 bars**\n\n")
        f.write(f"{len(CUTS)} cuts, every one on a beat. Four core clips shredded, "
                "plus four optional hero inserts.\n\n")

        f.write("## Structure\n\n")
        f.write("The shape every good anime edit uses: **build, total silence, "
                "then the reveal lands on the drop.**\n\n")
        f.write("| Bars | Time | Section | Cutting |\n|---|---|---|---|\n")
        f.write("| 1-4 | 0:00-0:06.4 | Cold open | 3 cuts, long. Sub-bass only. |\n")
        f.write("| 5-8 | 0:06.4-0:12.8 | The world | 4 cuts, one per bar. Beat enters. |\n")
        f.write("| 9-12 | 0:12.8-0:19.2 | The build | 8 cuts, halving. Riser. |\n")
        f.write("| **13** | **0:19.2-0:20.8** | **THE GAP** | **Black. Total silence.** |\n")
        f.write("| 14-17 | 0:20.8-0:27.2 | **THE DROP** | 8 cuts. Noctra reveal on the downbeat. |\n")
        f.write("| 18-20 | 0:27.2-0:32.0 | The break | 6 cuts. The scarf tears. |\n")
        f.write("| 21-22 | 0:32.0-0:35.2 | The Homing | 1 cut, held long. Biggest hit. |\n")
        f.write("| 23-24 | 0:35.2-0:38.4 | The fall | 3 cuts. Music stops dead. |\n")
        f.write("| 25 | 0:38.4-0:40.0 | Title | Logo slams on the downbeat. |\n")

        f.write("\n## Cut list\n\n")
        f.write("| # | Beat | In | Out | Len | Src | Slice | Technique | Frame |\n")
        f.write("|---|---|---|---|---|---|---|---|---|\n")
        for i, (b, ln, src, sl, tech, desc) in enumerate(CUTS, 1):
            f.write(f"| {i} | {b} | {t(b)} | {t(b + ln)} | {ln}b | `{src}` | {sl} | "
                    f"{tech} | {desc} |\n")

        f.write("\n## Music brief\n\n")
        f.write("Reference feel: the syncopated, off-kilter, bass-heavy energy of "
                "current anime openings and edits - *Otonoke* (Dandadan), and the "
                "phonk/trap edits built around Gojo and Gear 5 reveals. Commission "
                "or license original; the point is the **structure**, not the track.\n\n")
        f.write("**The single best idea in this brief:** the four-note lullaby Noctra "
                "wrote for Lumi is stated clean and gentle in bar 1, and the drop is "
                "the *same four notes* distorted, pitched down and played as a riff. "
                "The hype and the story are the same melody.\n\n")
        f.write("| Bars | Time | Section | Arrangement |\n|---|---|---|---|\n")
        for bars, time, sect, arr in MUSIC:
            f.write(f"| {bars} | {time} | **{sect}** | {arr} |\n")

        f.write("\n## Narration\n\n")
        f.write("Fourteen words. No VO at all across the drop.\n\n")
        f.write("| Beat | Time | Speaker | Line |\n|---|---|---|---|\n")
        for beat, who, line in NARRATION:
            f.write(f"| {beat} | {t(beat)} | {who} | \"{line}\" |\n")

        f.write("\n## Post recipe\n\n")
        f.write("**None of this goes in the prompt.** Generators bake these in badly "
                "and you lose all control over which frame they land on. Every one "
                "is an edit-stage effect.\n\n")
        f.write("| Effect | How |\n|---|---|\n")
        for name, how in POST:
            f.write(f"| **{name}** | {how} |\n")

        f.write("\n## Source clips\n\n")
        f.write("### Core - generate these four\n\n")
        f.write("| Clip | Time | Title | Note |\n|---|---|---|---|\n")
        for c in CLIPS:
            f.write(f"| `C{c['n']}` | {c['tin']}-{c['tout']} | {c['title']} | "
                    f"{c['note']} |\n")
        f.write("\n### Optional inserts - four more\n\n")
        f.write("Four clips can carry this. Eight makes it look like the reference "
                "edits, because the drop needs hero shots it does not have to share "
                "with a continuous take.\n\n")
        f.write("| Clip | Title | What it's for |\n|---|---|---|\n")
        for c in INSERTS:
            f.write(f"| `{c['n']}` | {c['title']} | {c['use']} |\n")

    total = sum(ln for _, ln, *_ in CUTS)
    print(f"bpm:        {BPM}  (beat {BEAT}s, bar {BAR}s)")
    print(f"cuts:       {len(CUTS)}  spanning {total} beats = {total * BEAT:.1f}s")
    print(f"core clips: {len(CLIPS)}   optional inserts: {len(INSERTS)}")
    print(f"vo words:   {sum(len(l.split()) for _, _, l in NARRATION)}")
    print(f"merged:     {os.path.join(out, 'ALL_PROMPTS.txt')}")
    print(f"written to: {out}")


if __name__ == "__main__":
    main()
