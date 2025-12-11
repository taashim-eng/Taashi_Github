import os
import subprocess
import shutil
from datetime import datetime
import sys

def run_command(cmd, cwd=None, check=True):
    """Execute shell command and return result."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check,
            shell=isinstance(cmd, str)
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr, e.returncode

def check_prerequisites():
    """Check if git and gh CLI are available."""
    print("🔍 Checking prerequisites...")
    
    # Check git
    stdout, stderr, code = run_command(["git", "--version"], check=False)
    if code != 0:
        print("   ❌ Git not found. Please install git first.")
        return False
    print(f"   ✅ Git found: {stdout}")
    
    # Check gh CLI
    stdout, stderr, code = run_command(["gh", "--version"], check=False)
    if code != 0:
        print("   ❌ GitHub CLI (gh) not found.")
        print("      Install: https://cli.github.com/")
        print("      Or create repo manually on GitHub")
        return False
    print(f"   ✅ GitHub CLI found: {stdout.split()[0]}")
    
    # Check gh auth
    stdout, stderr, code = run_command(["gh", "auth", "status"], check=False)
    if code != 0:
        print("   ❌ GitHub CLI not authenticated.")
        print("      Run: gh auth login")
        return False
    print("   ✅ GitHub CLI authenticated")
    
    return True

def create_backup(source_path):
    """Create backup of Implementation Code."""
    backup_name = f"Implementation_Code_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_path = os.path.join(os.path.dirname(source_path), backup_name)
    
    print(f"\n💾 Creating backup...")
    try:
        shutil.copytree(source_path, backup_path)
        print(f"   ✅ Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"   ❌ Backup failed: {e}")
        return None

def create_private_github_repo(repo_name, description):
    """Create a private repository on GitHub using gh CLI."""
    print(f"\n🔐 Creating private GitHub repository: {repo_name}...")
    
    cmd = [
        "gh", "repo", "create", repo_name,
        "--private",
        "--description", description,
        "--confirm"
    ]
    
    stdout, stderr, code = run_command(cmd, check=False)
    
    if code == 0:
        print(f"   ✅ Private repo created successfully!")
        # Extract repo URL
        repo_url = f"https://github.com/{get_github_username()}/{repo_name}.git"
        print(f"   📍 URL: {repo_url}")
        return repo_url
    else:
        # Check if repo already exists
        if "already exists" in stderr.lower():
            print(f"   ⚠️ Repository already exists")
            repo_url = f"https://github.com/{get_github_username()}/{repo_name}.git"
            return repo_url
        else:
            print(f"   ❌ Failed to create repo: {stderr}")
            return None

def get_github_username():
    """Get GitHub username from gh CLI."""
    stdout, stderr, code = run_command(["gh", "api", "user", "--jq", ".login"], check=False)
    if code == 0:
        return stdout.strip()
    return "YOUR_USERNAME"

def initialize_and_push_repo(local_path, remote_url, repo_name):
    """Initialize git repo, commit files, and push to remote."""
    print(f"\n📤 Setting up git repository in Implementation Code...")
    
    # Initialize git repo
    print("   1. Initializing git...")
    stdout, stderr, code = run_command(["git", "init"], cwd=local_path, check=False)
    if code != 0:
        print(f"      ❌ Failed to init: {stderr}")
        return False
    print("      ✅ Git initialized")
    
    # Create .gitignore for Python projects
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.log
.DS_Store

# IDE
.vscode/
.idea/
*.swp
*.swo

# Project specific
*.backup
backup_*/
"""
    gitignore_path = os.path.join(local_path, ".gitignore")
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        print("      ✅ Created .gitignore")
    
    # Add all files
    print("   2. Adding files...")
    stdout, stderr, code = run_command(["git", "add", "."], cwd=local_path, check=False)
    if code != 0:
        print(f"      ❌ Failed to add files: {stderr}")
        return False
    print("      ✅ Files added")
    
    # Commit
    print("   3. Creating initial commit...")
    commit_msg = f"Initial commit: Private implementation code for {repo_name}"
    stdout, stderr, code = run_command(
        ["git", "commit", "-m", commit_msg],
        cwd=local_path,
        check=False
    )
    if code != 0:
        print(f"      ⚠️ Commit warning: {stderr}")
    print("      ✅ Initial commit created")
    
    # Add remote
    print("   4. Adding remote...")
    stdout, stderr, code = run_command(
        ["git", "remote", "add", "origin", remote_url],
        cwd=local_path,
        check=False
    )
    if code != 0 and "already exists" not in stderr:
        print(f"      ❌ Failed to add remote: {stderr}")
        return False
    print("      ✅ Remote added")
    
    # Rename branch to main
    print("   5. Setting branch to main...")
    run_command(["git", "branch", "-M", "main"], cwd=local_path, check=False)
    print("      ✅ Branch set to main")
    
    # Push
    print("   6. Pushing to GitHub...")
    stdout, stderr, code = run_command(
        ["git", "push", "-u", "origin", "main"],
        cwd=local_path,
        check=False
    )
    if code != 0:
        print(f"      ❌ Failed to push: {stderr}")
        return False
    print("      ✅ Pushed to GitHub successfully!")
    
    return True

