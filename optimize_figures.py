import os
import shutil
from PIL import Image

TARGET_DIRS = [
    r"c:\Users\ASUS\Desktop\Kali-Nova\docs",
    r"c:\Users\ASUS\Desktop\Kali-Nova\docs\figures",
    r"c:\Users\ASUS\Desktop\Kali-Nova\report_images"
]

MAX_WIDTH = 1600

def optimize_pngs():
    total_orig = 0
    total_opt = 0
    count = 0

    for d in TARGET_DIRS:
        if not os.path.exists(d):
            continue
        print(f"\n--- Optimizing images in {d} ---")
        for fname in sorted(os.listdir(d)):
            if not fname.lower().endswith(".png"):
                continue
            
            fpath = os.path.join(d, fname)
            orig_size = os.path.getsize(fpath)
            total_orig += orig_size

            with Image.open(fpath) as img:
                w, h = img.size
                if w > MAX_WIDTH:
                    new_w = MAX_WIDTH
                    new_h = int(h * (MAX_WIDTH / w))
                    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                else:
                    img_resized = img.copy()

                # Save optimized
                img_resized.save(fpath, format="PNG", optimize=True)

            opt_size = os.path.getsize(fpath)
            total_opt += opt_size
            count += 1
            print(f"  {fname:32} {w}x{h} -> {img_resized.size[0]}x{img_resized.size[1]} | {orig_size/1024:.1f}KB -> {opt_size/1024:.1f}KB (saved {(orig_size-opt_size)/orig_size*100:.1f}%)")

        # Create paper aliases in docs if they don't exist or to ensure match
        if d.endswith("docs") or d.endswith("docs\\figures"):
            arch_src = os.path.join(d, "system_architecture.png")
            arch_dst = os.path.join(d, "architecture_diagram.png")
            if os.path.exists(arch_src):
                shutil.copy2(arch_src, arch_dst)
                print(f"  Created alias: architecture_diagram.png -> system_architecture.png")

            st_src = os.path.join(d, "tool_execution_workflow.png")
            st_dst = os.path.join(d, "state_transition_diagram.png")
            if os.path.exists(st_src):
                shutil.copy2(st_src, st_dst)
                print(f"  Created alias: state_transition_diagram.png -> tool_execution_workflow.png")

    print("\n" + "="*50)
    print(f"Processed {count} images.")
    print(f"Total size before: {total_orig / (1024*1024):.2f} MB")
    print(f"Total size after:  {total_opt / (1024*1024):.2f} MB")
    print(f"Total bandwidth/compile memory saved: {(total_orig - total_opt) / (1024*1024):.2f} MB")
    print("="*50)

if __name__ == "__main__":
    optimize_pngs()
