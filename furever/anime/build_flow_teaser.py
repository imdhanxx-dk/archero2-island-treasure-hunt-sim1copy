#!/usr/bin/env python3
"""
FurEver - 1:12 ANIME TEASER, BUILT FOR GOOGLE FLOW (Veo).

Flow is not a generic image generator and the generic prompts fail on it.
This rewrites the teaser for how Veo actually behaves:

  * 8-SECOND CLIPS, not 10. Nine clips x 8s = 1:12 exactly.
  * SEPARATE NEGATIVE FIELD. Veo has one. Instructive negatives written inside
    the prompt body ("no text", "no extra limbs") can summon the thing instead
    of suppressing it. The negative list is emitted separately to paste in.
  * ONE CAMERA MOVE PER CLIP. Compound moves (crash zoom into whip pan into
    crane) are why subjects end up off-screen - Veo cannot track through them.
  * EXPLICIT FRAMING. Veo needs to be told the subject stays in frame.
  * STRUCTURED SECTIONS. Subject / Action / Scene / Camera / Composition /
    Lighting / Style / Audio, in that order.
  * NO GENERATED MUSIC OR VOICE. Veo mixes its own score and its own chosen
    narrator into one track you cannot unmix. Prompts ask for diegetic sound
    effects only; music and VO are laid over in the edit.
  * SHORTER than the generic build. Long prompts dilute on Veo.

    python3 build_flow_teaser.py

Outputs into ./out/ :
    FLOW_PROMPTS.txt    all 9 prompts + negative field + end-card spec
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
    "user interface, progress bar, letterbox bars, music, background music, soundtrack, score, singing, humming, instruments, speech, narration, voice-over, dialogue, female voice, woman speaking, male voice, child voice, moving mouth, open mouth, "
    "talking animal, lip sync, speaking character, singing, subject out of "
    "frame, cropped subject, subject leaving frame, blank frame, frozen frame, "
    "slow motion throughout, chromatic aberration, glitch effect, VHS artifacts, "
    "light leak overlay, duplicated character, crowd of cats"
)

STYLE = (
    "2D cel-shaded Japanese anime, theatrical feature film quality, hand-drawn "
    "key animation, crisp ink linework with varied line weight, flat cel shading "
    "with hard shadow edges, hand-painted background art, saturated cinematic "
    "colour, subtle film grain, 24fps, widescreen 2.39:1"
)

# Veo bakes its generated audio into the clip and you cannot separate the music
# from the sound effects afterwards. So we ask for NOTHING but diegetic sound
# effects, and the music and voice-over go on in the edit where you control them.

NO_MUSIC_NO_VOICE = (
    "There is absolutely no music in this clip of any kind - no soundtrack, no "
    "score, no background music, no melody, no instruments, no singing and no "
    "humming. There is also no speech of any kind - no narration, no voice-over, "
    "no dialogue, no whispering and no breathing voice, male or female or child. "
    "Nobody speaks and nothing is sung. Every animal on screen keeps its mouth "
    "completely closed and still for the entire shot, and no mouth, jaw or muzzle "
    "moves at any point. The only audio in this clip is the natural diegetic "
    "sound of the scene itself, listed above, and nothing else."
)


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
        audio=("Wind moving steadily through tall grass. Fast light footpads running on dry soil. The long scarf snapping and fluttering in the airflow behind him. Distant birdsong. Everything open and airy. "
               + NO_MUSIC_NO_VOICE),
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
        audio=("The open wind dies away and is replaced by the deep hollow room tone of an enormous stone chamber. Faint electrical fizzing as each light fails. A low stone rumble building underneath. The final second is near-total silence. "
               + NO_MUSIC_NO_VOICE),
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
        audio=("The dead air of a vast underground stone hall. A single drip of water far away. Very large, slow, heavy footfalls on stone, unhurried. A deep low resonant hum rising from the gem. Fine dust settling. "
               + NO_MUSIC_NO_VOICE),
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
        audio=("Stone cracking and shattering. One enormous heavy impact. A long high glassy tearing sound as the scarf rips open. Then a sudden rush of moving air as the camera climbs, and open high-altitude wind. "
               + NO_MUSIC_NO_VOICE),
        note="Busiest clip. If it drifts, generate the fight and the sky as two "
             "separate 8s clips and cut them together.",
    ),
    dict(
        n=5, tin="0:32", tout="0:40", title="THE BROKEN WORLD",
        ingredients="none - landscape only",
        subject="A vast fantasy world seen from the air, with no characters in it. "
                "Three distinct regions in sequence below the camera.",
        action="A fast continuous forward flight across the landscape. First over a "
               "snowbound valley under a huge rippling green and violet aurora "
               "where absolutely nothing moves and a waterfall hangs frozen "
               "mid-fall. Then over a red rock canyon where fires burn steadily on "
               "bare stone with no fuel and embers stream upward. Then over a dense "
               "jungle canopy blazing with overwhelming turquoise and magenta "
               "bioluminescence, every leaf and vine glowing far too brightly.",
        scene="An enormous broken fantasy landscape at night. Each region is "
              "beautiful and visibly wrong - frozen solid, endlessly burning, or "
              "painfully overlit.",
        camera="One single fast continuous forward aerial flight, low over the "
               "terrain, moving the whole time. One continuous move only.",
        comp="Wide aerial shot. The horizon line stays level in the upper third "
             "for the entire eight seconds and the landscape fills the frame. The "
             "camera never tilts away from the terrain and never loses the horizon.",
        light="Aurora green and violet over the snow, hard orange firelight in the "
              "canyon, saturated turquoise glow in the jungle. Each region lit "
              "entirely by its own colour.",
        audio=("High wind at altitude throughout. Ice groaning and settling over the frozen valley. The low steady roar of open fire over the canyon. Dense layered insect and frog noise over the jungle. "
               + NO_MUSIC_NO_VOICE),
        note="No characters, so this one is safe from drift. Good clip to "
             "over-generate cheaply.",
    ),
    dict(
        n=6, tin="0:40", tout="0:48", title="LUMI - THE SECOND DROP",
        ingredients="Lumi + scarf",
        subject=f"{LUMI}. One single ring on the scarf now holds a bright green "
                "glowing star. The other nine are still empty and dark.",
        action="He stands braced and low on cracked stone ground as a storm of "
               "dark energy batters him. The gold markings on his forelegs and "
               "brow blaze to full brightness and an enormous curved golden shield "
               "of light expands outward around him. Debris and glowing fragments "
               "blast past him. He does not move backward.",
        scene="Shattered stone ground in near darkness, dark energy sweeping "
              "across it, fragments of rock and gold light suspended in the air.",
        camera="One single slow orbit around him from a low hero angle, rising "
               "slightly. One continuous move only.",
        comp="Low angle hero shot. The white cat is centred in the frame and fully "
             "visible from nose to tail for the entire eight seconds, occupying "
             "the middle third. The camera orbits around him but keeps him dead "
             "centre and never loses him.",
        light="Brilliant warm gold light radiating from the cat himself against a "
              "near-black background, hard rim lighting, the gold shield glowing.",
        audio=("A low sustained roar of energy pressing against him. Stone fragments clattering and skittering across the ground. A bright sustained ringing tone from the shield of light, like a struck glass rim held. "
               + NO_MUSIC_NO_VOICE),
        note="His power moment. This is the shot that has to make people want to "
             "play as him. Spend takes here.",
    ),
    dict(
        n=7, tin="0:48", tout="0:56", title="THE PURSUER",
        ingredients="Noctra only",
        subject=f"{NOCTRA}.",
        action="He walks slowly and steadily forward toward the camera down an "
               "empty road in heavy night rain, never hurrying. Rain steams and "
               "hisses where it touches him. The violet cracks across his body "
               "pulse brighter as he comes closer, and he does not break stride.",
        scene="An empty moorland road at night in torrential rain. Wet stone, "
              "standing water, a broken wooden post at the roadside. No lights "
              "anywhere.",
        camera="One single slow push-in toward him along the road. One continuous "
               "move only.",
        comp="Wide shot tightening to a medium shot. The enormous black cat is "
             "centred in the frame and fully visible for the entire eight seconds, "
             "walking directly toward the lens. He stays dead centre and the "
             "camera never loses him.",
        light="Near-total darkness and rain. He is lit only by the violet glow of "
              "his eyes, the cracks across his body and the gem in his chest, with "
              "rain catching that violet light as it falls.",
        audio=("Heavy rain falling on wet stone and standing water throughout. Water running off into the roadside. Slow, heavy, deliberate footfalls through puddles. A faint hiss where the rain touches him and turns to steam. "
               + NO_MUSIC_NO_VOICE),
        note="Menace, not action. The restraint here is what makes clip 6 and the "
             "end card land.",
    ),
    dict(
        n=8, tin="0:56", tout="1:04", title="THE FALL",
        ingredients="Lumi + scarf",
        subject=f"{LUMI}, except his scarf is torn and all ten silver rings are "
                "completely empty and dark.",
        action="His eyes open. He pushes himself up quickly, disoriented, looking "
               "around at a landscape he does not recognise. He looks down and "
               "touches one empty silver ring on the torn scarf with a paw. "
               "Nothing happens. He touches the next one. Nothing happens. He "
               "stops and his ears flatten back.",
        scene="A pale washed-out dawn meadow. Tall grass, weak morning light, "
              "insects drifting through the air. Everything is desaturated, still "
              "and quiet.",
        camera="One single slow rise from ground level as he sits up, settling "
               "into a close shot on his face and the scarf. One continuous move "
               "only.",
        comp="Low shot rising to a close-up. The white cat is centred in the frame "
             "and fully visible for the entire eight seconds, with his face and "
             "the torn scarf both clearly inside the frame. The camera keeps him "
             "centred and never loses him.",
        light="Pale, flat, desaturated morning light with no warmth in it at all.",
        audio=("Soft wind moving through meadow grass. Distant birdsong. His own quick unsteady breathing. Small dry metallic clicks as his paw touches each empty silver ring. Otherwise very quiet. "
               + NO_MUSIC_NO_VOICE),
        note="The silence after two drops is what sells the loss. Keep the grade "
             "pale - do not put warmth back in.",
    ),
    dict(
        n=9, tin="1:04", tout="1:12", title="END CARD PLATE",
        ingredients="none - abstract plate",
        subject="A completely black frame with a single small point of warm gold "
                "light at the exact centre. No characters, no landscape, no "
                "objects.",
        action="The single gold point of light ignites at the centre of the black "
               "frame and blooms slowly outward, its glow faintly revealing the "
               "texture of black woven fabric filling the whole frame. Ten small "
               "faint silver rings fade up around it, arranged in an irregular "
               "constellation pattern, and thin silver lines draw slowly between "
               "them. The gold point pulses gently once and holds steady.",
        scene="Pure black, with the faint texture of very dark woven cloth "
              "revealed only by the central glow.",
        camera="The camera is completely static and does not move at all for the "
               "entire eight seconds. No push, no drift, no shake.",
        comp="Perfectly symmetrical centred composition. The gold point sits at "
             "the exact centre of the frame. The ten silver rings are spread "
             "evenly around it with generous empty black space at the top and "
             "bottom of the frame, because titles and a button are composited "
             "into those areas afterwards. Nothing enters or crosses the frame.",
        light="A single warm gold light source at the centre, falling off quickly "
              "into pure black.",
        audio=("Near-total silence. A faint low room tone. One soft single chime as the gold light blooms outward, then quiet. "
               + NO_MUSIC_NO_VOICE),
        note="A CLEAN PLATE. The FUREVER logo and the PLAY NOW button are "
             "composited over this in the edit - never let Veo render text. Keep "
             "the top and bottom of the frame empty.",
    ),
]


END_CARD = """
COMPOSITE THIS OVER CLIP 9 (1:04-1:12). Never generate text in Veo - it will
produce garbled glyphs. Build this in After Effects, Premiere, CapCut or Canva
over the clean plate.

