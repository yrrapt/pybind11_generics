
import pyg_test
from pyg_test import get_list, ListHolder

class ChildList(pyg_test.TestList):
    def __init__(self, vec1, vec2):
        pyg_test.TestList.__init__(self, vec1)
        self._list2 = vec2

    def get_data(self):
        return self._list2

    def get_data_base(self):
        return pyg_test.TestList.get_data(self)


if __name__ == '__main__':
    vec1 = [1, 2, 3, 4]
    vec2 = [5, 6, 7]

    obj = ChildList(vec1, vec2)

    assert obj.get_data() == vec2
    assert obj.get_data_base() == vec1
    assert get_list(obj) == vec1

    holder = ListHolder(obj)
    obj_ref = holder.get_obj_ref()
    obj_ptr = holder.get_obj_ptr()
    assert obj_ref is obj
    assert obj_ptr is obj
    assert isinstance(obj_ref, ChildList)

    print('holder print before delete')
    print(holder.get_data())
    print('delete in python')
    del obj_ref
    del obj_ptr
    del obj
    print('delete in python done')
    print('holder print after delete')
    print(holder.get_data())
