# from pprint import pprint
# import fitz
# import re
# import json

# # Open the PDF
# doc = fitz.open("data/aa2023-46.pdf")

# # Initialize variables
# completed_sections = []  # List to store finished sections
# current_section = None  # Current section being built
# count = 0

# # Regular expression to detect section starts (e.g., "1.", "2.")
# section_start_pattern = r'^\s*\d+\.\s'

# # Process pages starting from page 15
# for page_num in range(15, len(doc)):
#     if count >= 12:  # Stop after 2 pages, matching your original limit
#         break
#     page = doc[page_num]
#     text_dict = page.get_text("dict")  # Get structured text
    
#     # Iterate through blocks and lines
#     for block in text_dict["blocks"]:
#         if "lines" not in block:
#             continue
#         for line in block["lines"]:
#             # Combine spans to get the full line text
#             line_text = "".join([span["text"] for span in line["spans"]]).strip()
            
#             # Check if this line starts a new section
#             match = re.match(section_start_pattern, line_text)
#             if match:
#                 # If there's an ongoing section, complete it
#                 if current_section:
#                     completed_sections.append(current_section)
                
#                 # Start a new section
#                 section_number = match.group().strip()
#                 section_content = line_text[len(section_number):].strip()
#                 current_section = {"section": section_number, "content": section_content}
#             else:
#                 # Append to the current section if it exists
#                 if current_section:
#                     current_section["content"] += " " + line_text
    
#     count += 1

# # Add the last section if it exists
# if current_section:
#     completed_sections.append(current_section)

# # Print the extracted sections
# for section in completed_sections:
#     print(f"Section {section['section']}:\n{section['content'].strip()}\n{'-'*40}")

# # Close the document
# doc.close()

# pprint(completed_sections)

# with open("structured_bnss.json", 'w', encoding='utf-8') as f:
#     json.dump(completed_sections, f, indent=4, ensure_ascii=False)

#------------------------------------------------------------------------------

import fitz
import re
import json

def process_content(content):
    # Split content into parts using sub-clause markers like "(1) ", "(2) "
    parts = re.split(r'(\(\d+\)\s)', content)
    if len(parts) > 1:
        # Title is the text before the first sub-clause marker
        title = parts[0].strip()
        subclauses = []
        # Process pairs of marker and text
        for i in range(1, len(parts), 2):
            marker = parts[i]  # e.g., "(1) "
            text = parts[i + 1] if i + 1 < len(parts) else ""  # Text following the marker
            number = re.search(r'\d+', marker).group()  # Extract number, e.g., "1"
            subclauses.append({number: text.strip()})
    else:
        # No sub-clauses; entire content is the title
        title = content.strip()
        subclauses = []
    return {'title': title, 'subclause': subclauses}

# Open the PDF file
doc = fitz.open("data/aa2023-46.pdf")

# Initialize variables
completed_sections = []
current_section = None
page_count = 0

# Regex pattern to detect section starts (e.g., "34.")
section_start_pattern = r'^\s*\d+\.\s'

# Process pages starting from page 15, limiting to 2 pages
for page_num in range(15, len(doc)):
    if page_count >= len(doc):
        break
    page = doc[page_num]
    text_dict = page.get_text("dict")  # Get structured text

    for block in text_dict["blocks"]:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            # Combine spans to get full line text
            line_text = "".join([span["text"] for span in line["spans"]]).strip()
            
            # Check if this line starts a new section
            match = re.match(section_start_pattern, line_text)
            if match:
                # Finalize the previous section if it exists
                if current_section:
                    current_section['content'] = process_content(current_section['content'])
                    completed_sections.append(current_section)
                
                # Start a new section
                section_number = match.group().strip()  # e.g., "34."
                section_content = line_text[len(section_number):].strip()  # Text after number
                current_section = {"section": section_number, "content": section_content}
            else:
                # Append to current section's content
                if current_section:
                    current_section["content"] += " " + line_text
    
    page_count += 1

# Finalize the last section
if current_section:
    current_section['content'] = process_content(current_section['content'])
    completed_sections.append(current_section)

# Output the extracted sections
for section in completed_sections:
    print(f"Section {section['section']}")
    print(f"Title: {section['content']['title']}")
    print("Subclauses:")
    for subclause in section['content']['subclause']:
        for num, text in subclause.items():
            print(f"  ({num}) {text}")
    print("-" * 40)

# Close the document
doc.close()

with open("structured_bnss.json", 'w', encoding='utf-8') as f:
    json.dump(completed_sections, f, indent=4, ensure_ascii=False)
