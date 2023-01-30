config = {
    'cpp': {
        'suffix': 'cpp',
        'images': ['code_runner'],
        'time_limit': 0,
        'sub_time_limit': 1000,
        'memory_limit': 256,
        # -DBOTRUNNER相当于C语言中的#define BOTRUNNER
        'compile_command': 'g++ -DBOTRUNNER -O2 -Wall {code} -o {target}',
        'run_command': '{target} < {data}'
    },
    'python': {
        'suffix': 'py',
        'images': ['code_runner'],
        'time_limit': 0,
        'sub_time_limit': 4000,
        'memory_limit': 256,
        'run_command': 'python3 {target} < {data}'
    },
    'java': {
        'suffix': 'java',
        'images': ['code_runner'],
        'time_limit': 0,
        'sub_time_limit': 1000,
        'memory_limit': 256,
        'compile_command': 'javac -encoding utf-8 {code}',
        'run_command': 'java -Dfile.encoding=utf-8 -cp /home/zzq_code/ Main < {data}'
    }
}
