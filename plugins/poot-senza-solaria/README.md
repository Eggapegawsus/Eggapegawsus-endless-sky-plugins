**UPDATED 1/31/2026, for ES Unstable 0.11.0**
 - [Download v1.0.0](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/releases/tag/v1.0.0-senza-solaria-station) (Latest)

Senza Solaria was originally intended to be a part of a much larger plugin call Peripherals or Outstanding Trinkets (POOT), but gradually evolved into something I felt should be a standalone plugin. 

So without further ado...
  
<img width="850" height="200" alt="Image" src="https://github.com/user-attachments/assets/dd4eb70f-bdbf-4f2b-a688-1d66f94aa3a4" /><br>  
# Senza Solaria Station (All-Outfit Station)
Senza Solaria is a progressively expanding all-outfits and ship station where each outfit/ship has an unlock requirement:
 - In order for the outfit or ship to be sold, you have to **_donate the outfit or ship to Senza Solaria Station_**

<br>

## Senza Solaria's Features
I always enjoyed playing with all outfit plugins like Ursa Polaris or Omnis, although it always felt like there were some gripes or issues I had while playing with them. With this being my own personal take on what I'd like from an all outfits plugin, I decided to include some of my own special features:

 - The station is availible from the _very beginning_ of the game
 - There are a few different stations across the galaxy, to not have to jump across 40 Systems just to buy _one_ outfit
 - Items are unlocked on an _as-obtained_ basis, to keep balance somewhat reasonable (More info below)
 - Outfits and ships are supported (Variants are somewhat, see below)
 - Built in plugin support, with [templates](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/tree/main/plugins/poot-senza-solaria/TEMPLATES) for adding plugins
 - [Cost balance changes](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/blob/main/plugins/poot-senza-solaria/data/solaria-VANILLA-BALANCE-CHANGES.txt) to some vanilla outfits and ships not normally obtainable or not obtainable more than once
 - An [updater and plugin compatibility script](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/tree/main/tools/scripts/senza-solaria-generator) to quickly update the plugin for the base game or add another plugin's content.
   - The hope of this is to ensure the plugin does not go out of date overtime should updates cease in the future, while also not having it be an absolute _slog_ to add compatibility for plugins with hundreds of items.
<img width="400" height="400" alt="Image" src="https://github.com/user-attachments/assets/fe023c9a-bf53-41b6-b311-3b00d7c7200e" />
<br>

## Unlocking Outfits and Ships

- For outfits, the outfit **must be IN the cargohold** of one of your ships within the system when you land on Senza Solaria Station

- For ships, the ship **must be part of your fleet in the system when you land, but _NOT_ the flagship** _(This is done to prevent the station from trying to potentially take your only ship and leave you stranded, softlocked)_
  - **NOTE: Donations can ONLY BE MADE AT SENZA SOLARIA, IN RUTILICUS**, although outfits and ships that have been donated can still be purchased at any of the Solaria stations.

   - <img width="681" height="342" alt="Image" src="https://github.com/user-attachments/assets/67dedf0a-3826-4f6b-9cd3-c9f287d39fe0" />
<br>
<br>

Once you arrive at the station with the outfit or ship, you will be prompted to donate it. <br>
(_If you decline donating, you can still do it later_)

Once you have given up the item to the station, the next time you land on the station, it will be availible for purchase.

<br>

## Plugin Support and Updates (Python Script)
If you would like to add support for a plugin, or update Senza Solaria to the newest version of the game, be sure to use the [Senza Solaria Updater and Plugin Compatibility Script](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/tree/main/tools/scripts/senza-solaria-generator)
.
 - The script will scan through a given directory, (As long as it is in a folder called "plugins" or "Endless Sky") and find every outfit and ship, then produce a plugin that will add them to Senza Solaria.

<br>

## Notes on Variants of ships
Due to the current limitations of the Endless Sky plugin system, variants of ships cannot have their own missions. Instead, variants will have to be manually added to their base ship's mission.<br>
<br>
I have also decided to not have the script add variants automatically for a few reasons:
 - Outfits not yet availible in the maingame could be purchased early (I.E. unlock the Firebird, variants equiped with a Jump Drive would also be purchasable)
 - Certain variants not meant to be capturable or with broken stats would be purchasable

<br>

To make a variant unlock with the base ship, find the event for the ship inside the plugins files and add the variant name directly below the base model ship:

```
event "Senza Solaria Stocks Auxiliary (ship)"
	shipyard "Senza Solaria Plugin Ships"
		"Auxiliary"
		"Auxiliary (Cargo)"
		"Auxiliary (Transport)"
#This will make the "Cargo" and "Transport" variants unlock at Senza Solaria when the Auxiliary is donated
```

 - The script will also create a file that contains all variants detected in the scanned directory.

_this plugin supports the following plugins:_

 - [(POOT) Respawning Authors](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/tree/main/plugins/poot-respawning-authors)

