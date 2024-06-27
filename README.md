# GUI Application Requirements

## Description

This Python GUI application consists of two main areas: a left area with interactive controls and a right area displaying visual representations based on the controls' settings.

## Left Area

1. **Slider:**
   - Range: 350 to 750.
   - Adjusts the height of the left bar in the right area.
   - Displays its current value at the bottom of the left bar.

2. **Checkboxes:**
   - Total of 12 checkboxes.
   - Each checkbox represents an internal value (to be defined later).
   - Changes in checkbox states update the height of the right bar in the right area.
   - Displays the sum of selected checkbox values at the bottom of the right bar.

## Right Area

1. **Left Bar:**
   - Displays height equal to the current value of the slider.
   - Bottom of the bar shows the exact numerical value of the slider.

2. **Right Bar:**
   - Displays height equal to the sum of selected checkbox values.
   - Bottom of the bar shows the calculated sum of selected checkbox values.

## Usage

- Adjust the slider to change the height of the left bar and see its value displayed below the bar.
- Select checkboxes to change the height of the right bar and observe the sum of selected checkbox values displayed below the bar.

## Customization

- **Names:** 
  - The names of the GUI display, checkboxes, and bars can be customized directly within the source code.
