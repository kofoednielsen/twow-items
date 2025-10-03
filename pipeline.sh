lua <(cat ItemTooltipLogger.lua json_dump_snippet) | python3 parser.py > database.json
python3 json_to_csv.py

