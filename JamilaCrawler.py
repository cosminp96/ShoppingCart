import json
import os
import requests
from bs4 import BeautifulSoup

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
    
    def checkForIngredient(self, ingredient_name):
        return any(ingredient['name']==ingredient_name for ingredient in self.data['items'])
    
    def getIngredientIndex(self, ingredient_name):
        for index in range(0, len(self.data['items'])):
            if self.data['items'][index]['name'] == ingredient_name:
                return index

    def getIngredientsFromRecipeURL(self):
        URL = input("Please enter a recipe's URL:\n")

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        ingredients = soup.find_all("li", {"class": "wprm-recipe-ingredient"})

        items_list = []

        for ingredient in ingredients:
            amount = ingredient.find("span", class_="wprm-recipe-ingredient-amount")
            unit = ingredient.find("span", class_="wprm-recipe-ingredient-unit")
            name = ingredient.find("span", class_="wprm-recipe-ingredient-name")
            note = ingredient.find("span", class_="wprm-recipe-ingredient-notes")

            item = {
                "name": name.text.lower().strip() if name is not None else "",
                "amount": int(amount.text.lower().strip()) if amount is not None else "",
                "unit": unit.text.lower().strip() if unit is not None else "",
                "note": note.text.lower().strip() if note is not None else ""
            }

            items_list.append(item)

        if 'items' not in self.data:
            self.data['items'] = items_list
        else:
            self.updateCart(items_list)

        with open(SHOPPING_CART_FILE_PATH, "w") as file:
            json.dump(self.data, file)
    
    def updateCart(self, items_list):
        return 0

jc = JamilaCrawler()
jc.loadJSON(SHOPPING_CART_FILE_PATH)
# jc.getIngredientsFromRecipeURL()
jc.printJSON()