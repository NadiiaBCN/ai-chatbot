#!/usr/bin/env python3
"""Setup script."""

import os
from pathlib import Path


def create_dirs():
    """Create necessary directories."""
    dirs = ["data/documents", "logs"]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {d}")


def check_env():
    """Check .env file."""
    if not Path(".env").exists():
        print("⚠ .env file not found!")
        print("Run: cp .env.example .env")
        return False
    print("✓ .env file exists")
    return True


def main():
    """Main setup."""
    print("=" * 50)
    print("AI Chatbot Setup")
    print("=" * 50)
    
    create_dirs()
    env_ok = check_env()
    
    if env_ok:
        print("\n✓ Setup complete!")
        print("\nNext steps:")
        print("1. Edit .env with your API keys")
        print("2. Add documents to data/documents/")
        print("3. Run: python -m src.main")
    else:
        print("\n⚠ Please create .env file first")


if __name__ == "__main__":
    main()
