import cv2, os
from PIL import Image
import numpy as np
from scipy import signal

###############################################################################
# Utility Functions
###############################################################################

def hist(img):
    """Return grayscale histogram of an image."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.calcHist([gray], [0], None, [256], [0, 256])


def read_frames(video):
    """
    Load all frames from a video file and return them as a list of BGR numpy arrays.
    Frame indices correspond exactly to indexes in this list.
    """
    cap = cv2.VideoCapture(video)
    frames = []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frames.append(frame)
    cap.release()
    return frames


def get_frame_difference(video):
    """
    Compute histogram correlations between consecutive frames.
    Returns:
        x = frame indices
        y = 1 - correlation score (difference)
    """
    frames = read_frames(video)
    x, y = [], []

    for n in range(len(frames) - 1):
        h1 = hist(frames[n])
        h2 = hist(frames[n + 1])
        diff = 1 - cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)

        x.append(n)
        y.append(diff)

    return x, y


def get_keyframes(video, smooth_window=9, peak_prominence=0.08):
    """
    Select keyframes based on histogram difference peaks.
    Fallback: evenly spaced if too few peaks found.
    """
    x, y = get_frame_difference(video)

    if len(y) < smooth_window:
        # Video too short → fallback to three evenly spaced frames
        total = len(x)
        return [total // 4, total // 2, 3 * total // 4]

    # Smooth the histogram difference curve
    y_smooth = signal.savgol_filter(y, smooth_window, 3)

    # Detect peaks = real visual changes
    peaks, _ = signal.find_peaks(y_smooth, prominence=peak_prominence)

    # Ensure at least 3 keyframes
    if len(peaks) < 3:
        total = len(x)
        return [total // 4, total // 2, 3 * total // 4]

    return peaks.tolist()


###############################################################################
# Image generation
###############################################################################

def make_side_by_side(images, outname):
    """
    Create a transparent PNG with images placed side-by-side with NO spacing.
    """
    widths = [img.width for img in images]
    heights = [img.height for img in images]

    total_w = sum(widths)
    max_h = max(heights)

    # Transparent background
    final = Image.new("RGBA", (total_w, max_h), (0, 0, 0, 0))

    x_offset = 0
    for img in images:
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        final.paste(img, (x_offset, 0), img)
        x_offset += img.width

    final.save(outname, "PNG")
    print("Saved:", outname)


def make_images(video):
    """
    Main function: extract keyframes and generate composite PNG.
    """
    print("Processing:", video)

    frames = read_frames(video)

    if len(frames) == 0:
        print("ERROR: No frames found in", video)
        return

    key_indices = get_keyframes(video)
    print("Keyframes:", key_indices)

    selected = []
    for idx in key_indices:
        if idx >= len(frames):
            continue
        frame = frames[idx]
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        selected.append(pil_img)
    base, _ = os.path.splitext(video)
    outname = f"{base}_stills.png"
    # outname = video.split(".")[0] + "_stills.png"
    make_side_by_side(selected, outname)


###############################################################################
# Main
###############################################################################

def main():
    for f in os.listdir():
        if f.lower().endswith(".mp4"):
            make_images(f)


if __name__ == "__main__":
    main()
