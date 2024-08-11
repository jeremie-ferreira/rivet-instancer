# Rivet Instancer

**Rivet Instancer** is a Blender addon designed to streamline the process of adding rivets along the selected edges of a mesh object. This tool offers an easy-to-use interface for customizing rivet placement and spacing, making it an invaluable asset for modeling tasks involving repeated hardware features.

## Features

- **Effortless Rivet Placement**: Automatically generate rivets along selected edges of a mesh object.
- **Adjustable Spacing**: Control the distance between rivets to match your design requirements.
- **Custom Rivet Object**: Specify any existing object in your scene to use as the rivet.

## Installation

1. **Download the Add-on**: 
    - Download the latest version of the add-on from the [releases page](https://github.com/jeremie-ferreira/rivet-instancer/releases).

2. **Install in Blender**:
    - Open Blender.
    - Go to `Edit > Preferences > Add-ons`.
    - Click on the `Install...` button.
    - Navigate to the downloaded `viewport_preset_switcher.zip` file and select it.
    - Enable the add-on by checking the box next to "Camera Preset Switcher".

![installation](https://github.com/user-attachments/assets/65074eb4-0bef-4601-85fe-3fb65b279a70)

3. **Save Preferences** (optional):
    - Click on the `Save Preferences` button at the bottom left to ensure the add-on is enabled every time you start Blender.

## Usage

1. **Prepare Your Scene**:
   - Ensure that you have an object in your scene that you want to use as the rivet. By default, it looks for an object named "RivetMaster".
   - Select the mesh object where you want to add rivets.
   - Enter Edit Mode and select the edges along which you want to place the rivets.

2. **Add Rivets**:
   - Switch back to Object Mode.
   - Open the 3D Viewport and find the "Generate Rivets" panel under the `Tool` tab.
   ![panel](https://github.com/user-attachments/assets/a0c4274b-40c5-44da-bbb4-490b49be36fd)
   - Click the "Generate Rivets" button to place the rivets along the selected edges.
   - Configure the `Rivet Object Name` (the name of the object to be used as the rivet) and `Spacing` (distance between rivets).
   ![parameters](https://github.com/user-attachments/assets/210bcd4f-2518-4246-b4a0-e7ce8f105f2f)


## Example

![usage](https://github.com/user-attachments/assets/2a18336d-5085-4fc1-a155-a9d8b1bfaa8e)

## Changelog

- **v1.0.0** (2024-08-11)
  - Initial release with functionality for placing rivets along selected edges.
  - Added options for spacing and customizable rivet objects.

## License

This addon is licensed under the Apache License. See the [LICENSE](./LICENSE) file for more details.

## Contact

For support or to report issues, please visit the [GitHub Issues page](https://github.com/jeremie-ferreira/rivet-instancer) or contact the author directly.

---

**Author**: Jeremie Ferreira
**Blender Compatibility**: 2.80 and above