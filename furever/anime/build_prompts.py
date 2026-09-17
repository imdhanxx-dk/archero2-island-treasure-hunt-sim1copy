#!/usr/bin/env python3
"""
FurEver — anime teaser prompt builder.

Expands the shot list into paste-ready files for a batch image/video generator.

    python3 build_prompts.py

Outputs into ./out/ :
    bulk_prompts_10s.txt   every shot, one full self-contained prompt per line
    core_cut_10s.txt       just the 16-shot core teaser cut
    narration_script.txt   timecoded VO script for a TTS or a voice actor
    shots.csv              spreadsheet of the whole edit
    character_refs.txt     three reference-still prompts to generate FIRST
"""

import csv
import os
import textwrap

SHOT_SECONDS = 10

STYLE = (
    "STYLE: 2D cel-shaded Japanese anime, theatrical feature-film quality, "
    "hand-drawn key-animation look, crisp confident ink linework with varied line "
    "weight, flat cel shading with hard-edged shadow terminators, warm rim light "
    "separating subject from background, lush hand-painted gouache backgrounds in "
    "the classic Japanese anime background-art tradition, rich cinematic color "
    "script, volumetric god-rays, floating dust and pollen particulate, subtle 35mm "
    "film grain, anamorphic lens flare, shallow depth of field, 2.39:1 cinemascope, "
    "24fps, no on-screen text, no subtitles, no watermark, no logo."
)

NEGATIVE = (
    "NEGATIVE: 3D render, CGI, Pixar style, photorealistic, live action, plastic "
    "sheen, western cartoon, chibi, deformed anatomy, extra limbs, extra tails, "
    "melting faces, morphing features, flickering, warped eyes, mismatched eye "
    "color, human faces on animals, text, letters, captions, subtitles, watermark, "
    "signature, UI overlay, low contrast mush, oversaturated neon clipping, jerky "
    "motion, frame blending, duplicated characters, crowd of cats."
)

LUMI = (
    "LUMI: a small white cat, true feline proportions on four legs, fluffy fur with "
    "a faint cream undertone at ears and tail-tip, large round pale-gold eyes with "
    "vertical pupils, thin delicate gold filigree markings tracing his forelegs and "
    "across his brow, wearing a long dark indigo-navy scarf of woven-night fabric "
    "with ten small circular silver fastenings stitched along it, scarf ends frayed "
    "and trailing behind him."
)

NOCTRA = (
    "NOCTRA: an enormous black cat, four to five times Lumi's size, fur so "
    "absolutely black it reads as a hole cut in the frame and absorbs surrounding "
    "light, pale violet eyes with slit pupils that emit a faint glow, thin violet "
    "fracture-lines crawling across his body like lightning trapped beneath stone, "
    "black smoke drifting continuously off his silhouette, a large cracked violet "
    "gem set in his chest with a single hairline gold fracture across it."
)

SCARF = (
    "THE NIGHTWEAVE: a long dark indigo scarf of impossibly black woven fabric that "
    "light falls into rather than off, ten small circular silver fastenings stitched "
    "along its length in an irregular constellation pattern, frayed trailing ends."
)

LOCKS = {"lumi": LUMI, "noctra": NOCTRA, "scarf": SCARF}


# ---------------------------------------------------------------------------
# THE SHOT LIST
#   core : belongs to the 16-shot core teaser cut
#   body : the shot itself, written as one continuous 10-second action
#   vo   : background narration, timed to ~10s at trailer pace. "" = silent.
# ---------------------------------------------------------------------------

