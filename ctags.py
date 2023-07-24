import os
import json
import subprocess
from settings import Settings


# ctags --fields=+S --output-format=json
# C:\Programs\ctags\ctags -R . --fields=+S --output-format=json --exclude=bin --exclude=obj --exclude=. --exclude=packages --exclude=node_modules --exclude=logs
# C:\Programs\ctags\ctags -R --fields=+S --output-format=json --exclude=bin --exclude=obj --exclude=. --exclude=packages --exclude=node_modules --exclude=logs .
# C:\Programs\ctags\ctags -R --fields=+S --output-format=json --exclude=bin --exclude=obj --exclude=. --exclude=packages --exclude=node_modules --exclude=logs -f tags_json.txt .



def run_ctags(out_tags_file, dir_to_analyze):
    if os.path.isfile(out_tags_file):
        os.remove(out_tags_file)

    command = [
        # r"C:\Programs\ctags\ctags",
        "ctags",
        "-R",
        "--fields=+S",
        "--output-format=json",
        # "--exclude=.",
        "--exclude=*/bin/*",
        "--exclude=*/obj/*",
        "--exclude=*/.vs/*",
        "--exclude=*/.azuredevops/*",
        "--exclude=*/packages/*",
        "--exclude=*/node_modules/*",
        "--exclude=*/logs/*",
        "--exclude=*/dist/*",
        "--exclude=*/package-lock.json",
        "--exclude=*.min.js",
        "--exclude=*.min.css",

        # ignore FE
        # "--exclude=*.css",
        # "--exclude=*.scss",
        # "--exclude=*.js",

        f"-f {out_tags_file}",
        # ".",
        # # "..",
        f"{dir_to_analyze}",
        # r"C:\GIT\Bitbucket\alloy_net6",
    ]
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



import json
from collections import defaultdict


def organize_tags(file_path):
    # Initialize a dictionary to store the organized tags
    organized_tags = defaultdict(lambda: defaultdict(list))

    # Open the file and read each line
    with open(file_path, 'r') as f:
        for line in f:
            # Parse the JSON object
            tag = json.loads(line)

            # Ignore ptag type
            if tag["_type"] == "ptag":
                continue

            # Extract the necessary information
            path = tag["path"]
            kind = tag["kind"]
            name = tag["name"]
            signature = tag.get("signature", "")

            # Add the tag to the organized tags dictionary
            organized_tags[path][kind].append(f"{name} {signature}")

    return organized_tags


def write_organized_tags_to_file(organized_tags, file_path, dir_to_analyze):
    with open(file_path, 'w') as f:
        for path, kinds in organized_tags.items():
            # Convert the absolute path to a relative path
            relative_path = os.path.relpath(path, dir_to_analyze)
            f.write(relative_path + ":\n")
            for kind, names in kinds.items():
                f.write("   " + kind + "\n")
                for name in names:
                    f.write("      " + name + "\n")


def get_code_map(s):
    dir_to_analyze = s.cwd
    out_tags_file = s.out_tags_file
    out_tags_structured_file = s.out_tags_structured_file
    run_ctags(out_tags_file, dir_to_analyze)
    organized_tags = organize_tags(out_tags_file)
    write_organized_tags_to_file(organized_tags, out_tags_structured_file, dir_to_analyze)
    # 'tags_structured.txt'
    with open(out_tags_structured_file, 'r', encoding='utf-8') as file:
        contents = file.read()
    return contents


if __name__ == '__main__':
    s = Settings()
    # "..", 
    # dir_to_analyze = ".", 
    # dir_to_analyze = r"C:\GIT\Bitbucket\alloy_net6"
    # out_tags_file = 'tags_json.txt'
    # out_tags_structured_file = 'tags_structured.txt'
    code_map = get_code_map(s)
    print(code_map)
    # run_ctags(out_tags_file, dir_to_analyze)
    # organized_tags = organize_tags(out_tags_file)
    # write_organized_tags_to_file(organized_tags, 'tags_structured.txt', dir_to_analyze)
