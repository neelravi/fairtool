# fairtool/archive.py

"""
Reads values from the NOMAD archives that `fair parse` writes (fair_parsed_*.json).

The results sit in NOMAD's legacy `run` section, in SI units. analyze.py and summarize.py
both use these helpers, so they report the same values.
"""

from typing import Optional

import numpy as np

from .parse import ELEMENTARY_CHARGE_VALUE


def get(node, *path):
    """Follows dict keys and list indices into parsed JSON; returns None if a step is missing."""
    for step in path:
        try:
            node = node[step]
        except (KeyError, IndexError, TypeError):
            return None
    return node


def band_gap_ev(calculation) -> Optional[float]:
    """
    Derives the band gap (eV) of a calculation from its eigenvalues.

    NOMAD 1.4 stores no band gap value for these runs, only the eigenvalues: `eigenvalues`,
    or `band_structure_electronic[].segment` for a band-structure run. As in NOMAD's VASP
    parser, a state is occupied when its occupation is at least 0.5. A band crossing the
    Fermi level makes the number of occupied states differ between k-points; that is a
    metal, with a gap of 0. Otherwise the gap is the lowest unoccupied minus the highest
    occupied energy over all k-points and spin channels.
    """
    try:
        blocks = get(calculation, "eigenvalues") or [
            segment
            for band_structure in get(calculation, "band_structure_electronic") or []
            for segment in get(band_structure, "segment") or []
        ]
        # Each block is shaped (spin channel, k-point, band); join them along the k-points
        energies = np.concatenate([np.asarray(block["energies"], dtype=float) for block in blocks], axis=1)
        occupations = np.concatenate([np.asarray(block["occupations"], dtype=float) for block in blocks], axis=1)
    except (KeyError, TypeError, ValueError):
        return None
    if energies.ndim != 3 or energies.shape != occupations.shape:
        return None

    occupied = occupations >= 0.5
    if occupied.all() or not occupied.any():
        return None
    n_occupied = occupied.sum(axis=2)  # per spin channel and k-point
    if (n_occupied != n_occupied[:, :1]).any():
        return 0.0
    gap = energies[~occupied].min() - energies[occupied].max()
    return max(float(gap), 0.0) / ELEMENTARY_CHARGE_VALUE