PALETTE
  Background       #05060B   near-black, the colour of the scarf
  Gold primary     #F0C24A   the logo, the button fill, the centre light
  Gold highlight   #FFD77A   glow and bloom on the gold
  Violet accent    #7B4BD6   Noctra's colour, used once and sparingly
  Off-white        #EDEAE3   the subtitle and the small print

TYPE
  FUREVER              a wide geometric sans, heavy weight, all caps,
                       letter-spacing about 0.18em. Gold #F0C24A with a soft
                       outer glow. This is the hero element.
  THE LOST STARKEEPER  the same family, light weight, all caps, letter-spacing
                       about 0.32em, roughly 30 percent of the logo size.
                       Off-white #EDEAE3 at about 80 percent opacity.
  PLAY NOW             medium weight, all caps, letter-spacing about 0.12em,
                       dark #05060B sitting on the gold button fill.

LAYOUT, top to bottom, centred
  1. The ten-ring constellation from the plate, small, upper-middle
  2. FUREVER
  3. THE LOST STARKEEPER
  4. PLAY NOW button
  5. Platform badges or a pre-register line, small, at the bottom

THE PLAY NOW BUTTON
  Rounded rectangle, corner radius about half its height, filled solid gold
  #F0C24A, with the text in near-black. Roughly 22 percent of frame width.
  Give it a soft gold outer glow and a slow breathing pulse, about 4 percent
  scale over 1.2 seconds, looping. It should look pressable, not decorative.

