# visualization.py
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd

def calculate_cdf(probabilities):
    """
    Calculate the cumulative distribution function from a probability dictionary.
    
    Args:
        probabilities (dict): Dictionary of {outcome: probability}
    
    Returns:
        tuple: (sorted outcomes, probabilities, cdf values)
    """
    # Sort by outcome
    sorted_probs = dict(sorted(probabilities.items()))
    outcomes = list(sorted_probs.keys())
    probs = list(sorted_probs.values())
    
    # Calculate CDF (probability of rolling >= X)
    cdf = []
    for i in range(len(outcomes)):
        # Sum all probabilities for outcomes >= current outcome
        cdf.append(sum(probs[i:]))
    
    return outcomes, probs, cdf

def apply_modifier(probabilities, modifier=0):
    """
    Apply a modifier to the outcomes in a probability dictionary.
    
    Args:
        probabilities (dict): Dictionary of {outcome: probability}
        modifier (int): Value to add to each outcome
        
    Returns:
        dict: Modified probability dictionary
    """
    if modifier == 0:
        return probabilities
    return {k + modifier: v for k, v in probabilities.items()}

def plot_dice_analysis(probabilities, title="Dice Roll Analysis", 
                      modifier=0, figsize=(12, 10)):
    """
    Create a clean visualization with both PMF and CDF, including modifier.
    
    Args:
        probabilities (dict): Dictionary of {outcome: probability}
        title (str): Chart title
        modifier (int): Flat modifier added to rolls
        figsize (tuple): Figure size
    
    Returns:
        tuple: (figure, sorted_probabilities, cdf_values)
    """
    # Apply modifier to outcomes
    probabilities = apply_modifier(probabilities, modifier)
    
    # Calculate probability distributions
    outcomes, probs, cdf = calculate_cdf(probabilities)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, gridspec_kw={'height_ratios': [1, 1]})
    
    # Plot 1: PMF (Bar chart)
    bars = ax1.bar(outcomes, probs, color='#3498db', alpha=0.8, width=0.8)
    
    # Add value labels more carefully - black text above bars
    max_prob = max(probs)
    for bar in bars:
        height = bar.get_height()
        # Only add text if the bar is tall enough
        if height > max_prob * 0.05:  # Skip very small values
            ax1.text(bar.get_x() + bar.get_width()/2., height + (max_prob * 0.02),
                    f'{height:.3f}', ha='center', va='bottom', 
                    color='black', fontsize=9)
    
    # Cleaner grid and styling
    ax1.grid(axis='y', linestyle='-', alpha=0.2)
    ax1.set_title(f"{title}", fontsize=14)
    ax1.set_ylabel("Probability", fontsize=12)
    ax1.set_xlabel("Roll Result", fontsize=12)
    
    # Ensure there's enough padding at the top
    ax1.set_ylim(0, max(probs) * 1.25)  # More padding for labels
    
    # Remove top and right spines
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Plot 2: CDF (Line chart)
    ax2.plot(outcomes, cdf, marker='o', linestyle='-', color='#2ecc71', 
            linewidth=3, markersize=6)
    
    # Cleaner grid and styling
    ax2.grid(True, linestyle='-', alpha=0.2)
    ax2.set_title("Probability of Rolling ≥ X", fontsize=14)
    ax2.set_xlabel("Difficulty Class", fontsize=12)
    ax2.set_ylabel("Probability", fontsize=12)
    ax2.set_ylim(0, 1.05)
    
    # Remove top and right spines
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    plt.tight_layout(pad=3.0)
    return fig, dict(zip(outcomes, probs)), cdf

def create_probability_table(outcomes, probs, cdf):
    """
    Create a DataFrame containing probability data.
    
    Args:
        outcomes (list): List of roll outcomes
        probs (list): List of probabilities
        cdf (list): List of cumulative probabilities
        
    Returns:
        pandas.DataFrame: Formatted probability table
    """
    data = {
        "Roll Result": outcomes,
        "Probability": [f"{p:.3f}" for p in probs],
        "Success Rate (≥)": [f"{c:.3f}" for c in cdf]
    }
    
    return pd.DataFrame(data)

def display_analysis(probabilities, title="Dice Roll Analysis", modifier=0):
    """
    Display improved dice analysis in Streamlit with probability table.
    
    Args:
        probabilities (dict): Dictionary of {outcome: probability}
        title (str): Chart title
        modifier (int): Flat modifier added to rolls
    """
    # Generate the visualization and get the data
    fig, sorted_probs, cdf_values = plot_dice_analysis(probabilities, title, modifier)
    
    # Display the chart
    st.pyplot(fig)
    
    # Create a DataFrame for the probability table
    outcomes = list(sorted_probs.keys())
    probs = list(sorted_probs.values())
    
    # Create and display the table
    df = create_probability_table(outcomes, probs, cdf_values)
    st.subheader("Probability Table")
    table_height = min(len(df) * 35 + 38, 500)
    st.dataframe(df, hide_index=True, height=table_height)