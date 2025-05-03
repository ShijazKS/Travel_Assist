## CONTEXTUAL MAB ##
Arms	Each category (e.g., tourism, beach, natural, etc.)
Agent	Your RLAgent class
Context	The state (e.g., Kerala, Assam) — determines localized preferences
Reward	The score calculated from user actions (like, dislike, read more, etc.)
Policy	Upper Confidence Bound (UCB) used to pick categories
Learning	Scores are updated and stored after every session

## Perception ##
Observing the user's behavior — e.g., whether they liked, disliked, or clicked "Read More" on a place.

## Action ##
Recommending categories to the user (e.g., ["natural", "tourism", "beach"])
which returns an ordered list of categories to prioritize.

## Learning ##
Updating your preference/reward system based on user interactions (reinforcement).
...scores are aggregated and saved via save_scores(...).
Over time, this accumulates preferences at both global and state level.

## Reasoning ##
Making a strategic decision about which categories to recommend next.
UCB (Upper Confidence Bound) algorithm
This balances:
    Exploitation: categories with known high reward.
    Exploration: trying less-visited categories to discover better options.
