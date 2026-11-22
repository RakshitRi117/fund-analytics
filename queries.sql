-- 1. Top 5 funds by AUM
SELECT
    f.scheme_name,
    f.fund_house,
    p.aum_crore
FROM fact_performance AS p
JOIN dim_fund AS f
    ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;


-- 2. Average NAV per month
SELECT
    d.year,
    d.month,
    ROUND(AVG(n.nav), 2) AS average_nav
FROM fact_nav AS n
JOIN dim_date AS d
    ON n.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 3. SIP year-over-year growth by month
SELECT
    month,
    sip_inflow_crore,
    yoy_growth_pct
FROM monthly_sip_inflows
WHERE yoy_growth_pct IS NOT NULL
ORDER BY month;


-- 4. Transaction amount and count by state
SELECT
    state,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_transaction_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_transaction_amount DESC;


-- 5. Funds with expense ratio below 1%
SELECT
    f.scheme_name,
    f.fund_house,
    p.expense_ratio_pct
FROM fact_performance AS p
JOIN dim_fund AS f
    ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct;


-- 6. Fund houses by latest reported AUM
SELECT
    a.fund_house,
    a.aum_lakh_crore,
    a.num_schemes
FROM fact_aum AS a
WHERE a.date_key = (
    SELECT MAX(date_key)
    FROM fact_aum
)
ORDER BY a.aum_lakh_crore DESC;


-- 7. Total category inflows
SELECT
    category,
    ROUND(SUM(net_inflow_crore), 2) AS total_net_inflow_crore
FROM category_inflows
GROUP BY category
ORDER BY total_net_inflow_crore DESC;


-- 8. Most-held stocks across fund portfolios
SELECT
    stock_name,
    sector,
    ROUND(SUM(market_value_cr), 2) AS total_market_value_cr
FROM portfolio_holdings
GROUP BY stock_name, sector
ORDER BY total_market_value_cr DESC
LIMIT 10;


-- 9. Top 10 funds by three-year return
SELECT
    f.scheme_name,
    f.category,
    p.return_3yr_pct
FROM fact_performance AS p
JOIN dim_fund AS f
    ON p.amfi_code = f.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 10;


-- 10. Pending-KYC investor transactions
SELECT
    state,
    COUNT(*) AS pending_transaction_count,
    ROUND(SUM(amount_inr), 2) AS pending_transaction_amount
FROM fact_transactions
WHERE kyc_status = 'Pending'
GROUP BY state
ORDER BY pending_transaction_amount DESC;