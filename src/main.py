import os

from discord.ext.commands import AutoShardedBot

from assist import Assistant
from top_api import top_setup

class AssistantDiscordBot(AutoShardedBot):
    """Responds to Discord User Queries"""

    def __init__(
            self,
            device_model_id=None,
            device_id=None,
            credentials=None,
            token=None,
            dbl_token=None):
        super(AssistantDiscordBot, self).__init__(
            command_prefix=None,
            fetch_offline_members=False
        )
        self.dbl_token = dbl_token
        self.assistant = Assistant(
            device_model_id=device_model_id,
            device_id=device_id,
            credentials=credentials,
            token=token
        )

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        if(self.dbl_token):
            top_setup(self, self.dbl_token)

    async def on_message(self, message):
        if message.author.bot:
            return
        lower_content = message.content.lower()
           
        if message.channel.id != '823581709064077373':
            return
            
        assistant_response = self.assistant.text_assist(lower_content)

        if assistant_response:
            await message.channel.send(assistant_response)


if __name__ == '__main__':
    device_model_id = os.environ.get('GA_DEVICE_MODEL_ID')
    device_id = os.environ.get('GA_DEVICE_ID')
    assistant_token = os.environ.get('GA_TOKEN')
    credentials = os.environ.get('GA_CREDENTIALS')

    discord_token = os.environ.get('DISCORD_TOKEN')

    client = AssistantDiscordBot(
        device_model_id=device_model_id,
        device_id=device_id,
        credentials=credentials,
        token=assistant_token
    )

    client.run(discord_token)
