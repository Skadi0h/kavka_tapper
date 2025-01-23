# KavkaTapper

KavkaTapper is a macOS application built with PyQt5 that allows users to select a screen region and perform automated clicking within that region. It focuses on automating clicks in a selected area of the screen while interacting with applications like Chrome.

## Features

- **Screen Region Selection**: Select a rectangular region on the screen by right-clicking and dragging the mouse.
- **Automated Clicking**: After selecting an area, pressing the 'T' key will initiate a series of automated clicks within that region.
- **App Focus**: The application will focus on an active window (currently, Chrome is supported).
- **Translucent and Frameless Window**: The app runs with a transparent background and no window borders.
- **Resizable and Maximizable**: The window is resizable and can be maximized for a full-screen experience.
  
## Requirements

- Python 3.11.6
- macOS (developed and tested on macOS)
- `uv`
- `pyautogui`
- `PyQt5`

## Installation

To install and run the project, follow these steps:

```bash
git clone https://github.com/Skadi0h/kavka_tapper.git;
cd kavka_tapper;
bash install;
```

## Usage

```bash
bash run
```
