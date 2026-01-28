import pandas as pd

def get_competitor_data(location, property_type, bedrooms):
    """
    Filter competitor data based on property characteristics
    """
    # Load the data
    df = pd.read_csv('data/competitors.csv')
    
    # Filter for exact matches
    exact_matches = df[
        (df['location'] == location) &
        (df['property_type'] == property_type) &
        (df['bedrooms'] == bedrooms)
    ]
    
    # Also get similar properties (same location and bedrooms, different type)
    similar = df[
        (df['location'] == location) &
        (df['bedrooms'] == bedrooms)
    ]
    
    return exact_matches, similar

def calculate_price_stats(exact_matches, similar):
    """
    Calculate pricing statistics from competitor data
    """
    stats = {}
    
    if len(exact_matches) > 0:
        stats['exact_avg'] = exact_matches['nightly_rate'].mean()
        stats['exact_min'] = exact_matches['nightly_rate'].min()
        stats['exact_max'] = exact_matches['nightly_rate'].max()
        stats['exact_count'] = len(exact_matches)
    else:
        stats['exact_avg'] = None
        stats['exact_count'] = 0
    
    if len(similar) > 0:
        stats['similar_avg'] = similar['nightly_rate'].mean()
        stats['similar_min'] = similar['nightly_rate'].min()
        stats['similar_max'] = similar['nightly_rate'].max()
        stats['similar_count'] = len(similar)
    else:
        stats['similar_avg'] = None
        stats['similar_count'] = 0
    
    return stats

def generate_base_recommendation(stats):
    """
    Generate a basic pricing recommendation from stats
    """
    if stats['exact_count'] > 0:
        # We have exact matches - use their average as baseline
        recommended_price = stats['exact_avg']
        confidence = "High"
        reasoning = f"Based on {stats['exact_count']} similar properties"
    elif stats['similar_count'] > 0:
        # No exact matches, use similar properties
        recommended_price = stats['similar_avg']
        confidence = "Medium"
        reasoning = f"Based on {stats['similar_count']} properties in same area"
    else:
        # No data at all
        recommended_price = None
        confidence = "Low"
        reasoning = "Insufficient competitor data"
    
    return {
        'price': recommended_price,
        'confidence': confidence,
        'reasoning': reasoning
    }
def prepare_chart_data(exact_matches, similar, recommended_price, property_details):
    """
    Prepare data for price comparison visualization
    """
    import pandas as pd
    
    chart_data = []
    
    # Use exact matches if available, otherwise similar
    competitors = exact_matches if len(exact_matches) > 0 else similar
    
    if len(competitors) > 0:
        # Add competitor data (limit to top 10 for clarity)
        for idx, row in competitors.head(10).iterrows():
            chart_data.append({
                'Property': f"{row['property_type']} ({row['bedrooms']}BR)",
                'Price': row['nightly_rate'],
                'Type': 'Competitor',
                'Details': f"{row['location']}"
            })
        
        # Add your property
        chart_data.append({
            'Property': f"YOUR {property_details['property_type']} ({property_details['bedrooms']}BR)",
            'Price': recommended_price,
            'Type': 'Your Property',
            'Details': property_details['location']
        })
    
    return pd.DataFrame(chart_data)
