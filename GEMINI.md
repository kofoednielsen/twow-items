## Gemini Added Memories
- You are writing a parser.py to convert the human readable item tooltips into a nice spreadsheet with stats that can be easily sorted and filtered.

### How to run
Run the follwing command
```
./pipeline.sh
```
Output can be found in database.json and database.csv

### How to inspect items
You can use the follow command to look at items from the parser result database.json
```
python3 sample.py "Distracting Dagger" "Anasterian's Legacy" | jq
```

To look at the raw tooltip data of an item, use:
```
raw_sample.sh "Distracting Dagger"
```
This command can only look at one item at a time
