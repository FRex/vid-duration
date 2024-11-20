#!/usr/bin/env python3
"""Script to run ffprobe from ffmpeg on each given file and print their durations."""
from subprocess import Popen, PIPE
import json
import sys
import os


FFMPEG_ARGS = ("ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-i")


def format_duration(duration: int) -> str:
    """Format duration into HH:MM:SS, MM:SS if under 1 hour, or ??? on negative."""
    h, m, s = duration // 3600, (duration % 3600) // 60, duration % 60
    ret = "???" if duration < 0 else f"{h:02d}:{m:02d}:{s:02d}"

    # NOTE: if hours is 00 then cut it off, so it's either hh:mm:ss with non-zero
    # hh or it's mm:ss with any mm, including just 00, like VLC and many other
    # tools display, so it's not just a single number of seconds for sub 1 min
    if ret.startswith("00:"):
        ret = ret[3:]
    return ret


def format_pretty_table(origdata, rjust=()) -> str:
    """Format data as a nice table, using pipe and dash ASCII characters as separators."""
    data = [None if row is None else tuple(map(str, row)) for row in origdata]
    colcount = max(map(len, (row for row in data if row is not None)))
    maxlens = colcount * [0]
    for row in data:
        if row is None:
            continue
        for i, l1 in enumerate(map(len, row)):
            if l1 > maxlens[i]:
                maxlens[i] = l1
    ret = []
    for row in data:
        if row is None:
            ret.append("|".join("-" * width for width in maxlens))
        else:
            parts = []
            for i, (data, width) in enumerate(zip(row, maxlens)):
                if i in rjust:
                    parts.append(data.rjust(width))
                else:
                    parts.append(data.ljust(width))
            ret.append("|".join(parts))
    return "\n".join(ret)


def prettysize(fsize: int) -> str:
    """Pretty print a filesize like X Bytes, X KiB, X MiB, etc."""
    if fsize < 1024:
        return f"{fsize} Bytes"
    if fsize < 1024 * 1024:
        return f"{fsize / 1024:.1f} KiB"
    if fsize < 1024 * 1024 * 1024:
        return f"{fsize / (1024 * 1024):.1f} MiB"
    return f"{fsize / (1024 * 1024 * 1024):.1f} GiB"


def main():
    """Main function to not do anything when this py file is imported instead of ran."""

    # run all processes in parallel since they access very little data from disk each
    jobs = []
    for fname in sys.argv[1:]:
        args = list(FFMPEG_ARGS) + [fname]
        p = Popen(args, stdout=PIPE, stderr=PIPE, bufsize=64 * 1024, encoding="UTF-8")
        jobs.append((p, fname))

    # join the started processes and collect the durations
    total_duration = 0
    total_fsize = 0
    rows = []
    rows.append(("File ", " Duration", " Size"))
    rows.append(None)
    for p, fname in jobs:
        #  NOTE: communicate to avoid deadlock if ffprobe has a lot of output
        stdout, stderr = p.communicate()
        del stderr  # TODO: handle or show these errors?
        duration = int(float(json.loads(stdout).get("format", {}).get("duration", -1)))
        total_duration += duration if duration > 0 else 0
        fsize = os.path.getsize(fname)
        total_fsize += fsize
        rows.append(
            (fname + " ", " " + format_duration(duration), " " + prettysize(fsize))
        )

    rows.append(None)
    rows.append(
        (
            "TOTAL ",
            " " + format_duration(total_duration),
            " " + prettysize(total_fsize),
        )
    )
    t = format_pretty_table(rows, rjust=(1, 2))
    print(t)


if __name__ == "__main__":
    main()
