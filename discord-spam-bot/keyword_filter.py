SPAM_KEYWORDS = [
    "free nitro",
    "discord.gg/",
    "crypto giveaway",
    "click this link",
    "earn money fast",
    "free crypto",
]

def is_suspicious(message: str) -> bool:
    message = message.lower()

    for keyword in SPAM_KEYWORDS:
        if keyword in message:
            return True

    return False