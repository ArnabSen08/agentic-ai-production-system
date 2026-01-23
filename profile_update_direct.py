#!/usr/bin/env python3
"""
Direct Profile README Updater using GitHub API
"""

import subprocess
import json
import base64

def run_gh_command(command):
    """Run a GitHub CLI command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None

def get_current_readme():
    """Get the current README content from GitHub."""
    print("📥 Fetching current README...")
    
    # Get file content using GitHub CLI
    result = run_gh_command("gh api repos/ArnabSen08/ArnabSen08/contents/README.md")
    if not result:
        return None, None
    
    file_data = json.loads(result)
    content = base64.b64decode(file_data['content']).decode('utf-8')
    sha = file_data['sha']
    
    return content, sha

def update_readme_with_project(content):
    """Add the Multi-Agent AI System project to the README."""
    print("✏️ Adding Multi-Agent AI System project...")
    
    new_project = """### 🤖 Production-Ready Multi-Agent AI System
**Enterprise-Grade AI System for Ready Tensor Certification** - Complete production system with 4 specialized agents (Coordinator, Research, Content, Validation), 90%+ test coverage, comprehensive security, real-time monitoring, and professional documentation.

**🔗 [Live Demo](https://arnabsen08.github.io/agentic-ai-production-system/) | [Repository](https://github.com/ArnabSen08/agentic-ai-production-system)**

**Tech Stack:** Python, Streamlit, OpenAI GPT-4, Pydantic, Pytest, Docker, GitHub Actions  
**Features:** Multi-agent coordination, Enterprise security, Real-time monitoring, 90%+ test pass rate, Production deployment ready

"""
    
    # Check if project already exists
    if "Production-Ready Multi-Agent AI System" in content:
        print("ℹ️ Project already exists in README")
        return content
    
    # Find the Featured Projects section
    if "## 🏆 Featured Projects" in content:
        lines = content.split('\n')
        updated_lines = []
        found_projects = False
        inserted = False
        
        for line in lines:
            updated_lines.append(line)
            
            # After the Featured Projects header, insert our project before the first existing project
            if found_projects and line.strip().startswith('### ') and not inserted:
                # Insert our project before this existing project
                updated_lines.insert(-1, new_project)
                inserted = True
            elif line.strip() == "## 🏆 Featured Projects":
                found_projects = True
        
        # If we didn't find any existing projects, add it after the header
        if found_projects and not inserted:
            # Find the line after "## 🏆 Featured Projects" and insert there
            for i, line in enumerate(updated_lines):
                if line.strip() == "## 🏆 Featured Projects":
                    updated_lines.insert(i + 1, "\n" + new_project)
                    break
        
        return '\n'.join(updated_lines)
    
    print("❌ Could not find Featured Projects section")
    return content

def update_github_readme(content, sha):
    """Update the README on GitHub."""
    print("📤 Updating README on GitHub...")
    
    # Encode content to base64
    encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    # Create the update payload
    update_data = {
        "message": "Add Production-Ready Multi-Agent AI System to featured projects",
        "content": encoded_content,
        "sha": sha
    }
    
    # Write to temporary file for gh api
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(update_data, f)
        temp_file = f.name
    
    try:
        # Update using GitHub CLI
        result = run_gh_command(f"gh api repos/ArnabSen08/ArnabSen08/contents/README.md --method PUT --input {temp_file}")
        if result:
            print("✅ README updated successfully!")
            return True
        else:
            print("❌ Failed to update README")
            return False
    finally:
        os.unlink(temp_file)

def main():
    """Main function."""
    print("🚀 Direct Profile README Updater")
    print("=" * 40)
    
    # Get current README
    content, sha = get_current_readme()
    if not content:
        print("❌ Failed to fetch current README")
        return False
    
    # Update content
    updated_content = update_readme_with_project(content)
    
    # Check if content changed
    if updated_content == content:
        print("ℹ️ No changes needed")
        return True
    
    # Update on GitHub
    if update_github_readme(updated_content, sha):
        print("\n🎉 Profile README updated successfully!")
        print("🔗 View your updated profile: https://github.com/ArnabSen08")
        return True
    
    return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)