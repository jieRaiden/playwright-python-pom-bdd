import json
from pathlib import Path

class JsonReader:



    def get_user_credentials(self):
        self.path = Path("data/credential.json")
        with self.path.open(encoding="utf-8") as f:
            return json.load(f)["login"]
        
    def get_addtocart_item(self):
        self.path = Path("data/addtocart.json")
        with self.path.open(encoding="utf-8") as f:
            return json.load(f)["item"]
        
    def get_orders_item(self):
        self.path = Path("data/orders.json")
        with self.path.open(encoding="utf-8") as f:
            return json.load(f)["Order1"]