TIMING, against the 8 seconds of clip 9
  1:04.0  plate only, the gold point blooming, nothing composited yet
  1:05.6  FUREVER slams in on the beat. Scale from 108 percent to 100 percent
          over 5 frames with a 2-frame white flash behind it. Hard, no easing.
  1:06.4  THE LOST STARKEEPER fades up underneath over 12 frames
  1:07.2  one of the ten silver rings quietly ignites green and holds
  1:08.0  PLAY NOW button scales up from 0 with a short overshoot, then starts
          its breathing pulse
  1:08.8  platform badges fade up at about 70 percent opacity
  1:09.6  hold everything steady to the end

  Total dwell on a complete, readable call to action: about 3.5 seconds. That
  is the minimum that reads on a phone. Do not cut it shorter.

TWO THINGS NOT TO GET WRONG
  The single green ring at 1:07.2 is the whole hook - it says the first star is
  already answering him, and it is the only saturated colour on screen. Do not
  add any other colour.

  Keep the button gold, never violet. Violet is Noctra's colour in this film and
  putting it on the call to action quietly tells the audience the wrong thing.

VERTICAL CUT
  For a 9:16 social version, stack the same order with more vertical spacing,
  make the button roughly 60 percent of frame width, and move the whole group
  up so the button sits above the bottom third where platform UI overlays sit.