SHOTS = [
    # ================= ACT I — THE FULL SKY =================
    dict(
        id="01", act="I. THE FULL SKY", core=True, title="Veylora at dawn",
        body=(
            "Extreme wide establishing shot, slow continuous crane-up over an enormous "
            "fantasy continent at first light. The camera begins low over a sea of "
            "waist-high meadow grass rippling in wind, then rises steadily and without "
            "cutting to reveal the whole world laid out to the horizon in distinct "
            "bands: golden grassland giving way to silver birch forest, a glass-blue "
            "coastline, a red canyon breathing heat-shimmer, terraced cloud-wreathed "
            "mountains, a luminous turquoise jungle, and a far white valley under a "
            "curtain of aurora. Mist lies in every valley. Birds lift in a long ribbon "
            "across the frame as the camera clears the last ridge and the sun breaks "
            "the horizon line, flaring the lens gold."
        ),
        locks=[], stage="THE FULL SKY",
        vo="Before anyone remembered the word FurEver, there was a world called Veylora. It was not built around kingdoms.",
        sfx="Low sustained drone. Distant wind. A single struck bell at the sunrise flare.",
    ),
    dict(
        id="02", act="I. THE FULL SKY", core=False, title="The Tenfold Sky",
        body=(
            "Wide low-angle night shot looking straight up past the silhouettes of "
            "ancient standing stones into a vast star field. The camera holds still, "
            "drifting almost imperceptibly. One by one, ten individual stars brighten "
            "out of the field — green-gold, silver, ice blue, ember red, storm white, "
            "turquoise, pale aurora green, warm gold, deep violet, and one impossible "
            "iridescent point at the very edge of frame — each flaring softly as it "
            "wakes. As the tenth ignites, all ten pulse together once, in unison, like "
            "a single heartbeat, and thin lines of light draw between them, forming a "
            "constellation across the whole sky."
        ),
        locks=[], stage="THE FULL SKY",
        vo="They were not lights hanging in the dark. They were alive. Ten different ways of understanding one single world.",
        sfx="Ten layered chimes, each a different pitch. They resolve into one chord.",
    ),
    dict(
        id="03", act="I. THE FULL SKY", core=True, title="The Starkeeper",
        body=(
            "Low tracking shot at cat's eye height, camera gliding backward just ahead "
            "of LUMI as he walks a stone path through tall evening grass. He is small "
            "and unhurried, tail up. The ten silver fastenings along his dark indigo "
            "scarf are each filled with a tiny living light in a different colour, and "
            "they drift and breathe as he moves, throwing coloured highlights across "
            "his white fur and across the grass on both sides of the path. Fireflies "
            "rise around him. He glances up at something off-frame, and the lights in "
            "the scarf all turn slightly, together, to look the same way."
        ),
        locks=["lumi"], stage="THE FULL SKY",
        vo="And one small cat carried all ten of them — for exactly as long as they wished to stay. That was the whole job.",
        sfx="Grass. Soft footpads. A faint choral hum from the scarf, ten voices.",
    ),
    dict(
        id="04", act="I. THE FULL SKY", core=False, title="Ten lights, breathing",
        body=(
            "Extreme macro close-up, shallow focus, on the fabric of the scarf itself, "
            "camera drifting slowly along its length past one fastening, then another, "
            "then another. Each silver ring holds a small living star that turns gently "
            "in place, casting its own colour across the black weave. The fabric is so "
            "dark that the light falls into it rather than off it. The camera reaches "
            "the tenth ring at the very end of the move — and it is empty. Dark. A bare "
            "silver circle with nothing in it. Hold on the empty ring as focus settles."
        ),
        locks=["scarf"], stage="THE FULL SKY",
        vo="",
        sfx="Fabric. The hum, very close now. It stops dead on the empty ring.",
    ),

    # ================= ACT II — THE BREAK =================
    dict(
        id="05", act="II. THE BREAK", core=True, title="The Vault goes wrong",
        body=(
            "Interior of an enormous ancient underground vault: black stone pillars, "
            "gold mosaic floor, a domed ceiling carved with constellations. Slow "
            "push-in on LUMI standing small at the centre of the vast space, lit only "
            "by his own scarf. The ten coloured lights begin to flicker out of rhythm, "
            "stuttering, swinging on their fastenings as if pulled by something. He "
            "lifts a paw to the scarf. The lights drag harder, all leaning the same "
            "direction. Behind him, deep between two distant pillars, the darkness "
            "thickens and begins to move toward the camera."
        ),
        locks=["lumi"], stage="THE BREAK",
        vo="There were rules older than the language they were written in. You cannot protect a thing by owning it. He never broke one.",
        sfx="Stone ambience. The hum turning discordant. A sub-bass vibration rising.",
    ),
    dict(
        id="06", act="II. THE BREAK", core=False, title="All ten go out",
        body=(
            "Locked-off medium shot of LUMI in the vault, still and alert, scarf lights "
            "guttering wildly and throwing swinging coloured shadows up the pillars. "
            "The flicker accelerates. Then, all at once, every light goes out together "
            "in a single frame, and the shot drops to near-total blackness, with only "
            "the faintest cold rim of light on the edge of his white fur and one "
            "highlight in his wide eye. Nothing moves for a long beat. Then, deep in "
            "the black behind him, two pale violet eyes open, high up, far larger and "
            "far higher than they should be."
        ),
        locks=["lumi"], stage="THE BREAK",
        vo="",
        sfx="Total audio cut on the blackout. Two seconds of absolute silence. Then a breath that is far too large.",
    ),
    dict(
        id="07", act="II. THE BREAK", core=True, title="Noctra",
        body=(
            "Slow, geometrically precise push-in through darkness toward NOCTRA as he "
            "walks out from between two vast pillars. His fur absorbs the residual "
            "light in the chamber, so he reads as a moving absence, a hole in the "
            "image, and the gold mosaic behind him dims as he passes it. Violet "
            "fracture-lines crawl and pulse across his body. Black smoke peels "
            "continuously off his outline and does not disperse. He stops. He lowers "
            "his head toward the camera, and the cracked violet gem in his chest "
            "pulses once, hard, throwing violet light up across his jaw and eyes."
        ),
        locks=["noctra"], stage="THE BREAK",
        vo="Something came up out of the dark that Veylora had spent four hundred years agreeing had never existed at all.",
        sfx="Deep sub-bass. Stone grinding. The gem pulse lands like a struck anvil.",
    ),
    dict(
        id="08", act="II. THE BREAK", core=False, title="The erased name",
        body=(
            "Slow lateral dolly along a ruined temple frieze in half-darkness, "
            "torchlight raking across it. Carved figures of a white cat and an enormous "
            "black cat stand side by side in ancient relief — and as the camera tracks "
            "on, the black cat's figure has been violently chiselled away to blank "
            "stone, leaving only a rough scar in the rock where he used to be. The "
            "camera continues along the wall past panel after panel, and in every "
            "single one the same shape has been removed. The last panel is entirely "
            "blank. Dust drifts through the torchlight."
        ),
        locks=[], stage="THE BREAK",
        vo="They took his name off the statues. They took it out of the books. They left one song behind, to frighten children indoors.",
        sfx="Dripping water. A distant children's choir singing a nursery rhyme, slightly wrong.",
    ),
    dict(
        id="09", act="II. THE BREAK", core=True, title="Light against shadow",
        body=(
            "Dynamic wide shot inside the collapsing vault, camera whip-panning to "
            "follow the action in one continuous move. A sheet of living shadow tears "
            "across the mosaic floor toward LUMI; he leaps aside and lands hard, and "
            "the gold filigree on his forelegs and brow ignites, throwing a curved "
            "golden barrier of light up between himself and the dark. The shadow "
            "slams into it and breaks around it in violent arcs. Pillars fracture. "
            "Ancient mosaic shatters into the air. He is driven backward across the "
            "floor, barrier held, never once striking out — every motion defensive."
        ),
        locks=["lumi", "noctra"], stage="THE BREAK",
        vo="",
        sfx="No music. Only impact, stone, and breathing. Let it be ugly.",
    ),
    dict(
        id="10", act="II. THE BREAK", core=True, title="The constellation breaks",
        body=(
            "Extreme slow-motion close-up, camera locked. A claw of pure darkness "
            "sweeps down across frame and strikes the dark indigo scarf across LUMI's "
            "chest. The fabric tears. All ten silver fastenings burst open at once in "
            "sequence across the frame, and the ten coloured lights blow outward and "
            "upward past the lens in trailing streaks, leaving the torn scarf whipping "
            "empty in the shockwave. Hold on his face in the last beat: pupils blown "
            "wide, the reflected colours draining out of his eyes one by one until "
            "there is nothing left in them but the vault."
        ),
        locks=["lumi"], stage="THE BREAK",
        vo="",
        sfx="A long, rising, glassy tear. Ten distinct notes leaving, high to low.",
    ),
    dict(
        id="11", act="II. THE BREAK", core=True, title="The Homing",
        body=(
            "Enormous wide exterior night shot of the mountainside above the vault, "
            "camera static and reverent. The roof of the ruin blows open and ten beams "
            "of coloured light tear vertically out of it into the night sky — green, "
            "silver, ice blue, ember red, storm white, turquoise, pale aurora, gold, "
            "violet, and one iridescent — then each one bends, separately, at a "
            "different angle, and streaks away over the horizon in a different "
            "direction, over ocean, forest, mountain and desert, leaving long fading "
            "trails of colour hanging across the whole sky."
        ),
        locks=[], stage="THE BREAK",
        vo="And ten stars did the one thing nobody in recorded history had ever seen them do. They went home. All of them. At once.",
        sfx="A single held orchestral swell. Ten departing pitches. Then nothing.",
    ),

    # ================= ACT III — THE EMPTY SKY =================
    dict(
        id="12", act="III. THE EMPTY SKY", core=True, title="The map burns",
        body=(
            "Slow push-in, extreme close-up on LUMI's face as he collapses sideways "
            "onto the broken mosaic floor, cheek against cold stone, the torn empty "
            "scarf pooled around him. His pupils are wide and searching. Reflected in "
            "his eye, faint ghost-images surface and dissolve one after another — a "
            "face, a doorway, a hand, a snowfall — each one fading out an instant "
            "after it appears, until the reflection holds nothing but the empty ruined "
            "ceiling above him. His eyes lose focus completely. The last thing that "
            "moves is his breath."
        ),
        locks=["lumi"], stage="THE EMPTY SKY",
        vo="The stars had never carried his memories. They had carried the map he kept them on. When it broke, so did he.",
        sfx="Everything underwater. A four-note lullaby, hummed, very faint.",
    ),
    dict(
        id="13", act="III. THE EMPTY SKY", core=True, title="Waking in the meadow",
        body=(
            "Low shot from ground level in tall sunlit meadow grass, lens almost "
            "touching the soil, shallow focus. Blue sky and slow clouds fill the top "
            "of frame. Insects drift through warm bars of light. LUMI's eyes open in "
            "the foreground, unfocused, blinking hard against the brightness. The "
            "camera slowly rises with him as he sits up, disoriented, turning his head "
            "left and right across a landscape he clearly does not recognise, wind "
            "moving the grass all around him and the torn indigo scarf hanging dark "
            "and empty around his neck."
        ),
        locks=["lumi"], stage="THE EMPTY SKY",
        vo="",
        sfx="Wind in grass. Birdsong. Unbearably peaceful. A long time before any music.",
    ),
    dict(
        id="14", act="III. THE EMPTY SKY", core=True, title="Nothing happens",
        body=(
            "Tight close-up, handheld micro-drift, on LUMI's paw and the scarf. He "
            "touches one empty silver fastening. Nothing happens. He touches the next "
            "one. Nothing happens. The camera tilts slowly up from the scarf to his "
            "face as he keeps touching them, faster now, working along the row — and "
            "the realisation arrives in his eyes and his ears flatten back against his "
            "skull. He stops. He looks out at the vast empty meadow around him. He has "
            "absolutely no idea who he is."
        ),
        locks=["lumi"], stage="THE EMPTY SKY",
        vo="He woke in a field with a scarf full of empty spaces, and no way of telling which one of them had been his own name.",
        sfx="Silence under the wind. One very small, unmusical note.",
    ),
    dict(
        id="15", act="III. THE EMPTY SKY", core=False, title="Nobody saw that",
        body=(
            "Wide comedic locked-off shot in the meadow. LUMI gathers himself with "
            "great dignity and attempts to stand. His legs fold and he goes "
            "face-first into the grass and disappears completely. A long still beat "
            "with nothing in frame but swaying grass. Then his head emerges, grass "
            "stuck to his ears, and he looks slowly and directly toward a tiny "
            "glowing bulb-shaped creature watching him from behind a flower. The "
            "creature stares back. It drops silently underground. Lumi's tail "
            "twitches once."
        ),
        locks=["lumi"], stage="THE EMPTY SKY",
        vo="He did not know what a Starkeeper was. He did not know where he was. He was, however, still extremely polite about it.",
        sfx="A single plucked string on the fall. Comic timing. Let the silence do it.",
    ),
    dict(
        id="16", act="III. THE EMPTY SKY", core=False, title="Mirrowen",
        body=(
            "Sweeping crane reveal as the camera rises over a ridge of flowering trees "
            "to disclose the city of Mirrowen in full morning light: stone towers "
            "wound with ivy, slow windmills, arched bridges over streams that glow "
            "faintly beneath the surface, market banners snapping, small copper "
            "airships drifting between rooftops on lazy thermals, and at the absolute "
            "centre an ancient tree so vast its branches carry the whole skyline. "
            "LUMI is a tiny white figure at the bottom of frame on the road below, "
            "walking toward it, scarf trailing."
        ),
        locks=["lumi"], stage="THE EMPTY SKY",
        vo="Somewhere inside that city, somebody knew who he used to be. That was the only plan he had.",
        sfx="Bells. Market noise rising as the crane clears the ridge. Warmth.",
    ),

    # ================= ACT IV — TEN REGIONS =================
    dict(
        id="17", act="IV. TEN REGIONS", core=False, title="Whispering Meadow — nothing ends",
        body=(
            "Slow lateral dolly through an overgrown meadow at golden hour, and "
            "something is deeply wrong with it. Every flower of every season is open "
            "at once. Grass stands shoulder-high and utterly motionless in wind that "
            "is clearly blowing. A long-fallen tree lies split open and still bright "
            "green, held upright by the living grass driving straight through its "
            "trunk. Nothing has rotted. The camera passes a wooden fence swallowed to "
            "the top rail, then a farm gate that cannot be opened for the roots, and "
            "settles on a village beyond, half-buried in green."
        ),
        locks=[], stage="THE EMPTY SKY",
        vo="The stars had gone home. And home had not been ready for them.",
        sfx="Too much birdsong. A creaking of roots under everything.",
    ),
    dict(
        id="18", act="IV. TEN REGIONS", core=True, title="Frostfang — the valley that will not thaw",
        body=(
            "Slow push-in down a snowbound alpine valley at night under an enormous "
            "curtain of green and violet aurora filling the entire upper frame and "
            "rippling continuously. Everything below is perfectly, unnaturally still: "
            "a frozen waterfall caught mid-fall, snow lying undisturbed on every "
            "surface in exactly the same depth, one small window of warm orange "
            "lamplight in a distant wooden house. Not one flake is falling. Not one "
            "thing moves except the aurora overhead. The camera arrives at the lit "
            "window and holds."
        ),
        locks=[], stage="THE EMPTY SKY",
        vo="A valley where the snow has not melted since the night it fell. Where nothing heals — because nothing is allowed to change.",
        sfx="Absolute silence. A distant, single, held violin note. Ice ticking.",
    ),
    dict(
        id="19", act="IV. TEN REGIONS", core=False, title="Ember Canyon — never finished",
        body=(
            "Wide low-angle shot pushing slowly up a canyon of red rock and black "
            "volcanic glass, heat-shimmer distorting the air across the whole frame. "
            "Fires burn steadily on bare stone with no fuel beneath them. Ash falls "
            "upward as often as down and never settles. Molten seams glow in the cliff "
            "walls, half-cooled, neither liquid nor solid. In the foreground a pine "
            "cone sits sealed shut with hardened resin on scorched ground, waiting, "
            "surrounded by fire that never quite reaches it. Embers stream past the "
            "lens in long trails."
        ),
        locks=[], stage="THE EMPTY SKY",
        vo="A canyon that has been burning for a year, and has not yet finished becoming anything at all.",
        sfx="Roar of standing fire. No crackle — it never consumes anything.",
    ),
    dict(
        id="20", act="IV. TEN REGIONS", core=False, title="Neon Rainforest — everything shouting",
        body=(
            "Slow steadicam glide through a dense night rainforest saturated in "
            "overwhelming bioluminescence: every leaf, vine, fungal shelf, root, "
            "insect and drop of river water blazing in turquoise, magenta and "
            "acid-green, all pulsing at different rates, far too bright, with no "
            "darkness anywhere for any of it to read against. The camera pushes "
            "through hanging light-vines into a small clearing where one researcher's "
            "blackout tent stands with its flap sealed — a single perfect square of "
            "true black in a world with none left."
        ),
        locks=[], stage="THE EMPTY SKY",
        vo="A forest screaming light in ten thousand voices, and not one living thing in it able to be seen.",
        sfx="Overwhelming insect noise, layered to painfulness. It cuts dead at the tent.",
    ),
    dict(
        id="21", act="IV. TEN REGIONS", core=True, title="Ten places to stand",
        body=(
            "One continuous impossible camera move: a slow pull-back from a single "
            "glowing green root deep underground, rising up through soil and stone "
            "into open sky, where the whole of Veylora is visible far below at dusk — "
            "and in ten separate distant places across the landscape, ten different "
            "coloured glows are burning up from beneath the ground: green in the "
            "meadow, silver in the forest, blue on the coast, red in the canyon, white "
            "on the peaks, turquoise in the jungle, aurora in the north, gold in far "
            "ruins, violet under a dead mountain, and one iridescent point beyond the "
            "edge of the map entirely."
        ),
        locks=[], stage="THE EMPTY SKY",
        vo="Ten stars. Ten homelands. And not a single one of them willing to be carried again.",
        sfx="Ten tones returning, one at a time, building to the chord from shot 02 — but incomplete.",
    ),

    # ================= ACT V — THE PURSUER =================
    dict(
        id="22", act="V. THE PURSUER", core=True, title="Two days behind",
        body=(
            "Locked-off wide shot of a wooden border post on an empty moorland road in "
            "heavy grey rain, camera perfectly still. A knotted cord hangs from the "
            "post, freshly tied, swinging slightly. The road behind it is empty. Hold. "
            "Rain falls. Then, very slowly, the darkness in the background of the "
            "frame resolves — it is not shadow, it is NOCTRA, enormous and motionless, "
            "already standing there, so black that he had read as empty air. He lowers "
            "his head to the knotted cord and looks at it for a long moment. He does "
            "not touch it. He walks on, in the direction the road goes."
        ),
        locks=["noctra"], stage="THE PURSUER",
        vo="Something has been following him since the first night. Across every border. It has not attacked him once.",
        sfx="Rain. Nothing else. No music at all until he moves.",
    ),
    dict(
        id="23", act="V. THE PURSUER", core=True, title="The one who knows",
        body=(
            "Extreme close-up, camera slowly pushing in on NOCTRA's face in near "
            "darkness, lit only by the violet glow of his own fracture-lines and the "
            "gem below frame. His expression is not rage — it is exhaustion, and "
            "something much more painful held very carefully still. The camera drifts "
            "down his chest to the cracked violet gem, and the single hairline gold "
            "fracture across it catches the light and, over the last beats of the "
            "shot, visibly widens by a fraction, glowing warm gold against the violet."
        ),
        locks=["noctra"], stage="THE PURSUER",
        vo="It is the only creature alive who knows his name. And it cannot tell him. Being told is not the same as remembering.",
        sfx="Very low breath. A single warm piano note on the gold fracture. Wrong instrument, deliberately.",
    ),
    dict(
        id="24", act="V. THE PURSUER", core=True, title="Find them",
        body=(
            "Wide two-shot at dusk on an open ridge under a huge bruised sky. LUMI "
            "stands small in the left of frame, scarf trailing, turned to face the "
            "right of frame where NOCTRA stands enormous and utterly still at a "
            "distance, smoke lifting off him into the wind. Neither approaches. The "
            "gap between them holds the centre of the composition for a long beat. "
            "Then Noctra turns away first and begins to walk into the deepening dark, "
            "and the camera holds on Lumi alone, watching him go, one paw lifted "
            "slightly as if to call out and not doing it."
        ),
        locks=["lumi", "noctra"], stage="THE PURSUER",
        vo="NOCTRA (V.O.): \"Find them. Find every one of them. And when you remember —\"",
        sfx="The narrator's voice, for the first time, is coming from inside the shot.",
    ),

    # ================= ACT VI — TITLE =================
    dict(
        id="25", act="VI. TITLE", core=True, title="Title card",
        body=(
            "Hard cut to absolute black. Total stillness. Then, at the exact centre of "
            "the frame, one small point of warm gold light ignites and slowly blooms "
            "outward, throwing a soft circular glow that reveals, very faintly, the "
            "weave of black fabric filling the entire frame — the texture of the "
            "Nightweave itself, with the ghosts of ten empty silver fastenings barely "
            "visible arranged around the light in a constellation. The gold point "
            "pulses once, gently, like something answering, and holds."
        ),
        locks=["scarf"], stage="TITLE",
        vo="NOCTRA (V.O.): \"— find me.\"",
        sfx="Absolute silence, then the four-note lullaby, played once, complete. Title sting.",
    ),
    dict(
        id="26", act="VI. TITLE", core=False, title="One light comes back",
        body=(
            "Final wide shot, golden hour, camera low and static. LUMI walks away from "
            "the lens along a stone path into an enormous open landscape, small against "
            "it, the torn indigo scarf trailing behind him in the wind. He is almost at "
            "the horizon. Then, without him noticing, a single one of the ten empty "
            "silver fastenings on the trailing scarf flickers — once, faintly, green — "
            "and goes dark again. He keeps walking. Behind him, far back at the very "
            "edge of the frame, something enormous and black is following at a "
            "distance, unhurried."
        ),
        locks=["lumi", "noctra"], stage="TITLE",
        vo="Ten stars left him. He is going to have to ask every single one of them to come back.",
        sfx="The full ten-note chord, but with two notes missing. Hold. Cut to black.",
    ),
]


