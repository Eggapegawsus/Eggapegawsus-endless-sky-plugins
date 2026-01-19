import re
import sys
import logging
from pathlib import Path


def senza_solaria_mission(outfit, thumbnail):
	return f"""
event `Senza Solaria Stocks {outfit}`
	outfitter "Senza Solaria Plugin Outfits"
		`{outfit}`
mission `Senza Solaria Supply {outfit}`
	invisible
	landing
	source
		planet "Senza Solaria"
	to offer
		has `outfit (cargo): {outfit}`
	on offer
		conversation
			scene "{thumbnail}"
			`Upon arriving at Senza Solaria, before you can even decide where to go, a group of researchers are already there to meet you the moment you step off of your ship.`
			`	"Our scanners detected an unknown outfit aboard your ship, would you be willing to donate it for us to reverse engineer?" says a researcher.`
			choice
				`	(Donate the {outfit} to be researched.)`
					goto donate
				`	(Don't donate.)`
					defer
			label donate
			`"Ah, perfect! We appreciate your donation, and assure you, your contribution will not go to waste!"`
			`The engineers carefully extract the donation from your ship, and take it to their research facility to reverse engineer."`
			``
			`	After idling at the spaceport for a few hours, you hear rumors of a new stock arriving soon at Senza Solaria.`
				accept
	on accept
		outfit `{outfit}` -1
		event `Senza Solaria Stocks {outfit}`
"""


def senza_solaria_mission_ship(ship, thumbnail):
	return f"""
event `Senza Solaria Stocks {ship}`
	shipyard "Senza Solaria Ships"
		`{ship}`

mission `Senza Solaria Supply {ship}`
	invisible
	landing
	source
		planet "Senza Solaria"
	to offer
		and	
			has `ship model: {ship}`
			not `flagship model: {ship}`
	on offer
		conversation
			scene "{thumbnail}"
			`Upon arriving at Senza Solaria With your {ship}, before you can even decide where to go, a group of researchers are already there to meet you the moment you step off of your ship.`
			`	"Our scanners detected a ship unknown to them within your fleet, would you be willing to donate it for us to research it?" says a researcher.`
			choice
				`	(Donate the {ship} to be researched.) WARNING: ALL INSTALLED OUTFITS WILL BE LOST.`
					goto donate
				`	(Don't donate.)`
					defer
			label donate
			`"Ah, perfect! We appreciate your donation, and assure you, your contribution will not go to waste!"`
			`The engineers guide your ship to an isolated landing pad a few miles from the spaceport, and carefully transport it inside of one of their research facilities."`
			``
			`	After idling at the spaceport for a few hours, you hear rumors of a new ship entering production soon at Senza Solaria.`
				accept
	on accept
		take ship `{ship}`
			"count" 1
		event `Senza Solaria Stocks {ship}`
"""


