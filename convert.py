import os
from pathlib import Path
import subprocess
from pprint import pprint

import ffmpeg

def convert_webp_to_apng(filepath: str, apng_delay: str):
    print("Converting WebP to APNG...")

    p = Path(filepath)
    output_path = p.with_suffix(".png")
    subprocess.run(["magick",
                    *([] if apng_delay == "-1" else ["-delay",  apng_delay]),
                    filepath,
                    "apng:" + str(output_path)
                   ])
    return str(output_path.absolute())

def process_file(filepath, fps_amount: str, resize_mode: str, smart_limit_duration: str, fallback_pts: str, crf: int, *args):
    if filepath.lower().endswith(".webp"):
        filepath = convert_webp_to_apng(filepath, args[0])

    p = Path(filepath)

    job = ffmpeg.input(filepath)

    # 30FPS
    job = job.filter('fps', fps=fps_amount)

    info = ffmpeg.probe(filepath)

    pprint(info)

    stream = info['streams'][0]
    fmt = info['format']

    if resize_mode == 'scale':
        # Try to scale to 512px
        if stream['width'] >= stream['height']:
            job = job.filter('scale', 512, -1)
        else:
            job = job.filter('scale', -1, 512)

    elif resize_mode == 'pad':
        if stream['width'] >= stream['height']:
            job = job.filter('pad', width=512, height='min(ih,512)', x='(ow-iw)/2', y='(oh-ih)/2', color="white@0")
        else:
            job = job.filter('pad', width='min(iw,512)', height=512, x='(ow-iw)/2', y='(oh-ih)/2', color="white@0")


    if 'duration' in fmt:
        print("Duration detected: %s" % fmt['duration'])
        duration = float(fmt['duration'])

        # Try speed up video if it's over 3 seconds
        if duration > 3.0:
            job = job.filter('setpts', f"({smart_limit_duration}/{duration})*PTS")
    else:
        print("Unable to determine duration")
        job = job.filter('setpts', f"{fallback_pts}*PTS")


    out_path = str(p.with_suffix('.webm'))

    if os.path.exists(out_path):
        out_path = str(p.with_suffix('.telegram.webm'))

    extra_args = {}

    if crf != -1:
      extra_args['crf'] = crf

    job = (
        job
        .output(
            out_path,
            pix_fmt='yuva420p',
            vcodec='libvpx-vp9',
            an=None,  # Remove Audio
            **extra_args,
        )
        .overwrite_output()
    )

    job.run_async()

    return out_path