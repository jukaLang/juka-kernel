from ipykernel.kernelbase import Kernel
import tempfile
import subprocess
import os

class JukaKernel(Kernel):
    implementation = 'Juka'
    implementation_version = '0.1'
    language = 'no-op'
    language_version = '0.0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Juka kernel - run juka in jupyter"

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        if not silent:
            temp = tempfile.NamedTemporaryFile(delete=False)
            try:
                temp.write(str.encode(code))
                temp.seek(0)
                temp.close()
                result = subprocess.run("Juka "+temp.name, shell=True, capture_output=True, text=True, env={'PATH': os.getenv('PATH')})
                if len(result.stderr) != 0:
                    stream_content = {'name': 'stderr', 'text': result.stderr}
                else:
                    stream_content = {'name': 'stdout', 'text': result.stdout}
            except:
                stream_content = {'name': 'stderr', 'text': "Something went wrong"}

            self.send_response(self.iopub_socket, 'stream', stream_content)

        return {'status': 'ok',
                # The base class increments the execution count
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
               }
