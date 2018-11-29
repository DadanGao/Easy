
class BoundedFlow:
    def __init__(self,bound_dir):
        self.bound_RFS_index_list = bound_dir["bound_RFS_index_list"]
        self.actions = bound_dir["actions"]
        self.postcondition = bound_dir["postcondition"]