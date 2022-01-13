# import required libraries
from vidgear.gears.stabilizer import Stabilizer
from vidgear.gears import CamGear
from vidgear.gears import WriteGear
import cv2

# Open suitable video stream
stream = CamGear(source="../auto_split_clip_by_scene/input/463397827651706880_max.mp4").start()

# initiate stabilizer object with default parameters
# stab = Stabilizer()

# border_type: 'black', 'reflect', 'reflect_101', 'replicate' and 'wrap'

# initiate stabilizer object with defined parameters
stab = Stabilizer(smoothing_radius=35, crop_n_zoom=False, border_size=0, border_type="wrap", logging=True)

output_params = {
    "-input_framerate": 60,
    # 加这一行会出现莫名其妙的错误
    # "-output_dimensions": (640, 360),
    "-r": 60,
    "-crf": 20,
    "-clones": ["-pix_fmt", "yuv422p10le"],
}

# Define writer with default parameters and suitable output filename for e.g. `reflect.mp4`
writer = WriteGear(output_filename="../auto_split_clip_by_scene/output/wrap.mp4", logging=True, **output_params)

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
    cv2.imshow("Stabilized Frame", stabilized_frame)

    # check for 'q' key if pressed
    # key = cv2.waitKey(1) & 0xFF
    # if key == ord("q"):
    #     break

# close output window
cv2.destroyAllWindows()

# clear stabilizer resources
stab.clean()

# safely close video stream
stream.stop()

# safely close writer
writer.close()
