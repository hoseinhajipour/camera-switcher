# Camera Switcher Addon for Blender

This Blender addon allows you to efficiently manage multiple cameras and create smooth camera switch animations with customizable transitions. It features a user-friendly UI panel for adding, removing, and setting active cameras, as well as generating camera animations with smooth transitions.

## Features

- **Camera Switch List**: Add and manage multiple cameras in a list.
- **Create Camera from View**: Create a new camera based on the current 3D view.
- **Set Active Camera**: Easily set any camera as the active one.
- **Generate Camera Animation**: Automatically create keyframe-based camera switch animations with transition frames.
- **Transition Frames**: Control the number of frames used for smooth transitions between cameras.
- **Collapsible UI**: Each camera in the list has a collapsible section for easy management.

## Installation

1. Download the addon `.py` file.
2. In Blender, go to `Edit` -> `Preferences` -> `Add-ons` tab.
3. Click the `Install...` button and select the downloaded `.py` file.
4. Enable the addon by checking the box next to "Camera Switcher" in the Add-ons list.

## Usage

1. Open the "Camera Tools" tab in the 3D View Sidebar.
2. Use the "Append Camera" button to add selected cameras to the list.
3. Use "Create Camera from View" to create a new camera based on the current 3D view.
4. Set start frames for each camera and adjust transition frames.
5. Click "Generate" to create the camera switch animation with smooth transitions.

## Operators

- **Append Selected Camera**: Adds selected cameras from the scene to the camera list.
- **Create Camera from View**: Creates a new camera from the current 3D view and adds it to the list.
- **Set Active Camera**: Sets the selected camera as the active camera.
- **Generate Camera Animation**: Generates keyframe-based animations with smooth transitions between cameras.

## Customization

- **Transition Frames**: The number of frames for smooth camera transitions can be adjusted in the UI.
- **Camera List**: You can modify the start frame for each camera and remove any camera from the list.

## Requirements

- Blender 2.8+ (tested with newer versions)
  
## License

This addon is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

Feel free to fork or contribute to this project!
