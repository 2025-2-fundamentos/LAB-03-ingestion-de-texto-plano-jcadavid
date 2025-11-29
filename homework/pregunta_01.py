"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    import pandas as pd

    # Read the fixed-width file
    # Skip the first 4 lines (header)
    # Define column widths based on inspection
    df = pd.read_fwf(
        "files/input/clusters_report.txt",
        colspecs=[(0, 9), (9, 25), (25, 41), (41, None)],
        header=None,
        names=["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"],
        skiprows=4
    )

    # Fill NaN values in the first 3 columns (forward fill)
    df[["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave"]] = \
        df[["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave"]].ffill()

    # Group by cluster and aggregate keywords
    # We group by the first 3 columns to keep them, and join the keywords
    df = df.groupby(
        ["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave"]
    )["principales_palabras_clave"].apply(lambda x: " ".join(x.astype(str))).reset_index()

    # Convert columns to appropriate types
    df["cluster"] = df["cluster"].astype(int)
    df["cantidad_de_palabras_clave"] = df["cantidad_de_palabras_clave"].astype(int)

    # Clean percentage column: replace ',' with '.' and remove ' %', then convert to float
    df["porcentaje_de_palabras_clave"] = df["porcentaje_de_palabras_clave"].str.replace(",", ".").str.replace(" %", "").astype(float)

    # Clean keywords column
    # Remove trailing dot and normalize spaces
    df["principales_palabras_clave"] = df["principales_palabras_clave"].str.replace(r"\.$", "", regex=True)
    df["principales_palabras_clave"] = df["principales_palabras_clave"].str.replace(r"\s+", " ", regex=True)

    # Sort by cluster just in case
    df = df.sort_values("cluster").reset_index(drop=True)

    return df
