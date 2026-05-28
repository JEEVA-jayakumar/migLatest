import os
import re

def search_files(directory):
    pattern = re.compile(r'\b(serviceProvider|networkPreferred|rentalPlanCode)\b\s*:\s*["\']?1["\']?')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.vue') or file.endswith('.js'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r') as f:
                        for i, line in enumerate(f):
                            if pattern.search(line):
                                print(f"{path}:{i+1}: {line.strip()}")
                except:
                    pass

search_files('src')
