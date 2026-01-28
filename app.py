import streamlit as st
import pandas as pd
from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Load our secret API key
load_dotenv()

# Set up the page
st.set_page_config(page_title="Holiday Pricing Optimizer", page_icon="🏠")

st.title("🏠 Holiday Let Pricing Optimizer")
st.write("**AI-powered dynamic pricing for short-term rentals**")
st.write("---")

# Test 1: Can we load the data?
st.subheader("📊 Test 1: Load Competitor Data")
try:
    df = pd.read_csv('data/competitors.csv')
    st.success(f"✅ Successfully loaded {len(df)} competitor properties!")
    
    with st.expander("👀 Click to see the data"):
        st.dataframe(df.head(20))
        
        # Show some quick stats
        st.write("**Quick Statistics:**")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Properties", len(df))
        col2.metric("Avg Price", f"£{df['nightly_rate'].mean():.2f}")
        col3.metric("Locations", df['location'].nunique())
        
except FileNotFoundError:
    st.error("⚠️ Data file not found! Did you run create_sample_data.py?")

# Test 2: Can we talk to Claude?
st.write("---")
st.subheader("🤖 Test 2: Claude AI Connection")

if st.button("Test Claude API Connection"):
    try:
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            st.error("❌ No API key found! Check your .env file")
        else:
            with st.spinner("Connecting to Claude..."):
                client = Anthropic(api_key=api_key)
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=100,
                    messages=[
                        {"role": "user", "content": "Say 'API connection successful! I'm ready to help with pricing analysis.' if you can read this."}
                    ]
                )
                st.success(message.content[0].text)
                st.balloons()
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")

# What's next?
st.write("---")
st.info("🎉 If both tests passed, you're ready to build the pricing features!")

# ============================================
# PRICING ANALYSIS FEATURE
# ============================================

st.write("---")
st.header("💰 Get Pricing Recommendation")

# Create two columns for the form
col1, col2 = st.columns(2)

with col1:
    st.subheader("Property Details")
    
    # Location dropdown
    location = st.selectbox(
        "📍 Location",
        options=["London", "Edinburgh", "Cornwall"],
        help="Select where your property is located"
    )
    
    # Property type dropdown
    property_type = st.selectbox(
        "🏠 Property Type",
        options=["Flat", "House", "Cottage"],
        help="What type of property is it?"
    )
    
    # Bedrooms
    bedrooms = st.selectbox(
        "🛏️ Number of Bedrooms",
        options=[1, 2, 3],
        help="How many bedrooms?"
    )

with col2:
    st.subheader("Amenities")
    
    # Amenities checkboxes
    has_parking = st.checkbox("🚗 Parking available", value=False)
    has_wifi = st.checkbox("📶 WiFi included", value=True)
    pet_friendly = st.checkbox("🐕 Pet friendly", value=False)
    
    st.write("")  # Spacing
    st.write("")
    
    # Analyze button
    analyze_button = st.button("🔍 Analyze Pricing", type="primary", use_container_width=True)

