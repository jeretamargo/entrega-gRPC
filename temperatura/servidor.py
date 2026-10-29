from concurrent import futures

import grpc
import temperatura_pb2
import temperatura_pb2_grpc


class ConversorTemperatura(
    temperatura_pb2_grpc.ConversorTemperaturaServicer
):
    def Convertir(self, request, context):
        celsius = request.celsius
        fahrenheit = celsius * 1.8 + 32

        return temperatura_pb2.RespuestaTemperatura(
            fahrenheit=fahrenheit
        )

def main():
    servidor = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    temperatura_pb2_grpc.add_ConversorTemperaturaServicer_to_server(
        ConversorTemperatura(),
        servidor,
    )

    servidor.add_insecure_port("0.0.0.0:50051")
    servidor.start()

    print("Servidor escuchando en el puerto 50051.")

    try:
        servidor.wait_for_termination()
    except KeyboardInterrupt:
        print("\nDeteniendo el servidor...")
        servidor.stop(0).wait()


if __name__ == "__main__":
    main()