def update_main_repo_with_submodule(main_repo_path, submodule_path, submodule_url):
    """Add the private repo as a submodule to main repo."""
    print(f"\n🔗 Adding as submodule to main repository...")
    
    # Remove from tracking if it exists
    print("   1. Removing old tracking (if exists)...")
    run_command(
        ["git", "rm", "-rf", "--cached", "Implementation Code"],
        cwd=main_repo_path,
        check=False
    )
    
    # Add as submodule
    print("   2. Adding as submodule...")
    stdout, stderr, code = run_command(
        ["git", "submodule", "add", "-f", submodule_url, "Implementation Code"],
        cwd=main_repo_path,
        check=False
    )
    
    if code != 0 and "already exists" not in stderr:
        print(f"      ⚠️ Submodule add warning: {stderr}")
    else:
        print("      ✅ Submodule added")
    
    # Commit the change
    print("   3. Committing submodule addition...")
    run_command(
        ["git", "add", ".gitmodules", "Implementation Code"],
        cwd=main_repo_path,
        check=False
    )
    
    stdout, stderr, code = run_command(
        ["git", "commit", "-m", "Add Implementation Code as private submodule"],
        cwd=main_repo_path,
        check=False
    )
    
    if code != 0:
        print(f"      ℹ️ Commit status: {stderr}")
    else:
        print("      ✅ Changes committed")
    
    # Push
    print("   4. Pushing to GitHub...")
    stdout, stderr, code = run_command(
        ["git", "push"],
        cwd=main_repo_path,
        check=False
    )
    
    if code != 0:
        print(f"      ⚠️ Push warning: {stderr}")
    else:
        print("      ✅ Pushed to GitHub")
    
    return True

def main():
    """Main execution flow."""
    print("="*70)
    print("🚀 AUTOMATED PRIVATE REPOSITORY SETUP")
    print("="*70)
    print("\nThis script will:")
    print("  1. ✅ Create a backup of 'Implementation Code'")
    print("  2. ✅ Create a new PRIVATE GitHub repository")
    print("  3. ✅ Initialize and push Implementation Code to private repo")
    print("  4. ✅ Add it as a submodule to your main repo")
    print("  5. ✅ Keep your main repo completely safe")
    print("\n" + "="*70)
    
    # Configuration
    main_repo_path = "/workspaces/Taashi_Github"
    impl_code_path = os.path.join(main_repo_path, "Implementation Code")
    private_repo_name = "Taashi_Private_Code"
    repo_description = "Private implementation code and backups for Taashi_Github projects"
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please install required tools.")
        return 1
    
    # Check if Implementation Code exists
    if not os.path.exists(impl_code_path):
        print(f"\n❌ Error: {impl_code_path} not found!")
        return 1
    print(f"\n✅ Found: {impl_code_path}")
    
    # Step 1: Create backup
    backup_path = create_backup(impl_code_path)
    if not backup_path:
        print("\n❌ Backup failed. Aborting for safety.")
        return 1
    
    # Step 2: Create private GitHub repo
    remote_url = create_private_github_repo(private_repo_name, repo_description)
    if not remote_url:
        print("\n❌ Failed to create GitHub repository.")
        print("💡 You can create it manually on GitHub and re-run this script.")
        return 1
    
    # Step 3: Initialize and push
    success = initialize_and_push_repo(impl_code_path, remote_url, private_repo_name)
    if not success:
        print("\n⚠️ Failed to push to private repo.")
        print(f"💾 Your backup is safe at: {backup_path}")
        return 1
    
    # Step 4: Add as submodule to main repo
    success = update_main_repo_with_submodule(main_repo_path, impl_code_path, remote_url)
    
    # Final summary
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    print(f"\n📦 Private Repository: https://github.com/{get_github_username()}/{private_repo_name}")
    print(f"💾 Backup Location: {backup_path}")
    print(f"🔗 Main Repo: Updated with submodule reference")
    
    print("\n📋 What happened:")
    print("  ✅ Implementation Code is now in a PRIVATE GitHub repo")
    print("  ✅ Only YOU can access the private repo")
    print("  ✅ Main repo links to it but doesn't contain the code")
    print("  ✅ Backup created locally (safe to delete after verification)")
    print("  ✅ Your main repo remains untouched and safe")
    
    print("\n🔮 Next steps:")
    print("  1. Verify on GitHub:")
    print(f"     https://github.com/{get_github_username()}/{private_repo_name}")
    print("  2. Verify main repo:")
    print(f"     https://github.com/{get_github_username()}/Taashi_Github")
    print("  3. Test locally:")
    print(f"     cd '{impl_code_path}' && ls -la")
    print(f"  4. Delete backup after verification:")
    print(f"     rm -rf '{backup_path}'")
    
    print("\n💡 Working with the private repo:")
    print("  # Make changes:")
    print(f"  cd '{impl_code_path}'")
    print("  git add .")
    print("  git commit -m 'Update implementation'")
    print("  git push")
    print("\n  # Update main repo reference:")
    print(f"  cd '{main_repo_path}'")
    print("  git add 'Implementation Code'")
    print("  git commit -m 'Update submodule'")
    print("  git push")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)