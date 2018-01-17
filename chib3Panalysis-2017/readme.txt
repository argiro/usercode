
# for PES estimation using chic

python makeRooDataSet-s-refit.py -o ds-chic.root -t chic
python pesAnalysis-s.py

# for PES check (systematics) using chib1P
pesAnalysis-chib-dscb-kinfit.py

# for simultaneous fit to 3P:

1. create tree where the variable names are the same for the 1S,2S and 3S masses
   prunetree.py

2. crate a dataset with corrected photon scale:
   - makeRooDataSetVaryScale.py
   - makeRooDataSet2SVaryScale.py
   - makeRooDataSet3SVaryScale.py-

3. Fit with simultaneousfit3P-kinfit.py
