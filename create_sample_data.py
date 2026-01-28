import pandas as pd
import numpy as np

# Set random seed for consistent results
np.random.seed(42)

locations = ['London', 'Edinburgh', 'Cornwall']
property_types = ['Flat', 'House', 'Cottage']
data = []

for location in locations:
    # Different base prices for different locations
    base_price = {'London': 150, 'Edinburgh': 100, 'Cornwall': 120}[location]
    
    for prop_type in property_types:
        for bedrooms in [1, 2, 3]:
            # Create 5 properties for each combination
            for i in range(5):
                # Adjust price based on property type
                type_multiplier = {'Flat': 0.9, 'House': 1.1, 'Cottage': 1.0}[prop_type]
                bedroom_add = bedrooms * 30
                
                # Calculate price with some randomness
                nightly_rate = base_price * type_multiplier + bedroom_add + np.random.randint(-20, 20)
                
                data.append({
                    'location': location,
                    'property_type': prop_type,
                    'bedrooms': bedrooms,
                    'nightly_rate': round(nightly_rate, 2),
                    'has_parking': np.random.choice([True, False]),
                    'has_wifi': True,
                    'pet_friendly': np.random.choice([True, False])
                })

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('data/competitors.csv', index=False)

print("✅ Sample data created successfully!")
print(f"📊 Created {len(df)} competitor properties")
print("\nFirst few rows:")
print(df.head(10))
