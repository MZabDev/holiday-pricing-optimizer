from anthropic import Anthropic
import os
import json

def get_ai_pricing_insights(property_details, stats, base_recommendation):
    """
    Use Claude to analyze pricing data and provide intelligent recommendations
    """
    
    # Get API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return None
    
    # Build the prompt for Claude
    prompt = f"""You are a revenue management expert for holiday rental properties.

PROPERTY DETAILS:
- Location: {property_details['location']}
- Type: {property_details['property_type']}
- Bedrooms: {property_details['bedrooms']}
- Parking: {'Yes' if property_details['has_parking'] else 'No'}
- WiFi: {'Yes' if property_details['has_wifi'] else 'No'}
- Pet Friendly: {'Yes' if property_details['pet_friendly'] else 'No'}

MARKET DATA:
- Exact competitor matches found: {stats['exact_count']}
- Similar properties found: {stats['similar_count']}
{f"- Average price (exact matches): £{stats['exact_avg']:.2f}" if stats['exact_avg'] else ""}
{f"- Price range (exact matches): £{stats['exact_min']:.2f} - £{stats['exact_max']:.2f}" if stats['exact_avg'] else ""}
{f"- Average price (similar): £{stats['similar_avg']:.2f}" if stats['similar_avg'] and not stats['exact_avg'] else ""}

BASELINE RECOMMENDATION:
- Suggested price: £{base_recommendation['price']:.2f}
- Confidence: {base_recommendation['confidence']}

Please provide:
1. A refined pricing recommendation (suggest a specific nightly rate)
2. Strategic reasoning (why this price makes sense)
3. Competitive positioning (budget/mid-range/premium and why)
4. 2-3 actionable tips to maximize revenue

Respond in JSON format with these exact keys:
{{
    "recommended_price": <number>,
    "positioning": "<budget|mid-range|premium>",
    "reasoning": "<2-3 sentences explaining the recommendation>",
    "tips": ["<tip 1>", "<tip 2>", "<tip 3>"]
}}

Only return the JSON, no other text."""

    try:
        # Call Claude API
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Parse the response
        response_text = message.content[0].text
        
        # Clean up response (remove markdown code blocks if present)
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]  # Remove ```json
        if response_text.startswith('```'):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith('```'):
            response_text = response_text[:-3]  # Remove ```
        response_text = response_text.strip()
        
        # Parse JSON
        ai_insights = json.loads(response_text)
        
        return ai_insights
        
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return None
