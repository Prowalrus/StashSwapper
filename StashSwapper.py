import os
import re

def get_profile_path(profiles_path, profile_name):
    for file_name in os.listdir(profiles_path):
        file_path = os.path.join(profiles_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = [file.readline() for _ in range(6)]
                content = ''.join(lines)
                if profile_name in content:
                    return file_path
    return None

def main():
    # Ask the user for the old and new profile names
    old_profile_name = input("Enter the old profile name: ")
    new_profile_name = input("Enter the new profile name: ")

    # Define the path to the profiles directory
    profiles_path = './user/profiles'

    # Get the paths of the old and new profiles
    old_profile_path = get_profile_path(profiles_path, old_profile_name)
    new_profile_path = get_profile_path(profiles_path, new_profile_name)

    if not old_profile_path:
        print(f"Old profile '{old_profile_name}' not found.")
        return
    if not new_profile_path:
        print(f"New profile '{new_profile_name}' not found.")
        return

    print(f"Old profile path: {old_profile_path}")
    print(f"New profile path: {new_profile_path}")

    # Extract the relevant section from the old profile
    with open(old_profile_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Use regular expressions to find the "Inventory" section and the next "Notes" section
    Inventory_pattern = re.compile(r'"Inventory".*?(?="Notes")', re.DOTALL)
    Inventory_match = Inventory_pattern.search(content)

    if not Inventory_match:
        print(f"Failed to find the required sections in the old profile '{old_profile_name}'.")
        return

    Inventory_section = Inventory_match.group(0)
    print(f"Extracted Inventory section from old profile:\n{Inventory_section}")

    # Open the new profile and overwrite the same data
    with open(new_profile_path, 'r', encoding='utf-8', errors='ignore') as file:
        new_content = file.read()

    # Use regular expressions to find the "Inventory" section and the next "Notes" section in the new profile
    new_Inventory_pattern = re.compile(r'"Inventory".*?(?="Notes")', re.DOTALL)
    new_Inventory_match = new_Inventory_pattern.search(new_content)

    if not new_Inventory_match:
        print(f"Failed to find the required sections in the new profile '{new_profile_name}'.")
        return

    new_start = new_Inventory_match.start()
    new_end = new_Inventory_match.end()

    print(f"Replacing Inventory section in new profile from position {new_start} to {new_end}")

    # Replace the old "Inventory" section with the new one
    new_content = new_content[:new_start] + Inventory_section + new_content[new_end:]

    # Write the updated content back to the new profile
    with open(new_profile_path, 'w', encoding='utf-8', errors='ignore') as file:
        file.write(new_content)

    print(f"Profile Inventory copied from '{old_profile_name}' to '{new_profile_name}' successfully.")

if __name__ == "__main__":
    main()
