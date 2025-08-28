"""
Utility Functions - Simplified Version
Helper functions for basic formatting and calculations
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

def format_volume(volume):
    """
    Format volume with appropriate units (K, M, B, T)
    
    Args:
        volume (float): Volume value
        
    Returns:
        str: Formatted volume string
    """
    if volume >= 1e12:
        return f"${volume/1e12:.1f}T"
    elif volume >= 1e9:
        return f"${volume/1e9:.1f}B"
    elif volume >= 1e6:
        return f"${volume/1e6:.1f}M"
    elif volume >= 1e3:
        return f"${volume/1e3:.1f}K"
    else:
        return f"${volume:.0f}"

def format_market_cap(market_cap):
    """
    Format market cap with appropriate units
    
    Args:
        market_cap (float): Market cap value
        
    Returns:
        str: Formatted market cap string
    """
    if market_cap >= 1e12:
        return f"${market_cap/1e12:.1f}T"
    elif market_cap >= 1e9:
        return f"${market_cap/1e9:.1f}B"
    elif market_cap >= 1e6:
        return f"${market_cap/1e6:.1f}M"
    else:
        return f"${market_cap:.0f}"
