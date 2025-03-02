# dice_probability/__init__.py

from .core import (
    # Dice definitions
    create_die, d4, d6, d8, d10, d12, d20,
    
    # Core functions
    die_probs, many_dice, Adv, disAdv, check,
    
    # Damage calculation
    damage_per_outcome, attack_outcomes, average_atk_damage
)

__version__ = '0.1.0'