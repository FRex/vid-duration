# Vid Duration

A simple Python 3 script to run `ffprobe` and print durations and sizes of media files.

Requires (and works on any) Python 3.6 or above, as tested using
[https://github.com/FRex/anypython](https://github.com/FRex/anypython),
due to usage of [f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings).

If you require support for older Python 3.x or 2.7, or find a mistake - let me know.


```
$ python3 vidduration.py /e/*.*
File         | Duration|      Size
-------------|---------|----------
E:/test1.mp3 |    48:53|  89.5 MiB
E:/test2.mp3 |    50:29|  69.3 MiB
E:/test3.mp3 | 01:07:06| 122.9 MiB
E:/test4.mp3 |    46:16|  84.7 MiB
E:/test5.mp4 |    00:29|  11.3 MiB
-------------|---------|----------
TOTAL        | 03:33:13| 377.8 MiB
```
