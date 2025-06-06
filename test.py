# import json

# # Load your JSON file
# with open('structured_bnss.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# def fix_subclauses(section_data):
#     fixed_subclauses = []
#     expected_num = 1
#     merged_text = ""

#     for clause in section_data["content"]["subclause"]:
#         # Get current subclause number and text
#         key = list(clause.keys())[0]
#         value = clause[key]

#         if int(key) == expected_num:
#             if merged_text:
#                 # Add merged text to the last valid subclause
#                 fixed_subclauses[-1][str(expected_num - 1)] += " " + merged_text.strip()
#                 merged_text = ""
#             fixed_subclauses.append({str(expected_num): value})
#             expected_num += 1
#         else:
#             # Merge into the last valid subclause
#             merged_text += " " + value.strip()

#     if merged_text:
#         # Attach leftover merge if any
#         fixed_subclauses[-1][str(expected_num - 1)] += " " + merged_text.strip()

#     section_data["content"]["subclause"] = fixed_subclauses
#     return section_data

# # Apply to each section
# corrected_data = [fix_subclauses(section) for section in data]

# # Save the new JSON file
# with open('structured_bnss_fixed.json', 'w', encoding='utf-8') as f:
#     json.dump(corrected_data, f, indent=4, ensure_ascii=False)

import json

# Load your JSON file
with open('structured_bnss.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def fix_subclauses(section_data):
    subclauses = section_data["content"].get("subclause", [])
    
    # If subclause list is empty, skip processing
    if not subclauses:
        return section_data

    fixed_subclauses = []
    expected_num = 1
    merged_text = ""

    for clause in subclauses:
        key = list(clause.keys())[0]
        value = clause[key]

        if int(key) == expected_num:
            if merged_text and fixed_subclauses:
                # Merge any leftover text to previous valid clause
                last_key = list(fixed_subclauses[-1].keys())[0]
                fixed_subclauses[-1][last_key] += " " + merged_text.strip()
                merged_text = ""
            fixed_subclauses.append({str(expected_num): value})
            expected_num += 1
        else:
            # Not sequential, collect text to merge
            merged_text += " " + value.strip()

    # If we still have leftover merged text
    if merged_text and fixed_subclauses:
        last_key = list(fixed_subclauses[-1].keys())[0]
        fixed_subclauses[-1][last_key] += " " + merged_text.strip()

    section_data["content"]["subclause"] = fixed_subclauses
    return section_data

# Process all sections
corrected_data = [fix_subclauses(section) for section in data]

# Save result to a new JSON file
with open('structured_bnss_fixed.json', 'w', encoding='utf-8') as f:
    json.dump(corrected_data, f, indent=4, ensure_ascii=False)
