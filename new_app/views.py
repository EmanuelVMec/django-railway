from django.shortcuts import render
import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import os

# 🔍 Mensaje de depuración: Inicia carga del modelo
print("[DEBUG] Iniciando la carga del modelo...")

# Cargar el modelo .pkl
try:
    model_path = os.path.join(settings.STATICFILES_DIRS[0], 'models', 'Modelocafe(1).pkl')
    model = joblib.load(model_path)
    print(f"[DEBUG] Modelo cargado exitosamente desde: {model_path}")
except FileNotFoundError as e:
    print(f"[ERROR] No se encontró el archivo del modelo en: {model_path}")
    raise e
except Exception as e:
    print(f"[ERROR] Error inesperado al cargar el modelo: {str(e)}")
    raise e

# Definir los nombres de las variables de salida
output_columns = [
        'Altura_de_planta_AP', 'Diametro_de_tallo_DT'  # Salidas del modelo (alturas y diámetro)

]

@api_view(['POST'])
def predict_cafe(request):
    try:
        # 🔍 Depuración: Ver datos recibidos
        print("[DEBUG] Datos recibidos en la solicitud:", request.data)

        data = request.data

        features = [
            data['ARCILLA'], data['ARENA'], data['B'], data['CE'], data['Ca'],
            data['Cu'], data['EDAD_EN_DIAS'], data['Fe'], data['HUMEDAD_AMBIENTAL'],
            data['HUMEDAD_SUELO'], data['INDICE_DE_LLUVIA'], data['K'], data['LIMO'],
            data['MO'], data['Mg'], data['Mn'], data['NH4'], data['N_total'],
            data['P'], data['PH'], data['PRESION_ATMOSFERICA'], data['S'],
            data['TEMPERATURA_AMBIENTAL'], data['TEMPERATURA_SUELO'], data['TIPO_DE_CAFE'], data['Zn']
        ]


        # 🔍 Depuración: Ver características
        print("[DEBUG] Características para la predicción:", features)

        # Predicción
        prediction = model.predict([features])
        print("[DEBUG] Predicción realizada con éxito:", prediction)

        # Construir respuesta
        prediction_dict = {col: val for col, val in zip(output_columns, prediction[0])}

        return Response({'prediction': prediction_dict})

    except KeyError as e:
        error_message = f"Falta la clave requerida en los datos: {str(e)}"
        print(f"[ERROR] {error_message}")
        return Response({'error': error_message})

    except ValueError as e:
        print(f"[ERROR] Error de conversión de datos: {str(e)}")
        return Response({'error': 'Datos inválidos. Asegúrese de enviar valores numéricos.'})

    except Exception as e:
        print(f"[ERROR] Error durante la predicción: {str(e)}")
        return Response({'error': str(e)})
