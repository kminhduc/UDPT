Python 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> import hashlib
... 
... M = 7
... 
... class ChordNode:
...     def __init__(self, node_id):
...         self.id = node_id
...         self.finger = {i: None for i in range(1, M + 1)}
...         self.successor = self
...         self.predecessor = None
...         self.keys = {}
... 
...     def __repr__(self):
...         return f"Node({self.id})"
... 
...     def find_successor(self, key_id):
...         print(f"[{self}] Đang tìm successor cho ID {key_id}...")
...         if self._is_in_range(key_id, self.id, self.successor.id):
...             print(f" -> Successor là {self.successor}")
...             return self.successor
...         else:
...             preceding_node = self.closest_preceding_finger(key_id)
...             print(f" -> Chuyển tiếp yêu cầu đến {preceding_node}")
...             return preceding_node.find_successor(key_id)
... 
...     def closest_preceding_finger(self, key_id):
...         for i in range(M, 0, -1):
...             finger_node = self.finger[i]
...             if self._is_in_range(finger_node.id, self.id, key_id):
...                 return finger_node
...         return self
... 
...     def _is_in_range(self, key_id, start_id, end_id):
...         if start_id < end_id:
...             return start_id < key_id <= end_id
...         else:
...             return start_id < key_id or key_id <= end_id
... 
...     def update_finger_table(self, ring):
...         print(f"Cập nhật bảng ngón tay cho {self}...")
...         for i in range(1, M + 1):
...             start_id = (self.id + 2**(i - 1)) % (2**M)
...             self.finger[i] = ring.find_node_successor(start_id)
...         
...         print(f"Bảng ngón tay của {self}:")
        for i, finger_node in self.finger.items():
            start_id = (self.id + 2**(i - 1)) % (2**M)
            print(f"  i={i}, start={start_id} -> {finger_node}")


class ChordRing:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id):
        if node_id in self.nodes:
            print(f"Lỗi: Node ID {node_id} đã tồn tại.")
            return
        
        new_node = ChordNode(node_id)
        self.nodes[node_id] = new_node
        
        sorted_ids = sorted(self.nodes.keys())
        
        for i, current_id in enumerate(sorted_ids):
            successor_id = sorted_ids[(i + 1) % len(sorted_ids)]
            predecessor_id = sorted_ids[(i - 1 + len(sorted_ids)) % len(sorted_ids)]
            
            self.nodes[current_id].successor = self.nodes[successor_id]
            self.nodes[current_id].predecessor = self.nodes[predecessor_id]
            
        print(f"Đã thêm {new_node}. Toàn bộ mạng được cập nhật.")
        
    def update_all_finger_tables(self):
        print("\n--- BẮT ĐẦU CẬP NHẬT TẤT CẢ BẢNG NGÓN TAY ---")
        for node_id in self.nodes:
            self.nodes[node_id].update_finger_table(self)
        print("--- KẾT THÚC CẬP NHẬT BẢNG NGÓN TAY ---\n")

    def find_node_successor(self, key_id):
        sorted_ids = sorted(self.nodes.keys())
        for node_id in sorted_ids:
            if node_id >= key_id:
                return self.nodes[node_id]
        # Nếu không tìm thấy (vòng lại)
        return self.nodes[sorted_ids[0]]
        
def get_hash(key_string):
    sha1 = hashlib.sha1(key_string.encode()).hexdigest()
