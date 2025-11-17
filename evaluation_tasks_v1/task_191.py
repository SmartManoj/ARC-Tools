import os
from arc_tools.grid import Grid
from arc_tools import logger
from helper import solve_task

def solve(grid: Grid):
    '''
    Replace interior pixels of nested rectangles with their containing rectangle's color.
    Each rectangle border (outline made of one color) has its interior colored pixels
    replaced with the border color. Additionally, rectangle borders that are contained
    within other rectangles are replaced with the containing rectangle's color.
    '''
    result = Grid([row[:] for row in grid])
    h, w = result.height, result.width

    # Find connected components for each color
    def get_connected_components(color):
        """Get all connected components of a color using flood fill"""
        visited = [[False] * w for _ in range(h)]
        components = []

        def flood_fill(start_r, start_c):
            stack = [(start_r, start_c)]
            component = []
            while stack:
                r, c = stack.pop()
                if r < 0 or r >= h or c < 0 or c >= w:
                    continue
                if visited[r][c] or result[r][c] != color:
                    continue
                visited[r][c] = True
                component.append((r, c))
                stack.extend([(r+1, c), (r-1, c), (r, c+1), (r, c-1)])
            return component

        for r in range(h):
            for c in range(w):
                if result[r][c] == color and not visited[r][c]:
                    component = flood_fill(r, c)
                    if len(component) > 0:
                        components.append(component)

        return components

    # Find all rectangle borders from connected components
    rectangles = []
    colors_found = set()

    for r in range(h):
        for c in range(w):
            if result[r][c] != 0:
                colors_found.add(result[r][c])

    for color in colors_found:
        components = get_connected_components(color)

        for pixels in components:
            if len(pixels) < 4:  # Need at least 4 pixels for a rectangle border
                continue

            min_r = min(p[0] for p in pixels)
            max_r = max(p[0] for p in pixels)
            min_c = min(p[1] for p in pixels)
            max_c = max(p[1] for p in pixels)

            # Check if all pixels are on the border of the bounding box
            is_border = all(p[0] == min_r or p[0] == max_r or p[1] == min_c or p[1] == max_c
                           for p in pixels)

            # Also check that the rectangle has a non-zero interior
            if is_border and (max_r > min_r and max_c > min_c):
                rectangles.append({
                    'color': color,
                    'min_r': min_r,
                    'max_r': max_r,
                    'min_c': min_c,
                    'max_c': max_c,
                    'area': (max_r - min_r) * (max_c - min_c),
                    'pixels': set(pixels)
                })

    # Helper function to check containment
    def contains_rectangle(outer, inner):
        """Check if outer rectangle completely contains inner rectangle"""
        return (outer['min_r'] <= inner['min_r'] and
                outer['max_r'] >= inner['max_r'] and
                outer['min_c'] <= inner['min_c'] and
                outer['max_c'] >= inner['max_c'])

    # Identify which rectangles are nested inside others
    nested_map = {}  # maps rectangle index to containing rectangle index
    for i, rect in enumerate(rectangles):
        containing_idx = None
        containing_area = float('inf')
        for j, outer_rect in enumerate(rectangles):
            if i != j and contains_rectangle(outer_rect, rect):
                # This rectangle is contained in outer_rect
                if outer_rect['area'] < containing_area:
                    containing_idx = j
                    containing_area = outer_rect['area']
        nested_map[i] = containing_idx

    # Process rectangles from outer to inner
    # For each rectangle, replace all interior pixels with the rectangle color
    # Then, if the rectangle is nested, replace everything with the containing rectangle color
    for i, rect in enumerate(rectangles):
        color = rect['color']
        min_r, max_r = rect['min_r'], rect['max_r']
        min_c, max_c = rect['min_c'], rect['max_c']

        # First, check if this rectangle is nested
        containing_idx = nested_map[i]
        if containing_idx is not None:
            # This rectangle is inside another rectangle
            # Replace ALL pixels (border and interior) with the containing rectangle's color
            containing_color = rectangles[containing_idx]['color']
            for r in range(min_r, max_r + 1):
                for c in range(min_c, max_c + 1):
                    if result[r][c] != 0:  # Don't replace 0s
                        result[r][c] = containing_color
        else:
            # This rectangle is not nested (it's outermost)
            # Replace interior pixels with the rectangle color
            for r in range(min_r + 1, max_r):
                for c in range(min_c + 1, max_c):
                    if result[r][c] != 0:
                        result[r][c] = color

    return result

if __name__ == "__main__":
    os.environ['initial_file'] = os.path.splitext(os.path.basename(__file__))[0]
    solve_task("7d1f7ee8", solve)
