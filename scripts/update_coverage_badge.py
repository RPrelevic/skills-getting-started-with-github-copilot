#!/usr/bin/env python3
"""
Automated Coverage Badge Updater

This script runs the test suite, extracts coverage percentage,
and automatically updates the coverage badge in README.md
"""

import subprocess
import re
import sys
import os
from pathlib import Path


def get_coverage_color(percentage):
    """Determine badge color based on coverage percentage"""
    if percentage >= 90:
        return "brightgreen"
    elif percentage >= 75:
        return "orange"
    else:
        return "red"


def get_python_command():
    """Determine the best Python command to use based on the platform"""
    if os.name == "nt":  # Windows
        return "py"
    else:  # Linux/Mac
        # Try python3 first, then python
        for cmd in ["python3", "python"]:
            try:
                subprocess.run([cmd, "--version"], capture_output=True, check=True)
                return cmd
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        raise RuntimeError("No suitable Python command found (tried python3, python)")


def run_tests_with_coverage():
    """Run pytest with coverage and capture the output"""
    try:
        # Get the project root directory (parent of scripts directory)
        project_root = Path(__file__).parent.parent
        
        # Determine the Python command to use
        python_cmd = get_python_command()
        
        # Run pytest with coverage from project root
        result = subprocess.run(
            [python_cmd, "-m", "pytest", "tests/", "--cov=src", "--cov-report=term"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        
        if result.returncode != 0:
            print("❌ Tests failed!")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return None
            
        # Extract coverage percentage from output
        coverage_match = re.search(r'TOTAL\s+\d+\s+\d+\s+(\d+)%', result.stdout)
        if coverage_match:
            return int(coverage_match.group(1))
        else:
            print("❌ Could not extract coverage percentage from output")
            print("Output:", result.stdout)
            return None
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return None


def update_readme_badge(coverage_percentage):
    """Update the coverage badge in README.md"""
    # Get the project root directory (parent of scripts directory)
    project_root = Path(__file__).parent.parent
    readme_path = project_root / "src" / "README.md"
    
    if not readme_path.exists():
        print(f"❌ README.md not found at {readme_path}")
        return False
    
    try:
        # Read current README content
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine badge color
        color = get_coverage_color(coverage_percentage)
        
        # Create new badge URL
        new_badge = f"![Coverage](https://img.shields.io/badge/Coverage-{coverage_percentage}%25-{color}?style=flat-square)"
        
        # Replace existing badge
        badge_pattern = r'!\[Coverage\]\(https://img\.shields\.io/badge/Coverage-\d+%25-\w+\?style=flat-square\)'
        
        if re.search(badge_pattern, content):
            updated_content = re.sub(badge_pattern, new_badge, content)
            
            # Write updated content back to file
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✅ Successfully updated README badge to {coverage_percentage}% ({color})")
            return True
        else:
            print("❌ Coverage badge not found in README.md")
            return False
            
    except Exception as e:
        print(f"❌ Error updating README: {e}")
        return False


def main():
    """Main function to run tests and update badge"""
    print("🧪 Running tests with coverage...")
    
    coverage = run_tests_with_coverage()
    if coverage is None:
        sys.exit(1)
    
    print(f"📊 Coverage: {coverage}%")
    
    print("📝 Updating README badge...")
    if update_readme_badge(coverage):
        print(f"🎉 Badge updated successfully! Coverage: {coverage}%")
        
        # Show color coding explanation
        if coverage >= 90:
            print("🟢 Excellent coverage!")
        elif coverage >= 75:
            print("🟡 Good coverage - consider improving")
        else:
            print("🔴 Poor coverage - needs attention")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()