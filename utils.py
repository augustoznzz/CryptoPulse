"""
Utility Functions
Helper functions for formatting and calculations
"""

import math

def format_price(price, min_decimals=2, max_decimals=8):
    """
    Format price with appropriate number of decimal places
    
    Args:
        price (float): Price to format
        min_decimals (int): Minimum decimal places
        max_decimals (int): Maximum decimal places
        
    Returns:
        str: Formatted price string
    """
    if price is None:
        return "0.00"
    
    # Determine appropriate decimal places based on price magnitude
    if price >= 1000:
        decimals = 2
    elif price >= 100:
        decimals = 3
    elif price >= 10:
        decimals = 4
    elif price >= 1:
        decimals = 5
    elif price >= 0.1:
        decimals = 6
    elif price >= 0.01:
        decimals = 7
    else:
        decimals = max_decimals
    
    # Ensure minimum decimals
    decimals = max(decimals, min_decimals)
    
    # Format the price
    formatted = f"{price:.{decimals}f}"
    
    # Remove trailing zeros, but keep at least min_decimals
    if '.' in formatted:
        formatted = formatted.rstrip('0')
        # Ensure we have at least min_decimals
        current_decimals = len(formatted.split('.')[1]) if '.' in formatted else 0
        if current_decimals < min_decimals:
            formatted = f"{price:.{min_decimals}f}"
    
    return formatted

def calculate_fibonacci_targets(entry_price, direction, base_distance):
    """
    Calculate Fibonacci-based take profit targets
    
    Args:
        entry_price (float): Entry price
        direction (str): 'LONG' or 'SHORT'
        base_distance (float): Base distance for calculations
        
    Returns:
        dict: Fibonacci target levels
    """
    fib_ratios = [0.618, 1.0, 1.618, 2.618]
    targets = {}
    
    for i, ratio in enumerate(fib_ratios, 1):
        if direction == 'LONG':
            target = entry_price + (base_distance * ratio)
        else:  # SHORT
            target = entry_price - (base_distance * ratio)
        targets[f'tp{i}'] = target
    
    return targets

def calculate_percentage_change(old_value, new_value):
    """
    Calculate percentage change between two values
    
    Args:
        old_value (float): Original value
        new_value (float): New value
        
    Returns:
        float: Percentage change
    """
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100

def calculate_risk_reward_ratio(entry, take_profit, stop_loss):
    """
    Calculate risk-reward ratio for a trade
    
    Args:
        entry (float): Entry price
        take_profit (float): Take profit price
        stop_loss (float): Stop loss price
        
    Returns:
        float: Risk-reward ratio
    """
    risk = abs(entry - stop_loss)
    reward = abs(take_profit - entry)
    
    if risk == 0:
        return float('inf')
    
    return reward / risk

def validate_price_levels(entry, targets, stops, direction):
    """
    Validate that price levels are logically ordered
    
    Args:
        entry (float): Entry price
        targets (list): List of take profit targets
        stops (list): List of stop loss levels
        direction (str): 'LONG' or 'SHORT'
        
    Returns:
        bool: True if levels are valid
    """
    if direction == 'LONG':
        # For long positions: targets should be above entry, stops below
        targets_valid = all(target > entry for target in targets)
        stops_valid = all(stop < entry for stop in stops)
    else:  # SHORT
        # For short positions: targets should be below entry, stops above
        targets_valid = all(target < entry for target in targets)
        stops_valid = all(stop > entry for stop in stops)
    
    # Targets should be in ascending order (for LONG) or descending (for SHORT)
    if direction == 'LONG':
        targets_ordered = all(targets[i] <= targets[i+1] for i in range(len(targets)-1))
    else:
        targets_ordered = all(targets[i] >= targets[i+1] for i in range(len(targets)-1))
    
    return targets_valid and stops_valid and targets_ordered

def safe_divide(numerator, denominator, default=0):
    """
    Safely divide two numbers, returning default if denominator is zero
    
    Args:
        numerator (float): Numerator
        denominator (float): Denominator
        default (float): Default value if division by zero
        
    Returns:
        float: Division result or default
    """
    if denominator == 0:
        return default
    return numerator / denominator

def round_to_significant_figures(number, sig_figs=5):
    """
    Round a number to specified significant figures
    
    Args:
        number (float): Number to round
        sig_figs (int): Number of significant figures
        
    Returns:
        float: Rounded number
    """
    if number == 0:
        return 0
    
    return round(number, -int(math.floor(math.log10(abs(number)))) + (sig_figs - 1))
