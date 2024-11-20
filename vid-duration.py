#!/usr/bin/env python3
"""Script to run ffprobe from ffmpeg on each given file and print their durations."""
from subprocess import Popen, PIPE
import json
import sys


FFMPEG_ARGS = ("ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-i")


def format_duration(duration: int) -> str:
    """Format duration into HH:MM:SS, or ??? on negative."""
    h, m, s = duration // 3600, (duration % 3600) // 60, duration % 60
    return "???" if duration < 0 else f"{h:02d}:{m:02d}:{s:02d}"


def main():
    """Main function to not do anything when this py file is imported instead of ran."""
    jobs = []

    # run all processes in parallel since they access very little data from disk each
    for fname in sys.argv[1:]:
        args = list(FFMPEG_ARGS) + [fname]
        p = Popen(args, stdout=PIPE, stderr=PIPE, bufsize=64 * 1024, encoding="UTF-8")
        jobs.append((p, fname))

    # join them and print and sum up durations
    total_duration = 0
    for p, fname in jobs:
        #  NOTE: communicate to avoid deadlock if ffprobe has a lot of output
        stdout, stderr = p.communicate()
        del stderr  # TODO: handle this
        duration = int(float(json.loads(stdout).get("format", {}).get("duration", -1)))
        total_duration += duration if duration > 0 else 0
        print(f"{format_duration(duration)} - {fname}")

    print(f"{format_duration(total_duration)}")


if __name__ == "__main__":
    main()
