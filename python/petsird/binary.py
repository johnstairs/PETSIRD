# This file was generated by the "yardl" tool. DO NOT EDIT.

# pyright: reportUnusedClass=false
# pyright: reportUnusedImport=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false

import collections.abc
import io
import typing

import numpy as np
import numpy.typing as npt

from .types import *

from .protocols import *
from . import _binary
from . import yardl_types as yardl

class BinaryPETSIRDWriter(_binary.BinaryProtocolWriter, PETSIRDWriterBase):
    """Binary writer for the PETSIRD protocol.

    Definition of the stream of data
    """


    def __init__(self, stream: typing.Union[typing.BinaryIO, str]) -> None:
        PETSIRDWriterBase.__init__(self)
        _binary.BinaryProtocolWriter.__init__(self, stream, PETSIRDWriterBase.schema)

    def _write_header(self, value: Header) -> None:
        HeaderSerializer().write(self._stream, value)

    def _write_time_blocks(self, value: collections.abc.Iterable[TimeBlock]) -> None:
        _binary.StreamSerializer(_binary.UnionSerializer(TimeBlock, [(TimeBlock.EventTimeBlock, EventTimeBlockSerializer()), (TimeBlock.ExternalSignalTimeBlock, ExternalSignalTimeBlockSerializer()), (TimeBlock.BedMovementTimeBlock, BedMovementTimeBlockSerializer()), (TimeBlock.GantryMovementTimeBlock, GantryMovementTimeBlockSerializer())])).write(self._stream, value)


class BinaryPETSIRDReader(_binary.BinaryProtocolReader, PETSIRDReaderBase):
    """Binary writer for the PETSIRD protocol.

    Definition of the stream of data
    """


    def __init__(self, stream: typing.Union[io.BufferedReader, io.BytesIO, typing.BinaryIO, str]) -> None:
        PETSIRDReaderBase.__init__(self)
        _binary.BinaryProtocolReader.__init__(self, stream, PETSIRDReaderBase.schema)

    def _read_header(self) -> Header:
        return HeaderSerializer().read(self._stream)

    def _read_time_blocks(self) -> collections.abc.Iterable[TimeBlock]:
        return _binary.StreamSerializer(_binary.UnionSerializer(TimeBlock, [(TimeBlock.EventTimeBlock, EventTimeBlockSerializer()), (TimeBlock.ExternalSignalTimeBlock, ExternalSignalTimeBlockSerializer()), (TimeBlock.BedMovementTimeBlock, BedMovementTimeBlockSerializer()), (TimeBlock.GantryMovementTimeBlock, GantryMovementTimeBlockSerializer())])).read(self._stream)

class CoincidenceEventSerializer(_binary.RecordSerializer[CoincidenceEvent]):
    def __init__(self) -> None:
        super().__init__([("detector_ids", _binary.FixedVectorSerializer(_binary.uint32_serializer, 2)), ("tof_idx", _binary.uint32_serializer), ("energy_indices", _binary.FixedVectorSerializer(_binary.uint32_serializer, 2))])

    def write(self, stream: _binary.CodedOutputStream, value: CoincidenceEvent) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.detector_ids, value.tof_idx, value.energy_indices)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['detector_ids'], value['tof_idx'], value['energy_indices'])

    def read(self, stream: _binary.CodedInputStream) -> CoincidenceEvent:
        field_values = self._read(stream)
        return CoincidenceEvent(detector_ids=field_values[0], tof_idx=field_values[1], energy_indices=field_values[2])


class SolidVolumeSerializer(typing.Generic[Shape, Shape_NP], _binary.RecordSerializer[SolidVolume[Shape]]):
    def __init__(self, shape_serializer: _binary.TypeSerializer[Shape, Shape_NP]) -> None:
        super().__init__([("shape", shape_serializer), ("material_id", _binary.uint32_serializer)])

    def write(self, stream: _binary.CodedOutputStream, value: SolidVolume[Shape]) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.shape, value.material_id)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['shape'], value['material_id'])

    def read(self, stream: _binary.CodedInputStream) -> SolidVolume[Shape]:
        field_values = self._read(stream)
        return SolidVolume[Shape](shape=field_values[0], material_id=field_values[1])


class CoordinateSerializer(_binary.RecordSerializer[Coordinate]):
    def __init__(self) -> None:
        super().__init__([("c", _binary.FixedNDArraySerializer(_binary.float32_serializer, (3,)))])

    def write(self, stream: _binary.CodedOutputStream, value: Coordinate) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.c)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['c'])

    def read(self, stream: _binary.CodedInputStream) -> Coordinate:
        field_values = self._read(stream)
        return Coordinate(c=field_values[0])


