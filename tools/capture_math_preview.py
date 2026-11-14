"""
Visual verification for Math Decks:
1. Card front for 2 x 7 = ?
2. Card back for 2 x 7 = 14
3. Advanced multiplication: 6 x 889 = ?
4. Deck picker showing bottom Matematika & Karra jadvali section
"""

import subprocess
import time
from pathlib import Path

root = Path(r"C:\Users\user\.gemini\antigravity\scratch\words-app\webapp")
artifact_dir = Path(r"C:\Users\user\.gemini\antigravity\brain\1f3a069b-dfc8-4f5c-8cdf-c960a29ee9ef")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Start a local static server to take screenshots
server = subprocess.Popen(["python", "-m", "http.server", "9988", "--directory", str(root)])
time.sleep(1)

try:
    # 1. Capture Math Deck Picker bottom section
    out_picker = artifact_dir / "preview_math_01_picker.png"
    subprocess.run([
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--window-size=390,844",
        f"--screenshot={out_picker}",
        "http://localhost:9988/index.html"
    ], timeout=15)
    print("Captured", out_picker)
finally:
    server.terminate()
