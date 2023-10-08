# import required libraries
from vidgear.gears.stabilizer import Stabilizer
from vidgear.gears import CamGear
from vidgear.gears import WriteGear
# import cv2

# Open suitable video stream
stream = CamGear(source=r"F:\影视\2022下\20220819\C0133.MP4").start()

# initiate stabilizer object with default parameters
# stab = Stabilizer()

# border_type: 'black', 'reflect', 'reflect_101', 'replicate' and 'wrap'

# initiate stabilizer object with defined parameters
stab = Stabilizer(smoothing_radius=35, crop_n_zoom=True, border_size=0, border_type="wrap", logging=True)

output_params = {
    "-input_framerate": 60,
    # 加这一行会出现莫名其妙的错误
    # "-output_dimensions": (640, 360),
    "-r": 60,
    "-crf": 16,
    "-preset": "medium",
    "-clones": [
        "-pix_fmt", "yuv422p10le",

        # "-c", "copy",
        # "-color_primaries", "bt2020",

        # color-primaries 输入内容的色彩格式：bt709, unspecified, bt601, bt470m, bt470bg, smpte240, film, bt2020, xyz, smpte431, smpte432, ebu3213
        # transfer-characteristics 输入内容的传输特性（CICP）:unspecified, bt709, bt470m, bt470bg, bt601, smpte240, lin, log100, log100sq10, iec61966, bt1361, srgb, bt2020-10bit, bt2020-12bit, smpte2084, hlg, smpte428
        # matrix-coefficients 输入内容的矩阵系数:identity, bt709, unspecified, fcc73, bt470bg, bt601, smpte240, ycgco, bt2020ncl, bt2020cl, smpte2085, chromncl, chromcl, ictcp
        # "-bsf:v", "h264_metadata=colour_primaries=9:transfer_characteristics=18:matrix_coefficients=9",
    ],
}

# Define writer with default parameters and suitable output filename for e.g. `reflect.mp4`
writer = WriteGear(output_filename="temp_output/wrap6.mp4", logging=True, **output_params)

# loop over
while True:

    # read frames from stream
    frame = stream.read()

    # check for frame if not None-type
    if frame is None:
        break

    # send current frame to stabilizer for processing
    stabilized_frame = stab.stabilize(frame)

    # wait for stabilizer which still be initializing
    if stabilized_frame is None:
        continue

    # {do something with the stabilized frame here}

    # write stabilized frame to writer
    writer.write(stabilized_frame)

    # Show output window
    # cv2.imshow("Stabilized Frame", stabilized_frame)

    # check for 'q' key if pressed
    # key = cv2.waitKey(1) & 0xFF
    # if key == ord("q"):
    #     break

# close output window
# cv2.destroyAllWindows()

# clear stabilizer resources
stab.clean()

# safely close video stream
stream.stop()

# safely close writer
writer.close()
