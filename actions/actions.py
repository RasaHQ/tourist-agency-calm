import datetime
import requests
from typing import Any, Optional, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormValidationAction
import aiohttp

country_info_map = {
            "USA": "The United States of America is a vast country located in North America, known for its diverse geography, multicultural society, and iconic landmarks. The capital of the United States is Washington, D.C., which is located in the eastern part of the country and is home to many famous monuments and museums, including the White House, the Lincoln Memorial, and the Smithsonian Institution",
            "Denmark": "Denmark is a small Nordic country located in northern Europe, known for its high standard of living, progressive social policies, and stunning natural scenery. The capital of Denmark is Copenhagen, which is located on the country's eastern coast and is home to many historic landmarks such as the Little Mermaid statue, Amalienborg Palace, and the colorful Nyhavn harbor",
            "Japan": "Japan is an island country located in East Asia, known for its unique blend of ancient traditions and modern culture. The capital of Japan is Tokyo, which is the country's largest city and one of the world's most populous metropolises. Tokyo is home to a vibrant arts and entertainment scene, as well as many historic landmarks such as the Imperial Palace, Tokyo Tower, and the Meiji Shrine",
            "China": "China is a vast country located in East Asia, with a rich and complex history dating back thousands of years. Its capital is Beijing, which is located in the northern part of the country and is known for its iconic landmarks such as the Forbidden City, Tiananmen Square, and the Great Wall of China",
            "Portugal": "Portugal's capital is Lisbon, which is located on the country's west coast and is known for its colorful architecture, historic landmarks such as the Belem Tower and Jeronimos Monastery, and lively cultural scene.",
            "Canada": "Canada, a country located in North America, is known for its natural beauty, friendly people, and diverse culture. The Canadian economy is characterized by a mix of modern industries and natural resource extraction, including oil, gas, and forestry.",
            "Spain": "Spain, a country located in southwestern Europe, is known for its vibrant culture, history, and architecture. The Spanish economy, one of the largest in Europe, is based on a mix of industries, including tourism, manufacturing, and agriculture.",
            "France": "France, a country located in Western Europe, is known for its rich history, art, culture, and cuisine. The French economy is diversified and includes a mix of industries such as aerospace, automotive, fashion, and tourism.",
            "Thailand": "Thailand, a country located in Southeast Asia, is known for its beautiful beaches, temples, and vibrant street life. The Thai economy is diversified and includes a mix of industries such as manufacturing, agriculture, and tourism.",
            "South Korea": "South Korea, a country located in East Asia, is known for its high-tech industry, vibrant pop culture, and rich history and tradition. The South Korean economy is one of the most advanced and developed in the world, with a focus on electronics, automobiles, shipbuilding, and other industries.",
            "Australia": "Australia, a country located in Oceania, is known for its diverse landscapes, wildlife, and laid-back lifestyle. The Australian economy is dominated by the service sector, with major industries including healthcare, finance, education, and tourism."}

class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_give_weather"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        country = tracker.get_slot("country")
        
        # make the API request to OpenWeatherMap
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.openweathermap.org/data/2.5/weather?q={country}&appid=e20a5433060a8bd213987c3d797beaff&units=metric") as response:
                weather_data = await response.json()
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        
        message = f"The temperature in {country} is {temperature} degrees Celsius, and the weather is {description}."
        dispatcher.utter_message(text=message)
        
        return [SlotSet("temperature", temperature)]
    
class ActionGetCountryInformation(Action):
    def name(self) -> Text:
        return "action_get_country_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        country = tracker.slots.get("country_destination")

        if country in country_info_map:
            
            country_info = country_info_map[country]

            dispatcher.utter_message(text=f"{country_info}")
        else:
            dispatcher.utter_message(text=f"We don't have information for {country}")

        return []

class ActionCheckBalance(Action):
    def name(self) -> Text:
        return "action_check_balance"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Hardcoded user balance for demonstration purposes
        user_balance = 500.0

        # Retrieve the booking amount from the tracker
        booking_amount = float(tracker.get_slot("booking_amount"))

        # Check if the user has sufficient balance
        has_sufficient_balance = user_balance >= booking_amount

        # Set the slot 'has_sufficient_balance' based on the check
        dispatcher.utter_message(f"Checking balance...")

        return [{"has_sufficient_balance": has_sufficient_balance}]
