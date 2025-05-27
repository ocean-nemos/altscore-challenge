# Nave a la deriva

**Contexto:**

Año 2315. Te encuentras atrapado en una nave espacial a la deriva en el espacio profundo. Los sistemas de navegación están dañados y la energía se agota rápidamente. En un golpe de suerte, detectas en el radar un robot de reparación no tripulado que se aproxima. Sabes que este robot utiliza llamadas HTTP para identificar y reparar sistemas averiados en naves cercanas. Tu única esperanza es simular una llamada de auxilio para que el robot te encuentre y repare tu nave.

## El Desafío:

Expon una API que cumpla con los siguientes requisitos:

**Primera Llamada:** `GET /status`

Retorna un objeto JSON con la siguiente estructura:

{
  "damaged_system": "<pick one of the systems>"
}

**Segunda Llamada:** `GET /repair-bay`

- Genera una página HTML simple que contenga un `<div>` con la clase "anchor-point".
- El contenido de este `<div>` debe ser un código único que corresponda al sistema_averiado según la siguiente tabla:

```json
{
  "navigation": "NAV-01",
  "communications": "COM-02",
  "life_support": "LIFE-03",
  "engines": "ENG-04",
  "deflector_shield": "SHLD-05"
}
```

**Tercera Llamada:** `POST /teapot`

Retorna un código de estado `HTTP 418 (I'm a teapot)`.
Ejemplo:

Si la primera llamada retorna:

```json
{
  "damaged_system": "engines"
}
```

La segunda llamada a `GET /repair-bay` generaría una página HTML similar a esta:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Repair</title>
</head>
<body>
<div class="anchor-point">ENG-04</div>
</body>
</html>
```

## Consideraciones Adicionales:

- La API debe estar programada en Python, TypeScript o Go (se verificará en la entrevista).
- La aplicación puede ser desplegada en cualquier plataforma de tu elección o incluso en tu máquina local (guardamos la URL de la API en la cual se completa el reto).
- Al registrar la URL de tu API, asegúrate de que sea accesible desde el exterior, tendrás tan solo 3 intentos y 5 minutos para que el robot te encuentre (aquí demuestras tu atención al detalle).

## Solución

Registra la URL de tu API aquí: `[POST] /v1/s1/e7/solution.`

- ¡No olvides consultar la Documentación!
- ¡El tiempo corre! El robot se acerca. Programa la API correctamente para guiar al robot hacia tu nave y asegurar tu supervivencia. ¡Buena suerte!