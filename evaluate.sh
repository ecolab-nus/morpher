tmux new-session -d -s my_session_name9 'python -u run_morpher.py morpher_benchmarks/fft/fix_fft.c fix_fft > ./evaluate_data/fft_default_light.txt'
tmux new-session -d -s my_session_name7 'python -u run_morpher.py morpher_benchmarks/gemm/gemm.c gemm > ./evaluate_data/gemm_default_light.txt'


tmux new-session -d -s my_session_name7 'python -u run_morpher.py morpher_benchmarks/array_add/array_add.c array_add ./config/config_stdnoc4x4.yaml > ./evaluate_data/array_add_4x4_light.txt'
tmux new-session -d -s my_session_name8 'python -u run_morpher.py morpher_benchmarks/array_cond/array_cond.c array_cond ./config/config_stdnoc4x4.yaml > ./evaluate_data/array_cond_4x4_light.txt'
tmux new-session -d -s my_session_name9 'python -u run_morpher.py morpher_benchmarks/fft/fix_fft.c fix_fft ./config/config_stdnoc4x4.yaml > ./evaluate_data/fft_4x4_light.txt'
tmux new-session -d -s my_session_name8 'python -u run_morpher.py morpher_benchmarks/hpcg/hpcg.c hpcg ./config/config_stdnoc4x4.yaml > ./evaluate_data/hpcg_4x4_light.txt'
tmux new-session -d -s my_session_name9 'python -u run_morpher.py morpher_benchmarks/trmm/trmm.c trmm ./config/config_stdnoc4x4.yaml > ./evaluate_data/trmm_4x4_light.txt'