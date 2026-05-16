Benchmarks

oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: gemma-4-31b-4bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128         18902.7       92.62    54.2 tok/s    10.9 tok/s      30.665    37.6 tok/s    17.79 GB
pp4096/tg128         79347.0      103.16    51.6 tok/s     9.8 tok/s      92.449    45.7 tok/s    19.30 GB
pp8192/tg128        172109.6      136.46    47.6 tok/s     7.4 tok/s     189.440    43.9 tok/s    19.61 GB
pp16384/tg128       341264.8      227.67    48.0 tok/s     4.4 tok/s     370.179    44.6 tok/s    20.45 GB
pp32768/tg128       805753.8      312.80    40.7 tok/s     3.2 tok/s     845.480    38.9 tok/s    22.79 GB
pp65536/tg128      3103968.9     1240.68    21.1 tok/s     0.8 tok/s    3261.536    20.1 tok/s    27.57 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          10.9 tok/s     1.00x    54.2 tok/s    54.2 tok/s     18902.7      30.665
2x           2.6 tok/s     0.24x    15.9 tok/s     8.0 tok/s    128345.9     226.232
4x           4.0 tok/s     0.37x    36.5 tok/s     9.1 tok/s     83401.3     241.672

 ===
 
 gemma-4-26b-it-bf16:
 
 "Model 'gemma-4-26b-a4b-it-bf16' (50.47GB) exceeds max-model-memory (50.40GB)"
 
- Model has been deleted from drive
 
 ===
 
 oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: Qwen3.5-35B-A3B-4bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128          4866.8       27.63   210.4 tok/s    36.5 tok/s       8.375   137.5 tok/s    19.25 GB
pp4096/tg128         16352.3       29.72   250.5 tok/s    33.9 tok/s      20.127   209.9 tok/s    20.03 GB
pp8192/tg128         33991.4       34.00   241.0 tok/s    29.6 tok/s      38.310   217.2 tok/s    20.38 GB
pp16384/tg128        80526.5       42.55   203.5 tok/s    23.7 tok/s      85.931   192.2 tok/s    21.00 GB
pp32768/tg128       206183.3       62.60   158.9 tok/s    16.1 tok/s     214.133   153.6 tok/s    22.34 GB
pp65536/tg128       483950.9      102.14   135.4 tok/s     9.9 tok/s     496.922   132.1 tok/s    25.02 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          36.5 tok/s     1.00x   210.4 tok/s   210.4 tok/s      4866.8       8.375
2x          33.2 tok/s     0.91x   149.8 tok/s    74.9 tok/s     13451.6      21.394
4x          40.5 tok/s     1.11x   152.8 tok/s    38.2 tok/s     26127.6      39.454

===

oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: DeepSeek-R1-Distill-Qwen-32B-MLX-4Bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128         21598.4       84.33    47.5 tok/s    12.0 tok/s      32.308    35.7 tok/s    17.89 GB
pp4096/tg128         54762.9      101.31    74.8 tok/s     9.9 tok/s      67.629    62.5 tok/s    19.03 GB
pp8192/tg128        127907.7      119.99    64.1 tok/s     8.4 tok/s     143.147    58.1 tok/s    19.92 GB
pp16384/tg128       349728.2      163.98    46.9 tok/s     6.1 tok/s     370.554    44.6 tok/s    21.89 GB
pp32768/tg128       802248.2      261.10    40.8 tok/s     3.9 tok/s     835.408    39.4 tok/s    25.93 GB
pp65536/tg128      1980231.7      369.36    33.1 tok/s     2.7 tok/s    2027.140    32.4 tok/s    34.04 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          12.0 tok/s     1.00x    47.5 tok/s    47.5 tok/s     21598.4      32.308
2x           9.1 tok/s     0.76x    49.5 tok/s    24.8 tok/s     41122.7      69.478
4x           9.7 tok/s     0.81x    91.5 tok/s    22.9 tok/s     33284.0      97.789

===

oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: Mistral-Small-3.2-24B-Instruct-2506-MLX-4bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128         19738.5       86.03    51.9 tok/s    11.7 tok/s      30.664    37.6 tok/s    13.14 GB
pp4096/tg128         76398.4       99.76    53.6 tok/s    10.1 tok/s      89.067    47.4 tok/s    13.92 GB
pp8192/tg128        155942.5      107.11    52.5 tok/s     9.4 tok/s     169.546    49.1 tok/s    14.57 GB
pp16384/tg128       281552.9      104.11    58.2 tok/s     9.7 tok/s     294.775    56.0 tok/s    15.69 GB
pp32768/tg128       573946.1      141.24    57.1 tok/s     7.1 tok/s     591.884    55.6 tok/s    18.25 GB
pp65536/tg128      1349190.3      192.96    48.6 tok/s     5.2 tok/s    1373.696    47.8 tok/s    23.31 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          11.7 tok/s     1.00x    51.9 tok/s    51.9 tok/s     19738.5      30.664
2x          15.4 tok/s     1.32x    64.1 tok/s    32.0 tok/s     31790.4      48.523
4x          16.1 tok/s     1.38x   125.0 tok/s    31.3 tok/s     24391.1      64.496

===

oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: Qwen3.5-27B-4bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128         15438.0       64.70    66.3 tok/s    15.6 tok/s      23.654    48.7 tok/s    15.85 GB
pp4096/tg128         62316.7       69.28    65.7 tok/s    14.5 tok/s      71.115    59.4 tok/s    17.27 GB
pp8192/tg128        127765.3       89.10    64.1 tok/s    11.3 tok/s     139.081    59.8 tok/s    17.90 GB
pp16384/tg128       286215.3      108.98    57.2 tok/s     9.2 tok/s     300.056    55.0 tok/s    19.15 GB
pp32768/tg128       603035.0      125.89    54.3 tok/s     8.0 tok/s     619.023    53.1 tok/s    21.65 GB
pp65536/tg128      1309074.5      164.96    50.1 tok/s     6.1 tok/s    1330.025    49.4 tok/s    26.68 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          15.6 tok/s     1.00x    66.3 tok/s    66.3 tok/s     15438.0      23.654
2x          13.7 tok/s     0.88x    58.9 tok/s    29.4 tok/s     34544.6      53.449
4x          15.1 tok/s     0.97x    55.4 tok/s    13.8 tok/s     73187.3     107.907

===

oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: gemma-4-26B-A4B-it-MLX-4bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128          3015.1       21.61   339.6 tok/s    46.6 tok/s       5.760   200.0 tok/s    14.24 GB
pp4096/tg128         11367.8       23.13   360.3 tok/s    43.6 tok/s      14.306   295.3 tok/s    14.69 GB
pp8192/tg128         22244.4       28.39   368.3 tok/s    35.5 tok/s      25.850   321.9 tok/s    14.79 GB
pp16384/tg128        45563.0       38.21   359.6 tok/s    26.4 tok/s      50.416   327.5 tok/s    15.19 GB
pp32768/tg128        97794.6       55.78   335.1 tok/s    18.1 tok/s     104.878   313.7 tok/s    15.97 GB
pp65536/tg128       235561.9       95.68   278.2 tok/s    10.5 tok/s     247.714   265.1 tok/s    17.66 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          46.6 tok/s     1.00x   339.6 tok/s   339.6 tok/s      3015.1       5.760
2x          59.5 tok/s     1.28x   298.2 tok/s   149.1 tok/s      6666.7      11.170
4x          68.2 tok/s     1.46x   333.3 tok/s    83.3 tok/s     11631.4      19.796

===

oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: gemma-4-26b-a4b-4bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128          3063.0       20.46   334.6 tok/s    49.3 tok/s       5.662   203.7 tok/s    13.98 GB
pp4096/tg128         11334.5       23.60   361.5 tok/s    42.7 tok/s      14.332   294.8 tok/s    14.40 GB
pp8192/tg128         22683.6       26.34   361.2 tok/s    38.3 tok/s      26.029   319.7 tok/s    14.54 GB
pp16384/tg128        46325.9       35.81   353.7 tok/s    28.1 tok/s      50.874   324.6 tok/s    14.94 GB
pp32768/tg128        99201.7       55.37   330.3 tok/s    18.2 tok/s     106.233   309.7 tok/s    15.71 GB
pp65536/tg128       240804.4      111.32   272.2 tok/s     9.1 tok/s     254.942   257.6 tok/s    17.41 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          49.3 tok/s     1.00x   334.6 tok/s   334.6 tok/s      3063.0       5.662
2x          59.2 tok/s     1.20x   290.6 tok/s   145.3 tok/s      6852.8      11.372
4x          68.9 tok/s     1.40x   542.1 tok/s   135.5 tok/s      5453.8      14.990

===

oMLX - LLM inference, optimized for your Mac
https://github.com/jundot/omlx
Benchmark Model: Qwen3.6-35B-A3B-4bit
================================================================================

Single Request Results
--------------------------------------------------------------------------------
Test                TTFT(ms)    TPOT(ms)        pp TPS        tg TPS      E2E(s)    Throughput    Peak Mem
pp1024/tg128          2741.2       17.01   373.6 tok/s    59.3 tok/s       4.901   235.0 tok/s    19.26 GB
pp4096/tg128          9292.6       18.21   440.8 tok/s    55.3 tok/s      11.605   364.0 tok/s    20.04 GB
pp8192/tg128         18522.3       19.89   442.3 tok/s    50.7 tok/s      21.048   395.3 tok/s    20.39 GB
pp16384/tg128        38775.9       23.70   422.5 tok/s    42.5 tok/s      41.785   395.2 tok/s    21.01 GB
pp32768/tg128        87749.0       32.46   373.4 tok/s    31.1 tok/s      91.871   358.1 tok/s    22.35 GB
pp65536/tg128       243522.6       53.79   269.1 tok/s    18.7 tok/s     250.355   262.3 tok/s    25.03 GB

Continuous Batching
pp1024 / tg128
--------------------------------------------------------------------------------
Batch           tg TPS   Speedup        pp TPS    pp TPS/req    TTFT(ms)      E2E(s)
1x          59.3 tok/s     1.00x   373.6 tok/s   373.6 tok/s      2741.2       4.901
2x          78.7 tok/s     1.33x   369.2 tok/s   184.6 tok/s      5368.2       8.801
4x          92.8 tok/s     1.56x   372.2 tok/s    93.0 tok/s     10448.3      16.523