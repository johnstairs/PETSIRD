#  Copyright (C) 2022-2023 Microsoft Corporation
#  Copyright (C) 2023-2024 University College London
#
#  SPDX-License-Identifier: Apache-2.0

import sys
import math
import random
import numpy
import numpy.typing as npt
from collections.abc import Iterator
import petsird

# these are constants for now
NUMBER_OF_ENERGY_BINS = 3
NUMBER_OF_TOF_BINS = 300
RADIUS = 400
CRYSTAL_LENGTH = (4, 4, 20)
# num crystals in a module
NUM_CRYSTALS_PER_MODULE = (5, 6, 2)
NUM_MODULES = 20
NUMBER_OF_TIME_BLOCKS = 6
NUMBER_OF_EVENTS = 1000
COUNT_RATE = 500


def make_coordinate(v: tuple) -> petsird.Coordinate:
    return petsird.Coordinate(c=numpy.array(v, dtype=numpy.float32))


def get_crystal() -> petsird.SolidVolume:
    """return a cuboid volume"""
    crystal_shape = petsird.BoxShape(
        corners=[
            make_coordinate((0, 0, 0)),
            make_coordinate((0, 0, CRYSTAL_LENGTH[2])),
            make_coordinate((0, CRYSTAL_LENGTH[1], CRYSTAL_LENGTH[2])),
            make_coordinate((0, CRYSTAL_LENGTH[1], 0)),
            make_coordinate((CRYSTAL_LENGTH[0], 0, 0)),
            make_coordinate((CRYSTAL_LENGTH[0], 0, CRYSTAL_LENGTH[2])),
            make_coordinate((CRYSTAL_LENGTH[0], CRYSTAL_LENGTH[1], CRYSTAL_LENGTH[2])),
            make_coordinate((CRYSTAL_LENGTH[0], CRYSTAL_LENGTH[1], 0)),
        ]
    )
    return petsird.BoxSolidVolume(shape=crystal_shape, material_id=1)


def get_detector_module() -> petsird.DetectorModule:
    """return a module of NUM_CRYSTALS_PER_MODULE cuboids"""
    crystal = get_crystal()
    rep_volume = petsird.ReplicatedBoxSolidVolume(object=crystal)
    N0 = NUM_CRYSTALS_PER_MODULE[0]
    N1 = NUM_CRYSTALS_PER_MODULE[1]
    N2 = NUM_CRYSTALS_PER_MODULE[2]
    for rep0 in range(N0):
        for rep1 in range(N1):
            for rep2 in range(N2):
                transform = petsird.RigidTransformation(
                    matrix=numpy.array(
                        (
                            (1.0, 0.0, 0.0, RADIUS + rep0 * CRYSTAL_LENGTH[0]),
                            (0.0, 1.0, 0.0, rep1 * CRYSTAL_LENGTH[1]),
                            (0.0, 0.0, 1.0, rep2 * CRYSTAL_LENGTH[2]),
                        ),
                        dtype="float32",
                    )
                )
                rep_volume.transforms.append(transform)
                rep_volume.ids.append(rep0 + N0 * (rep1 + N1 * rep2))

    return petsird.DetectorModule(
        detecting_elements=[rep_volume], detecting_element_ids=[0]
    )


def get_scanner_geometry() -> petsird.ScannerGeometry:
    """return a scanner build by rotating a module around the (0,0,1) axis"""
    detector_module = get_detector_module()
    radius = RADIUS
    angles = [2 * math.pi * i / NUM_MODULES for i in range(NUM_MODULES)]

    rep_module = petsird.ReplicatedDetectorModule(object=detector_module)
    module_id = 0
    for angle in angles:
        transform = petsird.RigidTransformation(
            matrix=numpy.array(
                (
                    (math.cos(angle), math.sin(angle), 0.0, 0.0),
                    (-math.sin(angle), math.cos(angle), 0.0, 0.0),
                    (0.0, 0.0, 1.0, 0.0),
                ),
                dtype="float32",
            )
        )
        rep_module.ids.append(module_id)
        module_id += 1
        rep_module.transforms.append(transform)

    return petsird.ScannerGeometry(replicated_modules=[rep_module], ids=[0])


def get_scanner_info() -> petsird.ScannerInformation:

    scanner_geometry = get_scanner_geometry()

    # TODO scanner_info.bulk_materials

    # TOF info (in mm)
    tofBinEdges = numpy.linspace(
        -RADIUS, RADIUS, NUMBER_OF_TOF_BINS + 1, dtype="float32"
    )
    energyBinEdges = numpy.linspace(
        430, 650, NUMBER_OF_ENERGY_BINS + 1, dtype="float32"
    )
    return petsird.ScannerInformation(
        model_name="PETSIRD_TEST",
        scanner_geometry=scanner_geometry,
        tof_bin_edges=tofBinEdges,
        tof_resolution=9.4,  # in mm
        energy_bin_edges=energyBinEdges,
        energy_resolution_at_511=0.11,  # as fraction of 511
        event_time_block_duration=1,  # ms
    )


def get_header() -> petsird.Header:
    subject = petsird.Subject(id="123456")
    institution = petsird.Institution(
        name="Diamond Light Source",
        address="Harwell Science and Innovation Campus, Didcot, Oxfordshire, OX11 0DE, UK",
    )
    return petsird.Header(
        exam=petsird.ExamInformation(subject=subject, institution=institution),
        scanner=get_scanner_info(),
    )


def get_events(
    header: petsird.Header, num_events: int
) -> Iterator[petsird.CoincidenceEvent]:
    detector_count = 5  # TODO header.scanner.number_of_detectors()
    for _ in range(num_events):
        yield petsird.CoincidenceEvent(
            detector_ids=[
                random.randrange(0, detector_count),
                random.randrange(0, detector_count),
            ],
            energy_indices=[
                random.randrange(0, NUMBER_OF_ENERGY_BINS),
                random.randrange(0, NUMBER_OF_ENERGY_BINS),
            ],
            tof_idx=random.randrange(0, NUMBER_OF_TOF_BINS),
        )


if __name__ == "__main__":
    # numpy random number generator
    rng = numpy.random.default_rng()

    with petsird.BinaryPETSIRDWriter(sys.stdout.buffer) as writer:
        # with petsird.NDJsonPETSIRDWriter(sys.stdout) as writer:
        header = get_header()
        writer.write_header(header)
        for t in range(NUMBER_OF_TIME_BLOCKS):
            start = t * header.scanner.event_time_block_duration
            num_prompts_this_block = rng.poisson(COUNT_RATE)
            prompts_this_block = list(get_events(header, num_prompts_this_block))
            # Normally we'd write multiple blocks, but here we have just one, so let's write a tuple with just one element
            writer.write_time_blocks(
                (
                    petsird.TimeBlock.EventTimeBlock(
                        petsird.EventTimeBlock(
                            start=start, prompt_events=prompts_this_block
                        )
                    ),
                )
            )
