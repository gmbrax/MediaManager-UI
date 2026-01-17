# ipc_manager.py
import socket
import struct
import uuid
import logging
from pathlib import Path

# Importa config PRIMEIRO (adiciona protobuf ao sys.path)
from config import SOCKET_PATH

# Agora importa protobuf - SEM o "protobuf."
import messages_pb2 as transport_pb2
import test_pb2

logger = logging.getLogger('MediaManager.IPC')


class IPCManager:
    """Gerencia comunicação IPC com o MediaManager Core"""

    def __init__(self, socket_path=None):
        self.socket_path = socket_path or SOCKET_PATH
        self.sock = None
        self.connected = False

    def connect(self):
        """Conecta ao core"""
        if self.connected:
            logger.warning("Já conectado")
            return

        if not Path(self.socket_path).exists():
            raise ConnectionError(f"Socket não existe: {self.socket_path}")

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(str(self.socket_path))
        self.connected = True
        logger.info(f"Conectado ao core via {self.socket_path}")

    def disconnect(self):
        """Desconecta do core"""
        if self.sock:
            self.sock.close()
            self.sock = None
            self.connected = False
            logger.info("Desconectado")

    def _send_request(self, action: str, payload_bytes: bytes) -> str:
        """Envia request e retorna request_id"""
        if not self.connected:
            raise ConnectionError("Not connected!")

        # Monta request
        request = transport_pb2.Request()
        request.request_id = str(uuid.uuid4())
        request.payload = payload_bytes
        request.headers["action"] = action

        # Serializa e envia
        request_bytes = request.SerializeToString()
        size = len(request_bytes)
        size_bytes = struct.pack('>I', size)

        self.sock.sendall(size_bytes + request_bytes)

        logger.debug(f"Enviado: action={action}, request_id={request.request_id}")

        return request.request_id

    def _receive_response(self) -> transport_pb2.Response:
        """Recebe response"""
        if not self.connected:
            raise ConnectionError("Not connected!")

        # Recebe tamanho (4 bytes)
        size_bytes = self.sock.recv(4)
        if not size_bytes:
            raise ConnectionError("Connection closed by server")

        size = struct.unpack('>I', size_bytes)[0]

        # Recebe payload
        message = b''
        while len(message) < size:
            chunk = self.sock.recv(size - len(message))
            if not chunk:
                raise ConnectionError("Connection closed while reading")
            message += chunk

        # Deserializa
        response = transport_pb2.Response()
        response.ParseFromString(message)

        logger.debug(f"Recebido: status={response.status_code}")

        return response

    # ========== COMANDOS DE TESTE ==========

    def echo(self, message: str) -> str:
        """Comando echo"""
        cmd = test_pb2.EchoCommand()
        cmd.message = message

        logger.info(f"Echo: '{message}'")
        self._send_request("echo", cmd.SerializeToString())

        response = self._receive_response()

        if response.status_code != 200:
            raise Exception(f"Echo failed: {response.status_code}")

        echo_resp = test_pb2.EchoResponse()
        echo_resp.ParseFromString(response.payload)

        logger.info(f"Echo response: '{echo_resp.message}'")
        return echo_resp.message

    def heartbeat(self) -> int:
        """Comando heartbeat - retorna RTT em ms"""
        import time

        t1 = int(time.time() * 1000)

        cmd = test_pb2.HeartbeatCommand()
        cmd.client_timestamp = t1

        logger.info(f"Heartbeat (T1={t1})")
        self._send_request("heartbeat", cmd.SerializeToString())

        response = self._receive_response()
        t4 = int(time.time() * 1000)

        if response.status_code != 200:
            raise Exception(f"Heartbeat failed: {response.status_code}")

        hb_resp = test_pb2.HeartbeatResponse()
        hb_resp.ParseFromString(response.payload)

        rtt = t4 - t1
        logger.info(f"Heartbeat OK (RTT: {rtt}ms)")

        return rtt

    def close_connection(self):
        """Fecha conexão graciosamente"""
        cmd = test_pb2.CloseCommand()

        logger.info("Enviando close...")
        self._send_request("close", cmd.SerializeToString())

        response = self._receive_response()

        if response.status_code == 200:
            close_resp = test_pb2.CloseResponse()
            close_resp.ParseFromString(response.payload)
            logger.info(f"Server: {close_resp.message}")

        self.disconnect()

    # ========== CONTEXT MANAGER ==========

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connected:
            try:
                self.close_connection()
            except:
                self.disconnect()