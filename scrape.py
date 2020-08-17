import requests
import json
from bs4 import BeautifulSoup, NavigableString, Tag
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Scrape(Resource):
    def get(self):
        postcode = request.args.get('postcode')
        info = {}
        counter = 0
        URL = 'http://www.homeandbuild.co.uk/search?postcode='+postcode+'&searchlabc=true'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        elems = soup.find_all('div', class_='item1')
        for elem in elems:
            #Get logo and Title
            img = elem.find('img')
            info['logo']='http://www.homeandbuild.co.uk'+img['src']
            info['building_authority_name']=img['title']
            counter = 2
            #Get all P tags in
            pss = elem.find_all('p')
            header = ''
            for ps in pss:
                s = ps.find('strong')
                if s != None:
                    header = s.get_text()
                nc = 0
                temp = {}
                for br in ps.find_all('br'):         
                    next_s = br.nextSibling
                    #process next_s to if its an anchor tag
                    a = br.find_next_sibling('a')
                    if br.nextSibling.name  == 'a':
                            next_s=a.text
                    #create temp dict which will then be appended to info dict.
                    temp[nc]=next_s
                    counter+=1
                    nc+=1
                #append temp to info dict.    
                info[header]=temp
        return jsonify({'info': info})

api.add_resource(Scrape, '/')

if __name__ == '__main__':
    app.run(debug=True)