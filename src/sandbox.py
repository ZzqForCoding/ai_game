import os
import subprocess
from subprocess import PIPE
from compiler import config
import json
import time

debug = False

class Sandbox:
    bots = dict()

    def __init__(self, uuid, code, lang):
        self.uuid = uuid
        # 代码
        self.code = code
        # 当前语言的代码编译与运行命令等参数
        self.config = config[lang]

        # 代码所在位置
        self.loc = '/home/zzq_code/'
        # 代码绝对路径
        if lang == 'java':
            self.path_code = self.loc + 'Main' + '.' + self.config['suffix']
        else:
            self.path_code = self.loc + 'code-' + self.uuid + '.' + self.config['suffix']
        # 需要运行的代码文件绝对路径
        self.path_target = self.loc + 'prog-' + self.uuid if self.config.get('compile_command') is not None else self.path_code
        # 输入文件
        self.path_data = self.loc + 'data-' + self.uuid
        # 容器
        self.container = None
        # 进程
        self.proc = None
        # 编译与否
        self.compiled = False

        self.create()

    def create(self):
        if self.container:
            return
        docker_images = self.get_local_images()
        use_images = self.config['images']
        # 在docker_images中过滤出存在于use_images中的镜像
        available_images = filter(lambda x : x['repo'] in use_images, docker_images)
        image = ''
        if available_images:
            # 取出tag最大的镜像
            image = max(available_images, key = lambda x : x['tag'])
            image = image['repo'] + ':' + image['tag']
        else:
            # 拉镜像
            pass
        self.image = image

        result = self.run_container(self.image)
        if result != 'ok':
            return result
        result = self.prepare_code()
        return result

    def compile(self):
        if self.compiled:
            return json.dumps({
                'returncode': 0,
                'status': 'ok'
            })
        if self.config.get('compile_command') is None:
            return json.dumps({
                'returncode': 0,
                'status': 'ok'
            })

        compile_command = self.config['compile_command'].format(code=self.path_code, target=self.path_target)
        command = 'docker exec -u zzq_code %s /bin/bash -c "%s"' % (self.container, compile_command)
        p = subprocess.run(command, stderr=PIPE, shell=True)
        if p.returncode != 0:
            # 编译错误
            if debug:
                raise RuntimeError('Compile Error: %s' % p.stderr)
            else:
                ret = {
                    'returncode': p.returncode,
                    'status': 'Compile Error',
                    'desp': p.stderr.decode()
                }
                return json.dumps(ret)
        self.compiled = True
        result = self.update_container(1, self.config['memory_limit'])
        ret = {}
        if result != 'ok':
            ret['returncode'] = 256
            ret['status'] = "Internal Error"
            ret['desp'] = result
        else:
            ret['returncode'] = 0
            ret['status'] = "ok"
        return json.dumps(ret)

    def prepare_data(self, data):
        file_data = open(self.path_data, 'w')
        file_data.write(data)
        file_data.close()
        p = subprocess.run('docker cp %s %s:%s' % (self.path_data, self.container, self.path_data), stderr=PIPE, shell=True, encoding='utf-8')
        if p.returncode != 0:
            os.remove(self.path_data)
            if debug:
                raise RuntimeError('Failed to copy data in container %s! Details: \n%s' % (self.container, p.stderr))
            else:
                return 'Prepare data error'
        os.remove(self.path_data)
        return 'ok'

    def run(self):
        run_command = self.config['run_command'].format(target=self.path_target, data=self.path_data)
        st = time.perf_counter()
        p = subprocess.run('docker exec -u zzq_code %s /bin/bash -c "timeout %d %s"' % (self.container, (self.config['time_limit'] + self.config['sub_time_limit']) / 1000, run_command), stdout=PIPE, stderr=PIPE, shell=True, encoding='utf-8')
        ed = time.perf_counter()
        t = int(float(ed - st) * 1000)
        if p.returncode != 0:
            # 运行错误
            if debug:
                raise RuntimeError('Failed to run program! Detail: \n%s' % p.stderr)
            else:
                if p.stderr == None or len(p.stderr) == 0:
                    ret = {
                        "returncode": p.returncode,
                        "status": "Time Limit Exceeded",
                        "desp": "",
                    }
                    return json.dumps(ret)
                ret = {
                    "returncode": p.returncode,
                    "status": "Runtime Error",
                    "desp": p.stderr.decode(),
                }
                return json.dumps(ret)
        ret = {
            "returncode": 0,
            "output": p.stdout,
            "time": t
        }
        return json.dumps(ret)

    # 获取docker镜像列表
    def get_local_images(self):
        # --no-trunc表示不截断
        p = subprocess.run('docker images --no-trunc', stdout=PIPE, stderr=PIPE, shell=True, encoding='utf-8')
        # 若执行异常则返回空
        if p.returncode != 0:
            if debug:
                raise RuntimeError('No docker installation found!')
            else:
                return list([])

        # 处理输出
        output = p.stdout.strip().split('\n')
        images_list = []
        for line in output[1:]:
            repo, tag, id, *time, size = line.split()
            images_list.append({
                'repo': repo,
                'tag': tag,
                'id': id,
                'time': ' '.join(time),
                'size': size
            })
        return images_list

    # 启动容器
    def run_container(self, image):
        p = subprocess.run('docker run -itd %s /bin/bash' % image, stdout=PIPE, stderr=PIPE, shell=True, encoding='utf-8')
        if p.returncode != 0:
            if debug:
                raise RuntimeError('Failed to run container with image %s! Details: \n%s' % (image, p.stderr))
            else:
                return p.stderr
        self.container = p.stdout.strip()
        return 'ok'

    def stop(self):
        result = self.stop_container()
        if result != 'ok':
            return result
        result = self.remove_container()
        return result

    # 准备好需要执行的代码文件
    def prepare_code(self):
        code_file = open(self.path_code, 'w')
        code_file.write(self.code)
        code_file.close()
        p = subprocess.run('docker cp %s %s:%s' % (self.path_code, self.container, self.path_code), stdout=PIPE, stderr=PIPE, shell=True, encoding='utf-8')
        if p.returncode != 0:
            os.remove(self.path_code)
            if debug:
                raise RuntimeError('Failed to copy code in container %s! Details: \n%s' % (self.container, p.stderr))
            else:
                return 'Prepare code error'
        os.remove(self.path_code)
        return 'ok'

    # 调整容器限制
    def update_container(self, cpu, memory):
        p = subprocess.run('docker update --cpus="{cpu}" --memory="{memory}m" --memory-swap="{memory}m" {container}'.format(cpu=cpu, memory=memory, container=self.container), stderr=PIPE, shell=True, encoding='utf-8')
        if p.returncode != 0:
            if debug:
                raise RuntimeError('Failed to update config of container %s! Detail: \n%s' % (self.container, p.stderr))
            else:
                return 'Update container error'
        return 'ok'

    def stop_container(self):
        p = subprocess.run('docker kill %s ' % self.container, stderr=PIPE, shell=True, encoding='utf-8')
        if p.returncode != 0:
            if debug:
                raise RuntimeError('Failed to stop container %s! Details: \n%s' % (self.container, p.stderr))
            else:
                return 'Kill container error'
        return 'ok'

    def remove_container(self):
        p = subprocess.run('docker rm %s' % self.container, stderr=PIPE, shell=True, encoding='utf-8')
        if p.returncode != 0:
            if debug:
                raise RuntimeError('Failed to stop container %s! Details: \n%s' % (self.container, p.stderr))
            else:
                return 'Remove container error'
        return 'ok'
