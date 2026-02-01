import re
from pathlib import Path


def senza_solaria_mission_outfit(outfit, thumbnail):
	return f"""
event `Senza Solaria Stocks {outfit} (outfit)`
	outfitter "Senza Solaria Plugin Outfits"
		`{outfit}`
mission `Senza Solaria Supply {outfit} (outfit)`
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
		event `Senza Solaria Stocks {outfit} (outfit)`
"""


def senza_solaria_mission_ship(ship, thumbnail):
	return f"""
event `Senza Solaria Stocks {ship} (ship)`
	shipyard "Senza Solaria Plugin Ships"
		`{ship}`

mission `Senza Solaria Supply {ship} (ship)`
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
		event `Senza Solaria Stocks {ship} (ship)`
"""

#Name fixer for appending existing files
def fixnames_v1(text):
	return text.replace('`', '')

def foundthing_verification(content, start_pos):
	foundthing_content = []
	foundthing_lines = content[start_pos:].splitlines()
	
	for line in foundthing_lines:
		strippedline = line.strip()
		if not strippedline:
			foundthing_content.append(line)
			continue
			
		foundthing_indented = len(line) > 0 and line[0].isspace()
		foundthing_commented = strippedline.startswith('#')
	
		if not foundthing_indented and not foundthing_commented:
			break
		foundthing_content.append(line)
	
	return foundthing_content

def find_ships_v4(input_filepath, output_single_folder, variants_source_ship):
	#List to store all found ships, and for all variants
	ship_list = []
	variant_list = []
	ship_set = set()
	variant_set = set()
	#Check to make sure a filepath was provided
	if not input_filepath.exists():
		print("No Filepath Detected!")
		return[]
	if not ("plugins" in input_filepath.parts or "plugin" in input_filepath.parts or "Endless Sky" in input_filepath.parts):
		print("Did not detect a folder named 'plugins' in the provided file directory. Please choose a folder within the plugins folder!")
		return []

	plugin_name = "_".join(input_filepath.name.lower().split())
	
	#The search for ships
	ship_name_definition = r'^ship\s+([^\n\r]*?)(?=\s*#|$)'
	ship_name_compiled = re.compile(ship_name_definition, re.MULTILINE)
	
	export_location = input_filepath / (f"{plugin_name}_senza_solaria") / "data"
	export_location.mkdir(parents=True, exist_ok=True)
	
	allunlock_export = export_location / f"{plugin_name}.senza.all.ships.txt"
	if not allunlock_export.exists():
		allunlock_export.write_text(f"shipyard `Senza Solaria Unlockall Ships Plugin`\n")
	
	#Checking if the mission already exists, or if it is within the variant or unlockall file
	existing_missions = set()
	for existing_file in export_location.rglob("*.txt"):
		if existing_file.is_file():
			if ".variants" in existing_file.name or ".all." in existing_file.name:
				continue
			existing_content = existing_file.read_text(encoding='utf-8', errors='ignore')
			existing_found = re.findall(r"event `Senza Solaria Stocks (.*?) \(ship\)`", existing_content)
			for name in existing_found:
				existing_missions.add(f"ship_{fixnames_v1(name)}")
		
	

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
							print("No actual ship found, skipping...")
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
							variant_set.add(actual_ship_found)
						else:
							actual_ship_found = actual_ship_parts[0]
							variant_detected = False
						
						existing_ship = actual_ship_found.strip('`"')
						
						#New verification for ships
						ship_verification = foundthing_verification(plugin_content, actual_ship.end())
						
						ship_lines_check_full = "\n".join(ship_verification)
						
						#Actual category check
						ship_has_category = any(line.strip().lower().lstrip('"`').startswith("category") for line in ship_verification)
						ship_has_thumbnail = any(o.lower().strip().startswith(("thumbnail", '"thumbnail"', "`thumbnail`")) for o in ship_verification)
						
						
							#Thuimbnail detection
						ship_has_sprite = any(o.lower().strip().startswith(("sprite", '"sprite"', "`sprite`")) for o in ship_verification)
						thumbnail_name = "outfit/unknown"
						thumbnail_found = False
						
						if ship_has_thumbnail:
							ship_thumbnail_temp = r'["`]?thumbnail["`]?\s+["`]?([^`"\n\r]+)["`]?'
							ship_has_thumbnail_search = re.search(ship_thumbnail_temp, ship_lines_check_full, re.IGNORECASE)
							if ship_has_thumbnail_search:
								thumbnail_test = ship_has_thumbnail_search.group(1).strip()
								if thumbnail_test:
									thumbnail_name = thumbnail_test
									thumbnail_found = True
									print(f"Thumbnail found for {actual_ship_found}")
						
						if not thumbnail_found and ship_has_sprite:
							ship_sprite_temp = r'["`]?sprite["`]?\s+["`]?([^`"\n\r]+)["`]?'
							ship_has_sprite_search = re.search(ship_sprite_temp, ship_lines_check_full, re.IGNORECASE)
							if ship_has_sprite_search:
								sprite_test = ship_has_sprite_search.group(1).strip()
								if sprite_test:
									thumbnail_name = sprite_test
									print(f"No thumbnail found for {actual_ship_found}, found sprite instead")
							
						ship_and_thumbnail = (actual_ship_found, thumbnail_name)
							
						#A boolean to check if anything was already in discovered_ships, then if it was in ship_list. if it doesn't find anything, it will make the tuple and add it to the lists
						
						if variant_detected:
							if not any(o[0] == actual_ship_found for o in variant_list):
								variant_list.append(ship_and_thumbnail)
						if ship_has_category:
							if not variant_detected:
								ship_set.add(existing_ship)
								
								if f"ship_{fixnames_v1(actual_ship_found)}" not in existing_missions:
									if not any(o[0] == actual_ship_found for o in discovered_ships):
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
	all_found_ships = sorted(list(ship_set))
	
	if all_found_ships:
		with open(allunlock_export, 'w', encoding='utf-8', errors='ignore') as f:
			f.write(f"shipyard `Senza Solaria Unlockall Ships Plugin`\n")
			for ship_name in all_found_ships:
				f.write(f"\t`{ship_name}`\n")
	if output_single_folder and ship_list:
		single_file = export_location / (f"{plugin_name}_senza_ships.txt")
		single_file_text = "\n".join([senza_solaria_mission_ship(o[0], o[1]) for o in ship_list])
		with open(single_file, 'a', encoding='utf-8') as f:
			f.write("\n" + single_file_text)
	if variant_set:
		variant_file = export_location / f"{plugin_name}.variants.txt"
		with open(variant_file, 'w', encoding='utf-8', errors='ignore') as f:
			if variant_file.stat().st_size == 0:
				f.write(f"#Variants found in files, be sure to add these to their proper missions based on the ship they are a variant of if you wish to be able to purchase them\n#If you would like to make these availible for purchase when playing with everything unlocked, remove the `#` infront of the next line.\n#shipyard `Senza Solaria Unlockall Ships Plugin`\n")
			for variant_name in sorted(list(variant_set)):
				f.write(f"\t{variant_name}\n")

	return ship_list