def find_ships_v3(input_filepath, output_single_folder, variants_source_ship):
	#List to store all found ships, and for all variants
	ship_list = []
	variant_list = []
	#Check to make sure a filepath was provided
	if not input_filepath.exists():
		print("No Filepath Detected!")
		return[]
	if not ("plugins" in input_filepath.parts or "plugin" in input_filepath.parts or "Endless Sky" in input_filepath.parts):
		print("Did not detect a folder named 'plugins' in the provided file directory. Please choose a folder within the plugins folder!")
		return []

	plugin_name = "_".join(input_filepath.name.lower().split())
	
	#The search for ships
	ship_name_definition = r'^ship\s+(.*)$'
	ship_name_compiled = re.compile(ship_name_definition, re.MULTILINE)
	
	export_location = input_filepath / (f"{plugin_name}_senza_solaria")
	export_location.mkdir(parents=True, exist_ok=True)
	
	allunlock_export = export_location / f"{plugin_name}.senza.all.ships.txt"
	allunlock_export.write_text(f"shipyard `Senza Solaria Unlockall Ships Plugin`\n")
	
	
	#Finds all file paths, if its a file it prints its name, then will try to read it and find all ships.
	for file_path in input_filepath.rglob("*.txt"):
		if export_location in file_path.parents or "new_missions" in file_path.parts: continue
		if file_path.is_file():
			print(f"\n--- Reading file: {file_path.name}")
			try:
				with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
					plugin_content = f.read()
					
					#Checks if an ship is a variant, then if it has a category
					discovered_ships = []
					for actual_ship in ship_name_compiled.finditer(plugin_content):
						actual_ship_found_test = actual_ship.group(1).strip()
						actual_ship_parts = re.findall(r'[^"\s]+|"[^"]*"|`[^`]*`', actual_ship_found_test)
						if not actual_ship_parts:
							continue
						
						actual_ship_parts = [p.strip('`"') for p in actual_ship_parts]
						if len(actual_ship_parts) >= 2:
							if variants_source_ship == True:
								actual_ship_found = f"`{actual_ship_parts[0]}` `{actual_ship_parts[1]}`"
							else:
								actual_ship_found = f"`{actual_ship_parts[1]}`"
							variant_detected = True
							variant_named = f"{actual_ship_parts[0]} +{actual_ship_parts[1]}"
							variant_named_true = f"{actual_ship_parts[1]}"
						else:
							actual_ship_found = actual_ship_parts[0]
							variant_detected = False
						
						if not actual_ship_found or not actual_ship_found.strip():
							print("No actual ship found, skipping...")
							continue
						
						#Searches for 1000 characters after the ship"" has been found
						ship_search = plugin_content[actual_ship.end() : actual_ship.end() +1000]
						
						#specifies to check for 20 lines after its own
						ship_lines_check = ship_search.split('\n')[:21]
						
						#New verification for ships
						ship_verification = []
						for line in ship_lines_check:
							strippedline = line.strip()
							if not strippedline:
								continue
							if line.startswith(('\t', '	')):
								ship_verification.append(line)
							else:
								break
						
						ship_lines_check_full = "\n".join(ship_verification)
						
						#Actual category check
						ship_has_category = any(o.lower().strip().startswith("category") for o in ship_verification)
						ship_has_thumbnail = any(o.lower().strip().startswith("thumbnail") for o in ship_verification)
						ship_has_sprite = any(o.lower().strip().startswith("sprite") for o in ship_verification)
						if ship_has_category or variant_detected:
							thumbnail_name = "ship/unknown"
							thumbnail_found = False
							
							if ship_has_thumbnail:
								ship_has_thumbnail_search = re.search(r'thumbnail `(.*?)`|thumbnail "(.*?)"|thumbnail ([^\s\n]+)', ship_lines_check_full)
								if ship_has_thumbnail_search:
									thumbnail_test = (ship_has_thumbnail_search.group(1) or ship_has_thumbnail_search.group(2) or ship_has_thumbnail_search.group(3) or "").strip()
									if thumbnail_test:
										thumbnail_name = thumbnail_test
										thumbnail_found = True
										print(f"Thumbnail found for {actual_ship_found}")
							if not thumbnail_found and ship_has_sprite:
								ship_has_sprite_search = re.search(r'sprite `(.*?)`|sprite "(.*?)"|sprite ([^\s\n]+)', ship_lines_check_full)
								if ship_has_sprite_search:
									ship_has_sprite_test = (ship_has_sprite_search.group(1) or ship_has_sprite_search.group(2) or ship_has_sprite_search.group(3) or "").strip()
									if ship_has_sprite_test:
										thumbnail_name = ship_has_sprite_test
										print(f"No thumbnail found for {actual_ship_found}, found sprite instead")
									else:
										thumbnail_name = 'ship/unknown'
										print(f"No sprite detected, implementing ship/unknown to {actual_ship_found}")
							
							ship_and_thumbnail = (actual_ship_found, thumbnail_name)
							
							#Variant Detection
							if variant_detected:
								if not any(o[0] == actual_ship_found for o in variant_list):
									variant_list.append(ship_and_thumbnail)
							else:
							#A boolean to check if anything was already in discovered_ships, then if it was in ship_list. if it doesn't find anything, it will make the tuple and add it to the lists
								if not any(o[0] == actual_ship_found for o in discovered_ships):
									ship_and_thumbnail = (actual_ship_found, thumbnail_name)
									discovered_ships.append(ship_and_thumbnail)
									if not any(o[0] == actual_ship_found for o in ship_list):
										ship_list.append(ship_and_thumbnail)
						else:
							print(f"{actual_ship_found} does not have a category defined, skipping")
				
				
				if discovered_ships:
					if not allunlock_export.exists():
						allunlock_export.write_text(f"shipyard `Senza Solaria Unlockall Ships Plugin`\n")
					if not output_single_folder:
						#Creates a subfolder for any ships that are detected within text files scanned
						base_folder_path = file_path.relative_to(input_filepath)
						ship_subfolder = export_location / base_folder_path.parent
						ship_subfolder.mkdir(parents=True, exist_ok=True)
				
						found_location = "\n".join([senza_solaria_mission_ship(o[0], o[1]) for o in discovered_ships])
						new_file_for_ships = ship_subfolder / f"{plugin_name}_{file_path.stem}.txt".replace("_", ".")
						with open(new_file_for_ships, 'a', encoding='utf-8') as f:
							f.write("\n" + found_location)
				else:
					print("TOUGH LUCK BUDDY, nothin found!")
			
			except UnicodeDecodeError:
				print(f"Apologies, couldn't read {file_path} because of unicode issue")
			except IOError as e:
				print(f"Apologies, couldn't read {file_path} due to IOError: {e}")
	if output_single_folder and ship_list:
		single_file = export_location / (f"senza_ships_{plugin_name}.txt")
		single_file_text = "\n".join([senza_solaria_mission_ship(o[0], o[1]) for o in ship_list])
		single_file.write_text(single_file_text, encoding='utf-8')
	if ship_list:
		with open(allunlock_export, 'a', encoding='utf-8', errors='ignore') as f:
			for ship_tuple_thing in ship_list:
				ship_name_tuple = ship_tuple_thing[0]
				f.write(f"\t`{ship_name_tuple}`\n")
	if variant_list:
		veriant_file = export_location / f"variants.in.{plugin_name}.txt"
		with open(veriant_file, 'w', encoding='utf-8', errors='ignore') as f:
			f.write(f"#Variants found in files, be sure to add these to their proper missions based on the ship they are a variant of if you wish to be able to purchase them\n\n")
			for variant_tuple in variant_list:
				f.write(f"\t{variant_tuple[0]}\n")

	return ship_list + variant_list



