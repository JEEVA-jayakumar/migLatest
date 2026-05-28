import os
import re

def fix_uppercase(content, model_path):
    # This regex targets q-input tags with the specific model_path
    # It replaces either :model-value or v-model with v-model and ensures a clean @update:model-value

    # First, simplify @update:model-value if it exists
    content = re.sub(
        r'@update:model-value="val => \{ ' + re.escape(model_path) + r' = val \? val\.toUpperCase\(\) : val; \}"',
        f'@update:model-value="{model_path} = {model_path}.toUpperCase()"',
        content
    )
    # Ensure it uses v-model for best compatibility with Quasar 2's internal handling
    content = re.sub(
        r':model-value="' + re.escape(model_path) + r'"',
        f'v-model="{model_path}"',
        content
    )
    return content

def process_file(filepath, models):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    for m in models:
        content = fix_uppercase(content, m)
    with open(filepath, 'w') as f:
        f.write(content)

# Main form
process_file('src/components/sat/showMarsFormComponent.vue', [
    'merchant.companyInformation.pan',
    'merchant.companyInformation.tan',
    'merchant.businessInformation.gstId',
    'viewBinding.partnersArr[index].pan',
    'merchant.bankInformation.bankDetails.ifsc'
])

# Data Entry components
process_file('src/components/sat/dataEntry/companyInformation.vue', ['merchant.companyInformation.pan', 'merchant.companyInformation.tan'])
process_file('src/components/sat/dataEntry/bankInformation.vue', ['merchant.bankInformation.bankDetails.ifsc'])
process_file('src/components/sat/dataEntry/partnersInformation.vue', ['partner.pan'])
process_file('src/components/sat/dataEntry/businessInformation.vue', ['merchant.businessInformation.gstId'])

# Change management
process_file('src/pages/sat/changemanagementeditdatarsmreject.vue', ['merchant.companyinformation.pan', 'merchant.bankInformation.bankDetails.ifsc'])
process_file('src/pages/sat/changemanagementeditdatafinancereject.vue', ['merchant.companyinformation.pan', 'merchant.bankInformation.bankDetails.ifsc'])
process_file('src/pages/sat/changemanagementeditdatareject.vue', ['merchant.companyinformation.pan', 'merchant.bankInformation.bankDetails.ifsc'])
process_file('src/pages/sat/changemanagementeditdata.vue', ['merchant.bankInformation.bankDetails.ifsc'])

print("Uppercase conversion refined.")

# Thorough default values check
# Looking for ANY numeric 1 assignments
def fix_defaults(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()

    # Use word boundaries to avoid matching things like 'someValue1'
    # Target: rentalPlanCode: 1, serviceProvider: 1, networkPreferred: 1 (with or without quotes)
    new_content = re.sub(r'\b(rentalPlanCode|serviceProvider|networkPreferred)\b\s*:\s*["\']?1["\']?', r'\1: ""', content)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed defaults in {filepath}")

files_to_check = [
    'src/components/sat/showMarsFormComponent.vue',
    'src/pages/sat/QrShortLead.vue',
    'src/pages/sat/changemanagementeditdata.vue',
    'src/pages/sat/changemanagementeditdatafinancereject.vue',
    'src/pages/sat/changemanagementeditdatareject.vue',
    'src/pages/sat/changemanagementeditdatarsmreject.vue',
    'src/configurations/DataEntryPreDefinition.js'
]
for f in files_to_check:
    fix_defaults(f)
