import streamlit as st
from dice_probability.visualization import display_analysis
# Import your existing dice probability code
from dice_probability.core  import d20, d4, d6, d8, Adv, disAdv, many_dice, die_probs
st.title("DC20 Dice Probability Calculator")

# Sidebar inputs
st.sidebar.header("Roll Configuration")

advantage = st.sidebar.number_input("Advantage", min_value=0, max_value=5, value=0)
disadvantage = st.sidebar.number_input("Disadvantage", min_value=0, max_value=5, value=0)

# Add modifier input with its own category
st.sidebar.header("Modifiers")
modifier = st.sidebar.number_input("Flat Modifier", min_value=-10, max_value=20, value=0)

# Help dice selection
st.sidebar.header("Help Dice")
help_d8 = st.sidebar.number_input("d8", min_value=0, max_value=3, value=0)
help_d6 = st.sidebar.number_input("d6", min_value=0, max_value=3, value=0)
help_d4 = st.sidebar.number_input("d4", min_value=0, max_value=3, value=0)


# Calculate roll probabilities using your existing functions
# Base roll with advantage/disadvantage
if advantage > 0 and disadvantage == 0:
    base_roll = Adv(d20, n=advantage+1)
elif disadvantage > 0 and advantage == 0:
    base_roll = disAdv(d20, n=disadvantage+1)
elif advantage > disadvantage:
    base_roll = Adv(d20, n=(advantage-disadvantage)+1)
elif disadvantage > advantage:
    base_roll = disAdv(d20, n=(disadvantage-advantage)+1)
else:
    base_roll = d20.copy()

# Add help dice
dice_to_roll = [base_roll]
if help_d8 > 0:
    dice_to_roll.extend([d8] * help_d8)
if help_d6 > 0:
    dice_to_roll.extend([d6] * help_d6)
if help_d4 > 0:
    dice_to_roll.extend([d4] * help_d4)

# Calculate combined probabilities
if len(dice_to_roll) > 1:
    roll_result = many_dice(*dice_to_roll)
    probabilities = die_probs(roll_result[0])
else:
    probabilities = die_probs(base_roll)

# Create a description of the roll
roll_description = "d20"
if advantage > 0 and disadvantage == 0:
    roll_description += f" with {advantage} advantage"
elif disadvantage > 0 and advantage == 0:
    roll_description += f" with {disadvantage} disadvantage"
elif advantage > disadvantage:
    roll_description += f" with {advantage-disadvantage} net advantage"
elif disadvantage > advantage:
    roll_description += f" with {disadvantage-advantage} net disadvantage"

help_dice_text = []
if help_d8 > 0:
    help_dice_text.append(f"{help_d8}d8")
if help_d6 > 0:
    help_dice_text.append(f"{help_d6}d6")
if help_d4 > 0:
    help_dice_text.append(f"{help_d4}d4")



if help_dice_text:
    roll_description += f" + {' + '.join(help_dice_text)}"

if modifier != 0:
    roll_description += f" {'+' if modifier > 0 else ''}{modifier}"

# Display the improved visualization with table
display_analysis(
    probabilities,
    title=f"DC20 Roll: {roll_description}",
    modifier=modifier
)