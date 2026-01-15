rate_choices = {
    1: "★☆☆☆☆",
    2: "★★☆☆☆",
    3: "★★★☆☆",
    4: "★★★★☆",
    5: "★★★★★",
}

# This converts the dictionary into the format Django expects:
# [(1, "★☆☆☆☆"), (2, "★★☆☆☆"), ...]
RATE_CHOICES = list(rate_choices.items())