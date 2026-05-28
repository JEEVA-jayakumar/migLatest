import os
import re

def fix_uppercase(filepath, model_path):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()

    # We want to find the q-input that handles this model
    # and ensure it uses :model-value and @update:model-value for reliable uppercase

    # Regex to find the q-input tag for this model
    # It might have v-model or :model-value already
    pattern = r'<q-input[^>]*?(?:v-model|:model-value)(?:\.trim)?="' + re.escape(model_path) + r'"[^>]*?>'

    def replacement(match):
        tag = match.group(0)
        # Remove existing v-model, :model-value, @update:model-value
        tag = re.sub(r'\s+(?:v-model|:model-value)(?:\.trim)?="[^"]+"', '', tag)
        tag = re.sub(r'\s+@update:model-value="[^"]+"', '', tag)
        tag = re.sub(r'\s+upper-case', '', tag)

        # Add the new ones
        if 'gstId' in model_path:
             new_parts = f' :model-value="{model_path}" @update:model-value="val => marsRequiredFormattingofGST(val ? val.toUpperCase() : val)"'
        else:
             new_parts = f' :model-value="{model_path}" @update:model-value="val => {{ {model_path} = val ? val.toUpperCase() : val; }}"'

        return tag.replace('<q-input', '<q-input' + new_parts)

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Fixed uppercase in {filepath} for {model_path}")

# Implementation Queue fix: Use ONLY placeholder
def fix_implementation_queue(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove any labels or v-if labels I added
    content = re.sub(r'\s+label="Assign To" v-if="!formData\.assignTo"', '', content)
    # Ensure it has placeholder="Assign To"
    if 'placeholder="Assign To"' not in content:
        content = content.replace('v-model="formData.assignTo"', 'v-model="formData.assignTo"\n              placeholder="Assign To"')

    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Fixed Implementation Queue in {filepath}")

# Main form
process_list = [
    ('src/components/sat/showMarsFormComponent.vue', [
        'merchant.companyInformation.pan',
        'merchant.companyInformation.tan',
        'merchant.businessInformation.gstId',
        'viewBinding.partnersArr[index].pan',
        'merchant.bankInformation.bankDetails.ifsc'
    ]),
    ('src/components/sat/dataEntry/companyInformation.vue', ['merchant.companyInformation.pan', 'merchant.companyInformation.tan']),
    ('src/components/sat/dataEntry/bankInformation.vue', ['merchant.bankInformation.bankDetails.ifsc']),
    ('src/components/sat/dataEntry/partnersInformation.vue', ['partner.pan']),
    ('src/components/sat/dataEntry/businessInformation.vue', ['merchant.businessInformation.gstId']),
    ('src/pages/sat/changemanagementeditdatarsmreject.vue', ['merchant.companyinformation.pan', 'merchant.bankInformation.bankDetails.ifsc']),
    ('src/pages/sat/changemanagementeditdatafinancereject.vue', ['merchant.companyinformation.pan', 'merchant.bankInformation.bankDetails.ifsc']),
    ('src/pages/sat/changemanagementeditdatareject.vue', ['merchant.companyinformation.pan', 'merchant.bankInformation.bankDetails.ifsc']),
    ('src/pages/sat/changemanagementeditdata.vue', ['merchant.bankInformation.bankDetails.ifsc'])
]

for filepath, models in process_list:
    for model in models:
        fix_uppercase(filepath, model)

implementation_files = [
    'src/components/sat/internalimplementationRequest.vue',
    'src/components/sat/assigned.vue',
    'src/components/sat/externalimplementationRequest.vue',
    'src/components/sat/Phonepeassigned.vue'
]
for f in implementation_files:
    fix_implementation_queue(f)