class BoxShapeSerializer(_binary.RecordSerializer[BoxShape]):
    def __init__(self) -> None:
        super().__init__([("corners", _binary.FixedVectorSerializer(CoordinateSerializer(), 8))])

    def write(self, stream: _binary.CodedOutputStream, value: BoxShape) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.corners)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['corners'])

    def read(self, stream: _binary.CodedInputStream) -> BoxShape:
        field_values = self._read(stream)
        return BoxShape(corners=field_values[0])


class AnnulusShapeSerializer(_binary.RecordSerializer[AnnulusShape]):
    def __init__(self) -> None:
        super().__init__([("inner_radius", _binary.float32_serializer), ("outer_radius", _binary.float32_serializer), ("thickness", _binary.float32_serializer), ("angular_range", _binary.FixedVectorSerializer(_binary.float32_serializer, 2))])

    def write(self, stream: _binary.CodedOutputStream, value: AnnulusShape) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.inner_radius, value.outer_radius, value.thickness, value.angular_range)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['inner_radius'], value['outer_radius'], value['thickness'], value['angular_range'])

    def read(self, stream: _binary.CodedInputStream) -> AnnulusShape:
        field_values = self._read(stream)
        return AnnulusShape(inner_radius=field_values[0], outer_radius=field_values[1], thickness=field_values[2], angular_range=field_values[3])


class RigidTransformationSerializer(_binary.RecordSerializer[RigidTransformation]):
    def __init__(self) -> None:
        super().__init__([("matrix", _binary.FixedNDArraySerializer(_binary.float32_serializer, (3, 4,)))])

    def write(self, stream: _binary.CodedOutputStream, value: RigidTransformation) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.matrix)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['matrix'])

    def read(self, stream: _binary.CodedInputStream) -> RigidTransformation:
        field_values = self._read(stream)
        return RigidTransformation(matrix=field_values[0])


class ReplicatedObjectSerializer(typing.Generic[T, T_NP], _binary.RecordSerializer[ReplicatedObject[T]]):
    def __init__(self, t_serializer: _binary.TypeSerializer[T, T_NP]) -> None:
        super().__init__([("object", t_serializer), ("transforms", _binary.VectorSerializer(RigidTransformationSerializer())), ("ids", _binary.VectorSerializer(_binary.uint32_serializer))])

    def write(self, stream: _binary.CodedOutputStream, value: ReplicatedObject[T]) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.object, value.transforms, value.ids)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['object'], value['transforms'], value['ids'])

    def read(self, stream: _binary.CodedInputStream) -> ReplicatedObject[T]:
        field_values = self._read(stream)
        return ReplicatedObject[T](object=field_values[0], transforms=field_values[1], ids=field_values[2])


class DetectorModuleSerializer(_binary.RecordSerializer[DetectorModule]):
    def __init__(self) -> None:
        super().__init__([("detecting_elements", _binary.VectorSerializer(ReplicatedObjectSerializer(SolidVolumeSerializer(BoxShapeSerializer())))), ("detecting_element_ids", _binary.VectorSerializer(_binary.uint32_serializer)), ("non_detecting_elements", _binary.VectorSerializer(ReplicatedObjectSerializer(SolidVolumeSerializer(_binary.UnionSerializer(GeometricShape, [(GeometricShape.BoxShape, BoxShapeSerializer()), (GeometricShape.AnnulusShape, AnnulusShapeSerializer())])))))])

    def write(self, stream: _binary.CodedOutputStream, value: DetectorModule) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.detecting_elements, value.detecting_element_ids, value.non_detecting_elements)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['detecting_elements'], value['detecting_element_ids'], value['non_detecting_elements'])

    def read(self, stream: _binary.CodedInputStream) -> DetectorModule:
        field_values = self._read(stream)
        return DetectorModule(detecting_elements=field_values[0], detecting_element_ids=field_values[1], non_detecting_elements=field_values[2])


