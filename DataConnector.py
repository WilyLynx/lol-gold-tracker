import requests
import pandas as pd
import json


class DataConnector:
    API_endpoint = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
    items_file = 'item.json'

    def __init__(self):
        self.load_items()

    def load_items(self):
        with open('item.json', 'r') as f:
            data = json.load(f)
        d = []
        for k in data['data']:
            d.append({
                'item_id': k,
                'total_price': data['data'][k]['gold']['total']
            })
        items_df = pd.DataFrame(d)
        items_df['item_id'] = items_df['item_id'].astype(int)
        self.items_df = items_df.set_index('item_id')    

    def fetchData(self):
        f = requests.get(self.API_endpoint, verify=False).text
        data = json.loads(f)
        players_items_cost = []
        for p in data['allPlayers']:
            p0_items_ids = [i['itemID'] for i in p['items']]
            items_cost = self.items_df[self.items_df.index.isin(p0_items_ids)].sum().values[0]
            players_items_cost.append({
                'summoner': p['summonerName'],
                'champion': p['championName'],
                'items_cost': items_cost,
                'team': p['team']
            })
        return pd.DataFrame(players_items_cost).sort_values(by='items_cost', ascending=False)

