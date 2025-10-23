# PACTree (SOSP AE)

* I copied the code over from the original SOSP'21 AE repository. 
* I think the previous ones (that I ran into correctness / infinite loop problems with) were from the PiBench repositories (or maybe not, I started this one from scratch)
* This one kind of just worked out of the box. No correctness issues, no infinte loops, no nothing. 
* I added rangeQuery(lo,hi) to the APIs -- previously it only supported scan(start,length) signatures
* I added linearizability to both rangeQuery(lo,hi) and scan(start,length) APIs in new functions (rangeQueryThenUnlockAll, scanThenUnlockAll). The performance results make sense
* Everything looks good with PACTree. 
* I had to run ./tools/get-numa-config.sh, which updated the include/numa-config.h file. This should be very important performance-wise in favour of PACTree. 
* With high thread counts (72,95), the worker thread fails at a exit(1) defined in the code. Worth looking at. Look up "done?" in the codebase to find it. 