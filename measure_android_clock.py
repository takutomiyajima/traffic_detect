#!/usr/bin/env python3
"""Bracket Android wall-clock reads with host times; stdlib only, no clock writes."""
import argparse
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


def sample(serial):
    before_ns = time.time_ns()
    mono_before_ns = time.monotonic_ns()
    proc = subprocess.run(
        ['adb', '-s', serial, 'shell', 'date', '+%s.%N'],
        capture_output=True, text=True, timeout=10, check=True,
    )
    mono_after_ns = time.monotonic_ns()
    after_ns = time.time_ns()
    raw = proc.stdout.strip()
    match = re.fullmatch(r'(\d{10,})\.(\d{1,9})', raw)
    if not match:
        raise ValueError('Android date did not return epoch seconds with fractional digits: ' + repr(raw))
    whole, fraction = match.groups()
    device_ns = int(whole) * 10**9 + int(fraction.ljust(9, '0'))
    # Decimal output is truncated. This is printed granularity, not oscillator accuracy.
    quantum_ns = 10 ** (9 - len(fraction))
    return {
        'host_before_epoch_ns': before_ns, 'host_after_epoch_ns': after_ns,
        'host_elapsed_monotonic_ns': mono_after_ns - mono_before_ns,
        'device_epoch_ns': device_ns, 'device_raw': raw,
        'printed_quantum_ns': quantum_ns,
    }


def summarize(samples, expected, jump_tolerance_ns=50_000_000):
    intervals = []
    reasons = []
    for row in samples:
        if 'error' in row:
            reasons.append('device_query_failed')
            continue
        before = row['host_before_epoch_ns']
        after = row['host_after_epoch_ns']
        elapsed = row['host_elapsed_monotonic_ns']
        if after < before or elapsed < 0 or abs((after - before) - elapsed) > jump_tolerance_ns:
            reasons.append('host_wall_clock_discontinuity')
            continue
        device = row['device_epoch_ns']
        intervals.append((before - device - row['printed_quantum_ns'], after - device))
    if len(samples) != expected or len(intervals) != expected:
        reasons.append('incomplete_measurement_batch')
    lower = max((i[0] for i in intervals), default=None)
    upper = min((i[1] for i in intervals), default=None)
    if lower is not None and upper < lower:
        reasons.append('no_constant_offset_fits_measurement_batch')
    ok = not reasons and lower is not None
    return {
        'status': 'measured_under_batch_assumptions' if ok else 'unknown',
        'offset_direction': 'host_time = device_time + offset',
        'offset_lower_s': lower / 10**9 if ok else None,
        'offset_upper_s': upper / 10**9 if ok else None,
        'offset_midpoint_s': (lower + upper) / (2 * 10**9) if ok else None,
        'batch_half_width_s': (upper - lower) / (2 * 10**9) if ok else None,
        'reasons': sorted(set(reasons)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serial', required=True)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--samples', default=5, type=int, choices=range(1, 21))
    args = parser.parse_args()
    if args.out.exists():
        parser.error('output exists; use a new trial or phase filename')
    rows = []
    for _ in range(args.samples):
        try:
            rows.append(sample(args.serial))
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            rows.append({'error': type(exc).__name__, 'detail': str(exc)})
            break
    result = {
        'schema_version': '1.0', 'serial': args.serial,
        'recorded_utc': datetime.now(timezone.utc).isoformat(),
        'method': 'host wall-clock brackets around adb shell date +%s.%N',
        'expected_samples': args.samples, 'samples': rows,
        'summary': summarize(rows, args.samples),
        'limitations': [
            'Assumes host and device clocks do not step within a query or measurement batch',
            'Printed fractional digits do not prove physical clock precision',
            'Bounds describe this batch; they do not bound drift throughout a capture',
            'Measure before and after capture; inspect disagreements before alignment',
            'UI operation timing uncertainty must be measured separately',
            'No accuracy relative to external UTC is established',
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'saved': str(args.out), **result['summary']}, ensure_ascii=False))
    return 0 if result['summary']['status'] != 'unknown' else 2


if __name__ == '__main__':
    raise SystemExit(main())
