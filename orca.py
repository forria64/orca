import os
import json
import random
import multiprocessing
from PIL import Image, ImageChops, ImageEnhance


def resize_and_save_24kb(image_path):
    try:
        with Image.open(image_path) as img:
            # Resize image to fit within 24kb
            img.thumbnail((200, 200))
            img.save(f"24k_artworks/{os.path.basename(image_path)}", optimize=True)
            debug_message(f"TAMED SMOL PHYXL POD AT 24k_artworks/{os.path.basename(image_path)}")
    except Exception as e:
        print(f"SMOL PHYXL DISAPPEARED INTO THE DEPTHS: {e}")


def generate_background(background_colors, serial_number):
    debug_message(f"PREPARING YOUR NET... NET NO. #{serial_number}")

    background_color = random.choice(background_colors)
    background = Image.new("RGB", (8500, 8500), background_color)

    tmp_path = f"tmp_files/background_{serial_number}.png"
    background.save(tmp_path)
    debug_message(f"YOUR NET HAS BEEN LOWERED INTO THE DEPTHS: {tmp_path}")

    return tmp_path, background_color


def color_element(args):
    interval, x, y, serial_number = args
    debug_message(f"A PHYXL IS STRUGGLING TO GET OUT OF ONE OF YOUR NETS! NET NO. #{serial_number}")

    element_path = f"assets/phyxl_{x}_{y}.png"
    element_color = random.choice(interval["element_colors"])
    colored_element = color_element_inner(element_path, element_color, 1.5, 1.5)

    tmp_path = f"tmp_files/element_{serial_number}_{x}_{y}.png"
    colored_element.save(tmp_path)
    debug_message(f"YOU'VE CAUGHT A WILD SEA PHYXL IN ONE OF YOUR NETS! NET NO. #{serial_number}")

    return tmp_path, element_color


def color_element_inner(layer_path, overlay_color, saturation_factor, sharpness_factor):
    image_directory, image_file_name = os.path.split(layer_path)
    input_path = os.path.join(image_directory, image_file_name)

    image = Image.open(input_path).convert("RGBA")
    color_layer = Image.new("RGBA", image.size, overlay_color)

    alpha = image.getchannel('A')
    alpha_thresh = alpha.point(lambda p: p if p > 0 else 0)

    color_layer.putalpha(alpha_thresh)

    result_image = ImageChops.overlay(image, color_layer)

    enhancer = ImageEnhance.Color(result_image)
    result_image = enhancer.enhance(saturation_factor)

    enhancer = ImageEnhance.Sharpness(result_image)
    result_image = enhancer.enhance(sharpness_factor)

    return result_image


def generate_artwork(interval, serial_number):

    # Generate Background
    background_path, background_color = generate_background(interval["background_colors"], serial_number)
    background = Image.open(background_path).convert("RGBA")

    # Overlay Shadow
    shadow_path = interval["shadow_path"]
    shadow = Image.open(shadow_path).convert("RGBA")
    background = Image.alpha_composite(background, shadow)

    # Parallel Element Coloring using multiprocessing
    with multiprocessing.Pool() as pool:
        element_data = pool.map(color_element, [(interval, x, y, serial_number) for x in range(1, 9) for y in range(1, 9)])

    # Overlay Elements
    debug_message(f"WRANGLING CAUGHT PHYXLS... NET NO. #{serial_number}")
    for element_path, _ in element_data:
        element = Image.open(element_path).convert("RGBA")
        background = Image.alpha_composite(background, element)

    # Overlay Texture
    texture_path = interval["texture_path"]
    texture = Image.open(texture_path).convert("RGBA")
    background = Image.alpha_composite(background, texture)

    # Overlay Outline
    outline_path = interval["outline_path"]
    outline = Image.open(outline_path).convert("RGBA")
    background = Image.alpha_composite(background, outline)

    # Save Artwork
    generated_path = f"generated_artworks/phyxls_{serial_number}.png"
    background.save(generated_path)
    debug_message(f"64 WILD SEA PHYXLS TAMED AT {generated_path}")
    
    # Resize and save 24kb version
    resize_and_save_24kb(generated_path)
    
    # Generate Metadata
    metadata = {
        "image_name": f"Phyxls #{serial_number}",
        "attributes": [
            {"category": "Background", "value": background_color},
        ] + [
            {"category": f"Phyxl ({x},{y})", "value": color}
            for (element_path, color), (x, y) in zip(element_data, [(x, y) for x in range(1, 9) for y in range(1, 9)])
        ]
    }

    metadata_path = f"metadata/phyxls_{serial_number}.json"
    with open(metadata_path, "w") as metadata_file:
        json.dump(metadata, metadata_file, indent=4)
        debug_message(f"A PASSPORT HAS BEEN ISSUED FOR YOUR WILD PHYXLS POD AT {metadata_path}")

    # Clean up tmp_files directory
    cleanup_tmp_files(serial_number)


