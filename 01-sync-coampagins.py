import discord
import requests
import json

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)



channel_id = 12121212
bot_token = 'ABABABAB'
currentId = 2155


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} (ID: {client.user.id})')

    # Get the channel by ID
    channel = client.get_channel(int(channel_id))

    url = 'https://api.taskon.xyz/v1/getCampaignList'
    headers = {'Content-Type': 'application/json'}
    data = {'page': {"page_no": 0, "size": 50},
            "options": {"campaign_status": "OnGoing", "user_campaign_status": "All", "name_line": ""}}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_data = json.loads(response.content)
        filter_idList = [obj['id'] for obj in response_data['result']['data'] if obj['id'] > currentId]
        sorted_id_list = sorted(filter_idList)

        infoUrl = 'https://api.taskon.xyz/v1/getCampaignInfo'
        infoheaders = {'Content-Type': 'text/plain'}

        for id in sorted_id_list:
            response = requests.post(infoUrl, headers=infoheaders, data=str(id))
            if response.status_code == 200:
                response_data = json.loads(response.content)
                result_data = response_data['result']
                rewardsList = result_data['winner_rewards']

                expAmt = 0
                for reward in rewardsList:
                    if reward['reward_type'] == 'Exp':
                        expAmt = reward['reward_params']['per_amount']

                await channel.send(
                    'New Campaigns Live on TaskOn @everyone  \n \n  ' + '👉 https://taskon.xyz/campaign/detail/' + str(
                        id) + '  \n \n' +

                    result_data['name'] + '.  \n  \n'

                                          '🏆 Prize Pool:  Whitelists \n  \n'

                                          '⭐ ' + str(expAmt) + 'EXP ⭐ Raffle \n \n'

                                                               'TaskOn enables you to easily find campaigns and start earning. \n \n'

                                                               'This is a third-party event held via the TaskOn platform and is not endorsed by TaskOn in any form. \n \n' +

                    result_data['image'])



client.run(bot_token)
