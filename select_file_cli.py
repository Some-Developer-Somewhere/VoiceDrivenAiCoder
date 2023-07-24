import os
import msvcrt
from settings import Settings


def print_file_options(files):
    print("\nChoose between the following options:")
    for i, file in enumerate(files, start=1):
        print(f"[{i}] {file}")
    print("[d] Default file")
    print("[c] Cancel")


# chosen_file = choose_file_option(s.cwd, s.default_context_fip)
#             s.context_fip = s.set_context_fip_abs(chosen_file)

def choose_file_option(s):
    cwd = s.cwd
    default_context_fip = s.default_context_fip

    files = [f for f in os.listdir(cwd) if os.path.isfile(f)]
    # default_file = default_context_fip

    print_file_options(files)

    while True:
        key_pressed = msvcrt.getch().decode("utf-8")

        if key_pressed.lower() == 'd':
            print(f"Default file '{default_context_fip}' chosen.")
            # return default_context_fip
            s.set_context_fip_abs(default_context_fip)
            print("s.context_fip")
            print(s.context_fip)
            break
        elif key_pressed == 'c':
            print("Cancel.")
            # return None
            break
        elif key_pressed.isdigit() and 1 <= int(key_pressed) <= len(files):
            chosen_file = files[int(key_pressed) - 1]
            print(f"File '{chosen_file}' chosen.")
            chosen_file_abs = os.path.join(cwd, chosen_file)
            # return chosen_file_abs
            s.set_context_fip_abs(chosen_file_abs)
            print("s.context_fip")
            print(s.context_fip)
            break
        else:
            print("Invalid option. Try again.")



if __name__ == "__main__":
    s = Settings()
    chosen_file = choose_file_option(s)

