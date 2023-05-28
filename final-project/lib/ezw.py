import numpy as np

# create a EZW tree class
class EZWTree:
    def __init__(self, value, level, quadrant, coordinates, children, parent):
        self.value = value
        self.level = level
        self.children = children if children is not None else []
        self.quadrant = quadrant
        self.coordinates = coordinates
        self.ezwcode = None
        self.parent = parent if parent is not None else None
    
def build_tree(image, level=0, coordinates=(1,0), quadrant=None, parent=None):
    i, j = coordinates
    # Base case: if the coordinates are out of the image boundary, return None
    if i >= image.shape[0] or j >= image.shape[1]:
        return None

    # create the list of children coordinates / quadrant 2,1,3,4
    child_coordinates = [(2*i, 2*j), (2*i, 2*j+1), (2*i + 1, 2*j), (2*i + 1, 2*j + 1)]

    node = EZWTree(image[i, j], level, quadrant, coordinates, children=[], parent=parent)

    # recursively create the children
    for coord in child_coordinates:
        ci, cj = coord
        # Check if the child coordinates are within the image boundary
        if ci < image.shape[0] and cj < image.shape[1]:
            child = build_tree(image, level+1, coord, quadrant, parent=node)
            node.children.append(child)

    return node

def dfs_set_value(node):
    # base case: if node is None, return False
    if node is None:
        return False

    # first process the children
    children_significant = [dfs_set_value(child) for child in node.children]

    # process the current node
    if np.abs(node.value) != 0:
        node.ezwcode = 'P' #Positive or negative non-zero
        return True
    else:
        # does code have significant descendant?
        if any(children_significant):
            node.ezwcode = 'Z' #Isolated zero
            return True
        else:
            node.ezwcode = 'T' #ZTR
            return False
        
def bfs_encode_list(root):
    # use BFS to traverse the tree
    queue = root.children.copy()
    dominant_pass_result = []
    while queue:
        node = queue.pop(0)
        # check ezwcode
        # check if the node is significant
        if node.ezwcode == 'P':
            dominant_pass_result.append(int(node.value))
        elif node.ezwcode == 'Z':
            dominant_pass_result.append(int(node.value))
        elif node.ezwcode == 'T':
            dominant_pass_result.append(node.ezwcode)
            continue
        # add the children to the queue
        if node.children:
            queue.extend(node.children)
    return dominant_pass_result

def transverse_encode(root):
    # use DFS to traverse the tree and set the ezwcode
    dfs_set_value(root)
    # use BFS to export the dominant_pass_result
    dominant_pass_result = bfs_encode_list(root)
    return dominant_pass_result

def enc_dp_sp(root_nodes_list):
    dpr_list = [[None for _ in range(16)] for _ in range(16)]
    for i in range(0, 16):
        for j in range(0, 16):
            dpr_list[i][j] = transverse_encode(root_nodes_list[i][j])
            # print('coor', root_nodes_list[i][j].coordinates, 'done')
    return dpr_list

# decode
def decode_tree(root, dominant_pass, recon_img):
    # print('------')
    # print('threshold:', threshold )
    # print(root.coordinates)
    # print(dominant_pass)
    # print(subdominant_pass)
    queue = root.children.copy()
    idx = 0
    
    while queue:
        node = queue.pop(0)
        ezwcode = dominant_pass[idx]
        i, j = node.coordinates
        if ezwcode != "T":
            recon_img[i, j] = ezwcode
            idx += 1
            # print(idx, node.coordinates, node.value)
        elif ezwcode == 'T': # ZTR
            idx += 1
            # print('T')
            continue
        if node.children:
            queue.extend(node.children)
    return

def dec_dp_sp(dpr_list, recon_root_nodes, recon_img):
    for i in range(0, 16):
        for j in range(0, 16):
            decode_tree(recon_root_nodes[i][j], dpr_list[i][j], recon_img)
    return recon_img