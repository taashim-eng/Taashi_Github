import os

def create_project_structure():
    # Define the root path for Project 16
    base_path = "/workspaces/Taashi_Github/16_Agentic_Financial_Analyst"
    
    # Define sub-directories
    folders = [
        base_path,
        os.path.join(base_path, "data"),
        os.path.join(base_path, "src"),
        os.path.join(base_path, "docs") # Added for future ADRs/Architecture docs
    ]
    
    print(f"🚀 Initializing Project 16 Structure...")
    
    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"   ✅ Created: {folder}")
        except Exception as e:
            print(f"   ❌ Error creating {folder}: {e}")

    print("\nDirectory setup complete. Ready for code injection.")

if __name__ == "__main__":
    create_project_structure()