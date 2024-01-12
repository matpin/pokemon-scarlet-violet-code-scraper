from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
webhook_url = os.environ.get('WEBHOOK_URL')


def notify_discord(codes):
    if len(codes) == 0:
        return
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title="New codes", color="03b2f8")
    for code in codes:
        embed.add_embed_field(name=f'Code: {code["code"]}',
                              value=f'Gift: {code["gift"]}\nExpires on: {code["expire_date"]}',
                              inline=False)
    webhook.add_embed(embed)
    webhook.execute()
