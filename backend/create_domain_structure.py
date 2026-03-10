import os

# Base path
base_path = r"F:\Propfirm\backend\app\domains"

# Domains to create
domains = ["identity", "challenge", "trading", "risk", "finance", "analytics", "notification"]

# Subdirectories for each domain
subdirs = ["models", "services", "schemas", "routes"]

# Create the structure
for domain in domains:
    domain_path = os.path.join(base_path, domain)
    os.makedirs(domain_path, exist_ok=True)
    
    for subdir in subdirs:
        subdir_path = os.path.join(domain_path, subdir)
        os.makedirs(subdir_path, exist_ok=True)
        
    # Create __init__.py files
    with open(os.path.join(domain_path, "__init__.py"), "w") as f:
        f.write(f"# {domain.capitalize()} domain package\n")
    
    for subdir in subdirs:
        subdir_path = os.path.join(domain_path, subdir)
        with open(os.path.join(subdir_path, "__init__.py"), "w") as f:
            f.write(f"# {domain.capitalize()} {subdir} package\n")

print("Domain structure created successfully!")