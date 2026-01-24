**UPDATED 1/18/2026, for ES 1.16.0**

Senza Solaria was originally intended to be a part of a much larger plugin call Peripherals or Outstanding Trinkets (poot), but gradually evolved into something I felt should be a standalone plugin.
  
<img width="850" height="200" alt="Image" src="https://github.com/user-attachments/assets/dd4eb70f-bdbf-4f2b-a688-1d66f94aa3a4" /><br>  
# Senza Solaria Station (All-Outfit Station)
Senza Solaria is a progressively expanding all-outfits and ship  station with a special requirement for something to be purchasable:
 - In order for any of the stations to sell an outfit or ship, you have to **_bring the outfit or ship to the station_**

## Senza Solaria's Features
I always enjoyed playing with all outfit plugins like Ursa Polaris or Omnis, although it always felt like there were some issues I had while playing with them. With this being my own personal take on what I'd like from an all outfits plugin, I decided to include some of my own special features to "fix" any issues I had:

 - The station is availible from the beginning of the game
 - Items are unlocked on an as-obtained basis (More info below)
 - Outfits and ships are supported (Variables are somewhat, see below)
 - Built in plugin support, with templates for adding plugins
 - A compatibility script to quickly update the mod for the base game or plugin content (More info Below)
 - Cost balance changes to some vanilla outfits not normally obtainable more than once

## Unlocking Outfits and Ships
- For outfits, the outfit **must be IN the cargohold** of one of your ships within the system
- For ships, the ship **must be in your fleet in the system, but NOT the flagship** _(This is done to prevent the station from trying to potentially take your only ship and leave you stranded, softlocked)_



Once you arrive at the station with the item, you will be prompted to donate the item (And don't worry about refusing to donate at the moment, you can always do it anytime in the future).
Once you have given up the item to the station, the next time you land on the station, it will be availible for purchase



 - **NOTE: Donations can ONLY BE MADE AT SENZA SOLARIA, IN RUTILICUS**, although outfits that have been donated can still be purchased at any of the Solaria stations.


## Plugin Support and Updates (Python Script)
If you would like to add support for a plugin, or update Senza Solaria to the newest version of the game, be sure to use the [Senza Solaria Generator script](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/tree/main/tools/scripts/senza-solaria-generator)
.
 - The script will scan through a given directory, (As long as it is in a folder called "plugins" or "Endless Sky") and find every outfit and ship, then produce files that when placed inside of a plugins data folder, will add them to Senza Solaria.

## Notes on Variants of ships
Due to the current limitations of the Endless Sky plugin system, variants of ships cannot have their own missions. Instead, variants will have to be manually added to their base ship's mission.<br>
<br>
I have also decided to not have the script add variants automatically for a number of reasons:
 - It could allow for outfits that have not been encountered to be purchasable
 - Outfits not yet availible in the maingame could be purchased early (I.E. obtain a Vanguard, variants with a jump would also be purchasable)
 - Certain variants not meant to be capturable or with broken stats would be purchasable
<br>
<br>
To add varaints, just find the mission of the ship in the file with missions, and add it to the event directly above the mission which adds the ship to an outfitter.

 - The script will also create a file that contains all variants detected in the scanned directory.
