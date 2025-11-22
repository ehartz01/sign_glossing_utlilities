import os
from moviepy.editor import VideoFileClip

# === CONFIGURATION ===
input_folder = "toponyms_clipped"     # folder containing the .mp4 files
output_folder = "cropped_videos"  # folder to save the processed videos

# Define cropping box (x1, y1, x2, y2)
# You may need to adjust these after checking one sample video
# Example: crop left half and remove bottom label area
CROP_BOX = (0, 0, 960, 1000)  # adjust based on your resolution (x1, y1, x2, y2)

os.makedirs(output_folder, exist_ok=True)
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".mp4"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        print(f"Processing {filename}...")

        # Load video
        clip = VideoFileClip(input_path)

        # Get dimensions
        w, h = clip.size

        # Define crop area:
        # - Keep left half (0 to w/2)
        # - Crop out top 1/4 and bottom 7/24 of height
        x1, x2 = 0, w / 2
        y1 = h / 4
        y2 = h - (7 * h / 24)

        cropped = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)

        # Remove audio
        cropped_no_audio = cropped.without_audio()

        # Export
        cropped_no_audio.write_videofile(
            output_path,
            codec="libx264",
            audio=False,
            threads=4,
            preset="medium"
        )

        clip.close()
        cropped.close()
        cropped_no_audio.close()

print("✅ Done! All videos cropped (top 1/4, bottom 7/24, right half removed) and audio stripped.")
