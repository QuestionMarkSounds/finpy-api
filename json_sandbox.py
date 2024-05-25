import json


string ='''{
  "data": [
    {
      "application": null,
      "application_fee_percent": null,
      "automatic_tax": {
        "enabled": false,
        "liability": null
      },
      "billing_cycle_anchor": 1716567517,
      "billing_cycle_anchor_config": null,
      "billing_thresholds": null,
      "cancel_at": null,
      "cancel_at_period_end": false,
      "canceled_at": null,
      "cancellation_details": {
        "comment": null,
        "feedback": null,
        "reason": null
      },
      "collection_method": "charge_automatically",
      "created": 1716567517,
      "currency": "eur",
      "current_period_end": 1719245917,
      "current_period_start": 1716567517,
      "customer": "cus_QALWc3kXrD97BF",
      "days_until_due": null,
      "default_payment_method": "pm_1PK0pD02koWkZWymFCWVQC7a",
      "default_source": null,
      "default_tax_rates": [],
      "description": null,
      "discount": null,
      "discounts": [],
      "ended_at": null,
      "id": "sub_1PK0pF02koWkZWymddXpLw5n",
      "invoice_settings": {
        "account_tax_ids": null,
        "issuer": {
          "type": "self"
        }
      },
      "items": {
        "data": [
          {
            "billing_thresholds": null,
            "created": 1716567517,
            "discounts": [],
            "id": "si_QALW1rRGkbXDq0",
            "metadata": {},
            "object": "subscription_item",
            "plan": {
              "active": true,
              "aggregate_usage": null,
              "amount": 2000,
              "amount_decimal": "2000",
              "billing_scheme": "per_unit",
              "created": 1716395708,
              "currency": "eur",
              "id": "price_1PJI8802koWkZWymUDKN85Tb",
              "interval": "month",
              "interval_count": 1,
              "livemode": false,
              "metadata": {},
              "meter": null,
              "nickname": null,
              "object": "plan",
              "product": "prod_Q9bKy7BuMuNYjd",
              "tiers_mode": null,
              "transform_usage": null,
              "trial_period_days": null,
              "usage_type": "licensed"
            },
            "price": {
              "active": true,
              "billing_scheme": "per_unit",
              "created": 1716395708,
              "currency": "eur",
              "custom_unit_amount": null,
              "id": "price_1PJI8802koWkZWymUDKN85Tb",
              "livemode": false,
              "lookup_key": null,
              "metadata": {},
              "nickname": null,
              "object": "price",
              "product": "prod_Q9bKy7BuMuNYjd",
              "recurring": {
                "aggregate_usage": null,
                "interval": "month",
                "interval_count": 1,
                "meter": null,
                "trial_period_days": null,
                "usage_type": "licensed"
              },
              "tax_behavior": "unspecified",
              "tiers_mode": null,
              "transform_quantity": null,
              "type": "recurring",
              "unit_amount": 2000,
              "unit_amount_decimal": "2000"
            },
            "quantity": 1,
            "subscription": "sub_1PK0pF02koWkZWymddXpLw5n",
            "tax_rates": []
          }
        ],
        "has_more": false,
        "object": "list",
        "total_count": 1,
        "url": "/v1/subscription_items?subscription=sub_1PK0pF02koWkZWymddXpLw5n"
      },
      "latest_invoice": "in_1PK0pF02koWkZWymMjoPrL5x",
      "livemode": false,
      "metadata": {},
      "next_pending_invoice_item_invoice": null,
      "object": "subscription",
      "on_behalf_of": null,
      "pause_collection": null,
      "payment_settings": {
        "payment_method_options": {
          "acss_debit": null,
          "bancontact": null,
          "card": {
            "network": null,
            "request_three_d_secure": "automatic"
          },
          "customer_balance": null,
          "konbini": null,
          "sepa_debit": null,
          "us_bank_account": null
        },
        "payment_method_types": null,
        "save_default_payment_method": "off"
      },
      "pending_invoice_item_interval": null,
      "pending_setup_intent": null,
      "pending_update": null,
      "plan": {
        "active": true,
        "aggregate_usage": null,
        "amount": 2000,
        "amount_decimal": "2000",
        "billing_scheme": "per_unit",
        "created": 1716395708,
        "currency": "eur",
        "id": "price_1PJI8802koWkZWymUDKN85Tb",
        "interval": "month",
        "interval_count": 1,
        "livemode": false,
        "metadata": {},
        "meter": null,
        "nickname": null,
        "object": "plan",
        "product": "prod_Q9bKy7BuMuNYjd",
        "tiers_mode": null,
        "transform_usage": null,
        "trial_period_days": null,
        "usage_type": "licensed"
      },
      "quantity": 1,
      "schedule": null,
      "start_date": 1716567517,
      "status": "active",
      "test_clock": null,
      "transfer_data": null,
      "trial_end": null,
      "trial_settings": {
        "end_behavior": {
          "missing_payment_method": "create_invoice"
        }
      },
      "trial_start": null
    }
  ],
  "has_more": false,
  "object": "list",
  "url": "/v1/subscriptions"
}'''

data = json.loads(string)
def print_len(data):
    print((len(data)))
print(data["data"][0]["plan"]["product"])