#!/usr/bin/env python3
import os
import re
import sys
import shutil
import argparse
from datetime import datetime

# The script lives at <blog>/.gemini/skills/study-publisher/scripts/.
BLOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

def sanitize_slug(name):
    # Strip extension
    name = os.path.splitext(name)[0]
    # Replace non-alphanumeric (except hyphens/underscores) with hyphens
    sanitized = re.sub(r'[^a-zA-Z0-9\-_]', '-', name)
    # Remove consecutive hyphens
    sanitized = re.sub(r'-+', '-', sanitized)
    return sanitized.strip('-').lower()

def extract_date_and_slug(filename):
    base = os.path.basename(filename)
    # Check if starts with YYYY-MM-DD-
    match = re.match(r'^(\d{4}-\d{2}-\d{2})-(.*)$', base)
    if match:
        post_date = match.group(1)
        slug = sanitize_slug(match.group(2))
    else:
        post_date = datetime.now().strftime("%Y-%m-%d")
        slug = sanitize_slug(base)
    return post_date, slug

def main():
    parser = argparse.ArgumentParser(description="Publish study drafts to Jekyll blog.")
    parser.add_argument("--source", "-s", required=True, help="Path to the draft markdown file.")
    parser.add_argument(
        "--collection",
        "-c",
        required=True,
        choices=["papers", "engineering", "series"],
        help="Destination Jekyll collection.",
    )
    parser.add_argument(
        "--series",
        help="Series slug. Required when --collection series is selected.",
    )
    
    args = parser.parse_args()
    
    source_path = os.path.abspath(args.source)
    if not os.path.isfile(source_path):
        print(f"Error: Source file '{source_path}' does not exist.")
        sys.exit(1)
        
    if not os.path.isdir(BLOG_DIR):
        print(f"Error: Jekyll blog directory not found at '{BLOG_DIR}'")
        sys.exit(1)
        
    print(f"Reading draft: {source_path}")
    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Determine date and slug
    post_date, slug = extract_date_and_slug(os.path.basename(source_path))
    post_filename = f"{post_date}-{slug}.md"
    
    if args.collection == "series" and not args.series:
        print("Error: --series is required when publishing to the series collection.")
        sys.exit(1)

    if args.collection == "series":
        dest_dir = os.path.join(BLOG_DIR, "_series", sanitize_slug(args.series))
    else:
        dest_dir = os.path.join(BLOG_DIR, f"_{args.collection}")
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, post_filename)
    
    # Image assets destination
    # We copy local images to assets/images/study/<slug>/
    assets_rel_dir = os.path.join("assets", "images", args.collection, slug)
    assets_dest_dir = os.path.join(BLOG_DIR, assets_rel_dir)
    
    source_dir = os.path.dirname(source_path)
    
    # Find all markdown images: ![alt](path)
    # Negative lookahead/behind to ignore remote urls or liquid syntax
    image_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
    
    def replacer(match):
        alt_text = match.group(1)
        img_path = match.group(2).strip()
        
        # Check if remote or liquid variable
        if (img_path.startswith("http://") or 
            img_path.startswith("https://") or 
            img_path.startswith("/") or 
            img_path.startswith("{{")):
            return match.group(0)
            
        # Resolve absolute local path
        abs_img_path = os.path.abspath(os.path.join(source_dir, img_path))
        if os.path.isfile(abs_img_path):
            os.makedirs(assets_dest_dir, exist_ok=True)
            img_filename = os.path.basename(abs_img_path)
            # Sanitize image filename too to prevent spaces in URL
            img_filename_sanitized = re.sub(r'[^a-zA-Z0-9\.\-_]', '-', img_filename)
            img_filename_sanitized = re.sub(r'-+', '-', img_filename_sanitized)
            
            dest_img_path = os.path.join(assets_dest_dir, img_filename_sanitized)
            
            print(f"Copying image: {abs_img_path} -> {dest_img_path}")
            shutil.copy2(abs_img_path, dest_img_path)
            
            # Rewrite path to Jekyll liquid absolute path
            # We use {{ site.baseurl }}/assets/images/study/<slug>/<img_filename>
            new_path = f"{{{{ site.baseurl }}}}/{assets_rel_dir}/{img_filename_sanitized}"
            return f"![{alt_text}]({new_path})"
        else:
            print(f"Warning: Image file '{abs_img_path}' referenced in markdown was not found.")
            return match.group(0)
            
    # Update image links in content
    updated_content = image_pattern.sub(replacer, content)
    
    # Update date field in Front Matter if present
    # Matches 'date: YYYY-MM-DD' or similar
    updated_content = re.sub(r'^date:\s*.*$', f'date: {post_date}', updated_content, flags=re.MULTILINE)
    
    print(f"Writing updated post to: {dest_path}")
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print("\nPublishing complete!")
    print(f"- Post Path: {dest_path}")
    print(f"- Image Dir: {assets_dest_dir if os.path.exists(assets_dest_dir) else 'None (No local images copied)'}")

if __name__ == "__main__":
    main()
