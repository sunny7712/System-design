import hashlib

SEARCH_SPACE = 2 ** 30

def hash_fn(key: str) -> int:
    return int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16) % SEARCH_SPACE

class Node:
    def __init__(self, identifier: str):
        self.identifier = identifier
        self.position = hash_fn(identifier)

    def __repr__(self):
        return f"Node({self.identifier})"
    

class ConsistentHashRing:
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes
        self.ring = []
        self.key_hash_to_node = {}
        self._build_ring()

    def _build_ring(self):
        self.ring = sorted(self.nodes, key=lambda node: node.position)
        
    def _rearrange_ring(self):
        self.ring.sort(key=lambda node: node.position)
        
    def _get_next_node(self, position: int) -> Node:
        for node in self.ring:
            if position <= node.position:
                return node
        return self.ring[0]  # Wrap around to the first node

    
    def get_node(self, key: str) -> Node:
        key_position = hash_fn(key)
        if key_position in self.key_hash_to_node:
            return self.key_hash_to_node[key_position] 
        
        if not self.ring:
            raise Exception("No nodes in the ring")
        
        if key_position in {node.position for node in self.ring}:
            raise Exception("Hash collision detected")
    
        node = self._get_next_node(key_position)
        self.key_hash_to_node[key_position] = node
        return node
    
    def add_node(self, node: Node):
        if node.position in {n.position for n in self.ring}:
            raise Exception("Hash collision detected")        
        self.ring.append(node)
        self._rearrange_ring()

        # Reassign all cached keys using _get_next_node
        for key_position in list(self.key_hash_to_node.keys()):
            self.key_hash_to_node[key_position] = self._get_next_node(key_position)
            
    def remove_node(self, node: Node):
        self.ring = [n for n in self.ring if n.position != node.position]
        
        if not self.ring:
            self.key_hash_to_node.clear()  # Clear cache if no nodes left
            return
            
        self._rearrange_ring()
        
        # Reassign all cached keys using _get_next_node
        for key_position in list(self.key_hash_to_node.keys()):
            self.key_hash_to_node[key_position] = self._get_next_node(key_position)