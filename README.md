# USB Camera Latency Testing Utility
## Description:

This utility is designed for testing USB camera latency. It measures the latency in switching between black and white frames and provides information about the time elapsed and frames processed.

## Notes:
- Ensure that the testing is performed on monitors with high refresh rates.
- The recommended testing refresh rate is set between 120Hz and 165Hz.
- Lower refresh rates may result in capped measured latency, typically capping out around 100ms.
- The utility tests using MJPEG mode.

## Requirements:
```
Python 3.x
OpenCV (cv2) library
```


## Run the script:

```
python main.py
```

## Instructions:

- After running the command, point your camera at the screen for the window to show.
- The utility will display a window titled 'Black/White Latency Testing Window.'
- Latency information, including time elapsed and frames processed, will be printed to the terminal.
- Press 'q' to quit the utility.

## Measurement
The utility continuously captures frames from the camera, converts them to grayscale, and measures the average intensity.

It detects transitions between black and white frames, measuring the time elapsed and frames processed during each transition.

## Troubleshooting

- If the window is not switching colors, adjust the `BW_THRESHOLD` variable in increments of 10
- If your camera is not being recognized, check the `CAM_IDX` variable
- If your camera is not being recognized, double check your camera supports `MJPEG`. If not, set the pixel format to something else.