#! /bin/bash

prefix="sigmod26"

parent_pmem_directories=(
    "/mnt/pmem0_mount/$prefix"
    "/mnt/pmem1_mount/$prefix"
)

child_directories=(
    "mimalloc_playground"
    "ralloc_playground"
    "lvmlc_playground"
    "pmemobj_playground"
    "pactree_playground"
    "lbtree_playground"
    "dptree_playground"
    "roart_playground"
    "bztree_playground"
    "utree_playground"
)

for parent_dir in "${parent_pmem_directories[@]}"; do
    for child_dir in "${child_directories[@]}"; do
        full_path="$parent_dir/$child_dir"
        if [ -d "$full_path" ]; then
            echo "Cleaning directory: $full_path"
            rm -rf "$full_path"/*
        else
            echo "Directory does not exist: $full_path"
            mkdir -p "$full_path"
        fi
    done
done


mkdir -p ./.experimental_cmake_builds
mkdir -p ./.my_experiments