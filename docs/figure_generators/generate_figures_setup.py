import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIRS = [
    r"c:\Users\ASUS\Desktop\Kali-Nova\Kali-Nova-Figures-Folder",
    r"c:\Users\ASUS\Desktop\Kali-Nova\docs\figures"
]

for d in OUTPUT_DIRS:
    os.makedirs(d, exist_ok=True)

def save_fig(fig, filename):
    for d in OUTPUT_DIRS:
        target = os.path.join(d, filename)
        fig.savefig(target, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), edgecolor='none')
    print(f"Saved {filename}")
    plt.close(fig)

print("Setup completed successfully.")
