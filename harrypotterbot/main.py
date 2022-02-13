from keep_alive import keep_alive
import os

import json
import requests
import discord

# Hugging Face profile link
API_URL = 'https://api-inference.huggingface.co/models/aishanisingh/'

class MyClient(discord.Client):
    def __init__(self, model_name):
        super().__init__()
        self.api_endpoint = API_URL + model_name
        huggingface_token = os.environ['HUGGINGFACE_TOKEN']

        # format the header in our request to Hugging Face
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(huggingface_token)
        }

    def query(self, payload):
        """
        make request to the Hugging Face model API
        """
        data = json.dumps(payload)
        response = requests.request('POST',
                                    self.api_endpoint,
                                    headers=self.request_headers,
                                    data=data)
        ret = json.loads(response.content.decode('utf-8'))
        return ret

    async def on_ready(self):
        # print when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
       
        self.query({'inputs': {'text': 'Hello!'}})

    async def on_message(self, message):
        """
        called whenever the bot sees a message in the channel
        """
        # ignore the message coming from itself
        if message.author.id == self.user.id:
            return

        # form query payload with the content of the message
        payload = {'inputs': {'text': message.content}}

        #set status as typing
        async with message.channel.typing():
          response = self.query(payload)
        bot_response = response.get('generated_text', None)
        
        # if ill-formed response
        if not bot_response:
            if 'error' in response:
                bot_response = '`Error: {}`'.format(response['error'])
            else:
                bot_response = 'Hmm... something is not right.'

        # sending the model's response to the Discord channel
        await message.channel.send(bot_response)

def main():
   
    client = MyClient('DialoGPT-small-harrypotter')
    
    keep_alive()
    client.run(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
  main()