def debug_message(message):
    print(f"ROWING... ROWING... ROWING... {message}")


def cleanup_directory(directory):
    debug_message(f"CLEANING UP FISHING EQUIPMENT AT {directory}")
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"YOU MISSED A SPOT! {file_path}: {e}")


def cleanup_tmp_files(serial_number):
    tmp_directory = "tmp_files"
    for file_name in os.listdir(tmp_directory):
        if f"{serial_number}" in file_name:
            file_path = os.path.join(tmp_directory, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"YOU MISSED A SPOT! {file_path}: {e}")


def generate_artworks_for_interval(interval):
    for i in range(interval["start"], interval["end"] + 1):
        generate_artwork(interval, i)


def prompt_continue():
    
    print("""
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┏━━━┓┏━━━┓┏━━━┓┏━━━┓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┃┏━┓┃┃┏━┓┃┃┏━┓┃┃┏━┓┃▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██████████▓▓▓▓▓▓▓┃┃ ┃┃┃┗━┛┃┃┃ ┗┛┃┃ ┃┃▓▓┏━━┓┏┓ ┏┓
▓▓██████▓▓████▓▓▓▓▓▓██████████████▓▓▓▓▓┃┃ ┃┃┃┏┓┏┛┃┃ ┏┓┃┗━┛┃▓▓┃┏┓┃┃┃ ┃┃
▓▓██████████▓▓▓▓▓▓██████████████████▓▓▓┃┗━┛┃┃┃┃┗┓┃┗━┛┃┃┏━┓┃┏┓┃┗┛┃┃┗━┛┃
▓▓▓▓▓▓▓▓██▓▓▓▓▓▓████████░░████      ▓▓▓┗━━━┛┗┛┗━┛┗━━━┛┗┛ ┗┛┗┛┃┏━┛┗━┓┏┛
▓▓▓▓▓▓▓▓████████████████████        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┃┃▓▓┏━┛┃▓
▓▓▓▓▓▓▓▓████████████████▓▓          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓┗┛▓▓┗━━┛▓
▓▓▓▓▓▓▓▓████████████████░░        ▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ORCA v2.0
Digital processing tool built for the Phyxls art project.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""")
    while True:
        print("<<< PRESS CTRL + C TO QUIT >>> <<< PRESS ENTER TO GO FISHING >>>", end="", flush=True)
        user_input = input().strip()
        if user_input == "":
            return True
        else:
            return False


def main():

    # Create Directories
    for directory in ["tmp_files", "generated_artworks", "metadata", "24k_artworks"]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    # Clear generated_artworks, metadata, and tmp_files directories at script start time
    cleanup_directory("generated_artworks")
    cleanup_directory("metadata")
    cleanup_directory("tmp_files")
    cleanup_directory("24k_artworks")
    
    # Read Configs
    with open("configs.json", "r") as configs_file:
        configs = json.load(configs_file)
        
    # Print out the config information
    print("CONFIGURATION INFORMATION:")
    print("")
    for key, value in configs.items():
        print(f"{key}:")
        if key == "intervals":
            for interval in value:
                for k, v in interval.items():
                    print(f"  {k}:")
                    if isinstance(v, list) or isinstance(v, dict):
                        if isinstance(v, dict):
                            for k1, v1 in v.items():
                                print(f"    {k1}: {v1}")
                        else:
                            for item in v:
                                print(f"    - {item}")
                    else:
                        print(f"    {v}")
        else:
            if isinstance(value, list) or isinstance(value, dict):
                for k, v in value.items():
                    print(f"  {k}: {v}")
            else:
                print(f"  {value}")
    print("")
    print("IF YOU ARE NOT SATISFIED WITH YOUR CONFIGURATION,")
    print("YOU CAN EDIT IT IN THE >>> configs.json <<< FILE.")

    if not prompt_continue():
        print("QUITTING...")
        return
        
    # Generate Artworks
    for interval in configs["intervals"]:
        generate_artworks_for_interval(interval)
    
    print("YOUR PHYXLS COLLECTION HAS BEEN SUCCESSFULLY GENERATED!")
    print("CHECK OUT YOUR CATCH IN THE >>> generated_artworks <<< AND >>> 24k_artworks <<< DIRECTORIES!")
    print("METADATA FOR ALL GENERATED ARTWORKS CAN BE FOUND IN THE >>> metadata <<< DIRECTORY!")

if __name__ == "__main__":
    main()

