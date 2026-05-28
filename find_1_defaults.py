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
                        if 'serviceProvider: 1' in content or 'networkPreferred: 1' in content or 'rentalPlanCode: 1' in content:
                            print(f"Found in {path}")
                            # Print lines
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if 'serviceProvider: 1' in line or 'networkPreferred: 1' in line or 'rentalPlanCode: 1' in line:
                                    print(f"  {i+1}: {line}")
                except:
                    pass

search_files('src')
