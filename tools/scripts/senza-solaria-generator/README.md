UPDATED 1/31/2026 for ES Unstable 0.11.0 

 - [Download v5.6.1](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/releases/tag/v1.0.1-SCRIPT-senza-solaria-updater) (Latest)
 - _Designed to be used with [Senza Solaria Station](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/tree/main/plugins/poot-senza-solaria)_


# Senza Solaria Updater and Plugin Compatibility Generator
This is a python script designed to parse through the Endless Sky directory or the plugin directory, and automatically make a plugin to allow all found outfits and ships in the directory to be used in Senza Solaria.
<br>
<br>
For plugin makers, it also has the bonus feature of quickly parsing through plugins or the base game's files to create a list of all found outfits, ship models, and variants within the selected directory. 
## How to Use

 - Start by opening the [Python Script or Windows Program](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/releases/tag/v1.0.1-SCRIPT-senza-solaria-updater), then copy the folder path of the plugin or game directory you wish to use (**NOTE: The selected directory MUST BE IN A FOLDER CALLED "plugins" or "Endless Sky")**
  
 - You can then choose to output everything into either a single folder or copy the folder structure of the selected directory (Keep it as single folder output for simplifying updating files in the future, multi-folder output for testing/debugging)
  
 - You can then choose to have the base ship model listed along side the variant in the "Ship Variants" file (Choose "No", unless you are testing/debugging something)
  
 - The script will then parse through the given directory, and find all ships and outfits, making a mission for each item found to be included in Senza Solaria, as well as making a file containing the names of all found outfits, ship models, and variants for the "unlock all" start.

<br>

 - **QUICKLY ADDING PLUGIN SUPPORT:** If you set the target directory of the script to Endless Sky's "plugins" folder (on windows for example, "C:\Users\USERNAME\AppData\Roaming\endless-sky\plugins" ), it will then make a ready-to-go plugin for every outfit and ship within the plugins folder, ready to be used the next time the game is launched.

      - **NOTE: This WILL add missions for content from disabled plugins.** This shouldn't be much of an issue, but will still show up in the errors.txt file

## More Info
**Adding Missing Ships or Outfits**

 - If for any reason the script misses a ship or outfit, Senza Solaria has [Outfit and Ship templates](https://github.com/Eggapegawsus/Eggapegawsus-endless-sky-plugins/tree/main/plugins/poot-senza-solaria/TEMPLATES) that can be used to quickly add a missing item. just copy the text and replace SAMPLESHIP or SAMPLEOUTFIT with the name of the missing item.
 - Also copy the items thumbnail or sprite and paste it between the quotes in _scene ""_ if you want it to have a visual image for when it is brought to the station

<br>
<br>

**Information for ships**
 - The script will attempt to first find a thumbnail for the ship, if it does not locate the thumbnail, it will then use the base sprite for the ship. If that fails, it will use outfit/unknown
  
 - Within the generated variants file, there is also an option at the top to include all detected variants in the "unlock-all" shop, by deleting the '#' infront of the shop line
  
 - If a ship within the scanned files does not have a designated category (I.E. "Heavy Warship", "Freighter") and has a base ship model ("Archon" "Archon (B)"), it will be considered a variant and added to the variants list
  
 - If it does not have a designated category and also lacks a base ship, it will be skipped and not added to the output plugin files

<br>
<br>

**Information for outfits**
 - The script will attempt to find the outfit image for said outfit, if it fails to find it, it will default to outfit/unknown
  
 - If an outfit lacks a category, it will be skipped and not added to the output plugin files

<br>
<br>

**Additional Information**
 - Inputing a directory with an already existing output folder from the script will update the existing files and leave any already existing ships and outfits. This can be used to update an already existing script output without wiping any custom or edited text in the existing files. This can be useful if you want to add variants to unlock along side the base model of a ship. (**NOTE: ALWAYS be sure to make a BACKUP of existing files before attempting to update them)**

<br>

 - In order for the script to work, **the target file or directory MUST BE LOCATED within a folder called "plugins" or "Endless Sky"**.
This is a safeguard to prevent the script from trying to scan an entire computers contents and causing who-knows-what kind of issues.


Feel free to use and modify this script as is needed, and thank you to those using Senza Solaria!
