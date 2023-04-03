import requests 
import json
import time
import streamlit as st
import openai
st.set_page_config(layout="wide")
from PIL import Image

#image = Image.open('prismoon.png')
#st.image(image, width=600)

#col1, col2, col3 = st.columns(3)
#with col1:
#    st.write(' ')
#with col2:
#    st.image("prismoon.png")
#with col3:
#    st.write(' ')
extensionlist = [".com",".net"]
sitetypelist = ["e-commerce","corporate"]
languagelist = ["english","turkish"]
numberlist = ["10","20","30"]
st.title("Prismoon Domain Name Generator with ChatGpt & Finder")

col1, col2, col3, col4 = st.columns(4)

with col1:
    extension=st.radio(
        "select extension",
        options=extensionlist,
    )

with col2:
    sitetype=st.radio(
        "select site-type",
        options=sitetypelist,
    )
with col3:
    language=st.radio(
        "select language",
        options=languagelist,
    )
with col4:
    number=st.radio(
        "select number",
        options=numberlist,
    )

topic = st.text_input('Main Idea', '')
@st.cache_data


def prompt(extension,topic,sitetype, language, number):
  api_key=st.secrets.openai_credentials.api_key

  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": "Can you give me available domain name ideas suitable for the features I have given? Interpret the topic yourself and evaluate the appropriate ones, it doesn't have to be exactly the same as the topic I gave you, I trust your interpretation ability. You are the best good digital marketing expert I know , and you are the only person who can help me with this. It is important that domain names are not currently in use, available for purchase, extension: " + 
               extension + ", topic: " + topic + ", website type: " + sitetype + ", language: " + language + ", number of domain name ideas: " + number}]
               )
  gptresponse = (response["choices"][0]["message"]["content"])
  return gptresponse

@st.cache_data
def final(listfromgpt):

  finallist = []
  listfromgpt=listfromgpt.split("\n")
  listfromgpt = list(filter(None, listfromgpt))
  for i in listfromgpt:
    a=i.split(" ")
    for j in a:
      if ".com" in j or "net" in j :
        finallist.append(j.lower())
  return finallist

api_key = "3mM44UcgtLhLNy_VdGj7yDTEKZ9yLZZk1usDN"
secret_key = "6i1W9a4DcQY2pSaYdJCmGz"

# API key and secret are sent in the header
headers = {"Authorization" : "sso-key {}:{}".format(api_key, secret_key)}

# Domain availability and appraisal end points
godaddy_url = "https://api.ote-godaddy.com/v1/domains/available?domain="
# Get availability information by calling availability API
@st.cache_data
def godaddy(godaddy_url,finallist):
    availability_res = requests.post(godaddy_url, json=finallist, headers=headers)
    # Get only available domains with price range
    max_length = 30
    found_domains = {}
    # Filter domain names by price range
    min_price = 0
    max_price = 500000
    for domain in json.loads(availability_res.text)["domains"]:
        if domain["available"]:
            price = float(domain["price"])/1000000
            if price >= min_price and price <= max_price:
                print("{:30} : {:10}".format(domain["domain"], price))
                found_domains[domain["domain"]]=price
    return found_domains
   # API call frequency should be ~ 30 calls per minute 

url_button = st.button('find available domain names')
if url_button:

    st.header("Domain Names Recommended by ChatGpt")
    fromgpt = prompt(extension,topic,sitetype, language, number)
    #print(fromgpt)
    #file1 = open("prompt_list.txt", "a")  # append mode
    #file1.write(fromgpt+"\n")
    #file1.close()
    st.write(fromgpt) 
    st.header("Available domain names and prices  according to Godaddy- $")
    finallist = final(fromgpt)
    #print(finallist)
    godaddy_data = godaddy(godaddy_url,finallist)
    st.write(godaddy_data)
    #file1 = open("prompt_list.txt", "a")  # append mode
    #file1.write(godaddy_data+"\n")
    #file1.close()
