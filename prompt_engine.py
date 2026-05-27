"""
prompt_engine.py
-----------------
The mock prompt engine. Generates drawing prompts from
curated seed data using template composition.

This is a mock prompt engine. I'm planning to replace it with a fine-tuned model.
But who knows if I'll ever get around to it.
"""

import random
from typing import Literal

# ── Types ──────────────────────────────────────────────────────────────

Category = Literal["character", "historical", "fictional", "environment", "any"]
Difficulty = Literal["warmup", "study", "challenge"]
Mood = Literal["dramatic", "peaceful", "mysterious", "playful", "melancholic", "any"]

# ── Seed data ──────────────────────────────────────────────────────────
# Mirrors src/lib/data/prompts.ts — single source of truth is the
# backend. Frontend data file is for type safety only.

CHARACTER_SEEDS = [
    {
        "subject": "a weary bounty hunter",
        "modifiers": [
            "scarred face",
            "mismatched armor",
            "haunted eyes",
            "desert setting",
        ],
    },
    {
        "subject": "a young street alchemist",
        "modifiers": [
            "glowing vials",
            "patched coat",
            "rooftop at dusk",
            "curious expression",
        ],
    },
    {
        "subject": "an elderly sea captain",
        "modifiers": ["storm-worn", "one glass eye", "compass tattoo", "fog setting"],
    },
    {
        "subject": "a masked court jester",
        "modifiers": [
            "bells hidden under rags",
            "sharp eyes",
            "torchlit hall",
            "secret agenda",
        ],
    },
    {
        "subject": "a blind swordmaster",
        "modifiers": [
            "serene expression",
            "rain soaked",
            "listening stance",
            "mountain pass",
        ],
    },
    {
        "subject": "a child inventor",
        "modifiers": [
            "goggles too big",
            "oil stained hands",
            "cluttered workshop",
            "proud smile",
        ],
    },
    {
        "subject": "a reformed assassin",
        "modifiers": [
            "flower market setting",
            "disguised",
            "tense posture",
            "civilian clothes",
        ],
    },
    {
        "subject": "a plague doctor",
        "modifiers": ["bird mask", "candlelit alley", "bag of herbs", "medieval city"],
    },
    {
        "subject": "a nomadic astronomer",
        "modifiers": [
            "star charts",
            "desert night",
            "ancient telescope",
            "weathered hands",
        ],
    },
    {
        "subject": "a disgraced knight",
        "modifiers": ["broken oath", "rusted armor", "kneeling", "rainy battlefield"],
    },
    {
        "subject": "a merchant of rare memories",
        "modifiers": [
            "glass jars of light",
            "market stall",
            "knowing smile",
            "twilight",
        ],
    },
    {
        "subject": "a cartographer of impossible places",
        "modifiers": [
            "ink-stained fingers",
            "floating maps",
            "library setting",
            "obsessed expression",
        ],
    },
]

HISTORICAL_SEEDS = [
    {
        "subject": "Mahatma Gandhi",
        "modifiers": [
            "spinning wheel",
            "simple dhoti",
            "peaceful determination",
            "warm light",
        ],
    },
    {
        "subject": "Abraham Lincoln",
        "modifiers": [
            "tall hat",
            "weathered face",
            "candlelit study",
            "deep in thought",
        ],
    },
    {
        "subject": "Frida Kahlo",
        "modifiers": [
            "floral crown",
            "bold gaze",
            "colorful backdrop",
            "self-possessed",
        ],
    },
    {
        "subject": "Leonardo da Vinci",
        "modifiers": [
            "workshop full of inventions",
            "chalk in hand",
            "curious gaze",
            "Renaissance setting",
        ],
    },
    {
        "subject": "Cleopatra",
        "modifiers": [
            "throne room",
            "commanding presence",
            "Nile at sunset",
            "elaborate headdress",
        ],
    },
    {
        "subject": "Nikola Tesla",
        "modifiers": [
            "electrical arcs",
            "late night laboratory",
            "intense focus",
            "coil machines",
        ],
    },
    {
        "subject": "Marie Curie",
        "modifiers": [
            "glowing radium samples",
            "laboratory coat",
            "exhausted but determined",
            "Paris setting",
        ],
    },
    {
        "subject": "Genghis Khan",
        "modifiers": [
            "steppe horizon",
            "battle standard",
            "calculating gaze",
            "on horseback",
        ],
    },
    {
        "subject": "Ada Lovelace",
        "modifiers": [
            "engine diagrams",
            "Victorian study",
            "mathematical notes",
            "evening light",
        ],
    },
    {
        "subject": "Sun Tzu",
        "modifiers": [
            "bamboo forest",
            "scroll in hand",
            "strategic calm",
            "ancient China",
        ],
    },
    {
        "subject": "Harriet Tubman",
        "modifiers": [
            "night setting",
            "North Star visible",
            "determined stride",
            "forest path",
        ],
    },
    {
        "subject": "Vincent van Gogh",
        "modifiers": [
            "paint-covered hands",
            "Arles countryside",
            "swirling sky",
            "wild eyes",
        ],
    },
    {
        "subject": "Simón Bolívar",
        "modifiers": [
            "Andes mountain pass",
            "military uniform",
            "rallying troops",
            "dramatic sky",
        ],
    },
    {
        "subject": "Hypatia of Alexandria",
        "modifiers": [
            "ancient library",
            "geometric diagrams",
            "teaching pose",
            "sunset light",
        ],
    },
]

