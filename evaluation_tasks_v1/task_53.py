import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Pattern: Each row follows a repeating sequence, with diagonal doubling.

    The pattern:
    1. There's a base repeating sequence (like [1, 2, 3, 4, 5, 6])
    2. Each row uses the sequence with a specific offset
    3. At position (r, r) on the diagonal, values may be doubled
    4. The pattern is column-based: value[r][c] depends primarily on c
    '''
    height = grid.height
    width = grid.width

    # Create output grid as a copy
    output_data = [list(grid[r]) for r in range(height)]

    # Find the repeating sequence and offset by analyzing non-zero values
    # Look at columns to find the pattern (since each column should have consistent values)

    # Try different periods and pick the best one
    best_period_choice = None
    best_sequence_choice = None
    best_score = -1

    for period in range(6, 10):
        # For each period, try to build a sequence by looking at column patterns
        # Skip positions on the diagonal as they may have doubling
        sequence_candidates = {}

        for r in range(height):
            for c in range(width):
                if grid[r][c] != 0 and c > r + 1:  # Skip diagonal and near-diagonal
                    col_mod = c % period
                    val = grid[r][c]
                    if col_mod not in sequence_candidates:
                        sequence_candidates[col_mod] = []
                    sequence_candidates[col_mod].append(val)

        # Build sequence from most common values
        if len(sequence_candidates) == period:
            from collections import Counter
            sequence = []
            total_consistency = 0
            for i in range(period):
                if i in sequence_candidates and sequence_candidates[i]:
                    counter = Counter(sequence_candidates[i])
                    most_common_val, most_common_count = counter.most_common(1)[0]
                    sequence.append(most_common_val)
                    # Score based on how many times the most common value appears
                    total_consistency += most_common_count
                else:
                    sequence = None
                    break

            if sequence and len(sequence) == period:
                # Score this period based on consistency
                if total_consistency > best_score:
                    best_score = total_consistency
                    best_period_choice = period
                    best_sequence_choice = sequence

    # Use the best period found
    if best_period_choice is not None and best_sequence_choice is not None:
        period = best_period_choice
        sequence = best_sequence_choice

        if True:  # Changed from "if sequence and len(sequence) == period:"
                # We found a valid sequence!
                # Now fill in all positions
                for r in range(height):
                    # Determine row offset by looking at non-diagonal non-zero values
                    row_vals = [(c, grid[r][c]) for c in range(width) if grid[r][c] != 0 and c != r]
                    if row_vals:
                        # Find offset for this row
                        c0, val0 = row_vals[0]
                        # val0 should be sequence[(c0 + offset) mod period]
                        # BUT if c0 > r, there's a shift due to diagonal doubling
                        # Find which index in sequence val0 is
                        if val0 in sequence:
                            val_idx = sequence.index(val0)

                            # Adjust for diagonal doubling shift
                            if c0 > r and r > 0:
                                # After diagonal (for r > 0), shift by -1
                                offset = (val_idx - c0 + 1) % period
                            else:
                                offset = (val_idx - c0) % period

                            # Fill row using this offset with diagonal doubling
                            for c in range(width):
                                if r == 0 or c < r:
                                    # Row 0 or before diagonal: normal pattern
                                    output_data[r][c] = sequence[(c + offset) % period]
                                elif c == r and r > 0:
                                    # Diagonal (only for r > 0): duplicate previous value
                                    output_data[r][c] = output_data[r][c-1]
                                elif c > r:
                                    # After diagonal: shift by -1
                                    output_data[r][c] = sequence[(c - 1 + offset) % period]
                                else:
                                    # Fallback
                                    output_data[r][c] = sequence[(c + offset) % period]

                return Grid(output_data)

    # Fallback: return original if pattern not found
    return grid

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("1e97544e", solve)
