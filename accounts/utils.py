import random


# Creating a function to generate random usernames
def generate_anonymous_username():
    nouns = [
        "void", "echo", "haze", "glow", "mist", "dusk", "dawn", "bloom",
        "ivy", "moss", "velvet", "pixel", "static", "ghost", "drift",
        "frost", "ember", "ash", "luna", "nova", "orbit", "comet", "star",
        "moon", "cloud", "rain", "storm", "dream", "whisper", "chaos",
        "venom", "shadow", "night", "abyss", "phantom", "glitch", "signal",
        "wire", "byte", "syntax", "kernel", "code", "matrix", "skull",
        "fawn", "clover", "honey", "lavender", "petal", "garden", "meadow",
        "willow", "orchid", "cherry", "berry", "arcade", "vhs", "cassette",
        "neon", "chrome", "diesel", "turbo", "flare", "pulse", "wave",
        "tide", "reef", "marble", "crystal", "silk", "linen", "rune",
        "tarot", "shrine", "saint", "angel", "devil", "demon", "reaper",
        "raven", "crow", "wolf", "viper", "cobra", "panther", "cyber",
        "afterglow", "frostbite", "wildfire", "moonlight", "skyline",
        "sunset", "overdose", "dreamcore", "nightcore", "glitchcore",
        "arcadecore", "wildheart", "starlight"
    ]

    adjectives = [
        "lonely", "sleepy", "dreamy", "cosmic", "chaotic", "cursed",
        "hidden", "silent", "broken", "toxic", "sacred", "soft", "dark",
        "gloomy", "blurry", "faded", "endless", "electric", "neon",
        "digital", "retro", "vintage", "icy", "frozen", "burning",
        "crimson", "scarlet", "silver", "golden", "ghostly", "ethereal",
        "celestial", "lunar", "solar", "angelic", "demonic", "haunted",
        "hollow", "wild", "savage", "midnight", "pastel", "glossy",
        "glittery", "velvet", "coquette", "fairy", "surreal", "liminal",
        "glitchy", "static", "pixelated", "chrome", "cyber", "terminal",
        "vapor", "nostalgic", "aesthetic", "delulu", "lowkey", "feral",
        "unhinged", "iconic", "based", "sigma", "moody", "divine",
        "wicked", "eternal", "temporary", "parallel", "distant",
        "heavenly", "infernal", "radioactive", "goth", "grunge", "indie",
        "kawaii", "alt", "emo", "softcore", "hardcoded", "underrated",
        "overrated", "obsidian", "shiny", "dusty", "fragile", "muted",
        "vivid", "hazy", "stormy", "melancholic", "edgy", "serene",
        "chaosfilled", "starry", "frosted", "burnt"
    ]

    noun = random.choice(nouns)
    adjective = random.choice(adjectives)
    number = random.randint(100, 9999)

    return f"{adjective.capitalize()}_{noun.capitalize()}_{number}"