
# This script runs point operations for the paper. 
# I'm not using the pre-created cmake variations because I want this to be standalone (and reproducible in the future).

#! /usr/bin/python3

import dis
from os import environ
import pathlib, sys
from my_utils.types import (
    CMakeVariation,
    Config,
    Metric,
    ThreadCount,
    Variation,
    Workload,
    MakeVariation,
)
import my_utils.metrics as metrics
from my_utils.utils import Experiment
import copy
from my_utils import constants



art_v_nolog = CMakeVariation(
    label="art-v-nolog",
    ds_name="04-artifact",
    target="Variation2",
    cmake_args=[
        "-Dds_name=04-artifact",
        "-DART_VARIATION=Variation2",
        "-DALLOCATOR=RALLOC_NUMA",
        "-DCMAKE_BUILD_TYPE=Release",
    ],
    has_libpapi=1,
    millis=8000,
    huge_pages=False,
    prefill_count=0,
    pin_kwargs=dict(socket_ordering=[1, 0], prefer_hyperthreads=True),
    numa_kwargs=dict(mode="func", socket_ordering=[1, 0], prefer_hyperthreads=True),
    distribution="zipf-ycsb",
    prefill_mode="-prefill-insert",
    alpha=0.99,
    perf=False,
    txn=False,
    environ={
    },
)

art_v_2log = CMakeVariation(
    label="art-v-2log",
    ds_name="04-artifact",
    target="Variation5",
    cmake_args=[
        "-Dds_name=04-artifact",
        "-DART_VARIATION=Variation5",
        "-DALLOCATOR=RALLOC_NUMA",
        "-DCMAKE_BUILD_TYPE=Release",
    ],
    has_libpapi=1,
    millis=8000,
    huge_pages=False,
    prefill_count=0,
    pin_kwargs=dict(socket_ordering=[1, 0], prefer_hyperthreads=True),
    numa_kwargs=dict(mode="func", socket_ordering=[1, 0], prefer_hyperthreads=True),
    distribution="zipf-ycsb",
    prefill_mode="-prefill-insert",
    alpha=0.99,
    perf=False,
    txn=False,
    environ={
    },
)


pactree = CMakeVariation(
    label="pactree",
    ds_name="21-pactree-sosp",
    target="Setbench",
    cmake_args=["-Dds_name=21-pactree-sosp", "-DCMAKE_BUILD_TYPE=Release"],
    has_libpapi=1,
    millis=8000,
    huge_pages=False,
    prefill_count=0,
    pin_kwargs=dict(socket_ordering=[1, 0], prefer_hyperthreads=True),
    numa_kwargs=dict(mode="func", socket_ordering=[1, 0], prefer_hyperthreads=True),
    distribution="zipf-ycsb",
    prefill_mode="-prefill-insert",
    alpha=0.99,
    perf=False,
    txn=False,
    environ={
        "PACTREE_SOCKET0_ROOT": f"/mnt/pmem0_mount/{constants.PMEM_PREFIX}/pactree_playground",
        "PACTREE_SOCKET1_ROOT": f"/mnt/pmem1_mount/{constants.PMEM_PREFIX}/pactree_playground",
    },
).with_additional_compile_def("PREFER_SOCKET0")

pactree_ralloc = pactree.replace(
    label="pactree-ralloc",
).with_allocator("RALLOC")

pactree_ralloc_linrq = pactree_ralloc.with_additional_compile_def("PACTree_Linearizable_RangeQuery").replace(
    label="pactree-ralloc-linrq",
)

# For resuming 
def already_done(sparsity, distribution, workload): 
    return False 


def main(description="BWTreeExperiment", skip_compilation=False):
    this_script = pathlib.Path(__file__).parent.resolve() / __file__


    base_variations = [
        art_v_nolog, 
        art_v_2log,
        pactree_ralloc,
        pactree_ralloc_linrq,
    ]

    workloads = [
        ("ReadHeavy", Workload(i=2.5, d=2.5)),
        ("ReadMostly", Workload(i=5, d=5)),
        ("Balanced", Workload(i=25, d=25)),
        ("WriteMostly", Workload(i=45, d=45)),
        ("WriteHeavy", Workload(i=47.5, d=47.5)),
    ]

    distributions = [
        ("Uniform", "uniform", 0.85),
        ("Zipf-99", "zipf-ycsb", 0.99),
    ]

    sparsities = [
        ("Dense", False),
        # ("Sparse", True), 
    ]


    retries = 1
    millis = 30000
    universe_size = 100_000_000
    universe_millions = universe_size // 1_000_000
    prefill_count = 30_000_000
    universe_coefficient = (universe_size) / (prefill_count)
    
    thread_counts = [
        ThreadCount(
            nprefill=48,
            nwork=36,
            nrq=12,
            rqsize=rqsize
        ) for rqsize in [
            int(sel * universe_size) for sel in [
                0.0001, 0.00025, 0.0005, 0.001, 0.005, 0.01
            ]
        ]
    ]

    for sparsity_str, is_sparse in sparsities: 
        for workload_str, workload in workloads: 
            for distribution_str, distribution, alpha in distributions: 
                if already_done(sparsity_str, distribution_str, workload_str):
                    print(f"Skipping {sparsity_str}-{distribution_str}-{workload_str} because already done")
                    continue

                experiment_description = f"RangeQuery-{distribution_str}-{workload_str}-{sparsity_str}-{universe_millions}Muniverse"

                variations = [copy.deepcopy(v) for v in base_variations]
                actual_variations = []
                for v in variations:
                    actual_variations.append(
                        v.replace(
                            prefill_count=prefill_count,
                            universe_coefficient=universe_coefficient,
                            millis=millis,
                            distribution=distribution,
                            alpha=alpha,
                            additional_run_args="-sparse" if is_sparse else "",
                        )
                    )
                config = Config(
                    description=experiment_description,
                    workloads=(workload,), # separating experiment per workload is cleaner
                    variations=actual_variations,
                    metrics=[
                        metrics.throughput,
                        metrics.update_throughput,
                        metrics.find_throughput,
                        metrics.l3_misses, 
                        metrics.rq_throughput,
                        metrics.total_rq, 
                        metrics.ptr_chases, 
                        metrics.ptr_chases_per_rq
                    ],
                    thread_counts=thread_counts,
                    retries=retries,
                )

                exp = Experiment(
                    config,
                    script_path=this_script,
                )
                exp.run(skip_compilation=skip_compilation)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        skip_compilation = False
        if len(sys.argv) == 3:
            skip_compilation = sys.argv[2].lower() in ["y", "yes", "true", "1"]

        main(description=sys.argv[1], skip_compilation=skip_compilation)
    else:
        main()