FICTIONAL_SEEDS = [
    {
        "subject": "Sherlock Holmes",
        "modifiers": [
            "Baker Street fog",
            "pipe and magnifying glass",
            "deductive gaze",
            "Victorian London",
        ],
    },
    {
        "subject": "Elizabeth Bennet",
        "modifiers": [
            "Pemberley gardens",
            "wit in her expression",
            "period dress",
            "book in hand",
        ],
    },
    {
        "subject": "Gandalf",
        "modifiers": [
            "Moria bridge",
            "staff raised",
            "dramatic lighting",
            "ancient power",
        ],
    },
    {
        "subject": "Dracula",
        "modifiers": [
            "castle battlements",
            "moonlit",
            "commanding presence",
            "shadows swirling",
        ],
    },
    {
        "subject": "Hamlet",
        "modifiers": [
            "castle at Elsinore",
            "skull in hand",
            "tormented",
            "night setting",
        ],
    },
    {
        "subject": "Don Quixote",
        "modifiers": [
            "windmill battle",
            "dented armor",
            "Rocinante rearing",
            "golden plains",
        ],
    },
    {
        "subject": "Medusa",
        "modifiers": [
            "snake hair",
            "ancient Greek setting",
            "powerful stance",
            "stone victims around",
        ],
    },
    {
        "subject": "Captain Ahab",
        "modifiers": [
            "ship deck in storm",
            "harpoon raised",
            "obsession in his eyes",
            "whale on horizon",
        ],
    },
    {
        "subject": "Lady Macbeth",
        "modifiers": [
            "candlelit chamber",
            "sleepwalking",
            "guilt expression",
            "castle setting",
        ],
    },
    {
        "subject": "Quasimodo",
        "modifiers": [
            "Notre Dame rooftop",
            "looking over Paris",
            "longing expression",
            "bell behind him",
        ],
    },
    {
        "subject": "Cyrano de Bergerac",
        "modifiers": [
            "dueling pose",
            "moonlit balcony",
            "theatrical flair",
            "17th century Paris",
        ],
    },
    {
        "subject": "The Count of Monte Cristo",
        "modifiers": [
            "Chateau d'If cliff",
            "cape in wind",
            "revenge and sorrow",
            "sea at night",
        ],
    },
    {
        "subject": "Robinson Crusoe",
        "modifiers": [
            "tropical beach",
            "makeshift tools",
            "scanning the horizon",
            "weathered survival",
        ],
    },
    {
        "subject": "Jekyll and Hyde",
        "modifiers": [
            "transformation moment",
            "mirror reflection",
            "Victorian laboratory",
            "dual nature",
        ],
    },
]

ENVIRONMENT_SEEDS = [
    {
        "subject": "a sunken cathedral",
        "modifiers": [
            "light through stained glass",
            "fish swimming through nave",
            "silent and eerie",
        ],
    },
    {
        "subject": "a market on a moving glacier",
        "modifiers": [
            "traders in thick furs",
            "ice fog",
            "lanterns swaying",
            "crevasse nearby",
        ],
    },
    {
        "subject": "a forest where the trees grow downward",
        "modifiers": [
            "roots in the sky",
            "canopy below",
            "disorienting light",
            "strange birds",
        ],
    },
    {
        "subject": "an abandoned space elevator",
        "modifiers": [
            "vines reclaiming steel",
            "cloud level view",
            "silent machinery",
            "golden hour",
        ],
    },
    {
        "subject": "a desert of broken hourglasses",
        "modifiers": [
            "sand spilling everywhere",
            "time motif",
            "sunset palette",
            "lone wanderer",
        ],
    },
    {
        "subject": "a city built inside a storm cloud",
        "modifiers": [
            "lightning as streets",
            "floating platforms",
            "rain upward",
            "electric atmosphere",
        ],
    },
    {
        "subject": "a lighthouse at the edge of a flat world",
        "modifiers": [
            "abyss beyond",
            "keeper watching",
            "stars close enough to touch",
            "wind-worn",
        ],
    },
    {
        "subject": "an underground river market",
        "modifiers": [
            "bioluminescent flora",
            "cave ceiling",
            "boats laden with goods",
            "echoing sounds",
        ],
    },
    {
        "subject": "ruins of a giant mechanical creature",
        "modifiers": [
            "people living inside its ribs",
            "steam still escaping",
            "jungle reclaiming it",
        ],
    },
    {
        "subject": "a library that rearranges itself at night",
        "modifiers": [
            "books mid-flight",
            "moonlight through dome",
            "lone reader",
            "dust and shadows",
        ],
    },
    {
        "subject": "a port town on the back of a sea turtle",
        "modifiers": [
            "curved horizon",
            "anchor chains into the ocean",
            "normal life on impossible ground",
        ],
    },
    {
        "subject": "a graveyard where the headstones are doors",
        "modifiers": [
            "light under some doors",
            "fog",
            "caretaker with keys",
            "twilight",
        ],
    },
]

