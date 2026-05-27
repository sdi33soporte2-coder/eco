#!/usr/bin/env python3
"""Rename 'eco' references to 'eco' in JS/TS/TSX/JSX/JSON files."""

import os
import re
import sys

EXCLUDE_DIRS = {'.git', 'venv', 'node_modules', 'website', '__pycache__'}
EXCLUDE_FILES = {'package-lock.json'}
BASE_DIR = '/home/danna/eco'

def should_process(filepath):
    rel = os.path.relpath(filepath, BASE_DIR)
    parts = rel.split(os.sep)
    for p in parts:
        if p in EXCLUDE_DIRS:
            return False
    fname = os.path.basename(filepath)
    if fname in EXCLUDE_FILES:
        return False
    ext = os.path.splitext(fname)[1].lower()
    return ext in ('.js', '.ts', '.tsx', '.jsx', '.json')

def has_eco(content):
    """Check if file has any eco-related pattern (case-insensitive)."""
    return bool(re.search(r'eco', content, re.IGNORECASE))

def replace_content(content, filepath):
    """
    Replace eco references following the rules:
    - 'eco' -> 'eco'
    - 'ECO' -> 'ECO'
    - 'ECO' -> 'ECO'
    - '.eco' -> '.eco'
    - '~/.eco' -> '~/.eco'
    - 'eco' -> 'eco'
    - Do NOT replace URLs to github.com/NousResearch
    """
    original = content
    
    # Step 1: Preserve GitHub NousResearch URLs by replacing them with placeholders
    # Pattern: github.com/NousResearch or github.com/NousResearch/...
    url_pattern = r'https?://github\.com/NousResearch/[^\s"\'`]*'
    urls = []
    def save_url(m):
        urls.append(m.group(0))
        return f'__URL_PLACEHOLDER_{len(urls)-1}__'
    
    content = re.sub(url_pattern, save_url, content)
    
    # Step 2: Replace 'eco' -> 'eco' (whole word boundaried)
    content = re.sub(r'eco', 'eco', content)
    content = re.sub(r'ECO-Agent', 'ECO', content)
    content = re.sub(r'ECO-AGENT', 'ECO', content)
    
    # Step 3: Replace '~/.eco' -> '~/.eco' (before .eco to avoid partial match)
    content = content.replace('~/.eco', '~/.eco')
    
    # Step 4: Replace '.eco' -> '.eco' (careful with word boundaries)
    # Only replace .eco when it's a dot-path reference (like config dir, not inside words)
    content = re.sub(r'(?<=\.)eco(?=\b)', 'eco', content)
    
    # Step 5: Replace standalone 'eco' with case mapping
    # 'eco' (lowercase) -> 'eco'
    # 'ECO' (capitalized) -> 'ECO'
    # 'ECO' (all caps) -> 'ECO'
    content = re.sub(r'\bhermes\b', 'eco', content)
    content = re.sub(r'\bHermes\b', 'ECO', content)
    content = re.sub(r'\bHERMES\b', 'ECO', content)
    
    # Step 6: Restore URLs
    for i, url in enumerate(urls):
        content = content.replace(f'__URL_PLACEHOLDER_{i}__', url)
    
    return content

def main():
    changed_files = []
    skipped_eco = []
    skipped_no_eco = []
    
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip excluded dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for fname in files:
            fpath = os.path.join(root, fname)
            if not should_process(fpath):
                continue
            
            try:
                with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
            except Exception as e:
                print(f"  SKIP (read error): {os.path.relpath(fpath, BASE_DIR)}: {e}")
                continue
            
            if not has_eco(content):
                skipped_no_eco.append(fpath)
                continue
            
            new_content = replace_content(content, fpath)
            
            if new_content == content:
                print(f"  NO CHANGE: {os.path.relpath(fpath, BASE_DIR)}")
                skipped_eco.append(fpath)
                continue
            
            try:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  CHANGED: {os.path.relpath(fpath, BASE_DIR)}")
                changed_files.append(fpath)
            except Exception as e:
                print(f"  ERROR writing {os.path.relpath(fpath, BASE_DIR)}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Total files changed: {len(changed_files)}")
    print(f"Files skipped (had eco but no change needed): {len(skipped_eco)}")
    print(f"Files skipped (no eco found): {len(skipped_no_eco)}")
    print(f"{'='*60}")
    
    if changed_files:
        print("\nChanged files:")
        for f in changed_files:
            print(f"  {os.path.relpath(f, BASE_DIR)}")

if __name__ == '__main__':
    main()
