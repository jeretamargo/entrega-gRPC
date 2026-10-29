from concurrent import futures
import time

import grpc
import psutil

import monitoreo_pb2
import monitoreo_pb2_grpc


class ServicioMonitoreo(
    monitoreo_pb2_grpc.MonitoreoServidorServicer
):
    def Consultar(self, request, context):
        # Prepara la medición de CPU.
        psutil.cpu_percent(interval=None)

        for numero in range(1, 6):
            time.sleep(2)

            cpu = psutil.cpu_percent(interval=None)
            ram_mb = psutil.virtual_memory().available / (1024 ** 2)
            disco_gb = psutil.disk_usage("/").free / (1024 ** 3)

            print(f"Enviando reporte {numero}...", flush=True)

            yield monitoreo_pb2.Reporte(
                cpu_porcentaje=cpu,
                ram_disponible_mb=ram_mb,
                disco_disponible_gb=disco_gb,
            )

def main():
    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    monitoreo_pb2_grpc.add_MonitoreoServidorServicer_to_server(
        ServicioMonitoreo(),
        servidor,
    )

    servidor.add_insecure_port("0.0.0.0:50052")
    servidor.start()

    print("Servidor de monitoreo escuchando en el puerto 50052.")

    try:
        servidor.wait_for_termination()
    except KeyboardInterrupt:
        print("\nDeteniendo el servidor...")
        servidor.stop(0).wait()


if __name__ == "__main__":
    main()