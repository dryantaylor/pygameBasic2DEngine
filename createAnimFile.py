import pygame
from zipfile import ZipFile


def create_file(anim_file_loc: str, timings: tuple[int, ...], image_locs: tuple[str, ...], does_loop: bool = False):
    frames = len(timings)
    non_zipped_image_locs = image_locs
    width, height = pygame.image.load(image_locs[0]).get_size()
    arclocs = ""
    with ZipFile(anim_file_loc, "w") as zip:
        n = 00
        for file in non_zipped_image_locs:
            arcname = f"{str(n).zfill(3)}.{file.split('.')[-1]}"
            zip.write(file, arcname)
            arclocs += f"{arcname},\r\n"
            n+=1
        arclocs = arclocs[:-3]

        timings_sting = ""
        for timing in timings:
            timings_sting += f"{timing},\r\n"
        timings_sting = timings_sting[:-3]
        zip.writestr("info.cfg",
        f"resolution={width},{height};\r\ndoes_loop={str(does_loop)};\r\ntimings={timings_sting};\r\nimage_locs={arclocs}")


