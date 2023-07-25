import os

def format_title(file):
    title_string = f"{'=' * len(file)}\n{file}\n{'=' * len(file)}"
    return title_string


def read_files(files):
    file_contents = {}
    error_files = []
    text_string = ""

    # Convert file paths to use forward slashes
    files = [os.path.normpath(file) for file in files]

    for file in files:
        try:
            with open(file, 'r') as f:
                content = f.read()
                file_contents[file] = content
                file_title = format_title(file)
                text_string += f"{file_title}\n{content}\n\n"
        except FileNotFoundError:
            error_files.append(file)
            print(f"Error: File '{file}' not found.")
        except:
            error_files.append(file)
            print(f"Error: Failed to read file '{file}'.")

    if len(error_files) == 0:
        print("All files read successfully.")
        # print(text_string)
    else:
        print(f"Failed to read {len(error_files)} file(s).")
        return ""
        # [print(e) for e in error_files]

    # return file_contents
    return text_string


if __name__ == '__main__':
    # Example usage
    files_list = [
        r"C:\GIT\Bitbucket\ai_exploration\CliTools\20230703_gpt_from_terminal\GptCli.py",
        # r"CliTools\20230703_gpt_from_terminal\gpt_chat_agent.py",
        "gpt_chat_agent.py",
        # "main.py",
        # "file1.txt",
        # "file2.txt",
        # "file3.txt",
        # "C:\\path\\to\\file4.txt",
        # "C:/path/to/file5.txt",
        # "C:\\path/to/file6.txt"
    ]
    text_string = read_files(files_list)
    print(text_string)
