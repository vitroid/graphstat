time analice 00080-last.gro -f voronoi_analysis[test.db] -O Ow -H Hw

sqlite (1st time)
real	5m38.104s
user	5m13.557s
sys	0m8.075s

sqlite (2nd time)
real	5m30.619s
user	5m19.017s
sys	0m6.296s

python dict(volatile)
real	4m35.892s
user	4m28.961s
sys	0m3.903s

Access to local MySQL is VERY slow...
It is more than 300 times slower than sqlite3. Ridiculous.