class ScannerGeometrySerializer(_binary.RecordSerializer[ScannerGeometry]):
    def __init__(self) -> None:
        super().__init__([("replicated_modules", _binary.VectorSerializer(ReplicatedObjectSerializer(DetectorModuleSerializer()))), ("ids", _binary.VectorSerializer(_binary.uint32_serializer)), ("non_detecting_volumes", _binary.OptionalSerializer(_binary.VectorSerializer(SolidVolumeSerializer(_binary.UnionSerializer(GeometricShape, [(GeometricShape.BoxShape, BoxShapeSerializer()), (GeometricShape.AnnulusShape, AnnulusShapeSerializer())])))))])

    def write(self, stream: _binary.CodedOutputStream, value: ScannerGeometry) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.replicated_modules, value.ids, value.non_detecting_volumes)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['replicated_modules'], value['ids'], value['non_detecting_volumes'])

    def read(self, stream: _binary.CodedInputStream) -> ScannerGeometry:
        field_values = self._read(stream)
        return ScannerGeometry(replicated_modules=field_values[0], ids=field_values[1], non_detecting_volumes=field_values[2])


class SubjectSerializer(_binary.RecordSerializer[Subject]):
    def __init__(self) -> None:
        super().__init__([("name", _binary.OptionalSerializer(_binary.string_serializer)), ("id", _binary.string_serializer)])

    def write(self, stream: _binary.CodedOutputStream, value: Subject) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.name, value.id)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['name'], value['id'])

    def read(self, stream: _binary.CodedInputStream) -> Subject:
        field_values = self._read(stream)
        return Subject(name=field_values[0], id=field_values[1])


class InstitutionSerializer(_binary.RecordSerializer[Institution]):
    def __init__(self) -> None:
        super().__init__([("name", _binary.string_serializer), ("address", _binary.string_serializer)])

    def write(self, stream: _binary.CodedOutputStream, value: Institution) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.name, value.address)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['name'], value['address'])

    def read(self, stream: _binary.CodedInputStream) -> Institution:
        field_values = self._read(stream)
        return Institution(name=field_values[0], address=field_values[1])


class ExamInformationSerializer(_binary.RecordSerializer[ExamInformation]):
    def __init__(self) -> None:
        super().__init__([("subject", SubjectSerializer()), ("institution", InstitutionSerializer()), ("protocol", _binary.OptionalSerializer(_binary.string_serializer)), ("start_of_acquisition", _binary.OptionalSerializer(_binary.datetime_serializer))])

    def write(self, stream: _binary.CodedOutputStream, value: ExamInformation) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.subject, value.institution, value.protocol, value.start_of_acquisition)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['subject'], value['institution'], value['protocol'], value['start_of_acquisition'])

    def read(self, stream: _binary.CodedInputStream) -> ExamInformation:
        field_values = self._read(stream)
        return ExamInformation(subject=field_values[0], institution=field_values[1], protocol=field_values[2], start_of_acquisition=field_values[3])


class DirectionSerializer(_binary.RecordSerializer[Direction]):
    def __init__(self) -> None:
        super().__init__([("c", _binary.FixedNDArraySerializer(_binary.float32_serializer, (3,)))])

    def write(self, stream: _binary.CodedOutputStream, value: Direction) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.c)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['c'])

    def read(self, stream: _binary.CodedInputStream) -> Direction:
        field_values = self._read(stream)
        return Direction(c=field_values[0])


class DirectionMatrixSerializer(_binary.RecordSerializer[DirectionMatrix]):
    def __init__(self) -> None:
        super().__init__([("matrix", _binary.FixedNDArraySerializer(_binary.float32_serializer, (3, 3,)))])

    def write(self, stream: _binary.CodedOutputStream, value: DirectionMatrix) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.matrix)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['matrix'])

    def read(self, stream: _binary.CodedInputStream) -> DirectionMatrix:
        field_values = self._read(stream)
        return DirectionMatrix(matrix=field_values[0])


class AtomSerializer(_binary.RecordSerializer[Atom]):
    def __init__(self) -> None:
        super().__init__([("mass_number", _binary.uint32_serializer), ("atomic_number", _binary.uint32_serializer)])

    def write(self, stream: _binary.CodedOutputStream, value: Atom) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.mass_number, value.atomic_number)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['mass_number'], value['atomic_number'])

    def read(self, stream: _binary.CodedInputStream) -> Atom:
        field_values = self._read(stream)
        return Atom(mass_number=field_values[0], atomic_number=field_values[1])


