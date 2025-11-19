import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Analyzes a sequence of patterns across 4 sections (divided by gray line 5)
    and predicts the next step in the sequence.

    The input has 15 rows with gray (5) dividers at rows 3, 7, 11.
    This creates 4 sections at rows 0-2, 4-6, 8-10, 12-14.

    Key insight: Only the MIDDLE row (row 1) of each section contains the pattern.
    Rows 0 and 2 are typically all zeros or constant.
    '''
    width = len(grid[0])

    # Extract the middle row from each of the 4 sections
    middle_rows = [
        [grid[1][col] for col in range(width)],   # Section 0, row 1
        [grid[5][col] for col in range(width)],   # Section 1, row 5
        [grid[9][col] for col in range(width)],   # Section 2, row 9
        [grid[13][col] for col in range(width)]   # Section 3, row 13
    ]

    # Also get the top/bottom rows to check if they have patterns
    top_rows = [
        [grid[0][col] for col in range(width)],
        [grid[4][col] for col in range(width)],
        [grid[8][col] for col in range(width)],
        [grid[12][col] for col in range(width)]
    ]

    bottom_rows = [
        [grid[2][col] for col in range(width)],
        [grid[6][col] for col in range(width)],
        [grid[10][col] for col in range(width)],
        [grid[14][col] for col in range(width)]
    ]

    # Predict the next row for each position
    predicted_top = predict_next_row(top_rows)
    predicted_middle = predict_next_row(middle_rows)
    predicted_bottom = predict_next_row(bottom_rows)

    return Grid([predicted_top, predicted_middle, predicted_bottom])

def predict_next_row(row_sequence):
    '''
    Given a sequence of 4 rows showing a progression,
    predict the 5th row.

    Strategy:
    1. Find the non-zero pattern in each row
    2. Detect if it's shifting (position changes) or growing (size changes)
    3. Extrapolate to predict the next step
    '''
    width = len(row_sequence[0])

    # Extract non-zero segments from each row
    segments = []
    for row in row_sequence:
        segment = extract_nonzero_segment(row)
        segments.append(segment)

    # Check if all rows are zeros (no pattern)
    if all(seg['start'] == -1 for seg in segments):
        return [0] * width

    # Analyze the pattern
    # Case 1: Shifting pattern (same values, different positions)
    if is_shifting_pattern(segments):
        return predict_shifting_pattern(segments, width)

    # Case 2: Growing pattern (size increases, position may stay same)
    elif is_growing_pattern(segments):
        return predict_growing_pattern(segments, width)

    # Case 3: Complex pattern (values change within object)
    else:
        return predict_complex_pattern(row_sequence, width)

def extract_nonzero_segment(row):
    '''Extract the start position, end position, and values of non-zero segment'''
    nonzero_indices = [i for i, v in enumerate(row) if v != 0]

    if not nonzero_indices:
        return {'start': -1, 'end': -1, 'values': [], 'length': 0}

    start = min(nonzero_indices)
    end = max(nonzero_indices)
    values = row[start:end+1]

    return {'start': start, 'end': end, 'values': values, 'length': end - start + 1}

def is_shifting_pattern(segments):
    '''Check if the pattern is shifting (same values, moving position)'''
    # Remove empty segments
    valid_segments = [s for s in segments if s['start'] != -1]
    if len(valid_segments) < 2:
        return False

    # Check if lengths are the same
    lengths = [s['length'] for s in valid_segments]
    if len(set(lengths)) != 1:
        return False

    # Check if values are the same
    first_values = valid_segments[0]['values']
    for seg in valid_segments[1:]:
        if seg['values'] != first_values:
            return False

    return True

def is_growing_pattern(segments):
    '''Check if the pattern is growing (size increases)'''
    valid_segments = [s for s in segments if s['start'] != -1]
    if len(valid_segments) < 2:
        return False

    # Check if lengths are increasing
    lengths = [s['length'] for s in valid_segments]
    for i in range(len(lengths) - 1):
        if lengths[i] >= lengths[i+1]:
            return False

    return True

def predict_shifting_pattern(segments, width):
    '''Predict next row for a shifting pattern'''
    valid_segments = [s for s in segments if s['start'] != -1]

    # Calculate the shift amount
    starts = [s['start'] for s in valid_segments]
    if len(starts) >= 2:
        shift = starts[-1] - starts[-2]
    else:
        shift = 1

    # Predict next position
    next_start = valid_segments[-1]['start'] + shift
    values = valid_segments[-1]['values']

    # Build the next row
    next_row = [0] * width
    for i, val in enumerate(values):
        pos = next_start + i
        if 0 <= pos < width:
            next_row[pos] = val

    return next_row

def predict_growing_pattern(segments, width):
    '''Predict next row for a growing pattern'''
    valid_segments = [s for s in segments if s['start'] != -1]

    # Calculate the growth amount
    lengths = [s['length'] for s in valid_segments]
    if len(lengths) >= 2:
        growth = lengths[-1] - lengths[-2]
    else:
        growth = 2

    # Determine the value to use
    # Typically the same color continues
    last_segment = valid_segments[-1]
    color = max(set(last_segment['values']), key=last_segment['values'].count)

    # Predict next size and position
    next_length = last_segment['length'] + growth
    next_start = last_segment['start']  # Usually same start position

    # Build the next row
    next_row = [0] * width
    for i in range(next_length):
        pos = next_start + i
        if 0 <= pos < width:
            next_row[pos] = color

    return next_row

def predict_complex_pattern(row_sequence, width):
    '''Handle complex patterns by analyzing column-by-column'''
    next_row = [0] * width

    # First check if this is a "leading 3s growing" pattern
    # This pattern has 3s at the start that grow, followed by 2s
    if is_leading_growth_pattern(row_sequence):
        return predict_leading_growth(row_sequence, width)

    # Otherwise, analyze column-by-column with context
    for col in range(width):
        values = [row_sequence[i][col] for i in range(4)]
        # Build complete row context
        next_row[col] = predict_complex_value_v2(values, col, row_sequence, next_row)

    return next_row

def is_leading_growth_pattern(row_sequence):
    '''Check if rows have leading 3s that grow, followed by 2s'''
    # Count leading 3s in each row
    leading_3s = []
    for row in row_sequence:
        count = 0
        for v in row:
            if v == 3:
                count += 1
            else:
                break
        leading_3s.append(count)

    # Check if they're growing consistently
    if leading_3s[0] > 0 and all(leading_3s[i] <= leading_3s[i+1] for i in range(len(leading_3s)-1)):
        # Check if followed by 2s
        last_row = row_sequence[-1]
        if leading_3s[-1] < len(last_row) and last_row[leading_3s[-1]] == 2:
            return True
    return False

def predict_leading_growth(row_sequence, width):
    '''Predict pattern where leading 3s grow'''
    # Count leading 3s in each row
    leading_3s = []
    for row in row_sequence:
        count = 0
        for v in row:
            if v == 3:
                count += 1
            else:
                break
        leading_3s.append(count)

    # Calculate growth rate
    if len(leading_3s) >= 2:
        growth = leading_3s[-1] - leading_3s[-2]
    else:
        growth = 1

    # Predict next count
    next_count = leading_3s[-1] + growth

    # Build next row
    next_row = [0] * width
    for i in range(width):
        if i < next_count:
            next_row[i] = 3
        else:
            # Copy from last row for remaining values
            next_row[i] = row_sequence[-1][i]

    return next_row

def predict_complex_value_v2(values, col, row_sequence, next_row):
    '''Predict next value with full context'''
    # Check for 2→3 conversion pattern FIRST (before checking if all same)
    # This is important because a column with [2,2,2,2] might need to convert to 3
    # based on context
    if all(v in [0, 2, 3] for v in values):
        if values[-1] == 3:
            return 3
        elif values[-1] == 2 and len(set(values)) == 1:  # All 2s
            # Find the previous non-zero column IN THE SAME GROUP
            # (not separated by 2+ consecutive zeros)
            prev_nonzero_col = None
            zero_count = 0
            for c in range(col - 1, -1, -1):
                prev_vals = [row_sequence[i][c] for i in range(4)]
                if any(v != 0 for v in prev_vals):
                    # Found a non-zero column
                    # Only use it if we haven't crossed a group boundary (2+ zeros)
                    if zero_count < 2:
                        prev_nonzero_col = c
                    break
                else:
                    zero_count += 1

            # If there's a previous non-zero column in the same group,
            # check if it has stabilized at 3
            if prev_nonzero_col is not None:
                prev_vals = [row_sequence[i][prev_nonzero_col] for i in range(4)]
                # Check if the previous column has stabilized at 3 in recent sections
                if all(v == 3 for v in prev_vals[2:]):  # Last 2 sections are 3
                    # This column should start converting
                    return 3

    # If all same and not a 2→3 conversion case, continue
    if len(set(values)) == 1:
        return values[0]

    # Check for other 2→3 conversion patterns (values changing)
    if all(v in [0, 2, 3] for v in values):
        return values[-1]

    # Default: continue with last value
    return values[-1]

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("351d6448", solve)
