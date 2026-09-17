#!/usr/bin/env python3
"""
FurEver - 40s ANIME TEASER, BUILT FOR GOOGLE FLOW (Veo).

Flow is not a generic image generator and the generic prompts fail on it.
This rewrites the teaser for how Veo actually behaves:

  * 8-SECOND CLIPS, not 10. Five clips x 8s = 40s exactly.
  * SEPARATE NEGATIVE FIELD. Veo has one. Instructive negatives written inside
    the prompt body ("no text", "no extra limbs") can summon the thing instead
    of suppressing it. The negative list is emitted separately to paste in.
  * ONE CAMERA MOVE PER CLIP. Compound moves (crash zoom into whip pan into
    crane) are why subjects end up off-screen - Veo cannot track through them.
  * EXPLICIT FRAMING. Veo needs to be told the subject stays in frame.
  * STRUCTURED SECTIONS. Subject / Action / Scene / Camera / Composition /
    Lighting / Style / Audio, in that order.
  * NATIVE AUDIO. Veo 3 generates sound from the prompt, so the music is
    described in the prompt - it drives the energy of the motion.
  * SHORTER. ~1,200 characters, not 3,000. Long prompts dilute on Veo.

    python3 build_flow_teaser.py

Outputs into ./out/ :
    FLOW_PROMPTS.txt    all 5 prompts + the negative field + the workflow
"""

import os

CLIP_SECONDS = 8
BPM = 150

# Paste this into Flow's NEGATIVE PROMPT field - never into the prompt body.
# Nouns and styles only. No "no", no "don't", no instructions.
NEGATIVE_FIELD = (
    "blurry, low quality, low resolution, 3D render, CGI, Pixar style, "
    "photorealistic, live action, plastic texture, western cartoon, chibi, "
    "deformed anatomy, extra limbs, extra tails, malformed paws, melting face, "
    "morphing features, warped eyes, mismatched eye colour, human face on an "
    "animal, text, letters, captions, subtitles, watermark, signature, logo, "
    "user interface, progress bar, letterbox bars, moving mouth, open mouth, "
    "talking animal, lip sync, speaking character, singing, subject out of "
    "frame, cropped subject, subject leaving frame, empty frame, static shot, "
    "slow motion throughout, chromatic aberration, glitch effect, VHS artifacts, "
    "light leak overlay, duplicated character, crowd of cats"
)

STYLE = (
    "2D cel-shaded Japanese anime, theatrical feature film quality, hand-drawn "
    "key animation, crisp ink linework with varied line weight, flat cel shading "
    "with hard shadow edges, hand-painted background art, saturated cinematic "
    "colour, subtle film grain, 24fps, widescreen 2.39:1"
)

# Describing the track in-prompt drives the ENERGY of the motion Veo generates.
# The generated audio itself is discarded in the edit - see the workflow notes.
MUSIC = {
    "build_low": (
        f"Fast, aggressive Japanese hip-hop instrumental at {BPM} BPM. Deep 808 "
        "sub-bass on the downbeats, sparse syncopated trap hi-hats, a plucked koto "
        "riff. Driving and forward-leaning, never calm or ambient."),
    "build_high": (
        f"Fast, aggressive Japanese hip-hop instrumental at {BPM} BPM, building "
        "hard. Triplet hi-hat rolls accelerating, taiko drum hits getting louder "
        "every bar, a rising synth riser, a snare roll. Relentless and tightening."),
    "drop": (
        f"{BPM} BPM. Distorted 808 bass, heavy taiko drums, "
        "aggressive off-kilter syncopation, a distorted pitched-down koto riff as "
        "the lead. Maximum energy, the loudest point of the whole track."),
    "drop_peak": (
        f"The beat at full intensity, {BPM} BPM, distorted 808 bass and heavy "
        "taiko, with a huge sustained orchestral swell rising over the top of it."),
    "cut_out": (
        "The music stops completely and instantly. No drums, no bass, no "
        "instruments. Only soft wind moving through grass and distant birdsong."),
}

# Veo attributes quoted dialogue to a visible character and lip-syncs it.
# Framing it as an unseen narrator, plus stating mouths stay shut, is the fix.
def vo(line):
    return (
        f"A deep male narrator speaks in voice-over: \"{line}\" The narrator is "
        "not a character in the scene and is never shown. His voice is recorded "
        "separately and laid over the picture. Every animal on screen keeps its "
        "mouth completely closed and still for the entire shot. Nothing visible "
        "in the frame is speaking, and no mouth, jaw or muzzle moves at any "
        "point. The voice is deep, gravelled, slow and heavy, with chest "
        "resonance and a stone-room reverb tail.")


