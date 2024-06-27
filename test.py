import pandas as pd
import json

# read the json file data.json
# create a dataframe with 2 columns source and target
df = pd.DataFrame(columns=['source', 'target'])

with open('response.json', 'r') as f:
    data = json.load(f)
    for element in data['args']:
        print(element)
        print(data['args'][element])
        for obj in data['args'][element]:
            print('target', obj['target'])
            print('source', obj['source'])

            # new_row = {'source': obj['source'], 'target': obj['target']}
            new_row = {'source': str(obj['source']['value']) + ' ' + str(obj['source']['unit']), 'target': str(obj['target']['value']) + ' ' + str(obj['target']['unit'])}

            df = pd.concat([df, pd.DataFrame([new_row])])

df.to_csv('data.csv', index=False)
print(df)