class BulkMaterialSerializer(_binary.RecordSerializer[BulkMaterial]):
    def __init__(self) -> None:
        super().__init__([("id", _binary.uint32_serializer), ("name", _binary.string_serializer), ("density", _binary.float32_serializer), ("atoms", _binary.VectorSerializer(AtomSerializer())), ("mass_fractions", _binary.VectorSerializer(_binary.float32_serializer))])

    def write(self, stream: _binary.CodedOutputStream, value: BulkMaterial) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.id, value.name, value.density, value.atoms, value.mass_fractions)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['id'], value['name'], value['density'], value['atoms'], value['mass_fractions'])

    def read(self, stream: _binary.CodedInputStream) -> BulkMaterial:
        field_values = self._read(stream)
        return BulkMaterial(id=field_values[0], name=field_values[1], density=field_values[2], atoms=field_values[3], mass_fractions=field_values[4])


class ScannerInformationSerializer(_binary.RecordSerializer[ScannerInformation]):
    def __init__(self) -> None:
        super().__init__([("model_name", _binary.string_serializer), ("scanner_geometry", ScannerGeometrySerializer()), ("bulk_materials", _binary.VectorSerializer(BulkMaterialSerializer())), ("gantry_alignment", _binary.OptionalSerializer(RigidTransformationSerializer())), ("tof_bin_edges", _binary.NDArraySerializer(_binary.float32_serializer, 1)), ("tof_resolution", _binary.float32_serializer), ("energy_bin_edges", _binary.NDArraySerializer(_binary.float32_serializer, 1)), ("energy_resolution_at_511", _binary.float32_serializer), ("event_time_block_duration", _binary.uint32_serializer), ("coincidence_policy", _binary.EnumSerializer(_binary.int32_serializer, CoincidencePolicy))])

    def write(self, stream: _binary.CodedOutputStream, value: ScannerInformation) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.model_name, value.scanner_geometry, value.bulk_materials, value.gantry_alignment, value.tof_bin_edges, value.tof_resolution, value.energy_bin_edges, value.energy_resolution_at_511, value.event_time_block_duration, value.coincidence_policy)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['model_name'], value['scanner_geometry'], value['bulk_materials'], value['gantry_alignment'], value['tof_bin_edges'], value['tof_resolution'], value['energy_bin_edges'], value['energy_resolution_at_511'], value['event_time_block_duration'], value['coincidence_policy'])

    def read(self, stream: _binary.CodedInputStream) -> ScannerInformation:
        field_values = self._read(stream)
        return ScannerInformation(model_name=field_values[0], scanner_geometry=field_values[1], bulk_materials=field_values[2], gantry_alignment=field_values[3], tof_bin_edges=field_values[4], tof_resolution=field_values[5], energy_bin_edges=field_values[6], energy_resolution_at_511=field_values[7], event_time_block_duration=field_values[8], coincidence_policy=field_values[9])


class HeaderSerializer(_binary.RecordSerializer[Header]):
    def __init__(self) -> None:
        super().__init__([("scanner", ScannerInformationSerializer()), ("exam", _binary.OptionalSerializer(ExamInformationSerializer()))])

    def write(self, stream: _binary.CodedOutputStream, value: Header) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.scanner, value.exam)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['scanner'], value['exam'])

    def read(self, stream: _binary.CodedInputStream) -> Header:
        field_values = self._read(stream)
        return Header(scanner=field_values[0], exam=field_values[1])


class TripleEventSerializer(_binary.RecordSerializer[TripleEvent]):
    def __init__(self) -> None:
        super().__init__([("detector_ids", _binary.FixedVectorSerializer(_binary.uint32_serializer, 3)), ("tof_indices", _binary.FixedVectorSerializer(_binary.uint32_serializer, 2)), ("energy_indices", _binary.FixedVectorSerializer(_binary.uint32_serializer, 3))])

    def write(self, stream: _binary.CodedOutputStream, value: TripleEvent) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.detector_ids, value.tof_indices, value.energy_indices)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['detector_ids'], value['tof_indices'], value['energy_indices'])

    def read(self, stream: _binary.CodedInputStream) -> TripleEvent:
        field_values = self._read(stream)
        return TripleEvent(detector_ids=field_values[0], tof_indices=field_values[1], energy_indices=field_values[2])


