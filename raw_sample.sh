lua <(cat ItemTooltipLogger.lua json_dump_snippet) | jq ".[] | select(.Name == \"$1\")"
