#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the MLZ
# Copyright (c) 2009-2018 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Nikhil Biyani <nikhil.biyani@psi.ch>
#
# *****************************************************************************

import numpy

try:
    import flatbuffers
    from nicos_ess.devices.datasinks.imagesink.fbschema import \
        EventHistogram, Array, ArrayUInt, ArrayDouble, DimensionMetaData
except ImportError:
    flatbuffers = None
    EventHistogram = None
    Array = None
    ArrayUInt = None
    ArrayDouble = None
    DimensionMetaData = None


class HistogramFlatbuffersSerializer(object):
    """ Encode the histogram using the flatbuffers schema hs00
    """

    file_identifier = "hs00"
    uint32_bytes = flatbuffers.number_types.Uint32Flags.bytewidth

    def _encodeMetadata(self, b, desc):
        # Serialize the metadatas for each dimensions
        dims = []
        for d in range(len(desc.shape)):
            pos_bin = 0
            if hasattr(desc, 'dimbins'):
                bins = desc.dimbins[d]
                # Write only if the number of bins = length + 1
                if len(bins) == desc.shape[d] + 1:
                    ArrayDouble.ArrayDoubleStartValueVector(b, len(bins))
                    # Prepend the bins
                    for bin in bins[::-1]:
                        b.PrependFloat64(bin)
                    pos_val = b.EndVector(len(bins))
                    ArrayDouble.ArrayDoubleStart(b)
                    ArrayDouble.ArrayDoubleAddValue(b, pos_val)
                    pos_bin = ArrayDouble.ArrayDoubleEnd(b)

            pos_unit = 0
            if hasattr(desc, 'dimunits'):
                pos_unit = b.CreateString(desc.dimunits[d])

            pos_label = b.CreateString(desc.dimnames[d])

            DimensionMetaData.DimensionMetaDataStart(b)
            DimensionMetaData.DimensionMetaDataAddLength(b, desc.shape[d])
            DimensionMetaData.DimensionMetaDataAddLabel(b, pos_label)
            if pos_unit:
                DimensionMetaData.DimensionMetaDataAddUnit(b, pos_unit)
            if pos_bin:
                DimensionMetaData.DimensionMetaDataAddBinBoundariesType(
                    b, Array.Array.ArrayDouble)
                DimensionMetaData.DimensionMetaDataAddBinBoundaries(b, pos_bin)
            dims.append(DimensionMetaData.DimensionMetaDataEnd(b))
        return dims

    def _encodeArray(self, builder, array, l_elements):
        # Serialize the data array
        ArrayUInt.ArrayUIntStartValueVector(builder, l_elements)
        if type(array) == bytearray:
            # Directly copy the bytes array
            l_bytes = l_elements * self.uint32_bytes  # Number of bytes in hist
            # Recalculate the head position of the buffer
            head = flatbuffers.number_types.UOffsetTFlags.py_type(
                builder.Head() - l_bytes)
            builder.head = head
            # Copy the bytes from histogram bytearray
            builder.Bytes[head:head + l_bytes] = array[0:l_bytes]
        else:
            array = array[:l_elements]
            for val in array[::-1]:
                builder.PrependUint32(val)
        pos_val = builder.EndVector(l_elements)
        ArrayUInt.ArrayUIntStart(builder)
        ArrayUInt.ArrayUIntAddValue(builder, pos_val)
        return ArrayUInt.ArrayUIntEnd(builder)

    def encode(self, timestamp_ns, arraydesc, array, source, metadata_ts=0,
               infostr=''):
        """Serialize using provided argument
        :param timestamp_ns: timestamp in ns
        :param arraydesc: array desc object of the associated image array
        :param array: the data array (can be in bytes or uint32)
        :param source: source name string
        :param metadata_ts: timestamp when last metadata was dumped
                        (if 0, metadata is dumped with this message)
        :param infostr: additional information
        :return: encoded bytes
        """
        rank = len(arraydesc.shape)
        builder = flatbuffers.Builder(16)

        pos_source = builder.CreateString(source)

        pos_metadata = 0
        if metadata_ts == 0:
            metadata = self._encodeMetadata(builder, arraydesc)
            EventHistogram.EventHistogramStartDimMetadataVector(builder, rank)
            for dim in metadata[::-1]:
                builder.PrependUOffsetTRelative(dim)
            pos_metadata = builder.EndVector(rank)
            metadata_ts = timestamp_ns

        EventHistogram.EventHistogramStartCurrentShapeVector(builder, rank)
        for s in arraydesc.shape[::-1]:
            builder.PrependUint32(s)
        pos_shape = builder.EndVector(rank)

        EventHistogram.EventHistogramStartOffsetVector(builder, rank)
        for iloop in [0] * rank:
            builder.PrependUint32(iloop)
        pos_offset = builder.EndVector(rank)

        pos_data = self._encodeArray(builder, array,
                                     numpy.prod(arraydesc.shape))

        pos_info = builder.CreateString(infostr)

        # BUILD THE BUFFER
        EventHistogram.EventHistogramStart(builder)
        EventHistogram.EventHistogramAddSource(builder, pos_source)
        EventHistogram.EventHistogramAddTimestamp(builder, timestamp_ns)
        if pos_metadata:
            EventHistogram.EventHistogramAddDimMetadata(builder, pos_metadata)
        EventHistogram.EventHistogramAddLastMetadataTimestamp(builder,
                                                              metadata_ts)
        EventHistogram.EventHistogramAddCurrentShape(builder, pos_shape)
        EventHistogram.EventHistogramAddOffset(builder, pos_offset)
        EventHistogram.EventHistogramAddDataType(builder,
                                                 Array.Array.ArrayUInt)
        EventHistogram.EventHistogramAddData(builder, pos_data)
        EventHistogram.EventHistogramAddInfo(builder, pos_info)
        hist = EventHistogram.EventHistogramEnd(builder)
        builder.Finish(hist)

        # Generate the output and replace the file_identifier
        buff = builder.Output()
        buff[4:8] = bytes(self.file_identifier)
        return bytes(buff)