ALL_SEEDS = CHARACTER_SEEDS + HISTORICAL_SEEDS + FICTIONAL_SEEDS + ENVIRONMENT_SEEDS

# ── Difficulty descriptors ─────────────────────────────────────────────

DIFFICULTY_DESCRIPTORS = {
    "warmup": [
        "Focus on basic shapes and silhouette only.",
        "Quick gesture — capture the energy, not the detail.",
        "Thumbnail only — no larger than a playing card.",
        "Loose lines welcome. Speed over accuracy.",
    ],
    "study": [
        "Include light and shadow.",
        "Pay attention to proportions.",
        "Add at least one detailed element.",
        "Consider the background even if you leave it minimal.",
    ],
    "challenge": [
        "Full composition with foreground, midground, and background.",
        "Include at least three light sources.",
        "Render textures: fabric, skin, metal, or stone.",
        "Tell a story — the viewer should wonder what happens next.",
    ],
}

# ── Mood descriptors ───────────────────────────────────────────────────

MOOD_DESCRIPTORS = {
    "dramatic": [
        "High contrast lighting.",
        "Strong diagonals in the composition.",
        "Tension in the pose or scene.",
    ],
    "peaceful": [
        "Soft diffused light.",
        "Open space in the composition.",
        "A sense of stillness.",
    ],
    "mysterious": [
        "Deep shadows with hidden details.",
        "An unanswered question in the image.",
        "Fog, smoke, or obscured elements.",
    ],
    "playful": [
        "Unexpected scale relationships.",
        "Bright accents against the moodier palette.",
        "A hint of movement or action.",
    ],
    "melancholic": [
        "Fading light — dusk or dawn.",
        "Isolation or distance between subjects.",
        "Something left behind or abandoned.",
    ],
}

# ── Main generate function ─────────────────────────────────────────────


def generate(
    category: Category = "any",
    difficulty: Difficulty = "study",
    mood: Mood = "any",
) -> dict:
    """
    Generate a drawing prompt.

    This is the function to replace when the fine-tuned model is ready.
    Keep the signature and return shape identical — the API route
    and frontend will work without any other changes.
    """

    # Pick seed pool based on category
    pool = {
        "character": CHARACTER_SEEDS,
        "historical": HISTORICAL_SEEDS,
        "fictional": FICTIONAL_SEEDS,
        "environment": ENVIRONMENT_SEEDS,
        "any": ALL_SEEDS,
    }.get(category, ALL_SEEDS)

    seed = random.choice(pool)

    # Pick 2 random modifiers from the seed
    modifiers = random.sample(seed["modifiers"], min(2, len(seed["modifiers"])))

    # Pick difficulty instruction
    difficulty_note = random.choice(DIFFICULTY_DESCRIPTORS[difficulty])

    # Pick mood instruction
    if mood == "any":
        mood_key = random.choice(list(MOOD_DESCRIPTORS.keys()))
        mood_note = random.choice(MOOD_DESCRIPTORS[mood_key])
    else:
        mood_note = random.choice(MOOD_DESCRIPTORS[mood])

    # Compose the prompt
    subject_line = seed["subject"]
    detail_line = " ".join(modifiers).capitalize() + "."

    prompt_text = f"{subject_line}. {detail_line} {mood_note} {difficulty_note}"

    # Derive category from the pool we picked from
    derived_category = (
        category
        if category != "any"
        else {
            id(CHARACTER_SEEDS): "character",
            id(HISTORICAL_SEEDS): "historical",
            id(FICTIONAL_SEEDS): "fictional",
            id(ENVIRONMENT_SEEDS): "environment",
        }.get(id(pool), "any")
    )

    return {
        "prompt": prompt_text,
        "subject": seed["subject"],
        "category": derived_category,
        "modifiers": modifiers,
        "difficulty": difficulty,
        "mood": mood if mood != "any" else mood_key,
    }
