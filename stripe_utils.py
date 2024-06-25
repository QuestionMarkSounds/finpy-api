from dotenv import dotenv_values


config = dotenv_values(".env")

def get_product_from_subscription(subscription):
    return subscription["data"][0]["plan"]["product"]

class Subscription:
    subscriptions = [ 
        {
            "key": "basic", 
            "id": config["BASIC_PROD_ID"]
        }, 
        {   
            "key": "premium", 
            "id": config["PREMIUM_PROD_ID"]
        }
    ]

    def name_from_id(id):
        # Using list comprehension to find the key where id is 4
        keys = [d["key"] for d in Subscription.subscriptions if d["id"] == id]

        # Since the result is a list, we'll get the first element if it exists
        key = keys[0] if keys else "none"
        return key