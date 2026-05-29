import os
import re

files_to_fix = [
    ('src/components/sat/pickTicketpopup.vue', 'formData.so', 'Select FSE Name*'),
    ('src/components/sat/reassignTicketPopup.vue', 'formData.so', 'Select FSE Name*')
]

for filepath, model_name, original_label in files_to_fix:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()

        pattern = f'label="{original_label}"'
        replacement = f':label="{model_name} ? \'\' : \'{original_label}\'"'

        if pattern in content:
            new_content = content.replace(pattern, replacement)
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Fixed {filepath}")
        else:
            print(f"Pattern not found in {filepath}")
