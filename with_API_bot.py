import logging 
import asyncio 
import requests 
from aiogram import Bot, Dispatcher, types 

API_TOKEN = '7586292019:AAHChEgA_fkbVNNXr71VumfWlob2RAMMkIk' 
WEATHER_API_KEY = '67314116a95d11ff4538996718d1b72d' 
 
bot = Bot(token=API_TOKEN) 
dp = Dispatcher() 

@dp.message() 
async def get_weather(message: types.Message): 
    #получаю название города от пользователя 
    city_name = message.text 
     
    #делаю запрос к API погоды 
    weather_data = get_weather(city_name) 
     
    if weather_data: 
        await message.reply(text=weather_data)
    else: 
        await message.reply(text='Не удалось получить данные о погоде. Убедитесь, что название города указано верно.') 
 
def get_weather(city): 
    params = { 
        'q': city, 
        'appid': WEATHER_API_KEY, 
        'units': 'metric',  #температура в градусах Цельсия 
        'lang': 'ru' 
    } 
     
    response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params) 
     
    if response.status_code == 200: 
        data = response.json() 
        #извлекаю данные
        temperature = data['main']['temp'] 
        humidity = data['main']['humidity'] 
        description = data['weather'][0]['description'] 
         
        return (f'Погода в {city}:\n' 
                f'Температура: {temperature}°C:\n'
                f'Влажность: {humidity}%\n' 
                f'Описание: {description.capitalize()}') 
    else: 
        return None 
 
async def main(): 
    logging.basicConfig(level=logging.INFO) 
    await dp.start_polling(bot) 
 
if __name__ == '__main__': 
    asyncio.run(main())