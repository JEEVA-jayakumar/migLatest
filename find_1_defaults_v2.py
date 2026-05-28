import os
import re

def search_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.vue') or file.endswith('.js'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                        # Use regex for word boundaries
                        if re.search(r'\b(serviceProvider|networkPreferred|rentalPlanCode)\b\s*:\s*1\b', content):
                            print(f"Found in {path}")
                            # Print lines
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if re.search(r'\b(serviceProvider|networkPreferred|rentalPlanCode)\b\s*:\s*1\b', line):
                                    print(f"  {i+1}: {line}")
                except:
                    pass

search_files('src')
