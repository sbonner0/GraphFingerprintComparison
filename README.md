# Graph Fingerprint Comparison Code -
A repository for the graph finger print comparison code, written in Python using the Graph-Tool pacakge. The paper entiteld Efficient Comparison of Massive Graphs Through The Use Of ‘Graph Fingerprints’ which this is the code for can be found here - http://www.mlgworkshop.org/2016/

This code can be used to compare two graph based upon their fingerprint.

## Requirements

This code has been tested on Python 2.7.5+ and requires the following packages to function correctly:
* numpy 
* scipy
* graph-tool

## Usage

To replicate the results found in the paper, please run the *EXP.py* scripts. Custom graphs can be compared by editing the *GFP.py* with the location of any two graphs which you would like to be compared.

## Cite

Please cite the associated papers for this work if you use this code:

```
@inproceedings{bonner2016efficient,
  title={Efficient Comparison of Massive Graphs Through The Use Of ‘Graph Fingerprints’},
  author={Bonner, Stephen and Brennan, John and Kureshi, Ibad and Stephen, McGough and Theodoropoulos, Georgios},
  booktitle={SIGKKD 12th International Workshop on Mining and Learning with Graphs (MLG)},
  year={2016}
}
```