def find_outfits_v4(input_filepath, output_single_folder):
	#List to store all found outfits, and for all variants
	outfit_list = []
	outfit_set = set()
	#Check to make sure a filepath was provided
	if not input_filepath.exists():
		print("No Filepath Detected!")
		return[]
	if not ("plugins" in input_filepath.parts or "plugin" in input_filepath.parts or "Endless Sky" in input_filepath.parts):
		print("Did not detect a folder named 'plugins' in the provided file directory. Please choose a folder within the plugins folder!")
		return []

	plugin_name = "_".join(input_filepath.name.lower().split())
	
	#The search for outfits
	outfit_name_definition = r'^outfit\s+(.*?)(?=#|$)'
	outfit_name_compiled = re.compile(outfit_name_definition, re.MULTILINE)
	
	export_location = input_filepath / (f"{plugin_name}_senza_solaria") / "data"
	export_location.mkdir(parents=True, exist_ok=True)
	
	allunlock_export = export_location / f"{plugin_name}.senza.all.outfits.txt"
	if allunlock_export.exists():
		allunlock_content = allunlock_export.read_text(encoding='utf-8', errors='ignore')
		allunlock_existing_content = re.findall(r"`(.*?)`", allunlock_content)
		outfit_set.update(allunlock_existing_content)
	else:
		allunlock_export.write_text(f"outfitter `Senza Solaria Unlockall Outfits Plugin`\n")
	
	#Checking if the mission already exists, or if it is within the variant or unlockall file
	existing_missions = set()
	for existing_file in export_location.rglob("*.txt"):
		if existing_file.is_file() and ".all." not in existing_file.name:
			existing_content = existing_file.read_text(encoding='utf-8', errors='ignore')
			existing_found = re.findall(r"event `Senza Solaria Stocks (.*?) \(outfit\)`", existing_content)
			for name in existing_found:
				existing_missions.add(f"outfit_{fixnames_v1(name)}")
		
	

	#Finds all file paths, if its a file it prints its name, then will try to read it and find all outfits.
	for file_path in input_filepath.rglob("*.txt"):
		if export_location in file_path.parents or "new_missions" in file_path.parts: continue
		if file_path.is_file():
			print(f"\n--- Reading file: {file_path.name}")
			try:
				with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
					plugin_content = f.read()
					
					#Checks if an outfit is a variant, then if it has a category
					discovered_outfits = []
					for actual_outfit in outfit_name_compiled.finditer(plugin_content):
						actual_outfit_found_test = actual_outfit.group(1).strip()
						actual_outfit_found = re.sub(r'^["`](.*)["`]$', r'\1', actual_outfit_found_test)
						
						#New verification for outfits
						outfit_verification = foundthing_verification(plugin_content, actual_outfit.end())
						
						outfit_lines_check_full = "\n".join(outfit_verification)
						
						#Actual category check
						outfit_has_category = any(line.strip().lower().lstrip('"`').startswith("category") for line in outfit_verification)
						
						#Verification for updating an existing all.outfits file
						if outfit_has_category:
							outfit_set.add(actual_outfit_found)
						else:
							print(f"{actual_outfit_found} does not have a category defined, skipping")
						
						
						#Thumbnail processing
						outfit_has_thumbnail = any(o.lower().strip().startswith(("thumbnail", '"thumbnail"', "`thumbnail`")) for o in outfit_verification)
						thumbnail_name = "outfit/unknown"
						thumbnail_found = False
						
						if outfit_has_thumbnail:
							outfit_thumbnail_temp = r'["`]?thumbnail["`]?\s+["`]?([^`"\n\r]+)["`]?'
							outfit_has_thumbnail_search = re.search(outfit_thumbnail_temp, outfit_lines_check_full, re.IGNORECASE)
							if outfit_has_thumbnail_search:
								thumbnail_test = outfit_has_thumbnail_search.group(1).strip()
								if thumbnail_test:
									thumbnail_name = thumbnail_test
									thumbnail_found = True
									print(f"Thumbnail found for {actual_outfit_found}")
						
							
						outfit_and_thumbnail = (actual_outfit_found, thumbnail_name)
						
						#A boolean to check if anything was already in discovered_outfits, then if it was in outfit_list. if it doesn't find anything, it will make the tuple and add it to the lists
						if outfit_has_category:
							outfit_set.add(actual_outfit_found)
							if f"outfit_{fixnames_v1(actual_outfit_found)}" not in existing_missions:
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
				
						found_location = "\n".join([senza_solaria_mission_outfit(o[0], o[1]) for o in discovered_outfits])
						new_file_for_outfits = outfit_subfolder / f"{plugin_name}_{file_path.stem}.txt".replace("_", ".")
						with open(new_file_for_outfits, 'a', encoding='utf-8') as f:
							f.write("\n" + found_location)
				else:
					print("TOUGH LUCK BUDDY, nothin found!")
			
			except UnicodeDecodeError:
				print(f"Apologies, couldn't read {file_path} because of unicode issue")
			except IOError as e:
				print(f"Apologies, couldn't read {file_path} due to IOError: {e}")
	all_found_outfits = sorted(list(outfit_set))
	
	if all_found_outfits:
		with open(allunlock_export, 'w', encoding='utf-8', errors='ignore') as f:
			f.write(f"outfitter `Senza Solaria Unlockall Outfits Plugin`\n")
			for outfit_name in all_found_outfits:
				f.write(f"\t`{outfit_name}`\n")
	if output_single_folder and outfit_list:
		single_file = export_location / (f"{plugin_name}_senza_outfits.txt")
		single_file_text = "\n".join([senza_solaria_mission_outfit(o[0], o[1]) for o in outfit_list])
		with open(single_file, 'a', encoding='utf-8') as f:
			f.write("\n" + single_file_text)

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
	
	outfits_discovered = find_outfits_v4(input_filepath, output_single_folder)
	for outfit in outfits_discovered:
		print(f"{outfit[0]} detected!")
		
	ships_discovered = find_ships_v4(input_filepath, output_single_folder, variants_source_ship)
	for ship in ships_discovered:
		print(f"{ship[0]} detected!")

	multi_input_loop = input('Plugin processing complete! Would you like to process another plugin? (y/n): ').lower().strip()
	if multi_input_loop in ("n", "no", "nope", "0"):
		print("Very well, thank you for using Senza Solaria!")
		break