# fireflyd -- The firefly reverse engineering effort

fireflyd is my attempt at creating a program that locally caches Firefly data, and allows you to submit/mark as done etc. your Firefly tasks from a HTTP API

# Features:

- [x] task retrieval
- [x] task marking
- [ ] file submission

# Problems

file submission -- requires RE of [**vendor.93fe217cd90803c037ba.min.js**](https://github.com/Cvdcamilleri/fireflyd/blob/master/firefly_assets/vendor.93fe217cd90803c037ba.min.js)
to find where folder IDs are generated/found
