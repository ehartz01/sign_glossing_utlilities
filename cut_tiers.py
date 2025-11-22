import pympi
import moviepy.editor as mp

def make_clips_from_elan(eaf_path, video_path, output_dir):
    """
    Creates video clips from ELAN annotations.

    Args:
        eaf_path (str): Path to the ELAN (.eaf) file.
        video_path (str): Path to the video file.
        output_dir (str): Directory to save the output clips.
    """

    eaf = pympi.Elan.Eaf(eaf_path)
    video = mp.VideoFileClip(video_path)

    for tier_name in ["Gloss (Ibrahim)"]:

        for ann in eaf.get_annotation_data_for_tier(tier_name):
            start = ann[0] / 1000  # Convert milliseconds to seconds
            end = ann[1] / 1000
            label = ann[2]
            if "/" in label:
                continue
            clip = video.subclip(start, end)

            # Create output file name based on tier name, start time, and label
            output_file = f"{output_dir}/{tier_name}_{start}_{label}.mp4"
            clip.write_videofile(output_file)

if __name__ == "__main__":
    # for i in range(1,40):
        # if i == 3:
        #     break
    # i = 13
    eaf_path = f"toponyms_p1_ibrahim.eaf"
    video_path = f"toponyms_p1_ibrahim.mp4"
    output_dir = f"toponyms_clipped"

    make_clips_from_elan(eaf_path, video_path, output_dir)


# import os
# from moviepy.editor import VideoFileClip

def crop_bottom_third(input_dir, output_dir):
    """
    Crop the bottom third of all videos in the input directory and save them to the output directory.

    Args:
        input_dir (str): Path to the directory containing input videos.
        output_dir (str): Path to the directory where cropped videos will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        if not os.path.isfile(input_path):
            continue

        try:
            clip = VideoFileClip(input_path)

            # Calculate the height of the lower third
            lower_third_height = clip.h // 3

            # Crop the video to remove the lower third
            cropped_clip = clip.crop(y1=0, y2=clip.h - lower_third_height)

            # Write the cropped video to the output directory
            cropped_clip.write_videofile(output_dir+f"/{file_name}", codec="libx264")
            print(f"Processed: {file_name}")
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")

# # Example usage
# input_directory = "swadesh_heavy"  # Replace with your input directory
# output_directory = "swadesh_clipped_cropped"  # Replace with your output directory
# crop_bottom_third(input_directory, output_directory)
