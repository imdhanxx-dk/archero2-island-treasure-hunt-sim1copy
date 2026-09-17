#!/usr/bin/env python3
"""
FurEver - 40-SECOND CINEMATIC ANIME TEASER.

Four chained 10-second clips = exactly 0:40. Each clip is written to continue
seamlessly from the end of the previous one, so they can be generated in
sequence and laid end to end with no cutting.

Assumes character reference stills already exist - feed the Lumi / Noctra /
scarf references in as image conditioning, and feed the last frame of each
clip in as the first frame of the next.

    python3 build_teaser_40.py

Outputs into ./out/ :
    teaser40_prompts.txt     the 4 prompts, one per line, paste-ready
    teaser40_prompts.md      the same 4, readable, with notes
    teaser40_narration.txt   VO only, timecoded, for the voice session
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_prompts import STYLE, NEGATIVE, LOCKS  # noqa: E402

CLIP_SECONDS = 10

# --- blocks that appear verbatim in every single prompt --------------------

CONTINUITY = (
    "Continue the video seamlessly from the last scene of the previous clip. "
    "Keep the same characters, appearance, clothing, environment, camera style, "
    "lighting, and overall visual consistency. The new scene must naturally begin "
    "exactly where the previous scene cut ended."
)

VOICE_DIRECTION = (
    "Voice: low, unhurried, warm, close-mic'd. Not a trailer boom. "
    "He is remembering, not announcing. (It is Noctra. Do not play it that way yet.)"
)

NO_LIPSYNC = (
    "NO LIP SYNC: the narration is off-screen voice-over only. No character in "
    "frame is speaking. Every character's mouth stays closed and still throughout "
    "the entire shot. Do not animate mouths, jaws, muzzles or whiskers to match "
    "the narration. Do not sync any facial movement to the audio. The voice does "
    "not belong to anyone visible in the frame."
)

NO_LIPSYNC_NEG = (
    "lip sync, lip-syncing, talking, speaking, mouth moving, mouth opening, jaw "
    "movement, muzzle animation, teeth showing, dialogue animation, singing, "
    "mouth flaps, character addressing camera"
)

# ---------------------------------------------------------------------------
# THE FOUR CLIPS
# ---------------------------------------------------------------------------

CLIPS = [
    dict(
        n=1, tin="0:00", tout="0:10",
        title="THE FULL SKY",
        stage="THE FULL SKY - every one of the ten hues present, warm gold and deep teal, abundance",
        locks=["lumi", "scarf"],
        vo=("Ten stars. And one small cat, who carried every single one of them "
            "- for exactly as long as they wished to stay."),
        body=(
            "Open in extreme macro on the black scarf fabric filling the frame, so dark "
            "that light falls into it rather than off it. The camera drifts slowly along "
            "its length past silver fastenings, each holding a small living star that "
            "turns in place and washes the lens with its own colour - green-gold, then "
            "silver, then ice blue, then ember red. At around four seconds the camera "
            "begins pulling back continuously and the frame widens to reveal that the "
            "scarf is being worn: LUMI is walking an old stone path through waist-high "
            "evening grass at golden hour, small and unhurried, tail up, all ten "
            "coloured lights breathing along the scarf and throwing colour across his "
            "white fur and the grass on both sides. The pull-back keeps going and the "
            "landscape of Veylora opens out enormously behind him - forest, a distant "
            "glass coastline, far mountains under an immense dusk sky - until he is very "
            "small in the middle of all of it. Fireflies lift around him. He walks on."
        ),
        note=("The only warm, safe, wide shot in the teaser. Everything after this is "
              "taking it away. End frame: Lumi small in a huge landscape, ten lights lit."),
        sfx=("Near silence, then a faint ten-voice choral hum that resolves into a warm "
             "chord as the frame widens. Grass. Footpads. Distant bells."),
    ),
    dict(
        n=2, tin="0:10", tout="0:20",
        title="THE BREAK",
        stage="THE BREAK - colour draining out of the frame, violet and near-black taking over",
        locks=["lumi", "noctra"],
        vo=("Then something came up out of the dark that the world had spent four "
            "hundred years agreeing had never existed."),
        body=(
            "Continue on LUMI in the landscape. The ten coloured lights along his scarf "
            "begin to stutter and swing out of rhythm, throwing wild coloured shadows "
            "across the grass, and the warm golden light drains out of the whole "
            "environment as the shot transitions into the vast underground Star Vault "
            "around him - black stone pillars, gold mosaic floor, a domed ceiling carved "
            "with constellations. He stops and lifts a paw toward the scarf. The flicker "
            "accelerates hard. Then every light dies at once, in a single frame, and the "
            "shot drops to near-total blackness with only a cold rim of light on the edge "
            "of his white fur. Hold on the black. Then, deep behind him, two pale violet "
            "eyes open far higher than they should be, and NOCTRA walks forward out from "
            "between two pillars in one slow unbroken move, his fur absorbing the light "
            "so completely that he reads as a hole cut in the image, violet fracture-lines "
            "crawling across him, black smoke peeling off his outline. He fills the frame "
            "and lowers his enormous head toward the camera, and the cracked violet gem "
            "in his chest pulses once, hard, throwing violet light up across his jaw."
        ),
        note=("Do not rush the blackout. The beat of pure black before the eyes open is "
              "the most important moment in the teaser. End frame: Noctra huge and close, "
              "gem lit."),
        sfx=("The warm chord detunes and goes sour. Sub-bass rises. Total silence on the "
             "blackout - cut everything, no room tone. Then one enormous breath, stone "
             "grinding, and the gem pulse landing like a struck anvil."),
    ),
    dict(
        n=3, tin="0:20", tout="0:30",
        title="THE HOMING",
        stage="THE BREAK into total desaturation - this clip spends the last colour in the teaser",
        locks=["lumi", "noctra"],
        vo=("They did not leave because they were afraid of him. They left because "
            "they were tired of being carried."),
        body=(
            "Continue from NOCTRA close in the dark. A claw of pure darkness sweeps down "
            "across the frame and strikes the dark indigo scarf across LUMI's chest. In "
            "extreme slow motion the fabric tears open and all ten silver fastenings "
            "burst apart in sequence, and the ten coloured lights blow outward and upward "
            "past the lens in long trailing streaks of green, silver, blue, red, white, "
            "turquoise and pale aurora, leaving the torn scarf whipping empty in the "
            "shockwave. The camera follows the lights upward in one continuous move, "
            "tearing up through the collapsing roof of the ruin and out into the open "
            "night sky above the mountainside, where the shot settles wide, static and "
            "low. The ten beams climb together, then each bends away at its own angle and "
            "streaks off over a different horizon - over ocean, over forest, over "
            "mountain, over desert - drawing ten long trails of colour right across the "
            "entire sky. The trails thin, fade, and go out one by one until the sky is "
            "completely empty and black."
        ),
        note=("The money shot. Generate this one the most times. Let the last trail fully "
              "fade - do not cut while colour is still on screen. End frame: empty black "
              "night sky."),
        sfx=("No music through the tear. Impact, stone, and a long glassy rip. Ten "
             "distinct notes leaving, high to low. Then a single held orchestral swell "
             "over the Homing that resolves into nothing but wind."),
    ),
    dict(
        n=4, tin="0:30", tout="0:40",
        title="THE EMPTY SKY",
        stage="THE EMPTY SKY - pale desaturated daylight, no saturated colour anywhere until one gold point at the very end",
        locks=["lumi", "scarf"],
        vo=("NOCTRA (V.O.): \"Find them. And when you remember - find me.\""),
        body=(
            "Continue from the empty night sky as it lightens into pale washed-out dawn "
            "and the camera descends to ground level in tall sunlit meadow grass, lens "
            "almost touching the soil, shallow focus, insects drifting through weak bars "
            "of light. LUMI's eyes open in the foreground, unfocused, blinking hard "
            "against the brightness. The camera rises gently with him as he sits up, "
            "disoriented, turning his head across a landscape he plainly does not "
            "recognise. He looks down at the torn indigo scarf. He touches one empty "
            "silver fastening with a paw. Nothing happens. He touches the next one. "
            "Nothing happens. His ears flatten back against his skull and he goes very "
            "still. The camera pushes in on the empty fastening until the frame falls "
            "entirely to black - then one small point of warm gold light ignites at the "
            "exact centre and blooms slowly outward, faintly revealing the weave of the "
            "black fabric and the ghosts of ten empty silver rings arranged around it in "
            "a constellation. The gold point pulses once, gently, and holds."
        ),
        note=("The tonal whiplash from the Homing into quiet daylight is the whole trick. "
              "Keep it pale - do not grade warmth back in. Final three seconds are a clean "
              "title plate: composite FUREVER, then THE LOST STARKEEPER, over the gold "
              "pulse in the edit. Never let the generator render text."),
        sfx=("Wind in grass. Birdsong. Unbearably peaceful, no music at all. Then silence, "
             "and the four-note lullaby played once, complete, on a solo instrument, over "
             "the gold point. Title sting."),
    ),
]


def build_prompt(c):
    parts = [
        CONTINUITY,
        f"{CLIP_SECONDS}-SECOND ANIME SHOT - CLIP {c['n']} OF 4 ({c['tin']}-{c['tout']}).",
        STYLE,
        f"COLOR STAGE: {c['stage']}.",
    ]
    parts += [LOCKS[k] for k in c["locks"]]
    parts += [
        f"SHOT: {c['body']}",
        (f"BACKGROUND NARRATION (off-screen voice-over, spoken over this clip): "
         f"\"{c['vo']}\""),
        VOICE_DIRECTION,
        NO_LIPSYNC,
        ("TIMING: one single continuous take, one camera move, one change of state; "
         "0-3s the frame settles with one element already in motion, 3-7s the move "
         "commits, 7-10s the state changes and the shot lands. No cuts inside the shot. "
         "The final frame must be a clean, stable hold that the next clip can continue "
         "directly from."),
        f"{NEGATIVE} {NO_LIPSYNC_NEG}.",
    ]
    return " ".join(" ".join(p.split()) for p in parts)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "out")
    os.makedirs(out, exist_ok=True)

    with open(os.path.join(out, "teaser40_prompts.txt"), "w") as f:
        for c in CLIPS:
            f.write(build_prompt(c) + "\n")

    with open(os.path.join(out, "teaser40_prompts.md"), "w") as f:
        f.write("# FUREVER - 40 SECOND TEASER\n\n")
        f.write("**4 chained clips x 10s = 0:40 exactly.** Generate in order, feed the\n")
        f.write("last frame of each clip in as the first frame of the next, lay them\n")
        f.write("end to end. No cutting required.\n\n")
        f.write("Every prompt carries the continuity prefix, its own narration line,\n")
        f.write("the voice direction, and an explicit no-lip-sync lock.\n\n")
        f.write("| Clip | Time | Title | Narration |\n|---|---|---|---|\n")
        for c in CLIPS:
            f.write(f"| {c['n']} | {c['tin']}-{c['tout']} | {c['title']} | "
                    f"{c['vo']} |\n")
        f.write("\n---\n\n")
        for c in CLIPS:
            f.write(f"## CLIP {c['n']} - {c['tin']}-{c['tout']} - {c['title']}\n\n")
            f.write(f"**Note:** {c['note']}\n\n")
            f.write(f"**Sound:** {c['sfx']}\n\n")
            f.write("```\n")
            f.write(build_prompt(c))
            f.write("\n```\n\n")

    with open(os.path.join(out, "teaser40_narration.txt"), "w") as f:
        f.write("FUREVER - 40 SECOND TEASER - NARRATION\n")
        f.write("=" * 68 + "\n\n")
        f.write(VOICE_DIRECTION.replace(". He is remembering", ".\n\nHe is remembering"))
        f.write("\n\n")
        f.write("THE TRICK: the narrator is Noctra. Nothing signposts it. He talks about\n")
        f.write("Lumi in the third person for thirty seconds, and then in clip 4 he speaks\n")
        f.write("TO him. Same voice, same read. The shift from description to imperative\n")
        f.write("does all the work by itself - do not perform the reveal.\n\n")
        f.write("Characters never lip-sync to this. It is off-screen voice-over only.\n")
        f.write("=" * 68 + "\n\n")
        for c in CLIPS:
            f.write(f"{c['tin']} - {c['tout']}   CLIP {c['n']} - {c['title']}\n")
            f.write(f"    \"{c['vo']}\"\n\n")

    words = sum(len(c["vo"].split()) for c in CLIPS)
    print(f"clips:      {len(CLIPS)} x {CLIP_SECONDS}s = "
          f"{len(CLIPS) * CLIP_SECONDS}s")
    print(f"vo words:   {words}")
    print(f"written to: {out}")


if __name__ == "__main__":
    main()
