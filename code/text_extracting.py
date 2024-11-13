import os
import re

directory = '/Users/dariabikina/Documents/python learning/moksha llm/raw/'
outputdirectory = '/Users/dariabikina/Documents/python learning/moksha llm/processed'

os.makedirs(outputdirectory, exist_ok=True)

def extract(file_path):
    with open(file_path, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    to_omit = set(range(0,43))
   #need to skip the first 43 lines
    to_omit.add(44)
   #and separately line 45

    filtered = [line for i, line in enumerate(lines) if i not in to_omit]

    content = "".join(filtered)

    #deleting "Последние новости" and everything past that 
    match = re.search(r"^(.*?)(?=\nПоследние новости)", content, re.DOTALL)

    # If a match is found, return it; otherwise, return None
    if match:
        return match.group(1)
    else:
        return None

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)

        relevant_text = extract(file_path)
        
    # If relevant text was found, save it to a new file
    if relevant_text:
            output_path = os.path.join(outputdirectory, filename)
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(relevant_text)
            print(f"Saved processed text to {output_path}")
       
