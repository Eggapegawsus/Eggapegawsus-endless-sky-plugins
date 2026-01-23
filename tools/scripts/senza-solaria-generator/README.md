# Senza Solaria Updater and Plugin Generator
This is a python script designed to parse through the Endless Sky directory or the plugin directory, and automatically make a plugin to be used alongside Senza Solaria.
<br>
<br>
It can also be used to parse through plugins to find a list of all outfits, ship models, and variants within the selected directory.
## How to Use

 - Start by copying the folder path of the plugin or game directory you wish to use (**NOTE: The selected directory MUST BE IN A FOLDER CALLED "plugins" "or" "Endless Sky")**
 - The script will then give you an option to output everything into either a single folder, or copy the original folder structure that it found the files in
 - It will then give you the option to have the base ship model listed along side thevariant in the "Ship Variants" file (I would advise "no" unless you are bug testing)
 - The script will then parse through the given directory, and find all ships and outfits, making mission for all found to be included in Senza Solaria, as well as making a file containing the names of all found outfits, ship models, and variants.
## More Info
This script will parse through a given directory for .txt files, and if it finds any matching an outfit or ship description, will give them a mission to be supported and used with Senza Solaria. This script is setup by default to work in the plugins folder, and in Endless Skys main folder (Specifically the steam release of the game).

NOTE: in order for the script to work, the target file or directory MUST BE LOCATED within a folder called "plugins" or "Endless Sky".
This is a safeguard to prevent the file from trying to scan an entire computers contents and causing who-knows-what kind of issues.

Feel free to use and modify this script as is needed.