NO_VO = (
    "There is no narration and no dialogue anywhere in this clip. It plays on "
    "music and sound effects alone. Every animal on screen keeps its mouth "
    "completely closed and still for the entire shot. Nothing visible in the "
    "frame is speaking, and no mouth, jaw or muzzle moves at any point.")

LUMI = (
    "A small white cat named Lumi, ordinary cat proportions on four legs, fluffy "
    "white fur with a cream tint at the ears and tail tip, large round pale gold "
    "eyes, thin delicate gold markings tracing his forelegs and across his brow. "
    "He wears a long dark indigo scarf with ten small circular silver rings "
    "stitched along its length")

NOCTRA = (
    "An enormous black cat named Noctra, four times the size of an ordinary cat, "
    "fur so deeply black it absorbs the light around it, pale glowing violet eyes "
    "with slit pupils, thin violet cracks running across his body like lightning "
    "under stone, black smoke drifting off his outline, a large cracked violet "
    "gem set in his chest")

CLIPS = [
    dict(
        n=1, tin="0:00", tout="0:08", title="THE WORLD",
        ingredients="Lumi + scarf",
        subject=f"{LUMI}, and each of the ten silver rings holds a tiny glowing "
                "star in a different colour - green, silver, blue, red, white, "
                "turquoise, pale green, gold, violet and iridescent.",
        action="He runs at full speed along a high grassy ridge, the ten coloured "
               "lights streaming behind him in a trail. Near the end of the shot "
               "he slows and stops at the ridge edge, and his head lifts.",
        scene="A vast fantasy landscape at golden hour. Tall meadow grass moving "
              "in wind, a distant forest, a blue coastline far below, and "
              "mountains on the horizon under an enormous sunset sky.",
        camera="One single smooth tracking shot travelling alongside him at "
               "ground level, drifting slowly backward and upward as it goes. "
               "One continuous move only.",
        comp="Wide shot. The white cat is centred in the frame and fully visible "
             "from nose to tail for the entire eight seconds. He stays in the "
             "lower middle of the frame as the landscape opens out behind him. "
             "The camera keeps him centred and never loses him.",
        light="Warm golden hour backlight, long shadows across the grass, visible "
              "god-rays, glowing pollen drifting through the air.",
        audio=MUSIC["build_low"] + " " + vo("Ten stars. One keeper."),
        note="The only warm clip. Its last frame seeds clip 2.",
    ),
    dict(
        n=2, tin="0:08", tout="0:16", title="THE LIGHTS DIE",
        ingredients="Lumi + scarf",
        subject=f"{LUMI}. The ten stars in the rings are flickering and failing.",
        action="The ten coloured lights in his scarf flicker hard and go out one "
               "after another. The warm light drains out of the landscape around "
               "him and the setting becomes a vast dark underground stone hall. "
               "He turns quickly on the spot, alarmed, as darkness spreads across "
               "the floor toward him.",
        scene="An enormous ancient underground vault with tall black stone "
              "pillars, a gold mosaic floor, and a domed ceiling carved with "
              "constellations. Darkness spreads across the gold floor like "
              "spilled ink.",
        camera="One single slow push-in toward the cat. One continuous move only.",
        comp="Medium shot. The white cat is centred in the frame and fully "
             "visible for the entire eight seconds. He remains in the middle of "
             "the frame as the darkness closes in around the edges. The camera "
             "keeps him centred and never loses him.",
        light="Warm light draining away to near-total darkness. By the end the "
              "only light is the last dying colour of the scarf rings and a cold "
              "rim highlight on his white fur.",
        audio=MUSIC["build_high"] + " " + vo("They all left him.") +
              " In the final second the music stops dead and there is complete "
              "silence.",
        note="Ends on near-black and silence. That gap is what makes clip 3 hit.",
    ),
    dict(
        n=3, tin="0:16", tout="0:24", title="NOCTRA - THE DROP",
        ingredients="Noctra only (do NOT add Lumi - two characters is where it drifts)",
        subject=f"{NOCTRA}.",
        action="Two glowing violet eyes open in total darkness. The enormous black "
               "cat walks slowly forward out of the black toward the camera, "
               "smoke pouring off him. He stops and lowers his head toward the "
               "lens, and the cracked violet gem in his chest flares brightly.",
        scene="The pitch-black interior of the underground vault. Almost nothing "
              "is visible except him. Faint dust hangs in the air.",
        camera="One single slow steady push-in toward him. One continuous move "
               "only.",
        comp="Medium shot rising to a tight medium close-up. The enormous black "
             "cat is centred in the frame for the entire eight seconds, with his "
             "head, shoulders and the glowing gem in his chest all visible inside "
             "the frame. He fills the middle of the frame and never moves out of "
             "it. The camera keeps him centred and never loses him.",
        light="Near-total darkness. He is lit only by the violet glow of his own "
              "eyes, the violet cracks across his body, and the gem in his chest.",
        audio="The clip opens with two seconds of complete silence and no sound "
              "at all, then the beat drops hard. " + MUSIC["drop"] + " " + NO_VO,
        note="THE reveal. This is the shot the whole teaser is built around. "
             "Generate it the most times.",
    ),
    dict(
        n=4, tin="0:24", tout="0:32", title="THE HOMING",
        ingredients="Lumi + Noctra",
        subject=f"{LUMI}. Also present: {NOCTRA}.",
        action="A sweeping wave of darkness rushes across the floor. The small "
               "white cat leaps aside and the gold markings on his forelegs blaze "
               "alight, throwing up a curved golden shield of light in front of "
               "him. A claw of darkness strikes the shield and tears across his "
               "scarf. The ten silver rings burst apart and ten coloured lights "
               "explode upward out of the scarf, flying up and out of the "
               "collapsing roof into the night sky above, where they separate and "
               "streak away in ten different directions across the stars.",
        scene="The vault floor breaking apart, gold mosaic fragments flying, "
              "pillars cracking. Then open night sky above a dark mountainside.",
        camera="One single continuous move that follows the ten lights upward "
               "from the floor into the open sky and then holds steady on the "
               "sky. One continuous move only.",
        comp="The white cat is centred and fully visible in the lower middle of "
             "the frame for the first half. Then the ten beams of light are "
             "centred in the frame for the second half. Something is always "
             "clearly framed in the centre and the camera never loses its "
             "subject.",
        light="Violent gold and violet light in the dark, hard rim lighting, "
              "coloured light streaking past the lens, then a wide clear night "
              "sky with ten glowing trails drawn across it.",
        audio=MUSIC["drop_peak"] + " The biggest impact in the track lands at the "
              "moment the ten lights burst out of the scarf. " + NO_VO,
        note="Busiest clip. If it drifts, generate the fight and the sky as two "
             "separate 8s clips and cut them together.",
    ),
    dict(
        n=5, tin="0:32", tout="0:40", title="THE FALL + TITLE",
        ingredients="Lumi + scarf",
        subject=f"{LUMI}, except now his scarf is torn and all ten silver rings "
                "are completely empty and dark.",
        action="His eyes open. He pushes himself up quickly, disoriented, looking "
               "around at a landscape he does not recognise. He looks down and "
               "touches one empty silver ring on the torn scarf with a paw. "
               "Nothing happens. He touches the next one. Nothing happens. He "
               "stops and his ears flatten back. The frame darkens to black, and "
               "one small point of warm gold light appears in the centre and "
               "glows softly.",
        scene="A pale, washed-out dawn meadow. Tall grass, weak morning light, "
              "insects drifting. Everything is desaturated and quiet.",
        camera="One single slow rise from ground level as he sits up, settling "
               "into a close shot. One continuous move only.",
        comp="Low shot rising to a close-up. The white cat is centred in the "
             "frame and fully visible for the entire eight seconds. His face and "
             "the torn scarf are both clearly in frame. The camera keeps him "
             "centred and never loses him. The final two seconds are pure black "
             "with a single small gold light dead centre.",
        light="Pale, flat, desaturated morning light with no warmth in it. Then "
              "total darkness with one warm gold point.",
        audio=MUSIC["cut_out"] + " " +
              vo("Find them. And when you remember - find me.") +
              " At the very end, one low musical sting.",
        note="The silence after the drop is what sells it. Keep the grade pale. "
             "Composite the FUREVER logo over the last 2s in the edit.",
    ),
]


