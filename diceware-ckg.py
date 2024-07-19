# import json
# import requests
import diceware_ckg_defs

DEBUG = True

# Number of dice rolls,
rolls = 6

# wordlist = requests.get("https://theworld.com/~reinhold/diceware.wordlist.asc")
# wordlist = requests.get ("https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt")
wordlistUrl = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"
words_dict = diceware_ckg_defs.Wordlist_dict(wordlistUrl)

dice = diceware_ckg_defs.Dieroll(rolls)

out = ""
for dieRoll in dice:
    # title does the capitalization
    out = out + words_dict[dieRoll].title()
print(out)
