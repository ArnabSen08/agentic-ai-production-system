#!/bin/bash

# Automated Profile README Updater Script
# This script updates your GitHub profile README with the Multi-Agent AI System project

echo "🚀 Automated Profile README Updater"
echo "=================================================="

# Check if gh CLI is available
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found: $(gh --version | head -1)"
else
    echo "⚠️ GitHub CLI not found. You may need to authenticate manually."
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo "📁 Working in temporary directory: $TEMP_DIR"

# Clone the profile repository
echo "📥 Cloning your profile repository..."
cd "$TEMP_DIR"
git clone https://github.com/ArnabSen08/ArnabSen08.git

if [ $? -ne 0 ]; then
    echo "❌ Failed to clone repository"
    exit 1
fi

cd ArnabSen08

# Check if README.md exists
if [ ! -f "README.md" ]; then
    echo "❌ README.md not found in profile repository"
    exit 1
fi

# Create the new project entry
NEW_PROJECT='### 🤖 Production-Ready Multi-Agent AI System
**Enterprise-Grade AI System for Ready Tensor Certification** - Complete production system with 4 specialized agents (Coordinator, Research, Content, Validation), 90%+ test coverage, comprehensive security, real-time monitoring, and professional documentation.

**🔗 [Live Demo](https://arnabsen08.github.io/agentic-ai-production-system/) | [Repository](https://github.com/ArnabSen08/agentic-ai-production-system)**

**Tech Stack:** Python, Streamlit, OpenAI GPT-4, Pydantic, Pytest, Docker, GitHub Actions  
**Features:** Multi-agent coordination, Enterprise security, Real-time monitoring, 90%+ test pass rate, Production deployment ready

'

# Backup original README
cp README.md README.md.backup

# Use sed to insert the new project after "## 🏆 Featured Projects"
echo "✏️ Updating README content..."

# Find the line number of "## 🏆 Featured Projects"
PROJECTS_LINE=$(grep -n "## 🏆 Featured Projects" README.md | cut -d: -f1)

if [ -z "$PROJECTS_LINE" ]; then
    echo "❌ Could not find '## 🏆 Featured Projects' section"
    exit 1
fi

# Find the next line that starts with "###" (first existing project)
FIRST_PROJECT_LINE=$(tail -n +$((PROJECTS_LINE + 1)) README.md | grep -n "^### " | head -1 | cut -d: -f1)

if [ -z "$FIRST_PROJECT_LINE" ]; then
    # No existing projects, add after the header
    INSERT_LINE=$((PROJECTS_LINE + 1))
else
    # Insert before the first existing project
    INSERT_LINE=$((PROJECTS_LINE + FIRST_PROJECT_LINE))
fi

# Create new README with the project inserted
{
    head -n $((INSERT_LINE - 1)) README.md
    echo "$NEW_PROJECT"
    tail -n +$INSERT_LINE README.md
} > README.md.new

# Replace the original with the new version
mv README.md.new README.md

echo "✅ README updated successfully!"

# Configure git (in case it's not configured)
git config user.name "ArnabSen08" 2>/dev/null || true
git config user.email "arnabsen08@users.noreply.github.com" 2>/dev/null || true

# Add and commit changes
echo "📤 Committing changes..."
git add README.md

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️ No changes to commit"
    exit 0
fi

# Commit the changes
git commit -m "Add Production-Ready Multi-Agent AI System to featured projects"

if [ $? -ne 0 ]; then
    echo "❌ Failed to commit changes"
    exit 1
fi

# Push changes
echo "📤 Pushing changes to GitHub..."
git push origin main

if [ $? -ne 0 ]; then
    echo "❌ Failed to push changes. You may need to authenticate."
    echo "💡 Try running: gh auth login"
    echo "📁 Changes are ready in: $TEMP_DIR/ArnabSen08"
    echo "🔧 You can manually push from there"
    exit 1
fi

echo "✅ Changes pushed successfully!"
echo "🎉 Profile README updated successfully!"
echo "🔗 View your updated profile: https://github.com/ArnabSen08"

# Cleanup
cd /
rm -rf "$TEMP_DIR"

echo "🧹 Cleanup completed"