"""


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
        f.write(f"#  9 clips x {CLIP_SECONDS}s = 1:12  |  music {BPM} BPM  |  two drops\n")
        f.write(rule + "\n")
        f.write("""
WHY THE EARLIER PROMPTS FAILED ON FLOW, AND WHAT CHANGED

  1. Veo generates 8-SECOND clips, not 10. Restructured to 9 x 8s = 1:12.

  2. Veo has a SEPARATE NEGATIVE PROMPT FIELD. The old prompts had a huge
     negative list buried in the prompt body, which on Veo can summon the very
     things it lists. The negative is now a separate block, below - paste it
     into Flow's negative field, never into the prompt.

  3. YOUR CHARACTERS WENT OFF-SCREEN because the old prompts stacked crash
     zooms into whip pans into crane moves. Veo cannot track a subject through
     a compound move. Every clip now has ONE camera move and an explicit
     COMPOSITION line stating the subject stays centred and fully in frame.

  4. Restructured into the order Veo reads best, so the instructions that
     matter sit near the front. Prompts still run 2,200-3,000 characters
     because the no-music / no-voice block is deliberately verbose - that
     explicitness is what stops Veo scoring the clip and picking its own
     narrator. If Veo starts dropping later instructions, shorten that block
     FIRST, once you have confirmed a few clips come back silent.

  5. Section order: SUBJECT / ACTION / SCENE / CAMERA / COMPOSITION /
     LIGHTING / STYLE / AUDIO.

HOW TO RUN IT IN FLOW

  * Use INGREDIENTS TO VIDEO. Add each character as an Ingredient - that is
    Flow's character-consistency feature and it works far better than
    describing the character in text.
  * Add ONLY the ingredients listed for that clip. Clip 3 is Noctra alone on
    purpose. Two characters in one generation is where Veo drifts worst.
  * Use FRAMES TO VIDEO to chain: take the last frame of each clip and set it
    as the starting frame of the next.
  * Generate 3-4 takes of every clip. Clips 3, 4 and 6 carry the most weight -
    spend your takes there. Clips 5 and 9 have no characters in them, so they
    are cheap and safe.
  * If clip 4 keeps breaking, split it: generate the fight as one 8s clip and
    the ten lights crossing the sky as another, and cut them together.
  * CLIP 9 IS A CLEAN PLATE. The FUREVER logo and the PLAY NOW button are
    composited over it in the edit. Never ask Veo for text - it produces
    garbled glyphs every time. Full end-card spec is at the bottom of this
    file.

AUDIO IS NOT GENERATED. READ THIS.

  Veo bakes its own audio into the clip and you CANNOT separate its music from
  its sound effects afterwards - they come down as one mixed track. It also
  picks its own narrator voice, which is why you got a woman reading it.

  So every prompt below asks for DIEGETIC SOUND EFFECTS ONLY, and states in
  plain terms that there is no music, no score, no singing and no speech of any
  kind, male or female. What you get back is a clean effects layer you can
  actually use - wind, rain, footfalls, stone, the scarf tearing.

  The music and the voice go on in the EDIT, where you control them.

  If a clip still comes back with music or a voice, regenerate it. Do not try
  to fix it in post - it cannot be unmixed.

