import os
import shutil
import argparse
import logging
from datetime import datetime

import yt_dlp
from pydub import AudioSegment


class MashupGenerator:
    def __init__(self, singer, num_videos, duration, output):
        self.singer = singer
        self.num_videos = num_videos
        self.duration = duration * 1000  # convert to milliseconds
        self.output = output

        self.audio_dir = "temp_audio"
        self.cut_dir = "temp_clips"

        self._setup_directories()
        self._configure_logging()

    # ----------------------------------------
    # Setup
    # ----------------------------------------

    def _configure_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s"
        )

    def _setup_directories(self):
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.cut_dir, exist_ok=True)

    def _cleanup(self):
        shutil.rmtree(self.audio_dir, ignore_errors=True)
        shutil.rmtree(self.cut_dir, ignore_errors=True)

    # ----------------------------------------
    # Download Section
    # ----------------------------------------

    def download_tracks(self):
        logging.info("Searching YouTube and downloading tracks...")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{self.audio_dir}/%(id)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]
        }

        search_query = f"ytsearch{self.num_videos}:{self.singer}"
        downloaded_files = []

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(search_query, download=True)

            if "entries" not in result:
                raise Exception("No tracks found.")

            for entry in result["entries"]:
                file_path = os.path.join(self.audio_dir, f"{entry['id']}.mp3")
                if os.path.exists(file_path):
                    downloaded_files.append(file_path)

        logging.info(f"Downloaded {len(downloaded_files)} tracks.")
        return downloaded_files

    # ----------------------------------------
    # Trim Section
    # ----------------------------------------

    def trim_tracks(self, tracks):
        logging.info("Trimming audio clips...")

        trimmed_files = []

        for index, file in enumerate(tracks):
            audio = AudioSegment.from_file(file)

            clip = audio[:self.duration] if len(audio) > self.duration else audio

            output_path = os.path.join(self.cut_dir, f"clip_{index}.mp3")
            clip.export(output_path, format="mp3")

            trimmed_files.append(output_path)

        return trimmed_files

    # ----------------------------------------
    # Merge Section
    # ----------------------------------------

    def merge_tracks(self, clips):
        logging.info("Merging clips into final mashup...")

        final_mix = AudioSegment.empty()

        for clip in clips:
            final_mix += AudioSegment.from_file(clip)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_output = self.output if self.output.endswith(".mp3") else f"{self.output}.mp3"

        final_mix.export(final_output, format="mp3")

        logging.info("Mashup successfully created.")
        return final_output

    # ----------------------------------------
    # Execute Workflow
    # ----------------------------------------

    def generate(self):
        try:
            tracks = self.download_tracks()
            clips = self.trim_tracks(tracks)
            final_file = self.merge_tracks(clips)

            logging.info(f"Final Output: {final_file}")

        except Exception as e:
            logging.error(f"Error occurred: {e}")

        finally:
            self._cleanup()


# ----------------------------------------
# CLI Interface
# ----------------------------------------

def parse_arguments():
    parser = argparse.ArgumentParser(description="YouTube Mashup Generator")
    parser.add_argument("singer", type=str, help="Singer name to search on YouTube")
    parser.add_argument("num_videos", type=int, help="Number of videos to download")
    parser.add_argument("duration", type=int, help="Duration (seconds) to trim from each video")
    parser.add_argument("output", type=str, help="Output MP3 file name")

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.num_videos <= 0 or args.duration <= 0:
        print("Number of videos and duration must be positive values.")
        return

    mashup = MashupGenerator(
        singer=args.singer,
        num_videos=args.num_videos,
        duration=args.duration,
        output=args.output
    )

    mashup.generate()


if __name__ == "__main__":
    main()