def build(c):
    return "\n".join([
        f"SUBJECT: {c['subject']}",
        f"ACTION: {c['action']}",
        f"SCENE: {c['scene']}",
        f"CAMERA: {c['camera']}",
        f"COMPOSITION: {c['comp']}",
        f"LIGHTING: {c['light']}",
        f"STYLE: {STYLE}.",
        f"AUDIO: {c['audio']}",
    ])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "out")
    os.makedirs(out, exist_ok=True)
    rule = "#" * 78

    with open(os.path.join(out, "FLOW_PROMPTS.txt"), "w") as f:
        f.write(rule + "\n")
        f.write("#  FUREVER - 40 SECOND ANIME TEASER - GOOGLE FLOW (VEO) BUILD\n")
        f.write(f"#  5 clips x {CLIP_SECONDS}s = 40s  |  music {BPM} BPM\n")
        f.write(rule + "\n")
        f.write("""
WHY THE EARLIER PROMPTS FAILED ON FLOW, AND WHAT CHANGED

  1. Veo generates 8-SECOND clips, not 10. Restructured to 5 x 8s.

  2. Veo has a SEPARATE NEGATIVE PROMPT FIELD. The old prompts had a huge
     negative list buried in the prompt body, which on Veo can summon the very
     things it lists. The negative is now a separate block, below - paste it
     into Flow's negative field, never into the prompt.

  3. YOUR CHARACTERS WENT OFF-SCREEN because the old prompts stacked crash
     zooms into whip pans into crane moves. Veo cannot track a subject through
     a compound move. Every clip now has ONE camera move and an explicit
     COMPOSITION line stating the subject stays centred and fully in frame.

  4. Prompts are ~1,200 characters instead of ~3,000. Long prompts dilute on
     Veo and the later instructions get dropped.

  5. Structured into the order Veo reads best:
     SUBJECT / ACTION / SCENE / CAMERA / COMPOSITION / LIGHTING / STYLE / AUDIO.

HOW TO RUN IT IN FLOW

  * Use INGREDIENTS TO VIDEO. Add each character as an Ingredient - that is
    Flow's character-consistency feature and it works far better than
    describing the character in text.
  * Add ONLY the ingredients listed for that clip. Clip 3 is Noctra alone on
    purpose. Two characters in one generation is where Veo drifts worst.
  * Use FRAMES TO VIDEO to chain: take the last frame of each clip and set it
    as the starting frame of the next.
  * Generate 3-4 takes of every clip. Clip 3 is the reveal and clip 4 is the
    busiest - spend your takes there.
  * If clip 4 keeps breaking, split it: generate the fight as one 8s clip and
    the ten lights crossing the sky as another, and cut them together.

ABOUT THE AUDIO

  Veo 3 generates its own sound from the AUDIO section, and the music
  description is there mostly to drive the ENERGY OF THE MOTION - describe a
  fast beat and Veo animates faster. But the generated audio will NOT be
  continuous across five separate clips.

  So: generate with the audio described, then MUTE the generated audio in the
  edit and lay one continuous 40-second track underneath. Keep any generated
  impact SFX you like as a separate layer.

  Track brief: 150 BPM, fast aggressive Japanese hip-hop / trap. Deep 808
  sub-bass, syncopated hi-hats, taiko drums, a plucked koto riff as the hook.
  Sparse for 8s, building for 8s, TOTAL SILENCE for 2s, then the drop at 0:16
  and held to 0:32, then everything cuts out dead for the last 8 seconds.

  The one idea worth keeping: the koto riff is the four-note lullaby Noctra
  wrote for Lumi. The drop is the same four notes distorted and pitched down.
  The hype and the story are the same melody.

""")
        f.write(rule + "\n#  NEGATIVE PROMPT - paste into Flow's negative field\n")
        f.write("#  Do NOT paste this into the prompt body.\n")
        f.write(rule + "\n\n")
        f.write(NEGATIVE_FIELD + "\n\n\n")

        for c in CLIPS:
            f.write(rule + "\n")
            f.write(f"#  CLIP {c['n']} OF 5   |   {c['tin']}-{c['tout']}   |   "
                    f"{c['title']}\n")
            f.write(f"#  INGREDIENTS: {c['ingredients']}\n")
            f.write(f"#  NOTE: {' '.join(c['note'].split())}\n")
            f.write(rule + "\n\n")
            f.write(build(c) + "\n\n\n")

    lens = [len(build(c)) for c in CLIPS]
    print(f"clips:      {len(CLIPS)} x {CLIP_SECONDS}s = {len(CLIPS) * CLIP_SECONDS}s")
    print(f"prompt len: {min(lens)}-{max(lens)} chars (was ~3000)")
    print(f"written to: {os.path.join(out, 'FLOW_PROMPTS.txt')}")


if __name__ == "__main__":
    main()
