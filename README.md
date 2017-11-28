# MusicUnderTheWeather

Outline: 
Okay, so this is a website that gives you music suggestions depending on the weather of your location. With the use of the Weather Underground API, we can find the weather of a user's location if they enter their city. The result of their search (with the input being the city) is a carefully curated list of songs for that given weather range (<30, 30-50, 50-70, 70-90, 90+ all in Farenhiet), and the user can choose to play the songs on the frames embedded in the site page. 


How to Run: 
- Enter your virtual environment 
- "python app.py" and then copy/paste http://127.0.0.1:5000/ into your given browser
- Create an account and login
- Enter your zipcode or any other zipcode if you really want to (!!NOTE!! Because of the way the API is set up, we can only access zip codes within the United States, so please make sure your zip code is within the US) 
- Listen to some qual music (if you refresh, you'll probably get another song suggestion. I say probably because it's random, so there is a chance of a repeat, but if you refresh twice, then there's less of a chance you'd get the same song three times in a row)