def find_outfits_v2(input_filepath, output_single_folder):
	#List to store all found outfits
	outfit_list = []
	#Check to make sure a filepath was provided
	if not input_filepath.exists():
		print("No Filepath Detected!")
		return[]
	if not ("plugins" in input_filepath.parts or "plugin" in input_filepath.parts or "Endless Sky" in input_filepath.parts):
		print("Did not detect a folder named 'plugins' in the provided file directory. Please choose a folder within the plugins folder!")
		return []

	plugin_name = "_".join(input_filepath.name.lower().split())
	
	#The search for outfits
	outfit_name_definition = r'^outfit `(.*?)`|^outfit "(.*?)"|^outfit ([^\s\n]+)'
	outfit_name_linecheck = r'outfit `|outfit "|outfit '
	outfit_name_compiled = re.compile(outfit_name_definition, re.MULTILINE)
	
	export_location = input_filepath / (f"{plugin_name}_senza_solaria")
	export_location.mkdir(parents=True, exist_ok=True)
	
	allunlock_export = export_location / f"{plugin_name}.senza.all.outfits.txt"
	allunlock_export.write_text(f"outfitter `Senza Solaria Unlockall Outfits Plugin`\n")
	
	
	#Finds all file paths, if its a file it prints its name, then will try to read it and find all outfits.
	for file_path in input_filepath.rglob("*.txt"):
		if export_location in file_path.parents or "new_missions" in file_path.parts: continue
		if file_path.is_file():
			print(f"\n--- Reading file: {file_path.name}")
			try:
				with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
					plugin_content = f.read()
					
					#Checks if an outfit has a category
					discovered_outfits = []
					for actual_outfit in outfit_name_compiled.finditer(plugin_content):
						actual_outfit_found = actual_outfit.group(1) or actual_outfit.group(2) or actual_outfit.group(3)
						
						if not actual_outfit_found or not actual_outfit_found.strip():
							print("No actual outfit found, skipping...")
							continue
						
						#Searches for 1000 characters after the outfit"" has been found
						outfit_search = plugin_content[actual_outfit.end() : actual_outfit.end() +1000]
						
						#specifies to check for 20 lines after its own
						outfit_lines_check = outfit_search.split('\n')[:21]
						
						#New verification for outfits
						outfit_verification = []
						for line in outfit_lines_check:
							strippedline = line.strip()
							if not strippedline:
								continue
							if line.startswith(('\t', '	')):
								outfit_verification.append(line)
							else:
								break
						
						outfit_lines_check_full = "\n".join(outfit_verification)
						
						#Actual category check
						outfit_has_category = any(o.lower().strip().startswith("category") for o in outfit_verification)
						outfit_has_thumbnail = any(o.lower().strip().startswith("thumbnail") for o in outfit_verification)
						if outfit_has_category:
							thumbnail_name = "outfit/unknown"
							if outfit_has_thumbnail:
								outfit_has_thumbnail = re.search(r'thumbnail `(.*?)`|thumbnail "(.*?)"|thumbnail ([^\s\n]+)', outfit_lines_check_full)
								outfit_has_sprite = re.search(r'sprite `(.*?)`|sprite "(.*?)"|sprite ([^\s\n]+)', outfit_lines_check_full)
								if outfit_has_thumbnail:
									thumbtest1 = outfit_has_thumbnail.group(1)
									thumbtest2 = outfit_has_thumbnail.group(2)
									thumbtest3 = outfit_has_thumbnail.group(3)
									unprocessed_thumbnail_name = (thumbtest1 or thumbtest2 or thumbtest3 or "").strip()
									if unprocessed_thumbnail_name == "":
										thumbnail_name = "outfit/unknown"
										print(f"No thumbnail detected, implementing outfit/unknown to {actual_outfit_found}")
									else:
										thumbnail_name = unprocessed_thumbnail_name
								else:
									thumbnail_name = 'outfit/unknown'
							
							#A boolean to check if anything was already in discovered_outfits, then if it was in outfit_list. if it doesn't find anything, it will make the tuple and add it to the lists
							if not any(o[0] == actual_outfit_found for o in discovered_outfits):
								outfit_and_thumbnail = (actual_outfit_found, thumbnail_name)
								discovered_outfits.append(outfit_and_thumbnail)
								if not any(o[0] == actual_outfit_found for o in outfit_list):
									outfit_list.append(outfit_and_thumbnail)
						else:
							print(f"{actual_outfit_found} does not have a category defined, skipping")
				
				
				if discovered_outfits:
					if not allunlock_export.exists():
						allunlock_export.write_text(f"outfitter `Senza Solaria Unlockall Outfits Plugin`\n")
					if not output_single_folder:
						#Creates a subfolder for any outfits that are detected within text files scanned
						base_folder_path = file_path.relative_to(input_filepath)
						outfit_subfolder = export_location / base_folder_path.parent
						outfit_subfolder.mkdir(parents=True, exist_ok=True)
				
						found_location = "\n".join([senza_solaria_mission(o[0], o[1]) for o in discovered_outfits])
						new_file_for_outfits = outfit_subfolder / f"{plugin_name}_{file_path.stem}.txt".replace("_", ".")
						with open(new_file_for_outfits, 'a', encoding='utf-8') as f:
							f.write("\n" + found_location)
				else:
					print("TOUGH LUCK BUDDY, nothin found!")
			
			except UnicodeDecodeError:
				print(f"Apologies, couldn't read {file_path} because of unicode issue")
			except IOError as e:
				print(f"Apologies, couldn't read {file_path} due to IOError: {e}")
	if output_single_folder and outfit_list:
		single_file = export_location / (f"senza_outfits_{plugin_name}.txt")
		single_file_text = "\n".join([senza_solaria_mission(o[0], o[1]) for o in outfit_list])
		single_file.write_text(single_file_text, encoding='utf-8')
	if outfit_list:
		with open(allunlock_export, 'a', encoding='utf-8', errors='ignore') as f:
			for outfit_tuple_thing in outfit_list:
				outfit_name_tuple = outfit_tuple_thing[0]
				f.write(f"\t`{outfit_name_tuple}`\n")

	return outfit_list

