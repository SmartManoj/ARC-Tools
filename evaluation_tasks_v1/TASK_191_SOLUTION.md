# ARC-AGI Task 191 Solution (7d1f7ee8)

## Problem Summary
This task involves nested rectangular structures where colored rectangles are outlined by different colors. The transformation rule replaces colored pixels based on the nesting hierarchy of rectangle borders.

## Pattern Analysis
The transformation has the following behavior:
1. Each color that forms a complete **rectangular border** (outline) encloses an interior region
2. If a rectangle border is nested inside another rectangle, **all pixels** of the inner rectangle (both border and interior) are replaced with the color of the containing rectangle
3. If a rectangle border is not nested, its **interior** non-border pixels are replaced with the rectangle's own color

## Algorithm
The solution uses the following approach:

1. **Connected Components Detection**: For each non-zero color, find all connected components using flood fill, since a color may appear in multiple disconnected regions

2. **Rectangle Border Identification**: For each connected component, check if it forms a valid rectangle border:
   - All pixels must be on the perimeter of their bounding box
   - The bounding box must have non-zero dimensions (height and width > 1)

3. **Nesting Hierarchy**: Build a containment map to identify which rectangles are nested inside others

4. **Pixel Replacement**:
   - For nested rectangles: Replace all pixels (border and interior) with the containing rectangle's color
   - For non-nested (outermost) rectangles: Replace only interior pixels with the rectangle's color

## Key Code Components
- `get_connected_components()`: Flood fill algorithm to find separate regions of each color
- `contains_rectangle()`: Check if one rectangle completely contains another
- `nested_map`: Dictionary tracking the containment hierarchy

## Results
- **Training Example 1**: ✓ PASSED
  - Input: 6 colors in nested structure (8→4→3, 8→2, 7→1)
  - Output: Correct hierarchical replacement
  
- **Training Example 2**: ✓ PASSED
  - Input: 5 colors with two separate rectangle hierarchies (2→4→1, 1→6, 3)
  - Output: Correct independent handling of separate hierarchies
  
- **Training Example 3**: ✓ PASSED
  - Input: 4 colors in single nested structure (1→2→8, 1→3)
  - Output: Correct replacement of all inner colors

## File Location
- Solution: `/home/user/ARC-Tools/evaluation_tasks_v1/task_191.py`
- Task Data: `/home/user/ARC-AGI/data/evaluation/7d1f7ee8.json`
