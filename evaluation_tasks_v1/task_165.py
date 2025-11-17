import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Transform based on isolated markers connecting to line structures.

    Pattern:
    1. Find isolated single-cell markers (non-zero cells not adjacent to same color)
    2. Find line structures (connected cells of same color, multiple cells)
    3. For each marker aligned with a structure:
       - Draw a path from structure to marker, filling with structure color
       - Change N cells in the structure to marker color, where N = path length
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find all structures and isolated markers
    visited = [[False] * w for _ in range(h)]
    structures = {}  # color -> list of cells
    isolated_markers = []  # (r, c, color)

    def bfs(sr, sc, color):
        """Find all connected cells of the same color"""
        queue = [(sr, sc)]
        visited[sr][sc] = True
        cells = [(sr, sc)]
        while queue:
            r, c = queue.pop(0)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and not visited[nr][nc] and result[nr][nc] == color:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
                    cells.append((nr, nc))
        return cells

    # Collect all structures and identify isolated markers
    for r in range(h):
        for c in range(w):
            if result[r][c] != 0 and not visited[r][c]:
                color = result[r][c]
                cells = bfs(r, c, color)
                structures[color] = cells

                # Check if this structure is an isolated marker (single cell)
                if len(cells) == 1:
                    isolated_markers.append((r, c, color))

    # Process each isolated marker
    for marker_r, marker_c, marker_color in isolated_markers:
        # Find structures that align with this marker
        for struct_color, struct_cells in structures.items():
            if struct_color == marker_color or len(struct_cells) == 1:
                continue

            struct_rows = [r for r, c in struct_cells]
            struct_cols = [c for r, c in struct_cells]
            min_row, max_row = min(struct_rows), max(struct_rows)
            min_col, max_col = min(struct_cols), max(struct_cols)

            # Find all cells aligned with marker in this structure
            aligned_vertical = [c for c in struct_cells if c[1] == marker_c]  # Same column
            aligned_horizontal = [c for c in struct_cells if c[0] == marker_r]  # Same row

            # Process vertical alignment (marker and structure in same column)
            # Only process if multiple cells are aligned (not just a single intersection)
            if aligned_vertical and len(aligned_vertical) > 1:
                # Find the structure cell closest to marker
                closest_cell = min(aligned_vertical, key=lambda x: abs(x[0] - marker_r))
                struct_row = closest_cell[0]
                path_length = abs(marker_r - struct_row) - 1

                if path_length > 0:
                    # Fill vertical path with struct_color
                    if marker_r < struct_row:
                        # Marker is above structure, fill upward
                        for r in range(marker_r + 1, struct_row):
                            result[r][marker_c] = struct_color
                    else:
                        # Marker is below structure, fill downward
                        for r in range(struct_row + 1, marker_r):
                            result[r][marker_c] = struct_color

                    # Change perpendicular cells (not in the same column as aligned cells)
                    perp_cells = [c for c in struct_cells if c[1] != marker_c]
                    if perp_cells:
                        # Sort by distance from aligned column (descending - farthest first)
                        perp_sorted = sorted(perp_cells, key=lambda x: abs(x[1] - marker_c), reverse=True)
                        # Change the first path_length cells (those with largest distance)
                        for i in range(min(path_length, len(perp_sorted))):
                            r, c = perp_sorted[i]
                            result[r][c] = marker_color

            # Process horizontal alignment (marker and structure in same row)
            # Only process if multiple cells are aligned (not just a single intersection)
            elif aligned_horizontal and len(aligned_horizontal) > 1:
                # Find the structure cell closest to marker
                closest_cell = min(aligned_horizontal, key=lambda x: abs(x[1] - marker_c))
                struct_col = closest_cell[1]
                path_length = abs(marker_c - struct_col) - 1

                if path_length > 0:
                    # Fill horizontal path with struct_color
                    if marker_c < struct_col:
                        # Marker is left of structure
                        for c in range(marker_c + 1, struct_col):
                            result[marker_r][c] = struct_color
                    else:
                        # Marker is right of structure
                        for c in range(struct_col + 1, marker_c):
                            result[marker_r][c] = struct_color

                    # Change perpendicular cells (not in the same row as aligned cells)
                    perp_cells = [c for c in struct_cells if c[0] != marker_r]
                    if perp_cells:
                        # Sort by distance from aligned row (descending - farthest first)
                        perp_sorted = sorted(perp_cells, key=lambda x: abs(x[0] - marker_r), reverse=True)
                        # Change the first path_length cells (those with largest distance)
                        for i in range(min(path_length, len(perp_sorted))):
                            r, c = perp_sorted[i]
                            result[r][c] = marker_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("696d4842", solve)