# ---------------------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------------------

def build_prompt(shot):
    """One fully self-contained, paste-ready prompt for a 10-second clip."""
    parts = [
        f"{SHOT_SECONDS}-SECOND ANIME SHOT.",
        STYLE,
        f"COLOR STAGE: {shot['stage']}.",
    ]
    parts += [LOCKS[k] for k in shot["locks"]]
    parts += [
        f"SHOT: {shot['body']}",
        (
            "TIMING: one single continuous take, one camera move, one change of state; "
            "0-3s the frame settles with one element already in motion, 3-7s the move "
            "commits, 7-10s the state changes and the shot lands. No cuts inside the shot."
        ),
        NEGATIVE,
    ]
    return " ".join(" ".join(p.split()) for p in parts)


def timecode(seconds):
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "out")
    os.makedirs(out, exist_ok=True)

    core = [s for s in SHOTS if s["core"]]

    # 1. every shot, one prompt per line
    with open(os.path.join(out, "bulk_prompts_10s.txt"), "w") as f:
        for s in SHOTS:
            f.write(build_prompt(s) + "\n")

    # 2. core cut only
    with open(os.path.join(out, "core_cut_10s.txt"), "w") as f:
        for s in core:
            f.write(build_prompt(s) + "\n")

    # 3. narration scripts - one per cut, so the timecodes are actually usable
    def write_narration(path, shots, header):
        with open(path, "w") as f:
            f.write("FUREVER - TEASER NARRATION SCRIPT\n")
            f.write(header + "\n")
            f.write("Voice: low, unhurried, warm, close-mic'd. Not a trailer boom.\n")
            f.write("He is remembering, not announcing. (It is Noctra. Do not play it that way yet.)\n")
            f.write("=" * 72 + "\n\n")
            t = 0
            for s in shots:
                tag = "[CORE]" if s["core"] else "[EXT] "
                f.write(f"{tag} {timecode(t)}-{timecode(t + SHOT_SECONDS)}  "
                        f"SHOT {s['id']} - {s['title']}\n")
                if s["vo"]:
                    for line in textwrap.wrap(s["vo"], 68):
                        f.write(f"        {line}\n")
                else:
                    f.write("        (SILENT - do not fill this. The silence is the point.)\n")
                f.write(f"        SFX: {s['sfx']}\n\n")
                t += SHOT_SECONDS

    write_narration(os.path.join(out, "narration_extended.txt"), SHOTS,
                    f"EXTENDED CUT - all {len(SHOTS)} shots, {timecode(len(SHOTS) * SHOT_SECONDS)}")
    write_narration(os.path.join(out, "narration_core.txt"), core,
                    f"CORE CUT - {len(core)} shots, {timecode(len(core) * SHOT_SECONDS)}")

    # 4. csv of the edit
    with open(os.path.join(out, "shots.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["shot", "act", "title", "core",
                    "ext_tc_in", "ext_tc_out", "core_tc_in", "core_tc_out",
                    "seconds", "narration", "sfx", "prompt"])
        t = ct = 0
        for s in SHOTS:
            if s["core"]:
                core_in, core_out = timecode(ct), timecode(ct + SHOT_SECONDS)
                ct += SHOT_SECONDS
            else:
                core_in = core_out = ""
            w.writerow([s["id"], s["act"], s["title"], "yes" if s["core"] else "no",
                        timecode(t), timecode(t + SHOT_SECONDS), core_in, core_out,
                        SHOT_SECONDS, s["vo"], s["sfx"], build_prompt(s)])
            t += SHOT_SECONDS

    # 5. character reference stills - generate these FIRST
    with open(os.path.join(out, "character_refs.txt"), "w") as f:
        refs = [
            ("LUMI", LUMI,
             "Full-body character reference sheet on a plain neutral studio "
             "background, three-quarter front view, neutral standing pose, even "
             "flat lighting, maximum design clarity, every detail of the scarf and "
             "the gold filigree markings clearly legible, anime character model "
             "sheet, settei style."),
            ("NOCTRA", NOCTRA,
             "Full-body character reference sheet on a plain mid-grey studio "
             "background, three-quarter front view, standing at full height, even "
             "flat lighting, maximum design clarity, the violet fracture-lines and "
             "the cracked chest gem clearly legible against the black fur, anime "
             "character model sheet, settei style."),
            ("NIGHTWEAVE", SCARF,
             "Prop reference sheet on a plain neutral background, the scarf laid "
             "out flat and fully extended so all ten silver fastenings are visible "
             "in their irregular constellation arrangement, even flat lighting, "
             "macro detail inset of a single fastening, anime prop model sheet, "
             "settei style."),
        ]
        f.write("GENERATE THESE THREE FIRST. Use them as reference/first-frame\n")
        f.write("images for every shot the character appears in. This matters more\n")
        f.write("than any prompt wording.\n")
        f.write("=" * 72 + "\n\n")
        for name, lock, framing in refs:
            f.write(f"--- {name} ---\n")
            body = " ".join(f"{STYLE} {lock} {framing} {NEGATIVE}".split())
            f.write(body + "\n\n")

    total = len(SHOTS) * SHOT_SECONDS
    core_total = len(core) * SHOT_SECONDS
    print(f"shots:      {len(SHOTS)}  ({timecode(total)})")
    print(f"core cut:   {len(core)}  ({timecode(core_total)})")
    print(f"narrated:   {sum(1 for s in SHOTS if s['vo'])}")
    print(f"silent:     {sum(1 for s in SHOTS if not s['vo'])}")
    print(f"written to: {out}")


if __name__ == "__main__":
    main()
