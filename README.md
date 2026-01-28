# 🏠 AI-Powered Holiday Let Pricing Optimiser

> Intelligent pricing recommendations for short-term rental properties using Claude AI

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)](https://streamlit.io/)
[![Claude](https://img.shields.io/badge/Claude-Sonnet%204-purple.svg)](https://www.anthropic.com/)

[🔗 Live Demo](#) | [📧 Contact](mailto:your.email@example.com)

---

## 📋 Overview

An AI-powered web application that analyses competitor data and provides strategic pricing recommendations for holiday rental properties. I built this to solve a real business problem I experienced whilst managing a holiday let for over 2 years.

**The Problem:** Property owners lose 15-20% of potential revenue through suboptimal pricing, whilst professional revenue management tools cost £200+/month - too expensive for individual owners.

**My Solution:** A free, AI-powered tool that democratises revenue management for small property owners.

---

## ✨ Key Features

- 🤖 **Claude AI Integration** - Intelligent market analysis with strategic reasoning
- 📊 **Interactive Visualisations** - Colour-coded price comparison charts
- 💡 **Strategic Insights** - Market positioning (budget/mid-range/premium)
- 🎯 **Personalised Tips** - 3 actionable revenue optimisation recommendations
- 📈 **Dual-Mode Analysis** - Basic statistical + AI-enhanced recommendations

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend/Backend | Streamlit | Rapid web development |
| AI Integration | Claude API (Sonnet 4) | Strategic analysis |
| Data Processing | Pandas, NumPy | Competitor filtering |
| Visualisation | Plotly | Interactive charts |
| Language | Python 3.11 | Core application |

**Architecture Highlights:**
- Modular design with clean separation of concerns
- Structured prompts returning JSON for consistent parsing
- Efficient data filtering and statistical calculations

---

## 🚀 Quick Start
```bash
# Clone the repository
git clone https://github.com/MZabDev/holiday-pricing-optimizer.git
cd holiday-pricing-optimizer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Generate sample data
python3 create_sample_data.py

# Run the application
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 💼 Business Impact

### Quantified Value

For a property averaging £150/night with 70% occupancy (260 bookable nights/year):

- **Revenue Optimisation:** 15% increase = **£4,095/year additional revenue**
- **Time Savings:** 5+ hours/week eliminated = **260 hours/year**
- **Risk Reduction:** Data-driven decisions reduce underpricing and vacancy risks

### Target Users

- Individual holiday let owners (1-3 properties)
- Small property management companies
- New Airbnb hosts establishing pricing strategy

---

## 🎯 How It Works

The application follows a four-step process:

1. **User Input** - Property details (location, type, bedrooms, amenities)
2. **Competitor Analysis** - Filters database for exact and similar matches
3. **Statistical Processing** - Calculates averages, ranges, confidence scores
4. **AI Enhancement** - Claude analyses data for strategic recommendations

---

## 📊 Data Strategy

This MVP uses realistic synthetic data rather than web scraping for three strategic reasons:

### Why Synthetic Data?

1. **Legal Compliance** - Respects platform Terms of Service (web scraping violates Airbnb/Booking.com ToS)
2. **Reliability** - Consistent demonstration without scraper breakage from anti-bot measures
3. **Strategic Focus** - Time invested in AI integration over fighting CAPTCHAs

### Production Approach

For production, I'd implement a three-tier strategy:

- **Tier 1 (Recommended):** AirDNA API integration - licensed, comprehensive data (£200-300/month)
- **Tier 2:** User-provided data uploads - shifts collection to users
- **Tier 3 (Last Resort):** Ethical small-scale scraping with rate limiting and disclosure

The synthetic data approach demonstrates product judgement - understanding MVP vs production requirements and making pragmatic decisions.

---

## 🔮 Future Enhancements

### Phase 2 (Productionisation)
- Live data integration (AirDNA API)
- User authentication and saved properties
- Historical tracking (recommendations vs actual performance)
- Seasonal pricing adjustments

### Phase 3 (Scale)
- Multi-property portfolio dashboard
- Calendar integration with Airbnb/Booking.com
- A/B testing framework for pricing strategies
- Email alerts for competitor price changes

---

## 🎓 What I Learnt

This project taught me valuable lessons about building AI-powered products:

**Technical Skills:**
- API integration with error handling and JSON parsing
- Prompt engineering for consistent AI outputs
- Data visualisation for non-technical users
- Full-stack web development with Python

**Product Thinking:**
- When to use AI vs traditional algorithms
- Balancing feature completeness with rapid iteration
- MVP vs production trade-offs
- User interface design for complex data

**Business Understanding:**
- Quantifying product value (revenue impact, time savings)
- Identifying gaps between enterprise and individual users
- Cost considerations and pricing strategy

---

## 💡 Why This Project Matters

This demonstrates key competencies for AI Product roles:

- ✅ **Problem Identification** - Real business problem from lived experience
- ✅ **Technology Selection** - AI where it adds genuine value
- ✅ **Execution** - Functional, polished prototype
- ✅ **Product Vision** - Clear path from MVP to production
- ✅ **Business Acumen** - Can quantify value and identify target users
- ✅ **Strategic Thinking** - Pragmatic decisions (synthetic data approach)

---

## 👨‍💻 About Me

**Background:** Recent BSc Management graduate with 2+ years hands-on holiday let management experience

**Technical Skills:** Python, AI/ML (Claude API, prompt engineering), Streamlit, Pandas, Plotly

**Learning Journey:** Completed AI For Everyone and BCG GenAI Job Simulation

**Current Focus:** Seeking AI Product Management & Strategy roles in London

**Why This Project?** I experienced this pricing challenge firsthand managing my own holiday let. This project combines domain expertise with technical skills to solve a real problem.

---

## 📫 Contact

- **Email:** your.email@example.com
- **LinkedIn:** [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- **GitHub:** [github.com/MZabDev](https://github.com/MZabDev)

---

## 📄 Project Structure
```
holiday-pricing-optimizer/
├── app.py                      # Main Streamlit application
├── create_sample_data.py       # Generate realistic competitor data
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── src/
│   ├── __init__.py
│   ├── data_handler.py         # Data loading and filtering
│   ├── pricing_engine.py       # Statistical calculations
│   └── llm_analyzer.py         # Claude AI integration
└── data/
    └── competitors.csv         # Sample competitor pricing data
```

---

## ⚖️ Licence

This project is available for portfolio and educational purposes.

---

## 🙏 Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Anthropic Claude](https://www.anthropic.com/)
- Inspired by real challenges in the holiday rental industry

---

**⭐ If you find this project interesting, please consider starring the repository!**

---

*Built as a portfolio project demonstrating AI product development skills | January 2026*
