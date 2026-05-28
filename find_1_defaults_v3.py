import os
import re

files_to_check = [
    'src/components/sat/showMarsFormComponent.vue',
    'src/pages/sat/changemanagementeditdata.vue',
    'src/pages/sat/changemanagementeditdatafinancereject.vue',
    'src/pages/sat/changemanagementeditdatakyc.vue',
    'src/pages/sat/changemanagementeditdatareject.vue',
    'src/pages/sat/changemanagementeditdatarsmreject.vue'
]

for filepath in files_to_check:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
            # Look for these fields initialized to 1 or "1"
            matches = re.finditer(r'\b(serviceProvider|networkPreferred|rentalPlanCode)\b\s*:\s*["\']?1["\']?', content)
            found = False
            for match in matches:
                if not found:
                    print(f"Found in {filepath}:")
                    found = True
                print(f"  {match.group(0)}")
