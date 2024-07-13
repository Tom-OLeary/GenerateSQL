from datetime import date


class Product:
    db_table: str = "products"

    date_created: date
    title: str
    market: str
    price: float
    description: str
    tax_rate: float = 6.25


# class PAdvertisingDaily:
#     db_table: str = "product_advertising_daily"
#
#     asin: str
#     product_id: int
#     brand_id: int
#     country_code: str = "US"
#     report_date: date = date(2022, 1, 1)
#     orders: int = 15
#     all_sales: float = 100.5
#     units_sold: int = 50
#     current_price_usd: float = 15.00
#     ad_sales: float = 200.00
#     ad_spend: float = 250.00
#     ad_orders: float = 15
#     clicks: int = 100
#     impressions: int = 200
#     view_attributed_sales_14d: float = 140.00
#     view_attributed_units_ordered_14d: int = 45
#     view_impressions: int = 250
#     current_price_breakeven_pct: float = 25.00
#     fba_selling_fees: float = 500.00
#     revenue_adj_estimate: float = 0.0
#     referral_fee_pct: float = 0.0
#     plc: float = 0.0
#     brand_name: str
#     product_name: str
#     parent_asin: str
#     ad_type: str = "product"
#
#
# class VPAdvertisingDaily(PAdvertisingDaily):
#     db_table: str = "vendor_product_advertising_daily"
#
#
# class BAdvertisingDaily:
#     db_table: str = "brand_advertising_daily"
#
#     brand_id: int
#     report_date: date
#     country_code: str
#     ad_sales: float = 200.00
#     ad_spend: float = 250.00
#     ad_orders: float = 15
#     clicks: int = 100
#     impressions: int = 200
#     orders: int = 15
#     all_sales: float = 100.5
#     units_sold: int = 50
#     ad_type: str = "brand"
#
#
# class VBAdvertisingDaily(BAdvertisingDaily):
#     db_table: str = "vendor_brand_advertising_daily"
#
#
# class TearsheetView:
#     db_table: str = "daily_product_tearsheet_view"
#
#     date: date
#     brand_id: int
#     product_id: int
#     country_code: str
#     amazon_product_advertising_cost: float
#     amazon_display_advertising_cost: float
#     amazon_brand_advertising_cost: float
#     total_amazon_income: float
#     total_amazon_expenses: float
#     manufacturing_cost: float
#     fba_product_sales: float
#     units_sold: int
#     fba_selling_fees: float
#     vat_taxes: float = 0.0
#     production_cost: float = 0.0
#
#
# class PricingAlgOutput:
#     db_table: str = "pricing_algorithm_output_view"
#
#     brand_id: int
#     product_id: int
#     referral_fee_pct: float = 0.0
#     plc: float = 0.0
#
#
# class AmzRevenueAdjustment:
#     db_table: str = "amazon_current_revenue_adjustment_estimates"
#
#     product_id: int
#     country_code: str
#     revenue_adj_estimate: float = 0.0



