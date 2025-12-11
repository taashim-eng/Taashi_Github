import os

def update_root_readme():
    readme_path = "/workspaces/Taashi_Github/README.md"
    
    # The content to insert
    ai_section = """
---
## 🧠 Section 3: AI & Agentic Architectures

### Project 16: The Wall Street Swarm (Multi-Agent Financial System)
* **Goal:** Automate high-value investment research by mimicking a human analyst team (Researcher + Quant + Writer).
* **Architecture:** **Agentic Workflow** using sequential hand-offs and deterministic tool use.
* **Key Tech:** Python, LLM Orchestration, Vector Search Patterns.
* **Why it Matters:** Demonstrates how to solve **hallucination** and **auditability** challenges in FinTech by decoupling "Reasoning" (LLM) from "Knowledge" (Deterministic Tools).
* **[View Project Code](./Implementation%20Code/16_Agentic_Financial_Analyst)**

"""

    print(f"📖 Reading: {readme_path}")
    
    # Check if file exists
    if not os.path.exists(readme_path):
        print(f"   ❌ Error: File not found at {readme_path}")
        return False
    
    try:
        # Read the file
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"   ✓ File read successfully ({len(content)} characters)")
        
        # Debug: Show a snippet of content around where we're searching
        if "Technical Leadership" in content:
            idx = content.find("Technical Leadership")
            print(f"   ✓ Found 'Technical Leadership' at position {idx}")
            snippet = content[max(0, idx-100):min(len(content), idx+100)]
            print(f"   Context: ...{snippet}...")
        else:
            print("   ⚠️ 'Technical Leadership' not found in file")
            print("   Searching for alternative markers...")
            # Search for common variations
            alternatives = ["## Technical Leadership", "### Technical Leadership", 
                          "technical leadership", "TECHNICAL LEADERSHIP"]
            for alt in alternatives:
                if alt in content:
                    print(f"   ✓ Found alternative: '{alt}'")
                    break
        
        # Multiple search strategies
        markers_to_try = [
            "## 🛠️ Technical Leadership Areas",
            "## Technical Leadership Areas",
            "## 🛠️ Technical Leadership",
            "## Technical Leadership",
            "### Technical Leadership", 
            "Technical Leadership Areas",
            "Technical Leadership"
        ]
        
        insert_index = -1
        found_marker = None
        
        for marker in markers_to_try:
            insert_index = content.find(marker)
            if insert_index != -1:
                found_marker = marker
                print(f"   ✅ Found marker: '{marker}' at position {insert_index}")
                break
        
        if insert_index == -1:
            print("   ⚠️ Could not find any Technical Leadership marker. Appending to end.")
            new_full_content = content.rstrip() + "\n\n" + ai_section
        else:
            # Find the start of the line containing the marker
            # Go backwards to find the last newline before the marker
            line_start = content.rfind('\n', 0, insert_index)
            
            if line_start == -1:
                # Marker is at the very beginning of the file
                line_start = 0
            else:
                # Include the newline in part_2
                line_start += 1
            
            # Split and insert
            part_1 = content[:line_start]
            part_2 = content[line_start:]
            
            # Ensure proper spacing
            if not part_1.endswith('\n'):
                part_1 += '\n'
            
            new_full_content = part_1 + ai_section + part_2
            
            print(f"   ✅ Inserting AI section before '{found_marker}'")
        
        # Create backup
        backup_path = readme_path + ".backup"
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   ✓ Backup created: {backup_path}")
        
        # Write the updated content
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_full_content)
        
        print(f"   ✅ README updated successfully! ({len(new_full_content)} characters)")
        print(f"   📊 Added {len(new_full_content) - len(content)} characters")
        
        return True
        
    except PermissionError:
        print(f"   ❌ Permission denied: Cannot write to {readme_path}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = update_root_readme()
    if success:
        print("\n🎉 Update complete!")
    else:
        print("\n❌ Update failed. Check errors above.")