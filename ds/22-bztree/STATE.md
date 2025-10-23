# BzTree 

* CMakeLists.txt is good and stable. 
* There's an example.cpp that showcases the setup of the data structure, which is also implemented in adapter.h 
* BzTree always segfaults as soon as I have insert+delete operations with higher than 0.2 Zipfian skew. The insert-only prefill works fine, but as soon as the main portion of experiment starts, the DS crashes. 
* There's no problems with uniform workloads. 
* The tree stats is probably incorrect as get very far off checksums. I stopped working on it as soon as I realized the DS doesn't play well with zipfian workloads. 
* I debugged the zipfian workloads. There's assertion errors. Possibly concurrency issues.
