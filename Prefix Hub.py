
import discord
import feedparser
import requests
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime

# Discord bot token
TOKEN = ""

# RSS feed URL (after authentication)
RSS_FEED_URL = 'https://leaked.cx/forums/hiphopleaks.rss'

# Forum page ID
PAGE_ID  = 0

# How long it takes before it reads the feed again
sleepInterval = 5

# Discord channel ID where you want to send the feed updates
CHANNEL_ID = ''

# Credentials for website authentication
USERNAME = ''
PASSWORD = ''

# Which forums the bot will scrape
pages = ['https://leaked.cx/forums/hiphopleaks', 'https://leaked.cx/forums/othergenreleaks', 'https://leaked.cx/forums/othermedialeaks']
pages_rss = ['https://leaked.cx/forums/hiphopleaks.rss', 'https://leaked.cx/forums/othergenreleaks.rss', 'https://leaked.cx/forums/othermedialeaks.rss']

# Artist role pings
artist_roles = {
    "juice wrld": {"role": "", "thumbnail": "https://wallpapers-clan.com/wp-content/uploads/2022/08/juice-wrld-pfp-15.jpg"},
    "lil uzi vert": {"role": "", "thumbnail": "https://i.pinimg.com/originals/d9/8e/29/d98e29caddd7b5f5947d1d271dc0a5b4.jpg"},
    "kanye west": {"role": "", "thumbnail": "https://lh3.googleusercontent.com/xfezNwf-YBEBvGGyWWb9vPDZR4407F_nEK7tBuKdLMTwA6xN95VBSeNF6RQojix5-CTKdm8pjEYVwHaZiMXd0o9cNJ8Zdr6k"},
    "future": {"role": "", "thumbnail": "https://i.ibb.co/vhJc9jY/b00fd08be2f9459ec5b2f1875ed9a02a.jpg"},
    "travis scott": {"role": "", "thumbnail": "https://steamuserimages-a.akamaihd.net/ugc/782985908102502358/2157D7CBA0ABB6D5E5EE9C222B8A0FBFEBC07B7E/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false"},
    "the weeknd": {"role": "", "thumbnail": "https://media.pitchfork.com/photos/5e3d7b57159e01000820beb9/1:1/w_512,h_512,c_limit/The-Weeknd.JPG"},
    "playboi carti": {"role": "", "thumbnail": "https://wallpapers-clan.com/wp-content/uploads/2022/07/playboi-carti-pfp-5.jpg"},
    "gunna": {"role": "", "thumbnail": "https://firebase.soulectiontracklists.com/cdn/image//t_square_extra_large/images/artists/blaccmass/tracks/gunna-world-is-yours.jpg"},
    "yeat": {"role": "", "thumbnail": "https://media.plus.rtl.de/music-deezer/artist/de332e65dc6029438aaea754888b2786/512x512-000000-80-0-0.jpg?tr=f-auto,w-512"},
    "trippie redd": {"role": "", "thumbnail": "https://i.pinimg.com/564x/e1/59/fc/e159fc0dd363debd6db7033b4ae098d9.jpg"},
    "ken carson": {"role": "", "thumbnail": "https://kansascity.events/wp-content/uploads/2024/04/ken-carson.jpg"},
    "drake": {"role": "", "thumbnail": "https://s11279.pcdn.co/wp-content/uploads/2020/04/toosie.png"},
    "lil wayne": {"role": "", "thumbnail": "https://www.appahang2.com/cdn/artists-avatar/1402/12/5712170926874196181709268741683017092687418771.webp"},
    "tory lanez": {"role": "", "thumbnail": "https://i.pinimg.com/736x/60/15/b8/6015b8c284b22046839d0a3e98266768.jpg"},
    "young thug": {"role": "", "thumbnail": "https://i.scdn.co/image/ab6761610000e5eb547d2b41c9f2c97318aad0ed"},
    "mac miller": {"role": "", "thumbnail": "https://scontent.cdninstagram.com/v/t51.29350-15/426230978_1330956550825521_4083831995184637062_n.jpg?stp=dst-jpg_e35&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi44MTN4ODAwLnNkci5mMjkzNTAifQ&_nc_ht=scontent.cdninstagram.com&_nc_cat=109&_nc_ohc=b0cFck5r-z4Q7kNvgHs36Wc&edm=APs17CUBAAAA&ccb=7-5&ig_cache_key=MzI5OTA1MzYzMjY2MTE5NjUwNA%3D%3D.2-ccb7-5&oh=00_AYCDwFGfefdeckwi8KDfL5KlC7v-YnFr4FgWogY_OAo4EQ&oe=665EE34F&_nc_sid=10d13b"},
    "migos": {"role": "", "thumbnail": "https://play-lh.googleusercontent.com/cRiE4Sv3JJNNl6M69ZcB8i0zXhjIZGpoB_D8uFNrf7_8eVIUYTwHuQQdBe4-fBjuikg"},
    "destroy lonely": {"role": "", "thumbnail": "https://d1dy244g59v5jo.cloudfront.net/artist-51/5146884dadc29d8c4090554a34e717453d6340e86fc86e047de7d497b325595cb3cb8d6e.jpg.512x512.jpg"},
    "chief keef": {"role": "", "thumbnail": "https://steamuserimages-a.akamaihd.net/ugc/814499342665234483/977E1E00DCAF9A39EE1C1069AB49D3DEC9B4BFBA/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false"},
    "lil tecca": {"role": "", "thumbnail": "https://steamuserimages-a.akamaihd.net/ugc/1783967784602355345/C6EEACAE67CF68F7A64D2056CC6D7E31BBFDD01C/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false"},
    "charlie xcx": {"role": "", "thumbnail": "https://i.pinimg.com/originals/3d/62/dc/3d62dc9eb53e030cb4da7b40cada23a2.jpg"},
    "camila cabello": {"role": "", "thumbnail": "https://media.plus.rtl.de/music-deezer/artist/4591e8a49868c2494652767f47695a90/512x512-000000-80-0-0.jpg?tr=f-auto,w-512"},
    "dua lipa": {"role": "", "thumbnail": "https://milocostudios.com/wp-content/uploads/2020/05/unnamed.jpg"},
    "ariana grande": {"role": "", "thumbnail": "https://i.ibb.co/W5wD7jn/img-pmg-512x512.webp"},
    "justin bieber": {"role" : "", "thumbnail": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRg0cdqKLwJetSGQeJjsudtMWJeEfSP1Y3B8Q&s"}
}


# Any unauthorized modification or tampering of the code below Line 237 for personal gain is strictly prohibited. 
# Such actions will result in the filing of a Copyright strike to takedown your GitHub repository or Discord bot. 
# We take intellectual property rights seriously and will enforce necessary measures to protect our work. Thank you for your understanding and cooperation.

# This project took a while to get where it's at, so please respect my kindness.



#                  ____  ____  _____ _____ _____  __       _   _ _   _ ____  
#                 |  _ \|  _ \| ____|  ___|_ _\ \/ /      | | | | | | | __ ) 
#                 | |_) | |_) |  _| | |_   | | \  /       | |_| | | | |  _ \ 
#                 |  __/|  _ <| |___|  _|  | | /  \       |  _  | |_| | |_) |
#                 |_|   |_| \_\_____|_|   |___/_/\_\      |_| |_|\___/|____/ 
#                                                                       @b9na





client = discord.Client(intents=discord.Intents.all())

def extract_csrf_token(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the CSRF token input field
    csrf_input = soup.find('input', {'name': '_xfToken'})
    
    # Extract the value of the CSRF token
    if csrf_input:
        csrf_token = csrf_input.get('value')
        return csrf_token
    else:
        print('CSRF token not found')
        return None

async def authenticate():
    session = requests.Session()
    
    # Perform initial request to get CSRF token and cookies
    login_page_response = session.get('https://leaked.cx/login/')
    
    # Extract CSRF token from the response HTML
    csrf_token = extract_csrf_token(login_page_response.text)
    
    # Construct login data with CSRF token and other required parameters
    login_data = {
        'login': USERNAME,
        'password': PASSWORD,
        'remember': 'on',
        '_xfRedirect': '',
        '_xfToken': csrf_token,
        '_xfResponseType': 'json'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Referer': 'https://leaked.cx/login/',
        'Origin': 'https://leaked.cx'
    }
    
    # Send login request with constructed data and headers
    login_response = session.post('https://leaked.cx/login/login', data=login_data, headers=headers)
    
    # Check if login was successful
    if login_response.status_code == 200:
        print('Authentication successful')
        return session
    else:
        print('Authentication failed')
        return None

async def fetch_feed_data(session):
    global PAGE_ID
    
    # If statement for PAGEID overflow
    if int(PAGE_ID) >= 3:
        PAGE_ID = 0
    
    # Download RSS feed content using the authenticated session
    rss_response = session.get(pages_rss[PAGE_ID])
    forum = session.get(pages[PAGE_ID])
    
    print(f"Searching through: {pages[PAGE_ID]}")
    
    if rss_response.status_code == 200 and forum.status_code == 200:
        # Parse the downloaded content using feedparser
        PAGE_ID += 1
        feed = feedparser.parse(rss_response.text)
        return feed, forum.content
    else:
        print(f"Failed to fetch RSS feed: {rss_response.status_code}")
        return None

async def send_feed_updates():
    session = await authenticate()
    THREAD_NAME = ""
    if session is None:
        return
    
    await client.wait_until_ready()
    channel = client.get_channel(int(CHANNEL_ID))
    
    while not client.is_closed():
        try:
            feed, forum = await fetch_feed_data(session)
            
            # Extracting data from the feed
            for entry in feed.entries:
                test = BeautifulSoup(forum, 'html.parser')

                mainDiv = test.find('div', attrs={"class":"structItemContainer-group js-threadList"})
                time = mainDiv.find("time").text.strip()
                
                term = entry.tags[0].term
                title = entry.title
                link = entry.link
                author = entry.author
                thumbnail = "https://leaked.cx/data/assets/logo/square192cx.png"
                    
                titleDiv = mainDiv.find("div", attrs={"class":"structItem-title"})
                    
                embed = discord.Embed(title=title.upper(), url=link, color=discord.Color.random())
                embed.set_footer(text=f"{term} | {time}")
                embed.set_thumbnail(url=thumbnail)
                    
                # Sending feed updates to the Discord channel

                artist = ""
                
                if title.lower() != THREAD_NAME.lower():
                        THREAD_NAME = title
                        labels = titleDiv.find_all("span")
                        rolePing = ""
                        for label in labels:
                            label_text = label.text.strip().lower()
                            if label_text in artist_roles:
                                artist = label_text
                            else:
                                pass

                        if any(artist in title.lower() for artist in artist_roles) or artist != "":
                            if artist == "":
                                artist = next(artist for artist in artist_roles if artist in title.lower())
                            else:
                                pass
                            thumbnail = artist_roles[artist]["thumbnail"]
                            rolePing = artist_roles[artist]["role"]
                            embed.set_thumbnail(url=thumbnail)
                        
                        # Sending Embed
                        #if "A moment ago" in time:
                        print(f'"{title}" was just posted by {author} [SUCCESS]')
                        if "A moment ago" in time:
                            if rolePing != "":
                                THREAD_NAME = title
                                await channel.send(f"<@&{rolePing}>", embed=embed)
                            else:
                                await channel.send(embed=embed)
                        break
                break

                
            # Sleep for an interval before fetching the feed again
            await asyncio.sleep(sleepInterval)  # 15 second interval
        except Exception as e:
            print(f"An error occurred: {e}")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Starting the background task to send feed updates
    await client.change_presence(activity=discord.activity.Game(name="Prefix Hub"))
    client.loop.create_task(send_feed_updates())

@client.event
async def on_message(message): # please support Prefix Hub
    # Check if the bot was mentioned in the message
    if client.user.mentioned_in(message) and message.mention_everyone is False:
        embed = discord.Embed(title="Prefix Hub", description=f"I'm a Discord bot powered by Prefix Hub, developed by <@948060905831268353>", url="https://discord.com/invite/SqMfMfRZVm")
        embed.set_thumbnail(url="https://i.ibb.co/68R6F17/Prefix-Hub.png")
        embed.set_author(name="@b9na", url="https://github.com/b9natwo")
        await message.channel.send(f"Hello {message.author.mention}", embed=embed)

# Running the bot
client.run(TOKEN)
