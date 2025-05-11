# About

This is an eye controlled photo gallery! Close your eyes for a litle bit longer than a blink to advance to the next image.

### Features

- **Eye Gesture Control**: Advance to the next image by closing your eyes for a bit longer than a blink.
- **Facial Landmark Detection**: Uses facial landmarks and eye aspect ratio (EAR) to detect user input.
- **Accessible Navigation**: Designed to provide an alternative method of navigation and offer more accessibility to users.

### Video Demo
  See the [video demo](demo/eye-control-demo.mp4) under the demo folder of this repo. 

  This video shows the application running in verbose mode, with 3 examples of long blinks that advance to the next image. The image advances when 'blink open' occurs at the end of a long blink. The end of the video also shows two examples of short blinks that do not count as a long blink, and will neither result in a 'blink open' nor an image advancement. However, the short blinks are still detected and indicated with 'eyes closed' on the screen. The average displayed in the terminal is the average of both eyes eye aspect ratios (EARs).
  

# Usage

Run the following command: `python main.py [--verbose|-v]`

Verbose mode can be set by the '--verbose' or '-v' flag. This will display the camera feed and all of the facial landmarks, as well as numerical data.

To advance to the next image, close your eyes for a bit longer than a blink. The image will advance when you open your eyes from the long blink. Any short blinks will not count as an advance signal.

To exit, press 'q' on the keyboard.

# Libraries Used

OpenCV, NumpPy, dlib

# Motivation and Next Steps

This project was a great exploration into facial landmark detection and gesture recognition. In the future, I'd love to support a variety of different gestures to continue to create accesible user experiences in a diverse array of applications and contexts.

# Photo Credit

All photos were taken by me on my recent trip to Norway and the United Kingdom :)
