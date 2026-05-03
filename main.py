import argparse
import os
import shutil
import re

from collections import defaultdict
from alive_progress import alive_bar
import questionary

def filter_only_media_files(f, accepted_extensions):
    _, ext = os.path.splitext(f)
    return ext.lower() in accepted_extensions

def get_selected_extensions(stats):
    """Display interactive checkbox menu to select file extensions.
    
    Args:
        stats: Dictionary mapping file extensions to their counts
        
    Returns:
        Set of selected extensions (lowercase) to include in copying
    """
    if not stats:
        return set()
    
    # Create choices
    choices = []
    excluded_extensions = {".json", ".html"}
    
    for ext in sorted(stats.keys()):
        count = stats[ext]
        label = f"{ext} ({count} files)"
        choices.append(label)
    
    # Display interactive checkbox menu
    selected_labels = questionary.checkbox(
        'Select file extensions to include:',
        choices=choices
    ).ask()
    
    if selected_labels is None:  # User cancelled with Ctrl+C
        return set()
    
    # Extract extensions from labels (e.g., ".jpg (1500 files)" -> ".jpg")
    selected_extensions = set()
    for label in selected_labels:
        ext = label.split(" (")[0].lower()
        selected_extensions.add(ext)
    
    return selected_extensions

def main():
    parser = argparse.ArgumentParser(prog='Organize Photo Media', description='Reorganize media')
    parser.add_argument('root_path')
    args = parser.parse_args()

    root_path = args.root_path

    stats = defaultdict(int)
    dir_with_files = []
    for (dirpath, dirnames, filenames) in os.walk(root_path):
        if len(filenames) > 0:
            dir_with_files.append(dirpath)
            for f in filenames:
                _, ext = os.path.splitext(f)
                stats[ext.lower()] += 1                
        
    #print("\n".join(dir_with_files))
    total = 0
    for k,v in stats.items():
        total += v
    
    for k,v in stats.items():
        print(k + " is present " + str(v) + " times. " + str(100 * v / total) + "%")

    # Get user's extension selection via interactive menu
    accepted_extensions = get_selected_extensions(stats)
    
    if not accepted_extensions:
        print("No extensions selected. Exiting.")
        return
    
    print(f"\nSelected extensions: {', '.join(sorted(accepted_extensions))}\n")

    media_path = "Media"
    untitled_path= os.path.join(media_path, "Untitled")
    if(not os.path.exists(media_path)):
        os.mkdir(media_path)
    if(not os.path.exists(untitled_path)):
        os.mkdir(untitled_path)

    regex_patter=r"Untitled(\(\d\))?|Spotlight(\(\d\))?"
   
    file_src_dst = []
    print("Processing Folders to gater media to copy...")
    with alive_bar(len(dir_with_files)) as bar:
        for dir in dir_with_files:
            dir_name = os.path.basename(os.path.normpath(dir))
            dest = os.path.join(media_path, dir_name)        
            if re.match(regex_patter, dir_name):
                dest = untitled_path


            files_to_copy = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]                    
            files_to_copy = list(filter(lambda f: filter_only_media_files(f, accepted_extensions), files_to_copy))
            if len(files_to_copy) > 0:
                if(not os.path.exists(dest)):
                    os.mkdir(dest)

            for f in files_to_copy:
                src=os.path.join(dir, f)
                dst=os.path.join(dest, f)
                file_src_dst.append((src, dst))
            bar()
    
    print("Copying files...")
    with alive_bar(len(file_src_dst)) as bar:
        for file in file_src_dst:
            src = file[0]
            dst = file[1]
            copy_file(src, dst)
            bar()

def copy_file(src, dst):
    #print("copy " + src + " to " + dst)
    shutil.copy(src, dst)

if __name__ == "__main__":
    main()