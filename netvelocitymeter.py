import speedtest
import click
from colorama import init, Fore
import time
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

init(autoreset=True)  # Inicializar colorama
sns.set(style="whitegrid")  # Configurar estilo para Seaborn

@click.command()
@click.option("--verbose", is_flag=True, help="Mostrar información detallada")
@click.option("--continuous", type=int, default=1, help="Realizar mediciones continuas con el número de mediciones especificado")
@click.option("--interval", type=int, default=60, help="Intervalo en segundos entre mediciones continuas")
@click.option("--output", type=click.Path(), help="Guardar los resultados en un archivo CSV")
@click.option("--plot", is_flag=True, help="Generar un gráfico de las mediciones")
@click.option("--connections", multiple=True, type=str, help="Tipos de conexiones a medir (ej: wifi ethernet)")
def main(verbose, continuous, interval, output, plot, connections):
    if not connections:
        connections = ["default"]

    if continuous > 1:
        continuous_speed_measurements(continuous, interval, output, plot, connections)
    else:
        download_speed, upload_speed, ping, packet_loss, jitter, server = run_speed_test(connections[0])
        if verbose:
            print_speed_results_verbose(download_speed, upload_speed, ping, packet_loss, jitter, server)
        else:
            print_speed_results(download_speed, upload_speed, ping, packet_loss, jitter, server)

def continuous_speed_measurements(count, interval, output, plot, connections):
    measurements = []
    for _ in range(count):
        for connection in connections:
            download_speed, upload_speed, ping, _, _, _ = run_speed_test(connection)
            measurements.append({"connection": connection, "download_speed": download_speed, "upload_speed": upload_speed, "ping": ping})
        time.sleep(interval)

    if output:
        save_results_to_csv(measurements, output)

    if plot:
        generate_speed_plot(measurements)

def run_speed_test(connection="default"):
    try:
        speed_test = speedtest.Speedtest()
        if connection == "wifi":
            speed_test.get_best_server(threads=None, pre_allocate=False)
        elif connection == "ethernet":
            speed_test.get_best_server(threads=None, pre_allocate=False, interfaces=speedtest.Config()._interfaces())

        download_speed = speed_test.download()
        upload_speed = speed_test.upload()
        ping = speed_test.results.ping
        packet_loss = speed_test.results.packet_loss
        jitter = speed_test.results.jitter
        server = speed_test.results.server
        return download_speed, upload_speed, ping, packet_loss, jitter, server
    except Exception as e:
        print(f"Error durante la prueba de velocidad: {e}")
        return 0, 0, 0, 0, 0, {}

def save_results_to_csv(measurements, output):
    with open(output, "w", newline="") as csvfile:
        fieldnames = ["Timestamp", "Connection", "Download Speed (Mbps)", "Upload Speed (Mbps)", "Ping (ms)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for measurement in measurements:
            writer.writerow({
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "Connection": measurement["connection"],
                "Download Speed (Mbps)": measurement["download_speed"] / 1024 / 1024,
                "Upload Speed (Mbps)": measurement["upload_speed"] / 1024 / 1024,
                "Ping (ms)": measurement["ping"]
            })

def generate_speed_plot(measurements):
    data = {
        "Timestamp": [measurement["Timestamp"] for measurement in measurements],
        "Connection": [measurement["Connection"] for measurement in measurements],
        "Download Speed (Mbps)": [measurement["download_speed"] / 1024 / 1024 for measurement in measurements],
        "Upload Speed (Mbps)": [measurement["upload_speed"] / 1024 / 1024 for measurement in measurements],
        "Ping (ms)": [measurement["ping"] for measurement in measurements]
    }

    df = pd.DataFrame(data)

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x="Timestamp", y="Download Speed (Mbps)", hue="Connection")
    sns.lineplot(data=df, x="Timestamp", y="Upload Speed (Mbps)", hue="Connection")
    sns.lineplot(data=df, x="Timestamp", y="Ping (ms)", hue="Connection")
    plt.xlabel("Timestamp")
    plt.ylabel("Speed / Ping")
    plt.title("Speed and Ping Measurements")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("speed_plot.png")
    plt.show()

if __name__ == "__main__":
    main()