#The main script loop
while True:
#	gets a directory and removes quotes
	temp_input_filepath = input("Please give a directory to search: ").strip().strip('"').strip("'")
	input_filepath = Path(temp_input_filepath).resolve()

#A check to see if the user wants everything to be in a single file, or in individual files
	while True:
		single_folder_test = input("Do you want to have the output go into a single file? (y/n): ").lower().strip()
		if single_folder_test in ("y", "yes", "yeah", "1"):
			output_single_folder = True
			break
		elif single_folder_test in ("n", "no", "nope", "0"):
			output_single_folder = False
			break
		else:
			print("Invalid input, please try again (y/n): ")
	while True:
		variants_source_test = input("Do you want to have the output for varients list the original ship model? (y/n): ").lower().strip()
		if variants_source_test in ("y", "yes", "yeah", "1"):
			variants_source_ship = True
			break
		elif variants_source_test in ("n", "no", "nope", "0"):
			variants_source_ship = False
			break
		else:
			print("Invalid input, please try again (y/n): ")
	
	outfits_discovered = find_outfits_v2(input_filepath, output_single_folder)
	for outfit in outfits_discovered:
		print(f"{outfit} detected!")
		  
	ships_discovered = find_ships_v3(input_filepath, output_single_folder, variants_source_ship)
	for ship in ships_discovered:
		print(f"{ship} detected!")

	multi_input_loop = input('Plugin processing complete! Would you like to process another plugin? (y/n): ').lower().strip()
	if multi_input_loop in ("n", "no", "nope", "0"):
		print("Very well, thank you for using Senza Solaria!")
		break