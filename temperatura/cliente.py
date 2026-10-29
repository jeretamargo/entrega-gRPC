import grpc

import temperatura_pb2
import temperatura_pb2_grpc


def main():
    try:
        celsius = float(input("Temperatura en Celsius: "))
    except ValueError:
        print("Error: ingresá un número válido.")
        return

    with grpc.insecure_channel("localhost:50051") as canal:
        cliente = temperatura_pb2_grpc.ConversorTemperaturaStub(canal)

        solicitud = temperatura_pb2.SolicitudTemperatura(
            celsius=celsius
        )

        respuesta = cliente.Convertir(solicitud)

        print(f"Temperatura en Fahrenheit: {respuesta.fahrenheit}")


if __name__ == "__main__":
    main()