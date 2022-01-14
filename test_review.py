from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

table = Flask(__name__)

@table.route('/review', methods=['POST'])
def index():
    if request.method == 'POST':
        search = request.json['text']
        url = "https://www.flipkart.com/search?q=" + search
        uClient = uReq(url)
        flipkart_page = uClient.read()
        uClient.close()
        flipkart_html = bs(flipkart_page, "html.parser")
        phone_list = flipkart_html.findAll('div',{'class':"_1AtVbE col-12-12"})
        phone = phone_list[3].div.div.div.a['href']
        phone_link = "https://www.flipkart.com" + phone
        prodRes = requests.get(phone_link)
        prodRes.encoding = 'utf-8'
        prod_html = bs(prodRes.text, "html.parser")
        comment_box = prod_html.findAll('div', {'class':'_16PBlm'})
        l=[]
        for i in range(len(comment_box)-1):
            my_dict={}
            rating = comment_box[i].findAll('div',{'class':'_3LWZlK _1BLPMq'})[0].text
            comment_head = comment_box[i].findAll('p', {'class':'_2-N8zT'})[0].text
            name = comment_box[i].findAll('p', {'class':'_2sc7ZR _2V5EHH'})[0].text
            comment = comment_box[i].findAll('div',{'class':''})[1].text
            my_dict['name']=name
            my_dict['rating']=rating
            my_dict['comment_head']=comment_head
            my_dict['comment']=comment
            l.append(my_dict)
            result = l
        return jsonify(result)


if __name__ == '__main__':
    table.run()



