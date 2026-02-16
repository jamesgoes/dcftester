# NVIDIA DCF Valuation Model

A simple web application for running discounted cash flow (DCF) analysis on NVIDIA with adjustable assumptions.

## Features

- Interactive DCF model with toggleable assumptions
- 5-year revenue and FCF projections
- Terminal value calculation
- Fair value per share estimation
- Clean, responsive UI

## Deploy to Railway

1. Push this code to a GitHub repository
2. Go to [Railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect the configuration and deploy

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:8080`

## Default Assumptions

- Current Revenue: $60B
- Revenue Growth: 25%
- Operating Margin: 35%
- Tax Rate: 15%
- CapEx: 5% of revenue
- NWC: 10% of revenue
- WACC: 10%
- Terminal Growth: 3%
- Shares Outstanding: 2,460M

## Model Details

The DCF model:
1. Projects 5 years of free cash flow with declining growth rates
2. Calculates terminal value using perpetual growth method
3. Discounts all cash flows to present value using WACC
4. Divides by shares outstanding for per-share valuation