class EventTimeBlockSerializer(_binary.RecordSerializer[EventTimeBlock]):
    def __init__(self) -> None:
        super().__init__([("start", _binary.uint32_serializer), ("prompt_events", _binary.VectorSerializer(CoincidenceEventSerializer())), ("delayed_events", _binary.OptionalSerializer(_binary.VectorSerializer(CoincidenceEventSerializer()))), ("triple_events", _binary.OptionalSerializer(_binary.VectorSerializer(TripleEventSerializer())))])

    def write(self, stream: _binary.CodedOutputStream, value: EventTimeBlock) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.start, value.prompt_events, value.delayed_events, value.triple_events)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['start'], value['prompt_events'], value['delayed_events'], value['triple_events'])

    def read(self, stream: _binary.CodedInputStream) -> EventTimeBlock:
        field_values = self._read(stream)
        return EventTimeBlock(start=field_values[0], prompt_events=field_values[1], delayed_events=field_values[2], triple_events=field_values[3])


class ExternalSignalTimeBlockSerializer(_binary.RecordSerializer[ExternalSignalTimeBlock]):
    def __init__(self) -> None:
        super().__init__([("start", _binary.uint32_serializer), ("signal_id", _binary.uint32_serializer), ("signal_values", _binary.VectorSerializer(_binary.float32_serializer))])

    def write(self, stream: _binary.CodedOutputStream, value: ExternalSignalTimeBlock) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.start, value.signal_id, value.signal_values)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['start'], value['signal_id'], value['signal_values'])

    def read(self, stream: _binary.CodedInputStream) -> ExternalSignalTimeBlock:
        field_values = self._read(stream)
        return ExternalSignalTimeBlock(start=field_values[0], signal_id=field_values[1], signal_values=field_values[2])


class BedMovementTimeBlockSerializer(_binary.RecordSerializer[BedMovementTimeBlock]):
    def __init__(self) -> None:
        super().__init__([("start", _binary.uint32_serializer), ("transform", RigidTransformationSerializer())])

    def write(self, stream: _binary.CodedOutputStream, value: BedMovementTimeBlock) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.start, value.transform)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['start'], value['transform'])

    def read(self, stream: _binary.CodedInputStream) -> BedMovementTimeBlock:
        field_values = self._read(stream)
        return BedMovementTimeBlock(start=field_values[0], transform=field_values[1])


class GantryMovementTimeBlockSerializer(_binary.RecordSerializer[GantryMovementTimeBlock]):
    def __init__(self) -> None:
        super().__init__([("start", _binary.uint32_serializer), ("transform", RigidTransformationSerializer())])

    def write(self, stream: _binary.CodedOutputStream, value: GantryMovementTimeBlock) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.start, value.transform)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['start'], value['transform'])

    def read(self, stream: _binary.CodedInputStream) -> GantryMovementTimeBlock:
        field_values = self._read(stream)
        return GantryMovementTimeBlock(start=field_values[0], transform=field_values[1])


class ExternalSignalTypeSerializer(_binary.RecordSerializer[ExternalSignalType]):
    def __init__(self) -> None:
        super().__init__([("type", _binary.EnumSerializer(_binary.int32_serializer, ExternalSignalTypeEnum)), ("description", _binary.string_serializer), ("id", _binary.uint32_serializer)])

    def write(self, stream: _binary.CodedOutputStream, value: ExternalSignalType) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.type, value.description, value.id)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['type'], value['description'], value['id'])

    def read(self, stream: _binary.CodedInputStream) -> ExternalSignalType:
        field_values = self._read(stream)
        return ExternalSignalType(type=field_values[0], description=field_values[1], id=field_values[2])


class TimeIntervalSerializer(_binary.RecordSerializer[TimeInterval]):
    def __init__(self) -> None:
        super().__init__([("start", _binary.uint32_serializer), ("stop", _binary.uint32_serializer)])

    def write(self, stream: _binary.CodedOutputStream, value: TimeInterval) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.start, value.stop)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['start'], value['stop'])

    def read(self, stream: _binary.CodedInputStream) -> TimeInterval:
        field_values = self._read(stream)
        return TimeInterval(start=field_values[0], stop=field_values[1])


class TimeFrameInformationSerializer(_binary.RecordSerializer[TimeFrameInformation]):
    def __init__(self) -> None:
        super().__init__([("time_frames", _binary.VectorSerializer(TimeIntervalSerializer()))])

    def write(self, stream: _binary.CodedOutputStream, value: TimeFrameInformation) -> None:
        if isinstance(value, np.void):
            self.write_numpy(stream, value)
            return
        self._write(stream, value.time_frames)

    def write_numpy(self, stream: _binary.CodedOutputStream, value: np.void) -> None:
        self._write(stream, value['time_frames'])

    def read(self, stream: _binary.CodedInputStream) -> TimeFrameInformation:
        field_values = self._read(stream)
        return TimeFrameInformation(time_frames=field_values[0])


