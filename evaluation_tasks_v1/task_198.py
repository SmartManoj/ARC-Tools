import os
from arc_tools.grid import Grid, detect_objects, Color
from arc_tools import logger
from arc_tools.plot import plot_grids
from helper import solve_task
from collections import deque

def solve(grid: Grid):
    '''
    Find the horizontal divider line (row of 5s).
    For each connected component of 3s, match it to a colored region.

    Algorithm:
    1. Find horizontal divider (row with mostly 5s)
    2. Extract all colored regions (non-0, non-3, non-5) above the divider
    3. Normalize shapes of colored regions
    4. For each 3-component:
       a. Try to match by normalized shape to a colored region
       b. If shape matches, use that color
       c. If no shape match, use column-based assignment from colored regions
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find horizontal divider (row with mostly or all 5s)
    divider_row = -1
    for r in range(h):
        count_fives = sum(1 for c in range(w) if result[r][c] == 5)
        if count_fives >= w * 0.5:  # At least 50% are 5s
            divider_row = r
            break

    if divider_row == -1:
        return result

    # BFS-based connected component finding
    def find_components(value, max_row=h):
        visited = [[False] * w for _ in range(max_row)]
        components = []

        for r in range(max_row):
            for c in range(w):
                if not visited[r][c] and result[r][c] == value:
                    queue = deque([(r, c)])
                    visited[r][c] = True
                    component = []

                    while queue:
                        cr, cc = queue.popleft()
                        component.append((cr, cc))
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = cr + dr, cc + dc
                            if 0 <= nr < max_row and 0 <= nc < w and not visited[nr][nc]:
                                if result[nr][nc] == value:
                                    visited[nr][nc] = True
                                    queue.append((nr, nc))

                    if component:
                        components.append(component)
        return components

    # Helper function to compute normalized shape (relative positions from min coords)
    def normalize_shape(cells):
        if not cells:
            return []
        min_r = min(r for r, c in cells)
        min_c = min(c for r, c in cells)
        return sorted([(r - min_r, c - min_c) for r, c in cells])

    # Helper function to get all rotations and reflections of a shape
    def get_shape_variants(shape):
        """Generate all rotations and reflections of a normalized shape"""
        variants = set()
        variants.add(tuple(shape))  # Original

        # Rotations (90, 180, 270 degrees)
        for rotation in range(1, 4):
            rotated = []
            for r, c in shape:
                if rotation == 1:  # 90 degrees clockwise
                    rotated.append((c, -r))
                elif rotation == 2:  # 180 degrees
                    rotated.append((-r, -c))
                else:  # 270 degrees
                    rotated.append((-c, r))
            # Normalize after rotation
            if rotated:
                min_r = min(rr for rr, cc in rotated)
                min_c = min(cc for rr, cc in rotated)
                normalized = tuple(sorted([(rr - min_r, cc - min_c) for rr, cc in rotated]))
                variants.add(normalized)

        # Reflections (horizontal and vertical)
        for r, c in shape:
            # Horizontal flip
            h_flip = [(-r, c) for r, c in shape]
            if h_flip:
                min_r = min(rr for rr, cc in h_flip)
                min_c = min(cc for rr, cc in h_flip)
                normalized = tuple(sorted([(rr - min_r, cc - min_c) for rr, cc in h_flip]))
                variants.add(normalized)

            # Vertical flip
            v_flip = [(r, -c) for r, c in shape]
            if v_flip:
                min_r = min(rr for rr, cc in v_flip)
                min_c = min(cc for rr, cc in v_flip)
                normalized = tuple(sorted([(rr - min_r, cc - min_c) for rr, cc in v_flip]))
                variants.add(normalized)

        return variants

    # Helper function to compute shape similarity score
    def shape_similarity(shape1, shape2):
        """Compute similarity score between two normalized shapes (higher is better)"""
        if not shape1 or not shape2:
            return -1000  # Very low score

        # Size penalty
        size_diff = abs(len(shape1) - len(shape2))

        # Bounding box dimensions
        max_r1 = max(r for r, c in shape1)
        max_c1 = max(c for r, c in shape1)
        max_r2 = max(r for r, c in shape2)
        max_c2 = max(c for r, c in shape2)
        bbox_diff = abs(max_r1 - max_r2) + abs(max_c1 - max_c2)

        # Compute overlap - count matching cells when overlaid
        shape1_set = set(shape1)
        shape2_set = set(shape2)
        overlap = len(shape1_set & shape2_set)

        # Score: higher is better (more similar)
        # Exact match gets bonus
        exact_match_bonus = 10000 if shape1 == shape2 else 0
        score = overlap * 100 + exact_match_bonus - size_diff * 2 - bbox_diff
        return score

    # Get colored regions above divider only
    colored_regions = {}  # color -> list of (component, normalized_shape)
    for color in range(1, 10):
        if color != 3 and color != 5:
            components = find_components(color, max_row=divider_row)
            for comp in components:
                shape = normalize_shape(comp)
                if color not in colored_regions:
                    colored_regions[color] = []
                colored_regions[color].append((comp, shape))

    # Build column-to-color mapping from colored regions above
    # For each column, track which color occupies it
    col_to_color = {}
    for color, comp_list in colored_regions.items():
        for comp, _ in comp_list:
            for r, c in comp:
                col_to_color[c] = color

    # Get all 3-components (both above and below divider)
    threes_components = find_components(3)

    # Match each 3-component to a colored region
    for three_comp in threes_components:
        three_shape = normalize_shape(three_comp)
        three_variants = get_shape_variants(three_shape)

        # Priority 1: Try exact shape matching first (including rotations/reflections)
        best_color = None
        exact_match_found = False

        for color, comp_list in colored_regions.items():
            for comp, color_shape in comp_list:
                # Check if three_shape matches color_shape or any variant
                if three_shape == color_shape or tuple(color_shape) in three_variants:
                    best_color = color
                    exact_match_found = True
                    break
            if exact_match_found:
                break

        # Priority 2: If no exact match, use proximity-based matching
        if not exact_match_found:
            # For proximity, consider only cells below the divider
            if three_comp[0][0] > divider_row:  # Component is below divider
                # Find the colored region with the closest cell
                min_distance = float('inf')

                for tr, tc in three_comp:
                    for color, comp_list in colored_regions.items():
                        for colored_comp, _ in comp_list:
                            for cr, cc in colored_comp:
                                dist = abs(tr - cr) + abs(tc - cc)
                                if dist < min_distance:
                                    min_distance = dist
                                    best_color = color
            else:
                # Component is above divider - use shape similarity or column mapping
                color_counts = {}
                for r, c in three_comp:
                    if c in col_to_color:
                        col_color = col_to_color[c]
                        color_counts[col_color] = color_counts.get(col_color, 0) + 1

                if color_counts:
                    best_color = max(color_counts, key=color_counts.get)
                else:
                    # Use shape similarity for above-divider components
                    best_score = -float('inf')
                    for color, comp_list in colored_regions.items():
                        for comp, color_shape in comp_list:
                            # Simple similarity: count overlapping cells when normalized
                            overlap = len(set(three_shape) & set(color_shape))
                            score = overlap * 100 - abs(len(three_shape) - len(color_shape)) * 10
                            if score > best_score:
                                best_score = score
                                best_color = color

                    if best_color is None and colored_regions:
                        best_color = list(colored_regions.keys())[0]

        # Fill the 3-component with the matched color
        if best_color is not None:
            for r, c in three_comp:
                result[r][c] = best_color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("845d6e51", solve)
