import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task

def solve(grid: Grid):
    '''
    Transform 2x2 blocks of 2s: some blocks become 8, others stay as 2.
    Pattern: find the row range with the most "pair blocks" (rows with 2+ blocks).
    Blocks in that range + adjacent rows stay. Others become 8.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find all 2x2 blocks of 2s
    blocks = []
    for r in range(h - 1):
        for c in range(w - 1):
            if (result[r][c] == 2 and result[r][c+1] == 2 and
                result[r+1][c] == 2 and result[r+1][c+1] == 2):
                blocks.append((r, c))

    if not blocks:
        return result

    # Group blocks by row
    row_to_blocks = {}
    for b in blocks:
        if b[0] not in row_to_blocks:
            row_to_blocks[b[0]] = []
        row_to_blocks[b[0]].append(b)

    # Get unique row indices and check for significant gaps
    block_rows = sorted(set(b[0] for b in blocks))

    # Find significant gaps (row jump > 2, meaning missing 2+ rows)
    gaps = []
    for i in range(len(block_rows) - 1):
        if block_rows[i+1] - block_rows[i] > 2:
            gaps.append((block_rows[i], block_rows[i+1]))

    # Find rows with pairs (2+ blocks)
    rows_with_pairs = [r for r in sorted(row_to_blocks.keys()) if len(row_to_blocks[r]) >= 2]

    blocks_to_change = set()

    # First check if there are gaps
    has_gap = len(gaps) > 0

    if has_gap:
        # Use gap-based logic first
        gap_row = gaps[0][0]
        before_gap = [b for b in blocks if b[0] <= gap_row]
        after_gap = [b for b in blocks if b[0] > gap_row]

        # The smaller section stays, others become 8
        if len(before_gap) > len(after_gap):
            blocks_to_change.update(before_gap)
        elif len(after_gap) > len(before_gap):
            blocks_to_change.update(after_gap)
        else:
            # Same size: first stays, second changes
            blocks_to_change.update(after_gap)
    elif rows_with_pairs:
        # Find the contiguous range with the most pairs
        # Try all possible contiguous sub-ranges
        pair_rows_set = set(rows_with_pairs)
        sorted_rows = sorted(row_to_blocks.keys())

        # Try all contiguous sub-ranges (must be consecutive, no gaps > 1)
        best_group = None
        best_score = -1
        two_pair_found = False

        for start_idx in range(len(sorted_rows)):
            for end_idx in range(start_idx, len(sorted_rows)):
                group = sorted_rows[start_idx:end_idx+1]
                # Check if group is consecutive (no gaps > 1 within the group)
                max_gap = max(group[i+1] - group[i] for i in range(len(group)-1)) if len(group) > 1 else 0
                if max_gap <= 1:  # Consecutive rows only
                    pair_count = sum(1 for r in group if r in pair_rows_set)
                    if pair_count > 0:
                        density = pair_count / len(group)

                        if pair_count >= 2:
                            # 2+ pair group: score based on density
                            score = density * 10000 + pair_count * 100
                            if score > best_score:
                                best_score = score
                                best_group = group
                                two_pair_found = True
                        elif not two_pair_found:
                            # Single-pair group: only use if no 2-pair group found
                            # Prefer groups that don't include first or last row
                            is_at_edge = (group[0] == sorted_rows[0] or group[-1] == sorted_rows[-1])
                            non_edge_bonus = 0 if is_at_edge else 1000
                            score = non_edge_bonus + len(group) * 100 + density * 10
                            if score > best_score:
                                best_score = score
                                best_group = group

        # Blocks in best_group stay, others become 8
        best_group_set = set(best_group) if best_group else set()
        for b in blocks:
            if b[0] not in best_group_set:
                blocks_to_change.add(b)

        # But within the best group, if there are rows with pairs and isolated blocks,
        # remove isolated outliers
        if best_group:
            for row in best_group:
                if row not in pair_rows_set and len(row_to_blocks[row]) == 1:
                    # Single isolated block at this row
                    # Check if it's truly isolated or adjacent to pairs
                    has_adjacent_pair = any(abs(row - pr) <= 1 for pr in rows_with_pairs)
                    if not has_adjacent_pair:
                        blocks_to_change.add(row_to_blocks[row][0])

        # Also handle blocks at the same row: if multiple blocks, keep the ones
        # that form a proper chain
        for row in best_group_set:
            row_blocks = [b for b in blocks if b[0] == row and b not in blocks_to_change]
            if len(row_blocks) > 1:
                # Multiple blocks: check if there's a block above to guide selection
                if row > 0:
                    blocks_above = [b for b in blocks if b[0] == row - 1 and b not in blocks_to_change]
                    if blocks_above:
                        # Keep the block(s) closest to blocks above
                        above_cols = [b[1] for b in blocks_above]
                        # Keep only the closest block(s)
                        closest_dist = min(min(abs(b[1] - ac) for ac in above_cols) for b in row_blocks)
                        blocks_to_keep = [b for b in row_blocks if min(abs(b[1] - ac) for ac in above_cols) == closest_dist]
                        blocks_to_remove = [b for b in row_blocks if b not in blocks_to_keep]
                        blocks_to_change.update(blocks_to_remove)
    else:
        # No pairs: find the "main chain" by greedy vertical continuation
        sorted_rows = sorted(row_to_blocks.keys())

        blocks_in_chain = set()
        current_col = None

        for row_idx in sorted_rows:
            blocks_at_row = sorted(row_to_blocks[row_idx], key=lambda b: b[1])

            if current_col is None:
                chosen = blocks_at_row[0]
            else:
                closest = min(blocks_at_row, key=lambda b: abs(b[1] - current_col))
                chosen = closest

            blocks_in_chain.add(chosen)
            current_col = chosen[1]

        blocks_to_change = set(blocks) - blocks_in_chain

    # Change identified blocks to 8
    for r, c in blocks_to_change:
        result[r][c] = 8
        result[r][c+1] = 8
        result[r+1][c] = 8
        result[r+1][c+1] = 8

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("817e6c09", solve)
