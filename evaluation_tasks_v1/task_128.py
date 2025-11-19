import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task


def solve(grid: Grid):
    '''
    The pattern: Detect horizontal line segments of colors 3 and 2, then create a summary.

    Steps:
    1. Find the background color (most common color)
    2. Detect all horizontal line segments of color 3
    3. Detect all horizontal line segments of color 2
    4. Sort each color's segments by length in descending order
    5. Combine segments: all 3s first, then all 2s
    6. Take first 6 elements (pad with 0 if needed)
    7. Reshape to 2x3 grid

    The output is a 2x3 grid showing the most significant line segments,
    with color 3 segments prioritized over color 2 segments.
    '''

    # Find background color (most common)
    color_counts = {}
    for row in grid:
        for cell in row:
            color_counts[cell] = color_counts.get(cell, 0) + 1

    background = max(color_counts.items(), key=lambda x: x[1])[0]

    # Detect horizontal line segments for colors 3 and 2
    def find_horizontal_segments(color):
        segments = []
        for row in grid:
            in_segment = False
            segment_length = 0
            for cell in row:
                if cell == color:
                    if not in_segment:
                        in_segment = True
                        segment_length = 1
                    else:
                        segment_length += 1
                else:
                    if in_segment:
                        segments.append(segment_length)
                        in_segment = False
                        segment_length = 0
            # Check if segment continues to end of row
            if in_segment:
                segments.append(segment_length)
        return segments

    # Get segments for each color
    segments_3 = find_horizontal_segments(3)
    segments_2 = find_horizontal_segments(2)

    # Sort by length descending
    segments_3.sort(reverse=True)
    segments_2.sort(reverse=True)

    # Combine: all 3s first, then all 2s
    combined = []
    for length in segments_3:
        combined.append(3)
    for length in segments_2:
        combined.append(2)

    # Pad to 6 elements
    while len(combined) < 6:
        combined.append(0)

    # Take first 6
    combined = combined[:6]

    # Reshape to 2x3 grid
    output = [
        combined[0:3],
        combined[3:6]
    ]

    return Grid(output)


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("5289ad53", solve)
