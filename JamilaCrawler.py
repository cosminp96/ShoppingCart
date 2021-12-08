import json
import os
import requests
from bs4 import BeautifulSoup

#region constants

SHOPPING_CART_FILE_NAME = 'shopping_cart.json'
SHOPPING_CART_FILE_PATH = os.path.join(os.path.dirname(__file__),SHOPPING_CART_FILE_NAME)

#endregion

class JamilaCrawler:

    def __init__(self):
        self.data = {}

    def loadJSON(self):
        try:
            with open(SHOPPING_CART_FILE_PATH, "r+") as file:
                try:
                    self.data = json.load(file)
                except:
                    self.data = {}
                    json.dump(self.data, file)
        except:
            self.data = {}
            with open(SHOPPING_CART_FILE_PATH, "w+") as file:
                json.dump(self.data, file)

    def printJSON(self):
        if 'items' in self.data:
            for item in self.data['items']:
                string = "Name: " + item['name']
                if item['amount'] != "" and item['amount'] > 0:
                    string += " - Amount: " + str(item['amount'])
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
        for item in items_list:
            update_index = -1
            if (self.data != {}):
                if (self.checkForIngredient(item['name'])):
                    update_index = self.getIngredientIndex(item['name'])
                
            if update_index != -1:
                self.__structurizeIngredients(update_index, item)
                if (item['amount'] != '' and item['unit'] == self.data['items'][update_index]['unit']):
                    self.data['items'][update_index]['amount'] = round(item['amount'] + self.data['items'][update_index]['amount'],2)
                    if int(self.data['items'][update_index]['amount']) >= 1000:
                        if self.data['items'][update_index]['unit'] == "ml":
                            self.data['items'][update_index]['unit'] = "L"
                            self.data['items'][update_index]['amount'] /= 1000
                        if self.data['items'][update_index]['unit'] == "mg":
                            self.data['items'][update_index]['unit'] = "Kg"
                            self.data['items'][update_index]['amount'] /= 1000
                    if int(self.data['items'][update_index]['amount']) > 1:
                        if self.data['items'][update_index]['unit'] == "lingura":
                            self.data['items'][update_index]['unit'] = "linguri"
            else:
                self.data['items'].append(item)
    
    def __structurizeIngredients(self, update_index, item):
        if self.data['items'][update_index]['unit'].lower() == "l" and item['unit'].lower() == "ml":
            item['unit'] = "L"
            item['amount'] /= 1000
        if self.data['items'][update_index]['unit'].lower() == "kg" and item['unit'].lower() == "mg":
            item['unit'] = "L"
            item['amount'] /= 1000
        if self.data['items'][update_index]['unit'].lower() == "linguri" and item['unit'].lower() == "lingura":
            item['unit'] = "linguri"

jc = JamilaCrawler()
jc.loadJSON()
jc.getIngredientsFromRecipeURL()
jc.printJSON()