# Show results when button is clicked
if analyze_button:
    st.write("---")
    st.subheader("📊 Analysis Results")
    
    # Import our pricing engine
    from src.pricing_engine import get_competitor_data, calculate_price_stats, generate_base_recommendation
    
    with st.spinner("Analyzing competitor data..."):
        # Get competitor data
        exact_matches, similar = get_competitor_data(location, property_type, bedrooms)
        
        # Calculate stats
        stats = calculate_price_stats(exact_matches, similar)
        
        # Generate recommendation
        recommendation = generate_base_recommendation(stats)
    
    # Display the recommendation
    if recommendation['price']:
        
        # Create tabs for basic vs AI analysis
        tab1, tab2 = st.tabs(["📊 Basic Analysis", "🤖 AI-Powered Insights"])
        
        with tab1:
            # Show the basic recommendation
            col1, col2, col3 = st.columns(3)
            
            col1.metric(
                "💷 Base Price",
                f"£{recommendation['price']:.2f}",
                help="Basic average of competitor prices"
            )
            
            col2.metric(
                "📈 Confidence",
                recommendation['confidence'],
                help="How confident we are in this recommendation"
            )
            
            col3.metric(
                "🏘️ Competitors Found",
                stats['exact_count'] if stats['exact_count'] > 0 else stats['similar_count'],
                help="Number of similar properties analyzed"
            )
            
            # Show reasoning
            st.info(f"**Reasoning:** {recommendation['reasoning']}")
            
            # Add price comparison chart
            st.write("### 📊 Price Comparison")
            
            from src.pricing_engine import prepare_chart_data
            import plotly.express as px
            
            chart_df = prepare_chart_data(
                exact_matches, 
                similar, 
                recommendation['price'],
                {
                    'property_type': property_type,
                    'bedrooms': bedrooms,
                    'location': location
                }
            )
            
            if len(chart_df) > 0:
                # Create color mapping
                colors = ['#FF6B6B' if t == 'Your Property' else '#4ECDC4' 
                         for t in chart_df['Type']]
                
                fig = px.bar(
                    chart_df,
                    x='Property',
                    y='Price',
                    color='Type',
                    color_discrete_map={
                        'Your Property': '#FF6B6B',
                        'Competitor': '#4ECDC4'
                    },
                    title='Your Price vs. Competitors',
                    labels={'Price': 'Nightly Rate (£)'},
                    hover_data=['Details']
                )
                
                fig.update_layout(
                    xaxis_title="",
                    yaxis_title="Nightly Rate (£)",
                    showlegend=True,
                    height=400,
                    hovermode='x unified'
                )
                
                # Rotate x-axis labels for readability
                fig.update_xaxes(tickangle=-45)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Add insight below chart
                avg_competitor = chart_df[chart_df['Type'] == 'Competitor']['Price'].mean()
                difference = recommendation['price'] - avg_competitor
                
                if difference > 0:
                    st.success(f"💡 Your price is £{difference:.2f} **above** the average competitor price - positioning for premium market.")
                elif difference < 0:
                    st.info(f"💡 Your price is £{abs(difference):.2f} **below** the average competitor price - competitive positioning.")
                else:
                    st.info(f"💡 Your price matches the average competitor price - middle market positioning.")
            
            # Show competitor details
            if stats['exact_count'] > 0:
                st.write("**Exact matches found:**")
                st.dataframe(exact_matches[['location', 'property_type', 'bedrooms', 'nightly_rate']])
                
                # Show price range
                st.write(f"**Price range:** £{stats['exact_min']:.2f} - £{stats['exact_max']:.2f}")
            
            elif stats['similar_count'] > 0:
                st.write("**Similar properties found:**")
                st.dataframe(similar[['location', 'property_type', 'bedrooms', 'nightly_rate']].head(10))
                
                st.write(f"**Price range:** £{stats['similar_min']:.2f} - £{stats['similar_max']:.2f}")
        
        with tab2:
            # Get AI insights
            from src.llm_analyzer import get_ai_pricing_insights
            
            with st.spinner("🤖 Claude is analyzing your property..."):
                property_details = {
                    'location': location,
                    'property_type': property_type,
                    'bedrooms': bedrooms,
                    'has_parking': has_parking,
                    'has_wifi': has_wifi,
                    'pet_friendly': pet_friendly
                }
                
                ai_insights = get_ai_pricing_insights(property_details, stats, recommendation)
            
            if ai_insights:
                # Display AI recommendation
                st.success("✨ AI Analysis Complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "🎯 AI Recommended Price",
                        f"£{ai_insights['recommended_price']:.2f}",
                        delta=f"£{ai_insights['recommended_price'] - recommendation['price']:.2f} vs basic",
                        help="Claude's intelligent pricing recommendation"
                    )
                
                with col2:
                    # Positioning with color
                    positioning_colors = {
                        'budget': '🟢',
                        'mid-range': '🟡',
                        'premium': '🔵'
                    }
                    positioning_emoji = positioning_colors.get(ai_insights['positioning'].lower(), '⚪')
                    
                    st.metric(
                        "📍 Market Positioning",
                        f"{positioning_emoji} {ai_insights['positioning'].title()}",
                        help="Where your property sits in the market"
                    )
                
                # Add price comparison chart for AI recommendation
                st.write("### 📊 AI-Enhanced Price Positioning")
                
                from src.pricing_engine import prepare_chart_data
                import plotly.express as px
                
                chart_df = prepare_chart_data(
                    exact_matches, 
                    similar, 
                    ai_insights['recommended_price'],
                    {
                        'property_type': property_type,
                        'bedrooms': bedrooms,
                        'location': location
                    }
                )
                
                if len(chart_df) > 0:
                    fig = px.bar(
                        chart_df,
                        x='Property',
                        y='Price',
                        color='Type',
                        color_discrete_map={
                            'Your Property': '#9D4EDD',
                            'Competitor': '#4ECDC4'
                        },
                        title='AI-Recommended Price vs. Market',
                        labels={'Price': 'Nightly Rate (£)'},
                        hover_data=['Details']
                    )
                    
                    fig.update_layout(
                        xaxis_title="",
                        yaxis_title="Nightly Rate (£)",
                        showlegend=True,
                        height=400
                    )
                    
                    fig.update_xaxes(tickangle=-45)
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Show reasoning
                st.write("### 💡 Strategic Reasoning")
                st.write(ai_insights['reasoning'])
                
                # Show tips
                st.write("### 🚀 Revenue Optimization Tips")
                for i, tip in enumerate(ai_insights['tips'], 1):
                    st.write(f"{i}. {tip}")
                
                # Show data comparison
                with st.expander("📊 See detailed comparison"):
                    comparison_data = {
                        'Method': ['Basic Average', 'AI Recommendation'],
                        'Price': [f"£{recommendation['price']:.2f}", f"£{ai_insights['recommended_price']:.2f}"],
                        'Confidence': [recommendation['confidence'], 'AI-Enhanced']
                    }
                    st.table(comparison_data)
            
            else:
                st.error("❌ Could not get AI insights. Please check your API key and credits.")
                st.info("💡 You can still use the Basic Analysis in the first tab!")
    
    else:
        st.error("❌ Not enough competitor data to generate a recommendation")
