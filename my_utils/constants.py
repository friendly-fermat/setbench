from .helpers import b
from pathlib import Path 


BASE_DIR = Path(__file__).resolve().parent.parent
PYTHON_DIR  = BASE_DIR / "venv" / "bin" / "python3"
TREVORS_TOOLS_DIR = Path("/home/sigmod26/repos/trevors-tools")
PLOT_PYTHON_DIR = TREVORS_TOOLS_DIR / "venv" / "bin" / "python3"
MICROBENCH_DIR = BASE_DIR / "microbench"
CMAKE_BUILD_DIR = BASE_DIR / ".experimental_cmake_builds"
TOOLS_DIR = BASE_DIR / "tools"
EXPERIMENTS_DIR = BASE_DIR / ".my_experiments"
PINNING = b(f"{TOOLS_DIR / 'get_pinning_cluster.sh'}").stdout.strip()
# PINNING = "18-35,90-107,36-53,108-125,54-71,126-143,0-17,72-89"
THREADS_PER_SOCKET = 2 * int(
    b('lscpu | grep "Core(s) per socket" | grep -E [0-9]+ -o').stdout.strip()
)
TOTAL_THREAD_COUNT = (
    2
    * int(b('lscpu | grep "Core(s) per socket" | grep -E [0-9]+ -o').stdout.strip())
    * int(b('lscpu | grep "Socket(s)" | grep -E [0-9]+ -o').stdout.strip())
)


USERNAME = b("whoami").stdout.strip()

# IMPORTANT: the directories must already exist.
PMEM_PREFIX = "sigmod26"

PMEM_DIRS = [
    Path(f"/mnt/pmem1_mount/{PMEM_PREFIX}/ralloc_playground"),
    Path(f"/mnt/pmem0_mount/{PMEM_PREFIX}/ralloc_playground"),
    Path(f"/mnt/pmem0_mount/{PMEM_PREFIX}/lvmlc_playground"),
    Path(f"/mnt/pmem1_mount/{PMEM_PREFIX}/lvmlc_playground"),
    Path(f"/mnt/pmem0_mount/{PMEM_PREFIX}/pmemobj_playground"),
    Path(f"/mnt/pmem1_mount/{PMEM_PREFIX}/pmemobj_playground"),
    Path(f"/mnt/pmem0_mount/{PMEM_PREFIX}/pactree_playground"),
    Path(f"/mnt/pmem1_mount/{PMEM_PREFIX}/pactree_playground"),
    Path(f"/mnt/pmem0_mount/{PMEM_PREFIX}/roart_playground"),
    Path(f"/mnt/pmem1_mount/{PMEM_PREFIX}/roart_playground"),
    Path(f"/mnt/pmem0_mount/{PMEM_PREFIX}/lbtree_playground"),
    Path(f"/mnt/pmem1_mount/{PMEM_PREFIX}/lbtree_playground"),
    Path(f"/mnt/pmem0_mount/{PMEM_PREFIX}/dptree_playground"),
    Path(f"/mnt/pmem1_mount/{PMEM_PREFIX}/dptree_playground"),
    Path(f"/mnt/pmem0_mount/{PMEM_PREFIX}/utree_playground"),
    Path(f"/mnt/pmem1_mount/{PMEM_PREFIX}/utree_playground"),
    Path(f"/mnt/pmem0_mount/{PMEM_PREFIX}/rntree_playground"),
    Path(f"/mnt/pmem1_mount/{PMEM_PREFIX}/rntree_playground"),
    Path(f"/mnt/pmem0_mount/{PMEM_PREFIX}/bztree_playground"),
    Path(f"/mnt/pmem1_mount/{PMEM_PREFIX}/bztree_playground"),
]