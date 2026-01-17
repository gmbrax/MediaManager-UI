# core_manager.py
import subprocess
import threading
import logging
import time
import socket
import atexit
import signal
from pathlib import Path
from typing import Optional, Callable
from config import (
    CORE_JAR_PATH,
    SOCKET_PATH,
    CORE_STARTUP_TIMEOUT,
)

# Logger para cleanup
_cleanup_logger = logging.getLogger('MediaManager.Cleanup')


class JavaCoreError(Exception):
    """Erro no core Java"""
    pass


class JavaCoreManager:
    _instances = []

    def __init__(self, jar_path=None, socket_path=None):
        self.jar_path = Path(jar_path) if jar_path else CORE_JAR_PATH
        self.socket_path = socket_path or SOCKET_PATH

        self.process = None
        self.ready = False
        self.crashed = False
        self.logger = logging.getLogger('MediaManager.Core')

        JavaCoreManager._instances.append(self)

    # ========== MODO 1: SÍNCRONO (ESPERA) ==========
    def start_and_wait(self, timeout=None):
        """
        Inicia o core e ESPERA até ficar ready (BLOQUEIA)
        """
        timeout = timeout or CORE_STARTUP_TIMEOUT
        self._launch_process()
        self._wait_until_ready(timeout)
        return self

    # ========== MODO 2: ASSÍNCRONO (BACKGROUND) ==========
    def start_background(self, on_ready: Optional[Callable] = None,
                         on_error: Optional[Callable] = None):
        """
        Inicia o core em BACKGROUND (NÃO BLOQUEIA)
        """
        self._launch_process()

        monitor_thread = threading.Thread(
            target=self._monitor_ready_async,
            args=(on_ready, on_error),
            daemon=True
        )
        monitor_thread.start()

        return self

    # ========== MÉTODOS INTERNOS ==========
    def _launch_process(self):
        """Lança o processo Java"""
        if not self.jar_path.exists():
            raise JavaCoreError(f"JAR não encontrado: {self.jar_path}")

        cmd = ['java', '-jar', str(self.jar_path)]
        self.logger.info(f"Iniciando core: {' '.join(cmd)}")

        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
        except FileNotFoundError:
            raise JavaCoreError("Java não encontrado. Instale o JDK/JRE.")
        except Exception as e:
            raise JavaCoreError(f"Erro ao iniciar core: {e}")

        # Threads de log
        threading.Thread(target=self._monitor_stdout, daemon=True).start()
        threading.Thread(target=self._monitor_stderr, daemon=True).start()
        threading.Thread(target=self._monitor_process, daemon=True).start()

    def _wait_until_ready(self, timeout):
        """Espera síncrona até ficar ready"""
        start = time.time()
        retry_interval = 0.5

        self.logger.info(f"Aguardando socket em {self.socket_path}")

        while not self.ready:
            if self.crashed:
                raise JavaCoreError("Core crashou antes de ficar ready")

            if self._check_socket_ready():
                self.ready = True
                self.logger.info("✓ Core READY!")
                return

            elapsed = time.time() - start
            if elapsed > timeout:
                self.stop()
                raise JavaCoreError(f"Core não ficou ready em {timeout}s")

            time.sleep(retry_interval)

    def _monitor_ready_async(self, on_ready, on_error):
        """Monitor assíncrono para modo background"""
        timeout = CORE_STARTUP_TIMEOUT
        start = time.time()
        retry_interval = 0.5

        while not self.ready and not self.crashed:
            if self._check_socket_ready():
                self.ready = True
                self.logger.info("✓ Core READY!")
                if on_ready:
                    try:
                        on_ready()
                    except Exception as e:
                        self.logger.error(f"Erro no callback on_ready: {e}")
                return

            if time.time() - start > timeout:
                error_msg = f"Timeout após {timeout}s"
                self.logger.error(error_msg)
                if on_error:
                    try:
                        on_error(error_msg)
                    except Exception as e:
                        self.logger.error(f"Erro no callback on_error: {e}")
                return

            time.sleep(retry_interval)

        if self.crashed and on_error:
            try:
                on_error("Core crashou durante startup")
            except Exception as e:
                self.logger.error(f"Erro no callback on_error: {e}")

    def _check_socket_ready(self):
        """Testa se socket aceita conexão"""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect(str(self.socket_path))
            sock.close()
            return True
        except (FileNotFoundError, ConnectionRefusedError, socket.timeout):
            return False
        except Exception:
            return False

    def _monitor_stdout(self):
        for line in self.process.stdout:
            self.logger.info(line.rstrip())

    def _monitor_stderr(self):
        for line in self.process.stderr:
            line = line.rstrip()
            self.logger.error(line)
            if any(x in line for x in ['Exception', 'Error', 'FATAL']):
                self.logger.critical(f"Erro crítico: {line}")

    def _monitor_process(self):
        """Monitora término do processo"""
        returncode = self.process.wait()
        self.crashed = True

        # Códigos de término graceful:
        # 0   = Exit normal
        # 130 = SIGINT (Ctrl+C) = 128 + 2
        # 143 = SIGTERM (kill)  = 128 + 15
        graceful_exits = [0, 130, 143]

        if returncode in graceful_exits:
            self.logger.info(f"Core terminou gracefully (exit code {returncode})")
        else:
            self.logger.error(f"Core terminou com erro (exit code {returncode})")

    # ========== MÉTODOS PÚBLICOS ==========
    def is_ready(self):
        """Checa se está pronto"""
        return self.ready and self.is_alive()

    def is_alive(self):
        """Checa se processo está rodando"""
        return self.process and self.process.poll() is None

    def stop(self):
        """Para o core"""
        if self.process and self.is_alive():
            self.logger.info("Parando core Java...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
                self.logger.info("Core parado com sucesso")
            except subprocess.TimeoutExpired:
                self.logger.warning("Forçando KILL")
                self.process.kill()
                self.process.wait()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @classmethod
    def cleanup_all(cls):
        """Para todas as instâncias ativas"""
        for instance in cls._instances:
            instance.stop()
        cls._instances.clear()


# Cleanup automático
atexit.register(JavaCoreManager.cleanup_all)


# Signal handlers
def _signal_handler(signum, frame):
    _cleanup_logger.info(f"Recebido sinal {signum} - encerrando...")
    JavaCoreManager.cleanup_all()
    exit(0)


signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)