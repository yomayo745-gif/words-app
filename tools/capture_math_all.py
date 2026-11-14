import subprocess
import time
from pathlib import Path

webapp_dir = Path(r"C:\Users\user\.gemini\antigravity\scratch\words-app\webapp")
artifact_dir = Path(r"C:\Users\user\.gemini\antigravity\brain\1f3a069b-dfc8-4f5c-8cdf-c960a29ee9ef")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

server = subprocess.Popen(["python", "-m", "http.server", "9988", "--directory", str(webapp_dir)])
time.sleep(1.2)

try:
    # 1. Front card: 2 x 7 = ?
    out1 = artifact_dir / "preview_math_01_front.png"
    subprocess.run([
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--window-size=390,844",
        f"--screenshot={out1}",
        "http://localhost:9988/index.html?deck=math-01-multiplication-table&index=6"
    ], timeout=15)
    print("Captured", out1)

    # 2. Back card: 2 x 7 = 14
    out2 = artifact_dir / "preview_math_02_back.png"
    subprocess.run([
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--window-size=390,844",
        f"--screenshot={out2}",
        "http://localhost:9988/index.html?deck=math-01-multiplication-table&index=6&flip=1"
    ], timeout=15)
    print("Captured", out2)

    # 3. Advanced front: 6 x 889 = ?
    out3 = artifact_dir / "preview_math_03_advanced_front.png"
    subprocess.run([
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--window-size=390,844",
        f"--screenshot={out3}",
        "http://localhost:9988/index.html?deck=math-02-advanced-multiplication&index=1"
    ], timeout=15)
    print("Captured", out3)

    # 4. Advanced back: 6 x 889 = 5334
    out4 = artifact_dir / "preview_math_04_advanced_back.png"
    subprocess.run([
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--window-size=390,844",
        f"--screenshot={out4}",
        "http://localhost:9988/index.html?deck=math-02-advanced-multiplication&index=1&flip=1"
    ], timeout=15)
    print("Captured", out4)

    # 5. Bottom sheet picker scrolled to bottom to show Matematika
    out5 = artifact_dir / "preview_math_05_picker_sheet.png"
    subprocess.run([
        edge_path,
        "--headless=new",
        "--disable-gpu",
        "--window-size=390,844",
        f"--screenshot={out5}",
        "http://localhost:9988/index.html?picker=1&search=matematika"
    ], timeout=15)
    print("Captured", out5)

finally:
    server.terminate()
print("All screenshots successfully captured!")
