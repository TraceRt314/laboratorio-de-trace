# Saben dónde estás aunque el GPS esté apagado

Documentación técnica del episodio 003 de El Laboratorio de Trace: cómo se calcula la posición de un móvil con el GPS apagado, a partir de redes wifi, antenas y mapas construidos por otros móviles. Todo esto exige que los servicios de ubicación del móvil estén activados: con Location Accuracy desactivada, Google indica que no se recogen señales inalámbricas ni datos de sensores [1], y Apple condiciona el envío a que Localización esté activada [3].

Fuentes consultadas entre el 25 y el 30 de octubre de 2026. Las páginas de ayuda de Google no muestran fecha de edición.

## Cómo funciona por dentro

**El GPS recibe, no emite.** Los satélites envían la hora y el móvil calcula su posición. Con cielo abierto, GPS.gov cita un error típico de hasta 4,9 m de radio en móviles, que empeora cerca de edificios, puentes y árboles. La página no se actualiza desde febrero de 2025 [20].

**El sistema elige la fuente, no la app.** Con el proveedor de ubicación combinada de Android, la app pide "alta precisión" o "bajo consumo" y el sistema decide la tecnología [7]. Google indica que, con Location Accuracy activada, recoge periódicamente información de sensores y señales inalámbricas cercanas (wifi, redes móviles, GPS, y sensores como acelerómetro, barómetro y giroscopio), con identificadores aleatorios, temporales y rotativos no asociados a una persona ni cuenta. Con la función desactivada, el dispositivo usa solo GPS y sensores y el servicio no recoge señales inalámbricas ni datos de sensores [1]. Maps dibuja un círculo azul claro cuando no está seguro de la posición, y esa es la representación de la precisión [2]. Ninguna de las páginas de Google da cifras en metros por tecnología [2].

**Wifi.** El móvil escucha las redes cercanas, con su identificador de punto de acceso (BSSID) y su potencia, y envía esa lista a un servidor que conoce dónde está cada punto y devuelve la posición. Apple lo documenta: el dispositivo envía periódicamente las ubicaciones geoetiquetadas de wifis y antenas cercanas [3] y usa ubicaciones de wifis y antenas obtenidas de forma colaborativa [4]. Android trata una lista de wifis como dato de ubicación: para las apps que apuntan a Android 10 o superior el escaneo exige el permiso `ACCESS_FINE_LOCATION` y los servicios de ubicación activados. Cada app en primer plano puede escanear cuatro veces cada dos minutos, y todas las de segundo plano juntas una vez cada 30 minutos (Android 9 y posteriores). Existe una opción de desarrollador para desactivar ese límite en pruebas locales [5]. La página no explica por qué se exige el permiso; para Bluetooth, la documentación de Android sí dice que hasta Android 11 un escaneo podía servir para deducir la ubicación [8]. El RTT (medición de distancia a puntos de acceso compatibles con IEEE 802.11-2016 FTM o 802.11az, desde Android 9) da un resultado típico de 1 o 2 metros [6]. Requiere puntos de acceso compatibles, así que no es una cifra general para cualquier router doméstico [6].

La posición se calcula con las ubicaciones conocidas de los puntos de acceso que oye el móvil. Las fuentes consultadas no detallan el algoritmo (trilateración, huella de señal u otro), así que "tres routers, un punto" es una simplificación didáctica.

**El mapa lo hacen los móviles.** Rye y Levin (Universidad de Maryland, IEEE S&P 2024) mostraron que el servicio de posicionamiento wifi de Apple, ante la consulta de un solo BSSID, responde con su ubicación y la de hasta 400 BSSID cercanos. Aplicando la técnica durante un año (de noviembre de 2022 a noviembre de 2023), desde un único punto de red y a unas 30 consultas por segundo, obtuvieron la ubicación precisa de más de 2.000 millones de BSSID en el mundo. Estudiaron, por ejemplo, routers Starlink y de viaje que entraban y salían de Ucrania y el apagón de BSSID en Gaza. Los usuarios cuyos dispositivos se rastreaban no habían aceptado participar ni podían salirse. La base se alimenta de dispositivos Apple que informan de su GPS y de los BSSID que ven [13]. Lo mapeado son puntos de acceso, no personas. Tras el aviso de los autores, Apple permitió excluir un punto de acceso añadiendo `_nomap` al nombre de la red, como ya hacían Google y WiGLE al menos desde 2016 [13].

