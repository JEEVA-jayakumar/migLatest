import sys

filepath = 'src/components/sat/showMarsFormComponent.vue'
with open(filepath, 'r') as f:
    content = f.read()

# Pattern to find q-input with q-date and q-icon
# We want to move the q-popup-proxy inside the q-icon

import re

# Generic replacement for all date inputs in this file
pattern = r'(<q-input[^>]*mask="####-##-##"[^>]*>)\s*<q-popup-proxy([^>]*)>\s*(<q-date[^>]*/>)\s*</q-popup-proxy>\s*<template v-slot:append>\s*<q-icon name="event" class="cursor-pointer" />\s*</template>\s*</q-input>'

replacement = r'''\1
 <template v-slot:append>
 <q-icon name="event" class="cursor-pointer">
 <q-popup-proxy\2>
 \3
 </q-popup-proxy>
 </q-icon>
 </template>
 <q-popup-proxy\2>
 \3
 </q-popup-proxy>
 </q-input>'''

new_content = re.sub(pattern, replacement, content)

with open(filepath, 'w') as f:
    f.write(new_content)
