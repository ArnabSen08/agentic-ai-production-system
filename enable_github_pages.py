#!/usr/bin/env python3
"""
GitHub Pages Enablement Helper Script
This script helps check and guide you through enabling GitHub Pages.
"""

import subprocess
import sys
import webbrowser
from urllib.parse import quote

def get_repo_info():
    """Get repository information from git remote."""
    try:
        # Get remote URL
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True, check=True)
        remote_url = result.stdout.strip()
        
        # Parse GitHub URL
        if 'github.com' in remote_url:
            if remote_url.startswith('https://'):
                # https://github.com/username/repo.git
                repo_path = remote_url.replace('https://github.com/', '').replace('.git', '')
            elif remote_url.startswith('git@'):
                # git@github.com:username/repo.git
                repo_path = remote_url.replace('git@github.com:', '').replace('.git', '')
            else:
                return None, None
            
            parts = repo_path.split('/')
            if len(parts) == 2:
                return parts[0], parts[1]  # username, repo
        
        return None, None
    except subprocess.CalledProcessError:
        return None, None

def check_github_pages_status():
    """Check if we can determine GitHub Pages status."""
    username, repo = get_repo_info()
    
    if not username or not repo:
        print("❌ Could not determine GitHub repository information")
        return False
    
    print(f"📁 Repository: {username}/{repo}")
    
    # Try to check if GitHub Pages is already live
    pages_url = f"https://{username}.github.io/{repo}/"
    print(f"🌐 Expected GitHub Pages URL: {pages_url}")
    
    return username, repo

def open_github_pages_settings():
    """Open GitHub Pages settings in browser."""
    username, repo = get_repo_info()
    
    if username and repo:
        settings_url = f"https://github.com/{username}/{repo}/settings/pages"
        print(f"\n🔧 Opening GitHub Pages settings: {settings_url}")
        
        try:
            webbrowser.open(settings_url)
            return True
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print(f"📋 Please manually visit: {settings_url}")
            return False
    
    return False

def main():
    """Main function to help enable GitHub Pages."""
    print("🚀 GitHub Pages Enablement Helper")
    print("=" * 50)
    
    # Check repository info
    repo_info = check_github_pages_status()
    if not repo_info:
        print("\n❌ This doesn't appear to be a GitHub repository")
        print("💡 Make sure you're in a directory with a GitHub remote")
        return
    
    username, repo = repo_info
    
    print(f"\n📋 To enable GitHub Pages for {username}/{repo}:")
    print("1. Go to repository Settings")
    print("2. Scroll to 'Pages' in the left sidebar")
    print("3. Under 'Source', select 'Deploy from a branch'")
    print("4. Select 'main' branch and '/ (root)' folder")
    print("5. Click 'Save'")
    
    # Ask if user wants to open settings
    response = input("\n🤔 Would you like me to open the GitHub Pages settings in your browser? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        if open_github_pages_settings():
            print("\n✅ GitHub Pages settings opened in browser")
        else:
            print(f"\n📋 Please manually visit: https://github.com/{username}/{repo}/settings/pages")
    
    print(f"\n🌐 Once enabled, your site will be available at:")
    print(f"   https://{username}.github.io/{repo}/")
    
    print(f"\n📱 Interactive demo will be at:")
    print(f"   https://{username}.github.io/{repo}/docs/web/index.html")
    
    print("\n⏰ Note: GitHub Pages may take 5-10 minutes to become active after enabling")

if __name__ == "__main__":
    main()