**Antenas.** La red puede estimar la posición a partir de la celda servidora, el timing advance (diferencia entre emisión y recepción) y la posición conocida de las celdas [17]. El resultado es un área, no un punto. Ogulenko et al. (2021) compararon las trazas GPS de voluntarios con las antenas que atendían sus conexiones: en más del 60 % de las conexiones el móvil estaba fuera del polígono de Voronoi de su antena, y el área de posiciones posibles es varias veces mayor que la de esa celda (para cubrir el 90 % hacen falta la celda y dos anillos de celdas vecinas) [18]. Para orientar el tamaño: el Gobierno Vasco describe la localización del 112 por antenas, previa al AML, con radios de 2 a 5 km en zona urbana y de 40 a 50 km o más en zona rural [29]. Esas cifras no son un registro del operador ni una medida de este laboratorio.

**Registro del móvil en la red.** El móvil no se "registra cada pocos segundos" en la antena. En reposo, el móvil envía una actualización de área de seguimiento periódica con un temporizador (T3412) cuyo valor por defecto es de 54 minutos, y la red puede modificarlo [31]. Además informa cuando cambia de área de seguimiento. Ninguna fuente citada indica que el operador guarde el timing advance de cada conexión; lo que la Ley 25/2007 obliga a conservar es el identificador de celda (ver Matices).

## El experimento del laboratorio

Se hizo con un móvil Android conectado por USB y scripts propios. Todo lo que sale en pantalla pasa por un filtro que enmascara direcciones MAC, nombres de red y coordenadas, y aquí no se reproduce ninguno. El móvil no tenía SIM, así que no hay medida de antenas y se ilustran con un diagrama. Son medidas de un solo móvil, en un solo sitio y un solo momento.

- **Escaneo sin conectar.** El móvil oyó nueve puntos wifi sin conectarse a ninguno. Un script estima la distancia con un modelo de pérdida logarítmica, con -40 dBm a un metro y exponente 3 en interiores, orientativo y con un error de ±50 %. Dio entre 2 y 63 metros.
- **Servidor de Apple.** Con un script que imita la petición descrita por Rye y Levin, se consultó solo por el router propio. El servicio, una API no documentada, devolvió 400 puntos con sus coordenadas, y el del router propio con una precisión estimada de 24 metros. Esa cifra es el radio de precisión que Apple asigna a la ubicación guardada de ese punto de acceso, no una medida de dónde está el móvil. No se usó cuenta de Apple.
- **Ubicación de Google.** Con el volcado del servicio de ubicación del sistema, la última posición calculada por red, sin GPS y con el móvil quieto en la mesa, declaraba una precisión de unos 15 metros. En Android, esa precisión es el radio de un círculo dentro del cual la posición real está con un 68 % de probabilidad [28]. Es la estimación del propio sistema, no un error medido contra una posición conocida.
- **BeaconDB.** Se enviaron las 12 redes que oía a esta base abierta y voluntaria [15]. No conocía ninguna, volvió a la geolocalización por IP y contestó con un radio de 25 kilómetros. Es el resultado de una consulta, no una cifra general de la geolocalización por IP.
- **Apps con permiso.** Se contaron 57 apps y servicios con permiso de ubicación precisa, incluidos los del sistema.
- **Modo avión.** Se activó el modo avión desde el ordenador y la wifi quedó apagada. Se encendió sin quitar el avión, se pidió un escaneo y la lista de vecinos volvió a aparecer. Después se quitó el avión.

