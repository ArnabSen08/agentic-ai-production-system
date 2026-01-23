#!/usr/bin/env python3
"""
Automated Profile README Updater
This script automatically updates your GitHub profile README to include the Multi-Agent AI System project.
"""

import subprocess
import sys
import os
import tempfile
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None, e.stderr

def clone_profile_repo():
    """Clone the profile repository to a temporary directory."""
    print("📥 Cloning your profile repository...")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    os.chdir(temp_dir)
    
    # Clone the repository
    stdout, stderr = run_command("git clone https://github.com/ArnabSen08/ArnabSen08.git")
    if stdout is None:
        print("❌ Failed to clone repository")
        return None
    
    profile_dir = os.path.join(temp_dir, "ArnabSen08")
    return profile_dir

def update_readme_content(readme_path):
    """Update the README.md content with the new project."""
    print("✏️ Updating README content...")
    
    # Read current README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # New project entry
    new_project = """### 🤖 Production-Ready Multi-Agent AI System
**Enterprise-Grade AI System for Ready Tensor Certification** - Complete production system with 4 specialized agents (Coordinator, Research, Content, Validation), 90%+ test coverage, comprehensive security, real-time monitoring, and professional documentation.

**🔗 [Live Demo](https://arnabsen08.github.io/agentic-ai-production-system/) | [Repository](https://github.com/ArnabSen08/agentic-ai-production-system)**

**Tech Stack:** Python, Streamlit, OpenAI GPT-4, Pydantic, Pytest, Docker, GitHub Actions  
**Features:** Multi-agent coordination, Enterprise security, Real-time monitoring, 90%+ test pass rate, Production deployment ready

"""
    
    # Find the Featured Projects section and add the new project
    if "## 🏆 Featured Projects" in content:
        # Split content at the Featured Projects section
        parts = content.split("## 🏆 Featured Projects")
        if len(parts) >= 2:
            # Find the next section or end of content
            after_projects = parts[1]
            
            # Look for the first existing project (starts with ###)
            lines = after_projects.split('\n')
            insert_index = 0
            
            for i, line in enumerate(lines):
                if line.strip().startswith('### '):
                    insert_index = i
                    break
            
            # Insert the new project before the first existing project
            lines.insert(insert_index, new_project)
            
            # Reconstruct the content
            updated_content = parts[0] + "## 🏆 Featured Projects" + '\n'.join(lines)
            
            # Write updated content
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print("✅ README updated successfully!")
            return True
    
    print("❌ Could not find Featured Projects section")
    return False

def commit_and_push_changes(profile_dir):
    """Commit and push the changes to GitHub."""
    print("📤 Committing and pushing changes...")
    
    os.chdir(profile_dir)
    
    # Configure git (in case it's not configured)
    run_command("git config user.name 'ArnabSen08'", check=False)
    run_command("git config user.email 'arnabsen08@users.noreply.github.com'", check=False)
    
    # Add changes
    stdout, stderr = run_command("git add README.md")
    if stdout is None:
        return False
    
    # Check if there are changes to commit
    stdout, stderr = run_command("git diff --cached --quiet", check=False)
    if stdout is not None:  # No changes
        print("ℹ️ No changes to commit")
        return True
    
    # Commit changes
    commit_message = "Add Production-Ready Multi-Agent AI System to featured projects"
    stdout, stderr = run_command(f'git commit -m "{commit_message}"')
    if stdout is None:
        return False
    
    # Push changes
    stdout, stderr = run_command("git push origin main")
    if stdout is None:
        print("❌ Failed to push changes. You may need to authenticate.")
        print("💡 Try running: gh auth login")
        return False
    
    print("✅ Changes pushed successfully!")
    return True

def main():
    """Main function to update the profile README."""
    print("🚀 Automated Profile README Updater")
    print("=" * 50)
    
    # Check if gh CLI is available
    stdout, stderr = run_command("gh --version", check=False)
    if stdout is None:
        print("⚠️ GitHub CLI not found. You may need to authenticate manually.")
    else:
        print(f"✅ GitHub CLI found: {stdout.split()[2]}")
    
    # Clone repository
    profile_dir = clone_profile_repo()
    if not profile_dir:
        return False
    
    # Update README
    readme_path = os.path.join(profile_dir, "README.md")
    if not os.path.exists(readme_path):
        print("❌ README.md not found in profile repository")
        return False
    
    if not update_readme_content(readme_path):
        return False
    
    # Commit and push
    if not commit_and_push_changes(profile_dir):
        print("\n💡 Manual steps to complete:")
        print(f"1. Navigate to: {profile_dir}")
        print("2. Review the changes: git diff")
        print("3. Push manually: git push origin main")
        return False
    
    print("\n🎉 Profile README updated successfully!")
    print("🔗 View your updated profile: https://github.com/ArnabSen08")
    
    # Cleanup
    import shutil
    shutil.rmtree(os.path.dirname(profile_dir))
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)