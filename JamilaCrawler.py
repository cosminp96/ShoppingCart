import json
import os

#region constants

SHOPPING_CART_FILE_NAME = 'shopping_cart.json'
SHOPPING_CART_FILE_PATH = os.path.join(os.path.dirname(__file__),SHOPPING_CART_FILE_NAME)

#endregion

class JamilaCrawler:
    data = {}

    def loadJSON(self, filename):
        with open(filename, "r+") as file:
            try:
                self.data = json.load(file)
            except:
                self.data = {}
                json.dump(self.data, file)

    def printJSON(self):
        if 'items' in self.data:
            for item in self.data['items']:
                string = "Name: " + item['name']
                if item['amount'] > "0":
                    string += " - Amount: " + item['amount']
                if item['unit'] != "":
                    string += " - Unit: " + item['unit']
                if item['note'] != "":
                    string += " - Note: " + item['note']
                print(string)