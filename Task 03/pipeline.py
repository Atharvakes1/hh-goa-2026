import time
import pygame
import warnings
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

# Import our custom modules
import face_module
import search_module
import blockchain_module

warnings.filterwarnings("ignore")
console = Console()

# --- CONFIGURATION ---
IMAGE_PATH = "test.jpg"
SERPAPI_KEY = "a7a8fc60d40ba99808892699b523d706c64b961b414475164c249ef474e17c53"  # <-- PASTE YOUR KEY HERE
MUSIC_FILE = "track.mp3"
# ---------------------

def play_music():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(-1) # Loops infinitely
    except Exception:
        console.print("[dim]Audio track not found, proceeding silently...[/dim]")

def print_hype_stats():
    """Simulates the 'Check Hype' popping letters from the HH Goa website"""
    console.clear()
    title = Text("\nHACKER HOUSE GOA 2026 // TASK #3", style="bold #FF1E75 justify-center")
    console.print(Align.center(title))
    time.sleep(1)
    
    stats = [
        "[bold #FFD12E]6800+ REGISTRATIONS[/bold #FFD12E]",
        "[bold #FF1E75]390+ HACKERS[/bold #FF1E75]",
        "[bold #08281A on #FFD12E] $50K+ BOUNTIES [/bold #08281A on #FFD12E]"
    ]
    
    for stat in stats:
        console.print(Align.center(Panel(stat, expand=False, border_style="#FF1E75")))
        time.sleep(0.8) # 3D Popping effect

def run_master_pipeline():
    play_music()
    print_hype_stats()
    
    console.print("\n[bold white on #FF1E75] INITIATING SOVIET UNION PIPELINE... [/bold white on #FF1E75]\n")
    time.sleep(1)

    # --- PHASE 1 ---
    console.print(Panel("[bold #FF1E75]PHASE 1: FACE IDENTIFICATION[/bold #FF1E75]", expand=False))
    encoding = face_module.encode_face(IMAGE_PATH)
    time.sleep(1)

    # --- PHASE 2 ---
    console.print("\n")
    console.print(Panel("[bold #FFD12E]PHASE 2: GENUINE REVERSE SEARCH[/bold #FFD12E]", expand=False))
    if not encoding:
        console.print("[bold red]Pipeline halted: No face detected.[/bold red]")
        return
        
    social_url = search_module.find_social_match(IMAGE_PATH, SERPAPI_KEY)
    time.sleep(1)

    # --- PHASE 3 ---
    console.print("\n")
    console.print(Panel("[bold #08281A on #FFD12E]PHASE 3: BLOCKCHAIN VERIFICATION[/bold #08281A on #FFD12E]", expand=False))
    if not social_url:
        console.print("[bold red]Pipeline halted: No social match found.[/bold red]")
        return
        
    tx_hash = blockchain_module.verify_on_chain(IMAGE_PATH, social_url)
    time.sleep(1.5)

    # --- THE FINALE ---
    if tx_hash:
        verified_panel = Panel(
            Text(f"✓ VERIFIED ON-CHAIN\n\nTeam: Soviet Union (Atharva, Arpit, Sundaram)\nTx Hash: {tx_hash}", justify="center", style="bold #08281A"),
            title="[bold #FF1E75] TASK #3 COMPLETE ",
            border_style="#FF1E75",
            style="on #FFD12E"
        )
        console.print("\n")
        console.print(Align.center(verified_panel))
        
        # Let the music play out for 5 seconds for the video outro
        time.sleep(5)

if __name__ == "__main__":
    run_master_pipeline()