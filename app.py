from flask import Flask, render_template, request
import math

app = Flask(__name__)

def calculate_dcf(revenue, revenue_growth, operating_margin, tax_rate,
                  capex_pct, nwc_pct, wacc, terminal_growth, shares):
    """Calculate DCF valuation for NVIDIA"""

    # Project 5 years of cash flows
    fcf_projections = []
    current_revenue = revenue

    for year in range(1, 6):
        # Revenue grows at declining rate
        growth_rate = revenue_growth * (0.9 ** (year - 1))
        current_revenue = current_revenue * (1 + growth_rate)

        # Calculate Free Cash Flow
        ebit = current_revenue * operating_margin
        nopat = ebit * (1 - tax_rate)
        capex = current_revenue * capex_pct
        nwc_change = current_revenue * growth_rate * nwc_pct

        fcf = nopat - capex - nwc_change
        fcf_projections.append({
            'year': year,
            'revenue': current_revenue,
            'fcf': fcf
        })

    # Calculate present value of cash flows
    pv_fcf = sum(proj['fcf'] / ((1 + wacc) ** proj['year'])
                 for proj in fcf_projections)

    # Terminal value
    terminal_fcf = fcf_projections[-1]['fcf'] * (1 + terminal_growth)
    terminal_value = terminal_fcf / (wacc - terminal_growth)
    pv_terminal = terminal_value / ((1 + wacc) ** 5)

    # Enterprise value and equity value
    enterprise_value = pv_fcf + pv_terminal
    equity_value = enterprise_value  # Simplified - no debt/cash adjustment
    price_per_share = equity_value / shares

    return {
        'projections': fcf_projections,
        'pv_fcf': pv_fcf,
        'terminal_value': terminal_value,
        'pv_terminal': pv_terminal,
        'enterprise_value': enterprise_value,
        'equity_value': equity_value,
        'price_per_share': price_per_share
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    # Default assumptions for NVIDIA
    defaults = {
        'revenue': 60000,  # $60B current revenue
        'revenue_growth': 0.25,  # 25% growth
        'operating_margin': 0.35,  # 35% operating margin
        'tax_rate': 0.15,  # 15% tax rate
        'capex_pct': 0.05,  # 5% of revenue
        'nwc_pct': 0.10,  # 10% of revenue
        'wacc': 0.10,  # 10% WACC
        'terminal_growth': 0.03,  # 3% terminal growth
        'shares': 2460  # 2.46B shares outstanding
    }

    if request.method == 'POST':
        # Get user inputs
        inputs = {
            'revenue': float(request.form.get('revenue', defaults['revenue'])),
            'revenue_growth': float(request.form.get('revenue_growth', defaults['revenue_growth'])),
            'operating_margin': float(request.form.get('operating_margin', defaults['operating_margin'])),
            'tax_rate': float(request.form.get('tax_rate', defaults['tax_rate'])),
            'capex_pct': float(request.form.get('capex_pct', defaults['capex_pct'])),
            'nwc_pct': float(request.form.get('nwc_pct', defaults['nwc_pct'])),
            'wacc': float(request.form.get('wacc', defaults['wacc'])),
            'terminal_growth': float(request.form.get('terminal_growth', defaults['terminal_growth'])),
            'shares': float(request.form.get('shares', defaults['shares']))
        }

        results = calculate_dcf(**inputs)
        return render_template('index.html', defaults=inputs, results=results)

    return render_template('index.html', defaults=defaults, results=None)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
