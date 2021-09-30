import os
from dotenv import load_dotenv
import discord
import requests
import json
from bs4 import BeautifulSoup

load_dotenv('.env')
client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as user { client.user }')

@client.event
async def on_message(message):
    if(message.author == client.user):
        return  

    elif(message.content.startswith('$hello')):
        await message.channel.send('Hello little Ent!')
    
    elif(message.content.startswith('$me')):
        await message.channel.send(f'You\'re name is { message.author.name }!')
    
    elif(message.content.startswith('$news')):
        category = ''

        if(' ' in message.content):
            category = message.content.split(' ')[1]

        await message.channel.send(getNews(category))

    elif(message.content.startswith('$lunch tomorrow')):
        await message.channel.send(getTomorrowLunch())

    elif(message.content.startswith('$dinner tomorrow')):
        await message.channel.send(getTomorrowDinner())

    elif(message.content.startswith('$lunch')):
        await message.channel.send(getLunch())

    elif(message.content.startswith('$dinner')):
        await message.channel.send(getDinner())
    
    elif(message.content.startswith('$shop')):
        await message.channel.send(getBestBuy())
    
 
def getNews(category):
    if(category == ''):
        newsUrl = f'https://newsapi.org/v2/top-headlines?country=us&apiKey=API_KEY'
    else:
        newsUrl = f'https://newsapi.org/v2/top-headlines?country=us&category={ category }&apiKey=API_KEY'

    response = requests.get(newsUrl)
    jsonData = json.loads(response.text)
    
    return f"\nAuthor: {jsonData['articles'][0]['author'] }"\
        + f"\nTitle: { jsonData['articles'][0]['title'] }"\
        + f"\nDescription: { jsonData['articles'][0]['description'] }"\
        + f"\nURL: { jsonData['articles'][0]['url'] }"

def getLunch():
    response = requests.get(os.getenv('MEAL_URL'))

    soup = BeautifulSoup(response.text, 'html.parser')
    lunch = soup.find_all(class_='jelovnik-date-content')[0].get_text()

    return lunch

def getDinner():
    response = requests.get(os.getenv('MEAL_URL'))

    soup = BeautifulSoup(response.text, 'html.parser')
    dinner = soup.find_all(class_='jelovnik-date-content')[1].get_text()

    return dinner

def getTomorrowLunch():
    response = requests.get(os.getenv('MEAL_URL'))

    soup = BeautifulSoup(response.text, 'html.parser')
    lunch = soup.find_all(class_='jelovnik-date-content')[2].get_text()
    return lunch

def getTomorrowDinner():
    response = requests.get(os.getenv('MEAL_URL'))

    soup = BeautifulSoup(response.text, 'html.parser')
    lunch = soup.find_all(class_='jelovnik-date-content')[3].get_text()
    return lunch

def getBestBuy():
    output = 'Best buys this week\n\n'
    response = requests.get(os.getenv('SHOP_URL'))

    soup = BeautifulSoup(response.content, 'html.parser')

    products = soup.find_all(id='featured_products')

    for p in products:
        productsInfo = p.find_all(['a'], href=True)

        for pi in productsInfo:
           output += f'https://bazzar.hr/{pi["href"]}\n\n'
    
    return output

client.run(os.getenv('BOT_TOKEN'))

