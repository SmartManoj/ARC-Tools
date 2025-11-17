import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Transform grid based on frame location (row or column of all 2s).

    For horizontal frame (row): Pair consecutive non-frame rows with content,
    merge each pair with OR operation, place before frame.

    For vertical frame (column): Pair consecutive rows, compact elements toward
    frame within each row, right-align to fill max width needed.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find the frame (a row or column of all 2s)
    frame_row = None
    frame_col = None

    for r in range(h):
        if all(result[r][c] == 2 for c in range(w)):
            frame_row = r
            break

    if frame_row is None:
        for c in range(w):
            if all(result[r][c] == 2 for r in range(h)):
                frame_col = c
                break

    if frame_row is not None:
        # HORIZONTAL FRAME: Pair and merge rows
        # Get non-frame rows with content
        content_rows = []
        for r in range(h):
            if r != frame_row and any(result[r][c] != 0 for c in range(w)):
                content_rows.append(r)

        # Pair them consecutively
        merged_rows = []
        for i in range(0, len(content_rows), 2):
            if i + 1 < len(content_rows):
                r1, r2 = content_rows[i], content_rows[i + 1]
                # Merge with MAX (OR operation)
                merged = [max(result[r1][c], result[r2][c]) for c in range(w)]
                merged_rows.append(merged)
            else:
                merged_rows.append([result[content_rows[i]][c] for c in range(w)])

        # Place merged rows relative to the frame
        if frame_row < h // 2:
            # Frame is at or near the top: place merged rows after the frame
            start_row = frame_row + 1
        else:
            # Frame is at or near the bottom: place merged rows before the frame
            start_row = frame_row - len(merged_rows)

        for i, merged_row in enumerate(merged_rows):
            for c in range(w):
                result[start_row + i][c] = merged_row[c]

        # Clear the rest
        if frame_row < h // 2:
            # Frame at top: clear rows above it and after the merged content
            for r in range(frame_row):
                for c in range(w):
                    result[r][c] = 0
            for r in range(start_row + len(merged_rows), h):
                for c in range(w):
                    result[r][c] = 0
        else:
            # Frame at bottom: clear rows before the merged content and below frame
            for r in range(h):
                if r < start_row or r > frame_row:
                    for c in range(w):
                        result[r][c] = 0

    elif frame_col is not None:
        # VERTICAL FRAME: Pair consecutive rows, compact within each row
        # Pair consecutive rows
        pairs = []
        for i in range(0, h, 2):
            if i + 1 < h:
                pairs.append((i, i + 1))
            else:
                pairs.append((i,))

        prev_widest_start_col = None

        # Process each pair
        for pair_idx, (r1, *rest) in enumerate(pairs):
            r2 = rest[0] if rest else None

            # Compact elements for each row in pair
            compacted = []
            if frame_col == 0:
                # Frame on left
                for r in [r1, r2] if r2 is not None else [r1]:
                    elements = [result[r][c] for c in range(frame_col + 1, w) if result[r][c] != 0]
                    compacted.append(elements)
            else:
                # Frame on right
                for r in [r1, r2] if r2 is not None else [r1]:
                    elements = [result[r][c] for c in range(frame_col) if result[r][c] != 0]
                    compacted.append(elements)

            # Find max width
            max_width = max(len(c) for c in compacted) if compacted else 0

            # For single-row pairs after first pair: use widest row's starting column from previous pair
            if r2 is None and pair_idx > 0 and prev_widest_start_col is not None:
                # Single-row pair: place at same starting column as previous pair's widest row
                start_col = prev_widest_start_col
                aligned = compacted  # No alignment needed
            else:
                # Apply right-alignment rules:
                # - First pair: no alignment
                # - Subsequent pairs: right-align all rows to max_width
                aligned = []
                for row_in_pair_idx, elements in enumerate(compacted):
                    if pair_idx == 0:
                        # First pair: no alignment
                        aligned.append(elements)
                    else:
                        # Subsequent pairs: right-align to max_width
                        if frame_col == 0:
                            # Frame on left: pad on left
                            aligned.append([0] * (max_width - len(elements)) + elements)
                        else:
                            # Frame on right: pad on left
                            aligned.append([0] * (max_width - len(elements)) + elements)

                # Determine start_col based on frame position and max_width
                if frame_col == 0:
                    start_col = frame_col + 1
                else:
                    start_col = frame_col - max_width

            # Reconstruct rows
            for idx, r in enumerate([r1, r2] if r2 is not None else [r1]):
                # Clear the row first
                for c in range(w):
                    result[r][c] = 0

                # Place frame
                result[r][frame_col] = 2

                # Place aligned elements
                if frame_col == 0:
                    # Frame on left: elements go to the right
                    for i, val in enumerate(aligned[idx]):
                        result[r][frame_col + 1 + i] = val
                else:
                    # Frame on right: elements go to the left
                    if pair_idx == 0:
                        # First pair: each row uses its own width
                        row_start_col = frame_col - len(aligned[idx])
                    else:
                        # Subsequent pairs: use the pre-computed start_col
                        row_start_col = start_col

                    for i, val in enumerate(aligned[idx]):
                        result[r][row_start_col + i] = val

            # Track the starting column of the widest row in this pair
            if aligned:
                widest_idx = max(range(len(compacted)), key=lambda i: len(compacted[i]))
                if frame_col == 0:
                    prev_widest_start_col = frame_col + 1
                else:
                    prev_widest_start_col = start_col

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("6ad5bdfd", solve)
