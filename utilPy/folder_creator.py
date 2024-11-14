import os
import shutil

vanessa_items = [
    "Anchor", "Astrolabe", "Barrel", "Bayonet", "Beach Ball", "Bolas",
    "Captain's Wheel", "Cannon", "Cannonade", "Catfish", "Cinders", "Clamera",
    "Concealed Dagger", "Coral", "Coral Armor", "Cutlass", "Duct Tape", "Extract",
    "Figurehead", "Flagship", "Fishing Rod", "Handaxe", "Grenade", "Golf Clubs",
    "Grapeshot", "Harpoon", "Honing Steel", "Holsters", "Icicle", "IllusoRay",
    "Javelin", "Jellyfish", "Katana", "Langxian", "Life Preserver", "Narwhal",
    "Pet Rock", "Piranha", "Pop Snappers", "Powder Keg", "Ramrod", "Repeater",
    "Revolver", "Rifle", "Sea Shell", "Seaweed", "Sharpening Stone", "Shipwreck",
    "Shoeblades", "Shovel", "Silencer", "Sniper Rifle", "Star Chart", "Switchblade",
    "The Boulder", "The Dam", "Tripwire", "Turtle Shell", "Vanessa's Amulet",
    "Wanted Poster", "Weather Glass", "Disguise", "Handaxe", "Honing Steel",
    "Icicle", "Javelin", "Jellyfish", "Katana", "Langxian", "Life Preserver",
    "Narwhal", "Pet Rock", "Piranha", "Pop Snappers", "Powder Keg", "Ramrod",
    "Repeater", "Revolver", "Rifle", "Sea Shell", "Seaweed", "Sharpening Stone",
    "Shipwreck", "Shoeblades", "Shovel", "Silencer", "Sniper Rifle", "Star Chart",
    "Switchblade", "The Boulder", "The Dam", "Tripwire", "Turtle Shell",
    "Vanessa's Amulet", "Wanted Poster", "Weather Glass", "Disguise", "Duct Tape",
    "Cinders", "Turbo Rifle", "Handaxe", "Lighter", "Pufferfish", "Disguise",
    "Star Chart", "Cannonball", "Feather"
]

monster_items = [
    # Level 1 Encounter Items
    "Medkit", "Bluenanas", "Duct Tape", "Pelt", "Fang", "Scrap", "Silk",
    "Insect Wing", "Stinger", "Langxian", "Eagle Talisman", "Cinders",
    "Lighter", "Gland", "Toxic Fang", "Extract",

    # Level 2 Encounter Items
    "Coconut", "Crusher Claw", "Sea Shell", "Proboscis", "Amber",

    # Level 3 Encounter Items
    "Safe", "Shadowed Cloak", "Concealed Dagger", "Grindstone",
    "Sharpening Stone", "Vial of Blood", "Bottled Lightning",
    "Tazidian Dagger", "Fire Potion", "Bar of Gold", "Fiery Cutlass",
    "Dog", "Temporary Shelter",

    # Level 4 Encounter Items
    "Scrap", "Tusked Helm", "Old Sword", "Red Piggles A", "Red Gumball",
    "Shoe Blade", "Red Piggles X", "Hammer", "Wrench", "Toolbox",
    "Multitool", "Energy Potion", "Icicle", "Weights", "Handaxe",
    "Frozen Bludgeon", "Snow Globe", "Clockwork Blades", "Gearnola Bar",
    "Junkyard Club", "Junkyard Repairbot"
]

dooley_items = [
    "Armored Core", "Chris Army Knife", "Claw Arm", "Cog", "Companion Core",
    "Critical Core", "Flamethrower", "Heavy Combat Armor", "Laser Pistol",
    "Lighter", "Plasma Grenade", "Thermal Lance", "Thrusters", "Weaponized Core"
]

# Folder suffixes
suffixes = ["_bronze", "_silver", "_gold", "_diamond"]

# Base directory to create folders in (change as needed)
base_directory = os.path.join("..", "training_images", "item_images")
destination_directory = os.path.join("..", "bazaarai", "item_images")

# Supported image extensions
image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}

def create_items_folders(items):
    # Create folders for each item with each suffix
    for item in items:
        # Format item name to be lowercase and remove spaces
        formatted_item = item.replace(" ", "").replace("`", "").lower()

        for suffix in suffixes:
            folder_name = f"{formatted_item}{suffix}"
            folder_path = os.path.join(base_directory, folder_name)

            # Create the folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {folder_path}")
            else:
                print(f"Folder already exists: {folder_path}")

def create_missing_suffix_folders():
    # Ensure the base directory exists
    if not os.path.exists(base_directory):
        print(f"Base directory {base_directory} does not exist.")
    else:
        # Go through each folder in the base directory
        for folder in os.listdir(base_directory):
            folder_path = os.path.join(base_directory, folder)

            # Check if it's a directory and matches one of the item names without suffix
            if os.path.isdir(folder_path):
                # Extract base item name by removing existing suffix (if any)
                base_name = folder
                for suffix in suffixes:
                    if folder.endswith(suffix):
                        base_name = folder.replace(suffix, "")
                        break

                # Create any missing suffix folders for the base item
                for suffix in suffixes:
                    new_folder_name = f"{base_name}{suffix}"
                    new_folder_path = os.path.join(base_directory, new_folder_name)

                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)
                        print(f"Created missing folder: {new_folder_path}")
                    else:
                        print(f"Folder already exists: {new_folder_path}")

def get_all_that_have_images():
    # Ensure the destination directory exists
    os.makedirs(destination_directory, exist_ok=True)

    # Function to check if a folder contains images
    def contains_images(folder_path):
        for file in os.listdir(folder_path):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                return True
        return False

    # Go through each folder in the base directory
    for folder in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder)

        # Check if it's a directory and contains images
        if os.path.isdir(folder_path) and contains_images(folder_path):
            # Define the destination path for the folder
            destination_path = os.path.join(destination_directory, folder)

            # Copy the folder to the destination
            shutil.copytree(folder_path, destination_path, dirs_exist_ok=True)
            print(f"Copied folder: {folder_path} to {destination_path}")
        else:
            print(f"No images found in folder: {folder_path}")

def move_images_to_train_and_validate():
    # Function to get all image files in a folder
    def get_image_files(folder_path):
        return [file for file in os.listdir(folder_path) if any(file.lower().endswith(ext) for ext in image_extensions)]

    # Go through each folder in the base directory
    for folder in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder)

        # Check if it's a directory
        if os.path.isdir(folder_path):
            # Get all images in the folder
            images = get_image_files(folder_path)

            # Check if there are two or more images
            if len(images) >= 2:
                # Define the primary and secondary paths
                validation_path = os.path.join(destination_directory, "data", folder)
                train_path = os.path.join(destination_directory, "item_images", folder)

                # Create the primary and secondary folders
                os.makedirs(validation_path, exist_ok=True)
                os.makedirs(train_path, exist_ok=True)

                # Copy the first image to the primary folder
                first_image = images[0]
                shutil.copy2(os.path.join(folder_path, first_image), validation_path)
                print(f"Copied {first_image} to {validation_path}")

                # Copy the rest of the images to the secondary folder
                for image in images[1:]:
                    shutil.copy2(os.path.join(folder_path, image), train_path)
                    print(f"Copied {image} to {train_path}")
            else:
                print(f"Skipped folder: {folder_path} (less than 2 images)")

if __name__ == "__main__":
    #move_images_to_train_and_validate()
    create_items_folders(vanessa_items)
    create_items_folders(monster_items)
    create_items_folders(dooley_items)