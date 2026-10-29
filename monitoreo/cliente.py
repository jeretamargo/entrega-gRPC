import grpc

import monitoreo_pb2
import monitoreo_pb2_grpc


def main():
    input("Presione Enter para consultar el estado del servidor...")

    with grpc.insecure_channel("localhost:50052") as canal:
        cliente = monitoreo_pb2_grpc.MonitoreoServidorStub(canal)

        solicitud = monitoreo_pb2.SolicitudMonitoreo()

        reportes = cliente.Consultar(solicitud)

        for numero, reporte in enumerate(reportes, start=1):
            print(f"\nReporte {numero}")
            print(f"CPU en uso: {reporte.cpu_porcentaje:.1f} %")
            print(f"RAM disponible: {reporte.ram_disponible_mb:.1f} MB")
            print(f"Disco disponible: {reporte.disco_disponible_gb:.1f} GB")

        print("\nMonitoreo finalizado.")


if __name__ == "__main__":
    main()