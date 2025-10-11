# Consistent Hashing Implementation

## Overview
An implementation of consistent hashing algorithm that provides stable data distribution across a dynamic set of nodes.

## Implementation Details

### Hash Space
- Search space size: 2^30
- Hashing algorithm: SHA-256
- Hash calculation: `hash_value % SEARCH_SPACE`

### Key Components
1. **Node**
   - Unique identifier
   - Position in hash ring (determined by hash function)

2. **ConsistentHashRing**
   - Maintains sorted list of nodes
   - Caches key-to-node mappings
   - Handles node addition and removal
   - Manages key redistribution

### Key Operations
1. **Key Assignment**
   - Hash the key to get position
   - Find next node in clockwise direction
   - Cache the mapping for future lookups

2. **Node Management**
   - Addition: Insert node and redistribute affected keys
   - Removal: Remove node and reassign its keys
   - Collision detection for node positions

## Usage Notes
- Initialize ring with a list of nodes
- Use `get_node(key)` for key-to-node mapping
- Handle node changes via `add_node()` and `remove_node()`
- Expect exceptions for hash collisions and empty rings