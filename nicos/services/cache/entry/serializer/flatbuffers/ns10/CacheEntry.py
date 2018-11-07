# automatically generated by the FlatBuffers compiler, do not modify

# namespace: 

from __future__ import absolute_import, division, print_function

import flatbuffers


# /// pylint: skip-file
class CacheEntry(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsCacheEntry(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = CacheEntry()
        x.Init(buf, n + offset)
        return x

    # CacheEntry
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # CacheEntry
    def Key(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return ""

    # CacheEntry
    def Time(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float64Flags, o + self._tab.Pos)
        return 0.0

    # CacheEntry
    def Ttl(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float64Flags, o + self._tab.Pos)
        return 0.0

    # CacheEntry
    def Expired(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

    # CacheEntry
    def Value(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return ""

def CacheEntryStart(builder): builder.StartObject(5)
def CacheEntryAddKey(builder, key): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(key), 0)
def CacheEntryAddTime(builder, time): builder.PrependFloat64Slot(1, time, 0.0)
def CacheEntryAddTtl(builder, ttl): builder.PrependFloat64Slot(2, ttl, 0.0)
def CacheEntryAddExpired(builder, expired): builder.PrependBoolSlot(3, expired, 0)
def CacheEntryAddValue(builder, value): builder.PrependUOffsetTRelativeSlot(4, flatbuffers.number_types.UOffsetTFlags.py_type(value), 0)
def CacheEntryEnd(builder): return builder.EndObject()
