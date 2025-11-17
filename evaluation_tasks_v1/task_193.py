import os
from collections import deque
from arc_tools.grid import Grid
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task


def solve(grid: Grid):
    '''
    Find rectangular blocks of 0s and mark them with plus patterns.
    Rules:
    1. Find all rectangular blocks of size 2x2 or larger
    2. Group by connected component
    3. For each component, mark all rectangles with area > 4
    4. Also mark 2x2 rectangles if their component has any marked rectangles
    5. Place plus patterns at rectangle centers
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find all rectangular blocks of 0s
    rectangles = find_maximal_rectangles(result)

    # Find connected components
    comp_map, comp_sizes = find_connected_components(result)

    # Group rectangles by component and find which to mark
    marked_rects = select_rectangles_to_mark(rectangles, comp_map, comp_sizes)

    # Mark the selected rectangles with plus patterns
    for (top, left), height, width in marked_rects:
        center_i = top + height // 2
        # For even width, use the left-middle position
        if width % 2 == 0:
            center_j = left + width // 2 - 1
        else:
            center_j = left + width // 2
        mark_plus_pattern(result, center_i, center_j)

    return result


def find_maximal_rectangles(grid):
    '''Find all rectangular blocks of 0s that are at least 2x2'''
    h, w = grid.height, grid.width
    rectangles = set()

    # Find all possible 2x2+ rectangular blocks
    for top in range(h):
        for left in range(w):
            if grid[top][left] != 0:
                continue

            # Try all possible heights and widths starting at (top, left)
            for height in range(2, h - top + 1):
                # Check if this height is valid (all must be 0)
                valid_h = True
                for di in range(height):
                    if grid[top + di][left] != 0:
                        valid_h = False
                        break
                if not valid_h:
                    break

                for width in range(2, w - left + 1):
                    # Check if full rectangle is all 0s
                    valid = True
                    for di in range(height):
                        for dj in range(width):
                            if grid[top + di][left + dj] != 0:
                                valid = False
                                break
                        if not valid:
                            break

                    if valid:
                        rectangles.add(((top, left), height, width))
                    else:
                        break  # Can't extend further in this direction

    return list(rectangles)


def find_connected_components(grid):
    '''Find all connected components of 0s and their sizes'''
    h, w = grid.height, grid.width
    visited = [[False] * w for _ in range(h)]
    comp_map = {}  # (i, j) -> component_id
    comp_sizes = {}  # component_id -> size

    def bfs(start_i, start_j, comp_id):
        queue = deque([(start_i, start_j)])
        visited[start_i][start_j] = True
        comp_map[(start_i, start_j)] = comp_id
        size = 1

        while queue:
            i, j = queue.popleft()
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < h and 0 <= nj < w and not visited[ni][nj] and grid[ni][nj] == 0:
                    visited[ni][nj] = True
                    comp_map[(ni, nj)] = comp_id
                    queue.append((ni, nj))
                    size += 1

        return size

    comp_id = 0
    for i in range(h):
        for j in range(w):
            if grid[i][j] == 0 and not visited[i][j]:
                size = bfs(i, j, comp_id)
                comp_sizes[comp_id] = size
                comp_id += 1

    return comp_map, comp_sizes


def select_rectangles_to_mark(rectangles, comp_map, comp_sizes):
    '''Select which rectangles to mark based on size criteria'''
    # Group rectangles by component
    comp_rects = {}
    for rect in rectangles:
        (top, left), h, w = rect
        comp = comp_map.get((top, left))
        if comp not in comp_rects:
            comp_rects[comp] = []
        comp_rects[comp].append(rect)

    # Mark rectangles: all area > 4, plus select 2x2s in special cases
    marked_rects = set()
    for comp in comp_rects:
        comp_size = comp_sizes.get(comp, 0)
        rects_in_comp = comp_rects[comp]

        if not rects_in_comp:
            continue

        # First, mark all rectangles with area > 4
        for rect in rects_in_comp:
            if rect[1] * rect[2] > 4:
                marked_rects.add(rect)

        # Then, handle 2x2 rectangles based on whether there are larger rects
        comp_has_large = any(r[1] * r[2] > 4 for r in rects_in_comp)

        if not comp_has_large:
            # No large rectangles - mark the largest 2x2 if component is large enough
            max_area = max(r[1] * r[2] for r in rects_in_comp)
            if max_area == 4 and comp_size >= 15:
                topmost = min([r for r in rects_in_comp if r[1] * r[2] == max_area],
                            key=lambda r: (r[0][0], r[0][1]))
                marked_rects.add(topmost)
        else:
            # Have large rectangles - mark 2x2s that DON'T overlap with them
            large_rects = [r for r in marked_rects if r in rects_in_comp]

            for rect in rects_in_comp:
                if rect[1] * rect[2] == 4:  # 2x2
                    # Only mark if it doesn't overlap with any marked > 4 rect
                    has_overlap = False
                    for large_rect in large_rects:
                        if _rects_overlap(rect, large_rect):
                            has_overlap = True
                            break
                    if not has_overlap:
                        marked_rects.add(rect)

    return marked_rects


def _rects_overlap(r1, r2):
    '''Check if two rectangles overlap'''
    (top1, left1), h1, w1 = r1
    (top2, left2), h2, w2 = r2
    return not (top1 + h1 <= top2 or top2 + h2 <= top1 or
                left1 + w1 <= left2 or left2 + w2 <= left1)


def _rects_touch_or_adjacent(r1, r2):
    '''Check if two rectangles touch, overlap, or are adjacent (share an edge or corner)'''
    (top1, left1), h1, w1 = r1
    (top2, left2), h2, w2 = r2

    # Check for overlap or adjacency (within 1 cell distance)
    row_overlap = (top1 <= top2 + h2 and top2 <= top1 + h1) or \
                  (top1 - 1 <= top2 + h2 and top2 - 1 <= top1 + h1)
    col_overlap = (left1 <= left2 + w2 and left2 <= left1 + w1) or \
                  (left1 - 1 <= left2 + w2 and left2 - 1 <= left1 + w1)

    return row_overlap and col_overlap


def mark_plus_pattern(grid, center_i, center_j):
    '''Mark a plus pattern centered at (center_i, center_j) with value 3'''
    h, w = grid.height, grid.width

    if 1 <= center_i < h - 1 and 1 <= center_j < w - 1:
        # Mark the center and four directions
        grid[center_i][center_j] = 3
        grid[center_i - 1][center_j] = 3
        grid[center_i + 1][center_j] = 3
        grid[center_i][center_j - 1] = 3
        grid[center_i][center_j + 1] = 3


if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("7e02026e", solve)