El mapa con tres anillos (15 m, un barrio y 25 km) es una ilustración sobre una calle de ejemplo, no una medida. El de 15 m y el de 25 km proceden de las mediciones anteriores. El anillo de antena no procede de ninguna medida de este laboratorio y su tamaño es ilustrativo: las cifras públicas para localización por antenas en zona urbana son de 2 a 5 km de radio [29].

## Qué dicen los estudios

- Rye y Levin (2024), un año de consultas, más de 2.000 millones de BSSID [13].
- Ogulenko et al. (2021), más de un 60 % de conexiones fuera de la zona teórica de su antena [18].

## Matices y límites

- **Hace falta tener la ubicación activada.** Los mecanismos descritos operan con los servicios de ubicación del móvil encendidos aunque el GPS no se use. Con Location Accuracy desactivada en Android no se recogen señales inalámbricas [1]. Para las apps, el escaneo wifi exige además los servicios de ubicación activados [5].
- **Una cifra general de "unos 20 m sin GPS" no tiene fuente.** Google Maps no da metros [2]. Lo cuantificado es RTT (1 o 2 m, con puntos compatibles) [6] y las medidas de 24 y 15 metros, que son de un solo móvil y un solo sitio.
- **Modo avión.** En iPhone, Apple documenta que el modo avión apaga la conexión móvil y la wifi, que apaga todas las radios salvo el Bluetooth, y que se pueden usar wifi y Bluetooth con el modo avión puesto si la aerolínea lo permite [12]. En Android, Google documenta que al activarlo por primera vez se apagan la wifi y el Bluetooth y que la siguiente vez el móvil recuerda el ajuste anterior [11]. La documentación de Android consultada no detalla el comportamiento de la radio móvil. Por tanto el modo avión sí apaga la radio celular, y lo que no garantiza es que la wifi y el Bluetooth sigan apagados si se reactivan. El código de AOSP indica que el ajuste de escaneo siempre disponible solo está activo si el modo avión está apagado, y que el escaneo BLE no está disponible con modo avión y Bluetooth desactivado [10]. Si el usuario enciende la wifi o el Bluetooth dentro del modo avión, esa radio escanea con normalidad, que es lo que muestra la prueba. No se verificó si el escaneo de ubicación usa esas radios en modo avión en iPhone, ni el comportamiento de capas de fabricante (Samsung, OnePlus).
- **El ajuste de escaneo.** La página de Google dice que se puede dejar que el móvil escanee redes wifi y dispositivos Bluetooth cercanos para mejorar la ubicación [9]. La documentación de la API de Android indica que, cuando el escaneo siempre disponible está activo, las apps pueden pedir escaneos y leer resultados aunque la wifi esté apagada. Ese método está marcado como obsoleto desde Android 10 [24]. La página de ayuda de Google no contiene esa frase. El código de AOSP no tiene versión fijada (rama `main`, 25 de octubre de 2026) [10].
- **Identificadores de Google.** Google afirma que no asocia los datos a una cuenta [1].
- **Las antenas.** La red sabe en qué celda estás y con qué timing advance [17], pero no hay fuente primaria consultada con cifras de precisión, ni sobre el registro continuo de posición por el operador. Wikipedia, la fuente que se cita, es secundaria [17].
- **Ley 25/2007.** Obliga a conservar durante doce meses la etiqueta de localización (identificador de celda) al inicio de la comunicación y los datos que permiten fijar la localización de la celda. El plazo puede variar entre seis meses y dos años por reglamento. La cesión exige autorización judicial [19]. Es la celda de las comunicaciones (llamadas, mensajes, datos), no un registro continuo de por dónde vas. El texto consolidado consultado es de 2014; su vigencia tras la sentencia del TJUE de 2014 no se ha comprobado.
- **El 112.** Desde el AML (Advanced Mobile Location), el móvil que llama al 112 calcula su posición con GPS, wifi y antenas y la envía al centro de emergencias, con una precisión de unos 15 a 20 metros según el Gobierno Vasco [29]. En Android lo implementa Emergency Location Service, que puede activar la ubicación para calcular la posición de emergencia y calcula la posición en el propio terminal [30]. Es un mecanismo aparte, que solo actúa en llamadas y SMS de emergencia. Las fuentes consultadas no cubren qué ocurre con el modo avión puesto.
- **BeaconDB y Mozilla.** BeaconDB es una base colaborativa y experimental, con cobertura desigual [15]. Mozilla anunció la retirada de su servicio el 13 de marzo de 2024 (claves nuevas, 27 de marzo sin envíos, 12 de junio claves de terceros, 31 de julio repositorio archivado) [16].
- **Historial de ubicaciones.** Google Maps lanzó "Your Timeline" el 21 de julio de 2015 [26]. El 13-14 de agosto de 2018 una investigación de AP, confirmada por investigadores de Princeton, halló que servicios de Google seguían guardando ubicaciones aunque se pausara el Historial de ubicaciones [25]. En noviembre de 2022 Google acordó pagar 391,5 millones de dólares a 40 estados de EE. UU., en una investigación abierta en 2018 tras el informe de AP [27]. El 12 de diciembre de 2023 Google anunció que Timeline se guardaría en el dispositivo, que las copias irían cifradas "para que nadie pueda leerlas, ni Google", y que el borrado automático por defecto para quien lo active pasaba de 18 a 3 meses [21]. Maps confirma que los datos de Timeline vienen del dispositivo y que, si haces copia, guarda una copia cifrada en sus servidores [22]. El traspaso fue gradual durante 2024. La prensa situó el borrado en servidores entre noviembre y diciembre de 2024, con un límite de 90 días [23].

