import sys
import logging
import argparse
from pathlib import Path
import tkinter as tk

from downloader.core import Downloader
from downloader.settings import Settings
from downloader.gui import DownloaderGUI
from downloader.utils import resource_path, HAS_THEMES, APP_NAME

if HAS_THEMES:
    from ttkthemes import ThemedTk

def run_cli(args):
    logger = logging.getLogger("cli")
    downloader = VideoDownloader(logger)
    
    if args.batch:
        with open(args.batch, 'r') as f:
            urls = [line.strip() for line in f if downloader.is_valid_url(line.strip())]
        results = downloader.batch_download(
            urls, args.output, args.quality, args.audio, 
            args.playlist, args.cookies, args.parallel, print
        )
        success_count = sum(1 for ok in results.values() if ok)
        print(f"Batch done: {success_count}/{len(urls)} successful")
        sys.exit(0 if success_count == len(urls) else 1)
    elif args.url:
        ok, _ = downloader.download(
            args.url, args.output, args.quality, args.audio, 
            args.playlist, args.cookies, print
        )
        sys.exit(0 if ok else 1)
    else:
        print("No URL or batch file provided for CLI mode.")
        sys.exit(1)

def main():
    """Main function to run the application."""
    # Ensure the settings directory exists
    settings_dir = Path.home() / f".{APP_NAME.lower().replace(' ', '_')}"
    settings_dir.mkdir(exist_ok=True)
    
    settings = Settings(path=settings_dir / "settings.json")
    downloader = Downloader()

    if HAS_THEMES:
        root = ThemedTk(theme="arc")
    else:
        root = tk.Tk()
        
    gui = DownloaderGUI(root, settings, downloader)
    root.mainloop()

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO, filename='downloader.log', filemode='a',
                        format='%(asctime)s - %(levelname)s - %(message)s')
    main()