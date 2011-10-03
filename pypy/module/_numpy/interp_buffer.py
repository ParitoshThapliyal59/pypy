from pypy.interpreter.buffer import RWBuffer
from pypy.rpython.lltypesystem import lltype, rffi
from pypy.rlib.rstring import StringBuilder

CHAR_TP = lltype.Ptr(lltype.Array(lltype.Char, hints={'nolength': True}))

class NumpyBuffer(RWBuffer):
    def __init__(self, array):
        self.array = array

    def getlength(self):
        return self.array.get_concrete().find_size() * self.array.find_dtype().num_bytes

    def getitem_noboundcheck(self, index):
        storage = self.array.get_concrete().get_root_storage()
        char_data = rffi.cast(CHAR_TP, storage)
        index = self.calc_index(index)
        return char_data[index]

    def getitem(self, index):
        if index > self.getlength():
            raise IndexError("Index out of bounds (0<=index<=%d)" % self.getlength())
        return self.getitem_noboundcheck(index)

    def setitem_noboundcheck(self, index, value):
        storage = self.array.get_concrete().get_root_storage()
        char_ptr = rffi.cast(CHAR_TP, storage)
        index = self.calc_index(index)
        char_ptr[index] = value

    def setitem(self, index, value):
        if index > self.getlength():
            raise IndexError("Index out of bounds (0<=index<=%d)" % self.getlength())
        self.setitem_noboundcheck(index, value)

    def setslice(self, index, newstring):
        if index + len(newstring) > self.getlength():
            raise IndexError("End of slice to set out of bounds (0<=index<=%d)" % self.getlength())
        for idx in range(0, len(newstring)):
            self.setitem_noboundcheck(index + idx, newstring[idx])

    def getslice(self, start, stop, step, size):
        builder = StringBuilder(size)

        for index in range(start, stop, step):
            builder.append(self.getitem_noboundcheck(index))

        return builder.build()

    def calc_index(self, index):
        return index

class NumpyViewBuffer(NumpyBuffer):
    def calc_index(self, index):
        box_size = self.array.find_dtype().num_bytes
        # index is a byte-index, calculate the box-index from it
        box_index = index / box_size
        # and we need the byte-inside-box index, too.
        in_box_index = index % box_size
        # now we use calc_index to get the correct box_index
        offset_index = self.array.calc_index(box_index)
        return offset_index * box_size + in_box_index