## Qué puedes hacer

1. **Apaga la wifi y el Bluetooth al salir de casa.** Sin ellos, el móvil no escucha a los vecinos. Dentro del modo avión se pueden volver a encender, y el móvil recuerda lo que dejaste activado [11].
2. **Desactiva el escaneo de wifi y de Bluetooth.** En Android, Ubicación, Servicios de ubicación, "Wi-Fi scanning" y "Bluetooth scanning" [9].
3. **Revisa qué apps tienen ubicación precisa.** En el laboratorio había 57 contando las del sistema. Android exige ese permiso para escanear wifis [5].
4. **Si tienes router, saca su red del mapa.** Termina el nombre de la red en `_nomap`. Google lo documenta como opt-out y anima a otros proveedores a respetarlo [14]. Apple lo admite en su página de privacidad [3]. No funciona con redes ocultas [3]. Solo evita que tu punto de acceso entre en la base, no que tu móvil escuche los de los demás [14].
5. **Revisa Timeline y su borrado automático** en Mi actividad. Puedes desactivarlo o borrarlo en cualquier momento [22].
6. **Asume que la radio móvil sigue conectada a la red mientras tengas cobertura y no actives el modo avión.** El modo avión la apaga [12].

## Fuentes

1. Google, Manage your Android device's location settings. <https://support.google.com/accounts/answer/3467281>
2. Google Maps Help, Find and improve your location's accuracy. <https://support.google.com/maps/answer/2839911>
3. Apple, About privacy and Location Services (mayo de 2026). <https://support.apple.com/en-us/102515>
4. Apple Legal, Location Services and Privacy (11 feb 2026). <https://www.apple.com/legal/privacy/data/en/location-services/>
5. Android Developers, Wi-Fi scanning overview (23 oct 2026). <https://developer.android.com/develop/connectivity/wifi/wifi-scan>
6. Android Developers, Wi-Fi location, ranging with RTT. <https://developer.android.com/develop/connectivity/wifi/wifi-rtt>
7. Android Developers, fused location provider. <https://developer.android.com/develop/sensors-and-location/location/retrieve-current>
8. Android Developers, permisos Bluetooth. <https://developer.android.com/develop/connectivity/bluetooth/bt-permissions>
9. Google, Manage your Pixel phone's location settings. <https://support.google.com/pixelphone/answer/3467281>
10. AOSP, WifiSettingsStore.java y BluetoothManagerService.java (rama main, 25 oct 2026). <https://android.googlesource.com/platform/packages/modules/Wifi/+/refs/heads/main/service/java/com/android/server/wifi/WifiSettingsStore.java> y <https://android.googlesource.com/platform/packages/modules/Bluetooth/+/refs/heads/main/service/src/com/android/server/bluetooth/BluetoothManagerService.java>
11. Google, Keep your Android's wireless connections on in Airplane mode. <https://support.google.com/pixelphone/answer/12639358>
12. Apple, Use Airplane Mode (11 feb 2026). <https://support.apple.com/108785>
13. Rye y Levin, Surveilling the Masses with Wi-Fi-Based Positioning Systems, IEEE S&P 2024, arXiv 2405.14975. <https://arxiv.org/abs/2405.14975>
14. Google, Control access point inclusion in Google's Location services. <https://support.google.com/maps/answer/1725632>
15. BeaconDB. <https://beacondb.net>
16. Mozilla, Retiring the Mozilla Location Service, 13 mar 2024. <https://github.com/mozilla/ichnaea/issues/2065>
17. Wikipedia, E-CellID (fuente secundaria). <https://en.wikipedia.org/wiki/E-CellID>
18. Ogulenko et al., The fallacy of the closest antenna, arXiv 2109.02154, 2021. <https://arxiv.org/abs/2109.02154>
19. Ley 25/2007, de conservación de datos, arts. 3, 5 y 6 (BOE). <https://www.boe.es/buscar/act.php?id=BOE-A-2007-18243>
20. GPS.gov, GPS Accuracy (archivo). <https://archive.gps.gov/systems/gps/performance/accuracy/>
21. Marlo McGriff, Google, 12 dic 2023. <https://blog.google/products/maps/updates-to-location-history-and-new-controls-coming-soon-to-maps/>
22. Google Maps Help, Manage your Google Maps Timeline. <https://support.google.com/maps/answer/14169818>
23. Android Authority, 13 nov 2024 (fuente de prensa). <https://www.androidauthority.com/google-maps-timeline-deadline-3499115/>
24. Android Developers, WifiManager.isScanAlwaysAvailable (obsoleto desde API 29). <https://developer.android.com/reference/android/net/wifi/WifiManager>
25. AP, Google tracks your movements, like it or not (agosto de 2018, copia en ABC13). <https://abc13.com/technology/ap-google-tracks-your-movements-like-it-or-not/3953696/>
26. Google Maps blog, Your Timeline: Revisiting the world that you've explored, 21 jul 2015. <https://maps.googleblog.com/2015/07/your-timeline-revisiting-world-that.html>
27. CNBC, Google settles with 40 states over location tracking practices, 14 nov 2022. <https://www.cnbc.com/2022/11/14/google-settles-with-40-states-over-location-tracking-practices.html> y nota de prensa de Oregon (NAAG) <https://www.naag.org/wp-content/uploads/2025/08/2022.11.14-OR-Press-Release.pdf>
28. Android Developers, Location.getAccuracy. <https://developer.android.com/reference/android/location/Location>
29. Gobierno Vasco, sistema AML para el 112, 16 feb 2022. <https://www.euskadi.eus/gobierno-vasco/-/noticia/2022/el-gobierno-vasco-incorpora-el-sistema-de-localizacion-de-llamadas-de-personas-que-necesiten-auxilio-de-los-servicios-de-emergencias-advance-mobile-location-aml/>
30. Google, Emergency Location Service, fundamentals. <https://developers.google.com/android/els/fundamentals>
31. 3GPP TS 24.301, temporizadores de gestión de movilidad EPS (T3412; espejo iTecSpec). <https://www.itecspec.com/3gpp/24.301/s/10.2>
