# RP2040 Macro Pad

**Project Status:** This project is currently suspended, but I plan to return to it and continue development in my free time.

## Available Methods

* `key<>` - Presses a key for a short moment. If preceded by Ctrl, Alt, or Shift, they will remain pressed until the next key. A standalone `key<ctrl>` will be ignored.
* `press<>` - Presses and holds the selected key until it is released.
* `realese<>` - Releases the currently held key. This is highly recommended for every key that was pressed using the `press<>` method.
* `text<>` - Automatically types text based on the `key<>` method. It features automatic Shift usage for uppercase letters and recognition of Polish diacritics.
* `media<>` - Allows control over media playback, system volume, screen brightness, and more.

*Note: If Ctrl, Shift, or Alt is not explicitly specified, the left one is used by default.*

## Usage Examples

To chain multiple methods in a single bind, use the `+` connector without any additional spaces.

* `key<ctrl>+key<a>+key<ctrl>+key<c>+key<DOWN_ARROW>` - Ctrl+A, Ctrl+C, (Down Arrow)
* `key<ctrl>+key<v>` - Ctrl+V
* `media<volup>` - Increases system volume
* `media<volup:10>` - Increases system volume (by 10 steps)
* `media<play>` - Resumes paused music or video
* `press<right_ctrl>+key<A>+realese<right_ctrl>` - Ctrl+A

## Detailed Method Descriptions

### `key<>`, `press<>` and `realese<>`
These methods accept the vast majority of standard keyboard keys that can be typed without requiring Shift, etc.
* Supports keys from `F1` to `F24`.
* Numbers are accepted literally (`1` instead of `one`).
* Numpad keys are simplified (`num1` instead of `numpad_one`).

### `media<>`
In practice, `Play` and `Pause` provide the exact same toggle effect. If media is currently playing, sending `Play` will act as a pause command.
* `Play` / `Pause` - Media playback control
* `VolUp` / `VolDown` - System volume control
* `Skip` / `BackSkip` - Next / Previous track
* `Stop` - Stop playback
* `Eject` - Eject disk
* `Fast_Forward` / `Rewind` - Fast forward and rewind
* `Mute` - Mute audio
* `BrightnessUp` / `BrightnessDown` - Screen brightness control

The `VolUp`, `VolDown`, `BrightnessUp`, and `BrightnessDown` methods can optionally take a step value ranging from 1 to 100 (e.g., `<BrightnessUp:20>`). If the specified value exceeds this range, it will be automatically capped to the maximum allowed limit (e.g., providing `234` will be interpreted as `100`).

## Planned Features (To-Do)

* `mouse<>` - Mouse movement and click control
* `wait<>` - Execution delay in seconds
