# turtle-wow item database

Hello, i made this tool to generate a json/csv database of all turtle-wow gear. 

##  Output

If you're just interrested in the data, I published it here:

### JSON

https://files.pyjam.as/twow-items.json

### Google Sheet

> You have to make a copy or press the little calculator button in the top left corner and then *Create Filter View* to play with filters.

https://docs.google.com/spreadsheets/d/1vGJ2C119Z0MG7ffqzioCsOzzC1-pL8T5XoLpXPcFXWU

## How to run

### Requirements

* Linux / MacOS / or the Windows Subsystem for Linux thingy
* Lua
* Python3

### Running it

Use https://github.com/McPewPew/ItemTooltipLogger. Configure it to log only names and toolips, and do not save as CSV and then scan all items id's. I did from 0 to 120000. You end up with a `ItemTooltipLogger.lua` file containing all item tooltips.

Bring the `ItemTooltipLogger.lua` into the same directory as this repository and finally just run `pipeline.sh`

## How to edit the code

I mostly got gemini to write all the boring parser logic and wrote some tooling to help gemini look at the raw tooltip data, and find the resulting parsed items.

Check out GEMINI.md
