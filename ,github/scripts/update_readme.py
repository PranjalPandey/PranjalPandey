# .github/scripts/update_readme.py
import datetime
import pytz # For accurate timezone handling
import re
import os

# --- Configuration ---
README_PATH = "README.md" # Assumes script runs from repo root
TIMEZONE = "Asia/Kolkata" # Your local timezone (IST)
START_MARKER = ""
END_MARKER = ""
# Example format: Monday, 28 April 2025, 03:50 PM IST
DATE_FORMAT = "%A, %d %B %Y, %I:%M %p %Z"
# --- -------------- ---

def update_readme_content(readme_content, new_dynamic_content):
    """Replaces content between markers in the README content."""
    # Use DOTALL flag to match across multiple lines
    pattern = re.compile(f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL)

    # Check if markers exist
    if not pattern.search(readme_content):
        print(f"Error: Markers '{START_MARKER}' or '{END_MARKER}' not found in {README_PATH}.")
        return None # Indicate failure

    # Replace content between markers
    replacement_string = f"{START_MARKER}\n{new_dynamic_content}\n{END_MARKER}"
    new_readme_content = pattern.sub(replacement_string, readme_content)
    return new_readme_content

if __name__ == "__main__":
    try:
        # Get current time in the specified timezone
        tz = pytz.timezone(TIMEZONE)
        now = datetime.datetime.now(tz)
        formatted_time = now.strftime(DATE_FORMAT)
        dynamic_content = f"🧭 Last updated on: {formatted_time}"

        # Read the current README content
        # Ensure the script finds README.md from the repo root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.abspath(os.path.join(script_dir, '..', '..')) # Go up two levels from .github/scripts
        readme_full_path = os.path.join(repo_root, README_PATH)

        if not os.path.exists(readme_full_path):
             print(f"Error: {README_PATH} not found at expected location: {readme_full_path}")
             exit(1)

        with open(readme_full_path, "r", encoding="utf-8") as f:
            current_content = f.read()

        # Generate the new README content
        new_content = update_readme_content(current_content, dynamic_content)

        if new_content is None:
            print("Failed to update README content due to missing markers.")
            exit(1)

        # Write the new content back only if it changed
        if new_content != current_content:
            with open(readme_full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ README updated successfully with timestamp.")
        else:
            print("✅ README content is already up-to-date. No changes made.")
            # Exit with a specific code or handle in workflow if needed
            # to prevent unnecessary commits if nothing changed. For simplicity,
            # we let the commit step handle checking for changes.

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        exit(1)