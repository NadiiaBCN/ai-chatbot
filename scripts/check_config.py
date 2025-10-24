#!/usr/bin/env python3
"""Validate configuration and environment."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env
load_dotenv()


def check_env_var(name: str, required: bool = True) -> bool:
    """Check if environment variable is set."""
    value = os.getenv(name)
    if not value:
        if required:
            print(f"❌ {name} is not set")
            return False
        else:
            print(f"⚠️  {name} is not set (optional)")
            return True

    # Check if it's still the placeholder
    if "your_" in value.lower() or "here" in value.lower():
        print(f"❌ {name} is set to placeholder value")
        return False

    print(f"✓ {name} is configured")
    return True


def check_directories():
    """Check if required directories exist."""
    dirs = ["data/documents", "logs"]
    all_ok = True

    for d in dirs:
        if Path(d).exists():
            print(f"✓ Directory {d} exists")
        else:
            print(f"❌ Directory {d} does not exist")
            all_ok = False

    return all_ok


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 11:
        print(
            f"✓ Python version {version.major}.{version.minor}.{version.micro} is OK")
        return True
    else:
        print(
            f"❌ Python version {version.major}.{version.minor}.{version.micro} is too old (need 3.11+)")
        return False


def check_packages():
    """Check if required packages are installed."""
    packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "telegram",
        "openai",
        "pinecone",
        "PyPDF2",
        "docx",
        "watchdog",
        "loguru"
    ]

    all_ok = True
    for package in packages:
        try:
            __import__(package)
            print(f"✓ Package {package} is installed")
        except ImportError:
            print(f"❌ Package {package} is not installed")
            all_ok = False

    return all_ok


def main():
    """Run all checks."""
    print("=" * 60)
    print("Configuration Validation")
    print("=" * 60)
    print()

    # Check if .env exists
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("Run: cp .env.example .env")
        print()
        sys.exit(1)

    print("✓ .env file exists")
    print()

    # Python version
    print("Checking Python version...")
    python_ok = check_python_version()
    print()

    # Environment variables
    print("Checking environment variables...")
    telegram_ok = check_env_var("TELEGRAM_BOT_TOKEN")
    openai_ok = check_env_var("OPENAI_API_KEY")
    pinecone_key_ok = check_env_var("PINECONE_API_KEY")
    pinecone_env_ok = check_env_var("PINECONE_ENVIRONMENT")
    pinecone_index_ok = check_env_var("PINECONE_INDEX_NAME")
    print()

    # Directories
    print("Checking directories...")
    dirs_ok = check_directories()
    print()

    # Packages
    print("Checking installed packages...")
    packages_ok = check_packages()
    print()

    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)

    all_checks = [
        python_ok,
        telegram_ok,
        openai_ok,
        pinecone_key_ok,
        pinecone_env_ok,
        pinecone_index_ok,
        dirs_ok,
        packages_ok
    ]

    if all(all_checks):
        print("✅ All checks passed! You're ready to run the bot.")
        print()
        print("Next steps:")
        print("1. Add documents to data/documents/")
        print("2. Run: python -m src.main")
        sys.exit(0)
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("- Missing .env: cp .env.example .env")
        print("- Missing packages: pip install -r requirements.txt")
        print("- Missing directories: python scripts/setup.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
