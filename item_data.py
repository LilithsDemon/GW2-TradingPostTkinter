import urllib3
import json
import requests
import os

class Database:
    def __init__(self):
        self.url = "http://www.gw2spidy.com/api/v0.9/json/all-items/all"

        self.http = urllib3.PoolManager()

    def refresh_data(self):
        self.content = self.http.request('GET', self.url)
        self.stringContent = str(self.content.data)

        self.stringContent = self.stringContent.replace("},{", "},\n{")
        self.stringContent = self.stringContent.replace("]}'", "]}")
        self.stringContent = self.stringContent.replace("b'{", "{")
        self.stringContent = self.stringContent.replace("\\'", "")
        self.stringContent = self.stringContent.replace('"Acquired', "")
        self.stringContent = self.stringContent.replace('\\\\\\\\\" ', "")
        self.stringContent = self.stringContent.replace('"Legendary\\\\', "")
        self.stringContent = self.stringContent.replace("\\\\\" ", "")
        self.stringContent = self.stringContent.replace('\\\\"Elon Red\\\\"', "Elon Red")
        self.stringContent = self.stringContent.replace('\\\\', "")

        self.file = open("items.json", "w")
        self.file.write(self.stringContent)
        self.file.close()

    def data(self):
        self.file = open("items.json")
        self.jsonToPython = json.loads(self.file.read())
        self.file.close()

        return self.jsonToPython['results']

if __name__ == "__main__":
    dataBaseSet = Database()
    dataBaseSet.refresh_data()
    dataSheet = dataBaseSet.data()

    print(dataSheet[0]['name'])
