"""
Script to fix the corrupted app_integrated.py file
"""

# Read the corrupted file
with open("app_integrated.py.corrupted", "r", encoding="utf-8") as f:
    content = f.read()

# Find and remove the corrupted section at the top
# The corruption starts after "API_BASE_URL = API_BASE_URL" and before "@st.cache_data"

# Split into lines for easier manipulation
lines = content.split('\n')

# Find the problematic section
fixed_lines = []
skip_mode = False

for i, line in enumerate(lines):
    # Check if we're at the corrupted line
    if 'API_BASE_URL = API_BASE_URL' in line and 'Display location info' in line:
        # Replace with the correct line
        fixed_lines.append('API_BASE_URL = API_BASE_URL.rstrip("/")')
        skip_mode = True
        continue
    
    # Stop skipping when we hit the @st.cache_data line
    if skip_mode and '@st.cache_data' in line:
        skip_mode = False
        fixed_lines.append('')  # Add blank line
        fixed_lines.append('')  # Add blank line
    
    # Skip lines while in skip mode
    if skip_mode:
        continue
    
    fixed_lines.append(line)

# Write the fixed content
fixed_content = '\n'.join(fixed_lines)

with open("app_integrated_fixed.py", "w", encoding="utf-8") as f:
    f.write(fixed_content)

print("✅ File fixed and saved as app_integrated_fixed.py")
print("Review the file and then:")
print("  move app_integrated_fixed.py app_integrated.py")
