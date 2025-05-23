"""Generate favicon files from SVG.
This script converts the SVG favicon to multiple PNG files of different sizes."""
import os
from pathlib import Path
from cairosvg import svg2png
import shutil

# Get the project root directory
PROJECT_ROOT = Path(__file__).resolve().parent

# Paths
STATIC_DIR = PROJECT_ROOT / 'static'
ICONS_DIR = STATIC_DIR / 'icons'
SVG_PATH = ICONS_DIR / 'favicon.svg'

# Ensure the icons directory exists
ICONS_DIR.mkdir(exist_ok=True)

# Icon sizes to generate
SIZES = {
    'favicon-16x16.png': 16,
    'favicon-32x32.png': 32,
    'apple-touch-icon.png': 180,
    'android-chrome-192x192.png': 192,
    'android-chrome-512x512.png': 512,
}

def generate_icons():
    """Generate PNG icons in different sizes from the SVG file."""
    if not SVG_PATH.exists():
        print(f"Error: Source SVG file not found at {SVG_PATH}")
        return

    # Read the SVG content
    with open(SVG_PATH, 'rb') as f:
        svg_content = f.read()

    # Generate each size
    for filename, size in SIZES.items():
        output_path = ICONS_DIR / filename
        try:
            svg2png(
                bytestring=svg_content,
                write_to=str(output_path),
                output_width=size,
                output_height=size
            )
            print(f"Generated {filename}")
        except Exception as e:
            print(f"Error generating {filename}: {e}")

if __name__ == '__main__':
    print("Generating favicon files...")
    generate_icons()
    print("Done!")