"""
    + "#" * 78 + """
#  THE MUSIC - license or commission one continuous 72-second track
""" + "#" * 78 + """

  150 BPM. Fast, aggressive Japanese hip-hop / trap. Deep 808 sub-bass,
  syncopated hi-hats, taiko drums, a plucked koto riff as the hook. Two drops.

    0:00  sparse, the koto motif stated clean and alone
    0:08  build - hi-hat rolls accelerating, taiko rising underneath
    0:16  TOTAL SILENCE for 2 seconds, then DROP ONE - Noctra
    0:24  drop continues, biggest single impact on the Homing
    0:32  half-time break, stripped back, spacious
    0:40  DROP TWO - the biggest one, Lumi's power moment
    0:48  stripped to a single kick and rain, menace, holding back
    0:56  everything cuts out dead - 8 full seconds of no music
    1:04  the koto motif once more, clean, then one low sting

  The one idea worth keeping: that koto riff is the four-note lullaby Noctra
  wrote for Lumi. Both drops are the same four notes, distorted and pitched
  down. The hype and the story are the same melody.

  Lay this under the whole cut. Keep the generated sound effects as a separate
  layer underneath it and duck them about 4dB whenever the beat is playing.

"""
    + "#" * 78 + """
#  THE VOICE-OVER - record or synthesise separately, then lay it over
""" + "#" * 78 + """

  DO NOT put these lines in a Veo prompt. That is what produced the wrong
  voice. Record them yourself or run them through a TTS where you can audition
  the voice, then place them on the timeline at these timecodes.

  VOICE DIRECTION
    Deep adult male. Heavy chest resonance, gravel in the bottom end.
    Close-mic'd with audible breath. Slow and weighted - every word lands like
    something heavy being set down. Not a hype-man, not a movie-trailer boom.
    He is remembering, not announcing.

    Track it twice and pitch the second take a full octave down underneath the
    first at about -12dB, so there is a floor beneath the voice you feel more
    than you hear it. Stone-room reverb tail, dry signal kept forward.

    (It is Noctra. Do not play it that way yet.)

  SCRIPT - 35 words across 72 seconds. Keep it this sparse.

    0:02   "Ten stars. One keeper."
    0:11   "They all left him."
    0:16 - 0:32   NOTHING. Both drops play on music and picture alone.
    0:34   "Ten homelands. Every one of them breaking."
    0:40 - 0:48  NOTHING.
    0:50   "Something has followed him since the first night.
            It has never once attacked."
    0:58   "Find them."
    1:06   "And when you remember - find me."

  The trick: he talks about Lumi in the third person for nearly a minute, and
  then at 0:58 the same voice speaks TO him. Same read - do not perform the
  reveal, the shift from description to instruction does it by itself.

""")
        f.write(rule + "\n#  NEGATIVE PROMPT - paste into Flow's negative field\n")
        f.write("#  Do NOT paste this into the prompt body.\n")
        f.write("#  Note: 'static shot' is deliberately NOT in this list - clip 9 "
                "needs a locked-off camera.\n")
        f.write(rule + "\n\n")
        f.write(NEGATIVE_FIELD + "\n\n\n")

        for c in CLIPS:
            f.write(rule + "\n")
            f.write(f"#  CLIP {c['n']} OF {len(CLIPS)}   |   {c['tin']}-{c['tout']}   |   "
                    f"{c['title']}\n")
            f.write(f"#  INGREDIENTS: {c['ingredients']}\n")
            f.write(f"#  NOTE: {' '.join(c['note'].split())}\n")
            f.write(rule + "\n\n")
            f.write(build(c) + "\n\n\n")

        f.write(rule + "\n#  END CARD - FUREVER / PLAY NOW\n")
        f.write("#  Composited in the edit over clip 9. Not generated.\n")
        f.write(rule + "\n")
        f.write(END_CARD + "\n")

    lens = [len(build(c)) for c in CLIPS]
    print(f"clips:      {len(CLIPS)} x {CLIP_SECONDS}s = {len(CLIPS) * CLIP_SECONDS}s")
    print(f"prompt len: {min(lens)}-{max(lens)} chars (was ~3000)")
    print(f"written to: {os.path.join(out, 'FLOW_PROMPTS.txt')}")


if __name__ == "__main__":
    main()
