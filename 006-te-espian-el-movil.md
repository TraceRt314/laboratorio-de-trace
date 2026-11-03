# Cómo saber si te espían el móvil (el *#21# no sirve)

Documentación técnica del episodio 006 de El Laboratorio de Trace: quién espía de verdad un móvil, qué códigos y señales no sirven para detectarlo, cómo se esconde una app espía en Android y dónde mirar en el móvil y en las cuentas.

Fuentes consultadas el 3 de noviembre de 2026.

## Quién te espía de verdad

**Spyware mercenario.** Apple lo describe como ataques dirigidos contra personas concretas. Dice que "la gran mayoría de usuarios nunca será objetivo", que los ataques cuestan "millones de dólares" y que se despliegan contra "un número muy reducido de personas, a menudo periodistas, activistas, políticos y diplomáticos". Desde 2021 ha notificado a usuarios en más de 150 países en total, pero no da el número de notificaciones ni atribuye los ataques [1]. Sus avisos son de "alta confianza", no de certeza absoluta [1].

**Casos documentados.**

- *Pegasus Project (18 de julio de 2021).* Una filtración de más de 50.000 números de teléfono seleccionados por clientes de NSO en más de 50 países desde 2016, con más de 80 periodistas de 17 medios en 10 países. NSO sostiene que es una lista de consultas HLR sin relación con los objetivos de Pegasus. Estar en la lista no es estar infectado. De los teléfonos que se analizaron en laboratorio se confirmó infección o intento en el 85 %, es decir 37, una muestra pequeña y no aleatoria de quienes aceptaron el análisis [2].
- *México.* Citizen Lab, con R3D, documentó en octubre de 2022 periodistas y un defensor de derechos humanos infectados con Pegasus entre 2019 y 2021, años después de que el presidente asegurara que el Gobierno ya no usaba ese spyware [3].
- *España.* CatalanGate (Citizen Lab, abril de 2022) identificó al menos 65 personas atacadas o infectadas, al menos 63 con Pegasus y 4 con Candiru, y al menos 2 con ambos. Citizen Lab no atribuye el ataque de forma concluyente, pero habla de "fuertes indicios circunstanciales" de relación con autoridades españolas. Una corrección posterior, del 23 de diciembre de 2022, retiró de la lista de atacados directos al eurodiputado Antoni Comín [4]. El 10 de mayo de 2022 el Gobierno informó de que el Centro Criptológico Nacional había revisado los terminales de todos los ministros y de que tres estaban infectados, los del presidente, la ministra de Defensa y el ministro del Interior, además de un intento fallido contra el ministro de Agricultura. Las infecciones de Defensa e Interior fueron en junio de 2021. El Gobierno no atribuyó los ataques [5].

No existe una cifra mundial fiable de víctimas de Pegasus. Los casos confirmados por laboratorios se cuentan por decenas o cientos en cada investigación [2][4].

**Stalkerware.** La Coalition Against Stalkerware lo define como software que permite a un usuario remoto monitorizar la actividad del dispositivo de otra persona "sin su consentimiento o sin una notificación explícita y persistente". No considera que haya consentimiento cuando la app solo exige acceso físico al móvil, desbloquearlo o iniciar sesión con usuario y contraseña para instalarla [6]. Quien la instala vincula el móvil de la víctima a sus propias credenciales para ver los datos de forma remota [7].

**Las cifras de Kaspersky.**

- *2023.* 31.031 usuarios afectados, frente a 29.312 en 2022. Top 10 mundial con Rusia 9.890, Brasil 4.186 (segundo), India 2.492, Irán 1.578, Turquía 1.063, Indonesia 871, EE. UU. 799, Yemen 624, México 592 (noveno) y Alemania 577 [8].
- *España y Latinoamérica en 2023.* España 257 (cuarta de Europa), Colombia 149 (tercera de Latinoamérica), Perú 138 (cuarto), Argentina 95 (quinto) y Chile 63 (séptimo) [8].
- *2024 y 2025.* Más de 34.000 usuarios afectados en esos dos años y unos 127.000 en cinco, con 33 familias nuevas y usuarios afectados en más de 160 países. Rusia, Brasil e India están entre los tres más afectados en 2025. La nota no da cifras por país ni por año para 2024 y 2025 por separado [9].
- *Qué miden.* Usuarios únicos de móviles con productos de seguridad de Kaspersky, no detecciones totales. Quien usa otro antivirus no entra [10]. Es un suelo, no el total mundial.

No hay una cifra abierta del porcentaje de víctimas de stalkerware que lo son por violencia de pareja. La literatura académica lo plantea como contexto principal [7], pero no como porcentaje. Que el stalkerware afecte a decenas de miles de usuarios de Kaspersky al año y que Pegasus se cuente por decenas o cientos de casos confirmados por investigación es una comparación de este documento, no de ninguna fuente.

## Los mitos que no sirven

**Los códigos del tipo `*#21#`.** Los códigos de servicios suplementarios los define el estándar 3GPP TS 22.030. La activación es `*SC*SI#`, la desactivación `#SC*SI#`, la interrogación `*#SC*SI#` y el borrado `##SC*SI#`. Su Anexo B asigna los códigos de desvío de llamadas [11].

| Código | Qué hace de verdad | Fuente |
|---|---|---|
| `*#21#` | Consulta el desvío incondicional (todas las llamadas) | [11][12][13] |
| `*#61#` | Consulta el desvío si no contestas | [11][12] |
| `*#62#` | Consulta el desvío si estás apagado o sin cobertura | [11][12][14] |
| `*#67#` | Consulta el desvío si estás ocupado | [11][12] |
| `##002#` | Borra todos los desvíos | [11][12] |
| `*#06#` | Muestra el IMEI del equipo | [15] |
| `*#*#4636#*#*` | Abre un menú de pruebas de Android, no estándar y no presente en todas las marcas | [16] |

- *No hay consulta de espionaje en la norma.* Los códigos preguntan a la red del operador por un ajuste de red. Que por eso no detecten una app instalada en el sistema es una inferencia a partir de la norma, no una cita literal de ella [11].
- *Los verificadores coinciden.* Maldita.es (27 de julio de 2021) explica que `*#21#` solo muestra si las llamadas están desviadas a otro número. Para desviarlas hace falta acceso al móvil o al área de cliente del operador, y quien desvía "no podría escuchar las conversaciones" ni llamar desde tu número [13]. PolitiFact (18 de marzo de 2024) llegó a la misma conclusión y probó el código en dos teléfonos de operadores distintos [17]. Dubawa (septiembre de 2022) confirma que `*#62#` muestra desvíos y `##002#` los cancela, sin confirmar espionaje alguno [14].
- *Los códigos varían por operador.* Orange España publica la tabla completa, con `##002#` para desactivar todos los desvíos [12]. Telcel (México) publica en su página `*21*NÚMERO#` para activar y `#21#` para quitar, y no incluye la consulta [18].
- *`*#*#4636#*#*`.* Abre información del teléfono, de la red y del Wi-Fi, y MakeUseOf avisa de que tocar la radio desde ese menú puede dejarte sin llamadas ni datos hasta reactivarla [16]. No es una prueba de nada relacionado con el espionaje.

**La trampa real del desvío, el WhatsApp.** Rahul Sasi (CloudSEK) documentó en mayo de 2022 que el atacante convence a la víctima de marcar un número que empieza por un código de desvío (por ejemplo `**67*` o `*405*` seguido del número del atacante). Después registra WhatsApp en su dispositivo, pide el código por llamada de voz y la llamada le llega a él. Por último activa la verificación en dos pasos para dejar fuera a la víctima. BleepingComputer (31 de mayo de 2022) comprobó que "generalmente funciona", lo confirmó en Verizon y Vodafone y señala que el atacante necesita un desvío incondicional, que el operador muestra un aviso al activarse el desvío y que la víctima recibe un SMS de que WhatsApp se registra en otro dispositivo. El remedio principal es la verificación en dos pasos [19]. Según WhatsApp, la única forma de sacar a quien se ha apoderado de la cuenta es volver a registrarla con el código de 6 dígitos y cambiar la contraseña no lo echa. Al registrar de nuevo se cierran todas las sesiones, y si pide un PIN de verificación en dos pasos que no conoces hay que esperar 7 días [20]. Chequeado (Argentina) describe una variante por buzón de voz, en la que el código cae al contestador y los estafadores acceden a él, y recomienda cambiar o quitar la clave del buzón con la operadora [21]. No se halló ninguna estadística pública fiable de cuentas secuestradas por este método. El caso documentado es el de Sasi de 2022.

**"Se calienta y gasta batería."** Apple dice que el dispositivo puede notarse más caliente al configurarlo, restaurar una copia o completar una actualización, sobre todo de versión mayor, y que "estas condiciones son normales" [22]. También lista causas normales de gasto de batería, como una actualización que termina en segundo plano, apps legítimas activas y poca cobertura, y recomienda esperar unos días tras actualizar [23]. En sentido contrario, la Coalition dice que un comportamiento inusual (batería, datos, notificaciones extrañas) puede ser señal de stalkerware "pero no tiene por qué serlo, y algunos stalkerware funcionan sin ninguno de estos efectos". La señal más común es que el agresor sabe demasiado sobre lo que haces [24]. INCIBE incluye en su lista de señales el menor rendimiento, la batería, las apps que se abren o cierran solas, los mensajes raros y el consumo alto de datos, y la presenta como una lista de preguntas, no como una prueba [25]. Un síntoma que es común sin spyware y puede faltar con spyware no sirve como detector.

**"Oigo ecos o clics."** No se encontró ningún estudio académico ni norma que mida si una intervención produce clics o ecos audibles. La explicación divulgativa los atribuye a pérdida de paquetes, cambios de antena, latencia o interferencias [26]. Esa fuente no es primaria y la conclusión prudente, que un clic o un eco no prueba que te escuchen ni lo contrario, es de este documento.

**"Me llegan mensajes raros."** Lo habitual es phishing. Aparte está la sextorsión, un timo concreto que describe INCIBE. Llega un correo que dice que tu dispositivo lleva meses infectado con software espía, que te han grabado con la cámara viendo porno y que enviarán el vídeo a tus contactos si no pagas en bitcoins en 48 horas. No hay ninguna infección ni ninguna grabación. No hay que pagar ni responder [27]. Un correo que pide dinero por un supuesto programa espía, sin esa amenaza sexual, sigue siendo una estafa o una extorsión, pero no es sextorsión.

**"El micrófono me escucha para los anuncios."** El estudio Panoptispy (PETS 2018, Northeastern) analizó 17.260 apps de cuatro tiendas. Tras el análisis dinámico de 9.100 apps, el 53 %, no encontró "ningún archivo de audio verdadero positivo". Sí halló bibliotecas de terceros que graban y suben capturas o vídeo de la pantalla sin permisos ni aviso. Appsee estaba en 33 apps de su muestra de Google Play, la app GoPuff grababa la pantalla y enviaba datos como el código postal, y la app SAHIC envió 45 capturas con búsquedas y mensajes mediante TestFairy. Google dijo haber revisado GoPuff y Appsee y "tomado las acciones adecuadas" [28]. Los autores declaran límites. Las pruebas dinámicas fueron en dos Nexus 5 con Android 4.4.4, solo Android, y pueden dar falsos negativos, así que la ausencia de audio en una muestra de 2018 no es prueba universal de hoy [28]. Aparte, 404 Media publicó en agosto de 2024 la presentación comercial de Cox Media Group sobre su "Active Listening", una afirmación comercial. Meta dijo que no usa el micrófono para anuncios, según TechSpot [29][30]. No se encontró ningún análisis técnico independiente que demuestre que funcionara a escala.

**"El punto verde me avisa de todo."** Desde iOS 14 aparece un punto naranja cuando una app usa el micrófono y uno verde cuando usa la cámara, sola o con micrófono [31]. El Centro de control indica qué app los ha usado recientemente [32]. En Android 12 y posteriores aparece un indicador verde arriba a la derecha, y al tocarlo se ve la app [33]. El AOSP considera el uso activo si está en marcha o tiene menos de 5 segundos [34]. Garantizan que una app normal que usa las APIs del sistema dispara el indicador, no que un sistema comprometido a nivel de kernel no pueda suprimirlo [34]. Jamf Threat Labs (19 de febrero de 2026) analizó el spyware Predator, que con un gancho en SpringBoard intercepta las actualizaciones del sensor antes de que lleguen a la interfaz y evita que aparezcan los puntos. Jamf aclara que no es una vulnerabilidad nueva y que exige un dispositivo ya comprometido por completo, con acceso al kernel [35].

**"Mi antivirus me protege del todo."** AV-Comparatives y la EFF (septiembre de 2025) probaron 13 productos con 17 casos de stalkerware en un solo Samsung Galaxy A36 con Android 15 sin root. Detectaron Malwarebytes el 100 %, Bitdefender, ESET, Kaspersky y McAfee el 94 %, Avast, Avira y F-Secure el 88 %, Norton y Sophos el 82 %, G Data el 65 % y Trend Micro el 59 %. Google Play Protect detectó el 53 %, nueve de 17. La muestra es pequeña, es un solo móvil y una instantánea, y Play Protect solo analiza apps instaladas [36]. En 2018, según el resumen del estudio de Chatterjee et al., un antivirus principal marcaba como mucho el 13 % de las apps de doble uso [7]. La prueba de 2025 mide casos de stalkerware, no apps de doble uso legítimas como un localizador familiar [36][7].

## Cómo se esconde una app espía en Android

**Quién la instala.** Hace falta el móvil desbloqueado y unos minutos, o las credenciales [6][7]. Por eso la primera defensa es el código de desbloqueo.

**El permiso de accesibilidad.** Android define un servicio de accesibilidad como una app que "inspecciona el contenido de la pantalla e interactúa con apps en nombre del usuario", y advierte de que es "una herramienta especializada" para asistencia general. Con `canRetrieveWindowContent` puede leer la interfaz y con `canPerformGestures` puede pulsar por ti [37]. Google Play prohíbe usar esa API en apps de monitorización [38], pero una app instalada fuera de la tienda no pasa por esa política.

**Otros tres permisos.**

- *Acceso a notificaciones.* Un `NotificationListenerService` recibe del sistema las notificaciones nuevas o eliminadas [39], lo que incluye mensajes y códigos de verificación. La página consultada no documenta cómo lo concede el usuario.
- *Administrador del dispositivo.* La API permite bloquear el equipo, borrarlo, forzar contraseña y desactivar la cámara, y "para desinstalar un admin de dispositivo, primero hay que anularlo como administrador". Android la marca como en desuso desde Android 9 [40].
- *Ubicación en segundo plano.* Se concede como "Permitir siempre" y aparece en el administrador de permisos [41].

**El icono.** Chatterjee et al. documentan que todas las apps espía analizadas que se distribuyen fuera de la tienda pueden configurarse para ocultar su icono del cajón de apps, y 2 de las 61 de la tienda también (Cerberus y TrackView). Android no obliga a mostrar icono [7].

**Doble uso.** El mismo estudio encontró "docenas" de herramientas abiertamente espía, pero la mayoría de las apps relevantes son de doble uso (seguridad infantil, antirrobo, localizar amigos), fáciles de reutilizar para espiar a una pareja [7]. Google Play solo permite apps de monitorización diseñadas y comercializadas para que padres vigilen a sus hijos o empresas gestionen empleados, y exige declararlas con la marca `isMonitoringTool` [42].

**Android 13 y los ajustes restringidos.** En apps instaladas fuera de la tienda, Android bloquea por defecto ciertos permisos (el ejemplo de Google es accesibilidad) hasta que el usuario elige "Permitir ajustes restringidos". Google explica que con ese acceso la app "puede leer el contenido de tu pantalla e interactuar con apps" [43]. Quien instala la app tiene que dar ese paso en el móvil.

## El experimento del laboratorio

Se hizo con el emulador oficial de Android (Android 15, imagen de Google con Play Store) en el ordenador del autor. No se usó ningún móvil real.

La app es una demostración propia, "Eco (laboratorio de Trace)", de unas pocas líneas. Es un servicio de accesibilidad sin actividad de lanzador, por eso no tiene icono, que escribe en el registro local del sistema (logcat) el texto que se teclea y la app que se abre. No envía nada fuera del emulador y no se publica.

- **Instalación.** Se instaló por adb y se activó la accesibilidad desde adb, simulando a alguien con el móvil desbloqueado en la mano.
- **Lo que se ve.** Al escribir "Quedamos a las 8" en Mensajes, el registro mostró cada letra, desde `tecleas en com.google.android.apps.messaging: [Quedamos a l]` hasta `[Quedamos a las 8]`.
- **Sin icono.** Ni en el escritorio ni en el cajón de apps.
- **Ajustes › Accesibilidad.** En Android 15 la demo aparece arriba del todo, en "Aplicaciones descargadas", como "Activado".
- **El script de revisión.** `revisa.py` es de solo lectura, funciona por adb y revisa los servicios de accesibilidad activos, los administradores del dispositivo, el acceso a notificaciones, las apps de terceros sin icono de lanzador, las apps instaladas por un instalador que no es Play Store y el último uso de micrófono, cámara y ubicación (appops). Marcó la demo en tres apartados, accesibilidad, sin icono en el escritorio e instalada fuera de la tienda [44].
- **Cómo se usa.** Con la depuración USB activada, `python3 revisa.py` con el móvil conectado. No cambia nada en el móvil [44].

Límites. Es una demo propia y un solo emulador. Las apps espía comerciales pueden comportarse distinto. El script no detecta spyware mercenario ni el espionaje por cuenta (WhatsApp vinculado, iCloud, ubicación compartida). Que no salga nada no garantiza que no haya nada.

## iPhone y tus cuentas

**iPhone.** Apple basa la seguridad de las apps en "distribución centralizada, firma de código y un sandbox estricto" [45]. Chatterjee et al. encontraron que las apps de doble uso que existen en Android y en iOS funcionan distinto en iOS, por su modelo de permisos más restrictivo. TrackView en iOS no oculta el icono ni usa la cámara a escondidas, y en Android sí. En iOS hallaron 2.724 apps, y de una muestra de 500, 97 (20 %) eran capaces de vigilancia de pareja, frente al 28 % en Android [7]. Eso es el estado de 2018. La guía de seguridad personal de Apple lista las vías que revisar, que son el acceso a la cuenta de Apple, el uso compartido de ubicación, y las apps y perfiles de configuración [46]. Que sea la vía más frecuente es una inferencia a partir de esa estructura, no una estadística.

- *Perfiles de configuración.* Escuelas y empresas usan perfiles y herramientas MDM que pueden dar acceso a datos o ubicación. Se revisan en Ajustes › General › VPN y gestión de dispositivos. Si no hay perfiles, no hay gestión instalada. Borrar un perfil elimina sus ajustes, apps y datos [47].
- *Dispositivos de la cuenta.* Ajustes › tu nombre, bajando hasta la lista de dispositivos, y "Eliminar de la cuenta". Un dispositivo eliminado pierde acceso a iCloud y Buscar y deja de mostrar códigos de verificación [48].
- *Copia en iCloud.* Si el iPhone hace copia en iCloud sin que la hayas activado tú, alguien puede haberlo hecho (Ajustes, tu nombre, tu dispositivo, copia de iCloud) [24]. La guía de Apple incluye secciones sobre proteger la cuenta y la verificación en dos pasos, pero no se leyó el cuerpo que explica el mecanismo.
- *Comprobación de seguridad (Safety Check).* Exige iOS 16 o posterior y verificación en dos pasos. Tiene el restablecimiento de emergencia, que corta de golpe todo lo compartido, y "Gestionar compartición y acceso", persona por persona y app por app, con revisión de los dispositivos conectados a la cuenta. Ruta, Ajustes › Privacidad y seguridad › Comprobación de seguridad [49]. No revisa cuentas ajenas a Apple ni redes sociales, no cambia todo, y algunas opciones no están disponibles con Tiempo de uso o un perfil MDM. Tiene botón de salida rápida [50]. La ruta en iOS 26 y el nombre exacto en español en cada país no están verificados.
- *Buscar.* En la pestaña Personas se toca el nombre y "Dejar de compartir mi ubicación". Borrar la app Buscar no detiene la compartición, y la otra persona puede notar que dejaste de compartir [51].

**Cuentas, vale para Android y iPhone.**

- *WhatsApp.* En Android, menú ⋮ › Dispositivos vinculados, tocar el dispositivo y Cerrar sesión [52]. En iPhone, Ajustes › Dispositivos vinculados [53]. Un ordenador que no es tuyo permite leer los chats desde ahí. WhatsApp advierte de que activar la verificación en dos pasos o una contraseña no echa a quien ya está dentro, y que primero hay que registrar de nuevo la cuenta [54].
- *Google.* Cuenta de Google › Seguridad e inicio de sesión › Tus dispositivos › Gestionar todos los dispositivos, o google.com/devices. Si no estás seguro de que una sesión sea tuya, ciérrala. Puede mostrar "sesiones" en lugar de dispositivos, y es normal tener varias por dispositivo [55].
- *Ubicación compartida en Google Maps.* Foto de perfil › Compartir ubicación, tocar el perfil y Detener [56]. A nivel de Android, Ajustes › Ubicación › Servicios de ubicación › Compartir ubicación en Google, con "Dejar de compartir" junto a cada persona. Quien recibe ve tu nombre, foto, ubicación en tiempo real y estado de batería [57].

## Si encuentras una

**Antes de borrarla.** La Coalition recomienda crear un plan de seguridad, con un dispositivo más seguro y un programa de ayuda a supervivientes de confianza. Quitar la app "puede ser detectada por el abusor y podría aumentar el abuso y el acoso", así que solo debe intentarse si es seguro, y al quitarla también se van las pruebas [24]. Hay que buscar ayuda desde un dispositivo al que el agresor nunca haya tenido acceso físico, y en peligro inmediato llamar a las autoridades locales [58]. INCIBE describe un caso real cuyos pasos fueron reunir pruebas, denunciar y desinstalar [59]. La guía general del NCSC dice que en móviles lo más seguro ante una infección es un restablecimiento de fábrica, pero es una guía de malware, no de stalkerware, y borra las pruebas [60].

**Líneas de ayuda verificadas.** El stalkerware le puede pasar a cualquiera, y quien espía puede ser una pareja, una expareja o un familiar. En peligro inmediato, la policía o el número de emergencias de tu país.

- *España, 017.* La línea de ayuda en ciberseguridad de INCIBE, gratuita y confidencial, de 8 a 23 horas los 365 días, para ciudadanos, empresas, menores y su entorno. Tiene WhatsApp en el 900 116 117 [72].

Las tres siguientes son líneas de violencia contra las mujeres. En el vídeo se dieron como si fueran generales, y no lo son (está en la fe de erratas).

- *España, 016.* Gratuito y confidencial, con información y apoyo psicosocial 24 horas, asesoramiento jurídico de 8 a 22 horas y 53 idiomas. Tiene WhatsApp en el 600 000 016 (solo mensajes) y correo 016-online@igualdad.gob.es. La página dice que las llamadas no se guardan en el registro de llamadas en ciertos modelos, pero no que no aparezcan en la factura [61].
- *México, 079 opción 1.* Línea de las Mujeres, 24 horas, 365 días, gratuita y confidencial. El 911 es la emergencia general [62].
- *Argentina, 144.* Gratuita, 24 horas, 365 días en sus canales, con WhatsApp en el 11-2771-6463 [63].
- *Chile, Colombia y Perú.* No se pudo abrir la página oficial de ninguna de las tres líneas, así que no se dan números. Consulta el directorio internacional de Lila.help, que es el que cita la Coalition [64][58].

## Matices y límites

- **Las cifras de Kaspersky son de usuarios de Kaspersky.** Cuentan usuarios únicos, no población, y las cifras de 2023 son las últimas con desglose por país que se pudieron abrir. El informe completo de 2024 y 2025 no se encontró [8][9][10].
- **Pegasus no es lo normal.** Aun así existe, y los casos de México y España son reales y están documentados [3][4][5]. Quien no está en el perfil de periodista, activista, político o diplomático tiene un riesgo mucho más cercano, que es alguien con acceso al móvil o a la cuenta [1].
- **El estudio de Cornell es de 2018.** La prueba de antivirus de 2025 mejora mucho los datos, pero es una instantánea de 17 casos en un solo móvil [7][36].
- **Herramientas forenses.** MVT (Amnistía Internacional) es una herramienta de línea de comandos para análisis forense consensuado y no está pensada para la autoevaluación de usuarios finales. Sus indicadores públicos "pueden pasar por alto trazas recientes y dar una falsa sensación de seguridad" [65]. stalkerware-indicators, de Echap, reúne indicadores de 176 apps y no es una app para el usuario final, y sus autores advierten de que no encontrar coincidencias no significa que no haya stalkerware [66]. TinyCheck, de Kaspersky, necesita una Raspberry Pi y está pensado para ONG y policía [67].
- **Reiniciar.** CISA dice que apagar y reiniciar el dispositivo "puede eliminar" algún spyware y recomienda hacerlo cada semana. No es una garantía [68].
- **Rutas de menú.** Los nombres cambian según fabricante y versión. La ruta de Ajustes › Accesibilidad para apps descargadas, y la de administradores del dispositivo (Ajustes › Seguridad y privacidad › Más ajustes de seguridad › Apps de administración del dispositivo) no están respaldadas por un documento oficial de Google, así que la ruta puede cambiar según el fabricante. Las del experimento son las del emulador con Android 15.
- **Lo que no se verificó y por eso no se usa.** El desglose por año de TrackView y Eyezy, la cifra de apps de creepware retiradas por Google, el número de países de las alertas de Apple de 2026, la política de Google de 2020 sobre icono visible y notificación persistente, la estimación de la Coalition de casi un millón de casos al año, que Pegasus se venda solo a gobiernos, el mecanismo de las copias de iCloud, y cualquier estadística de secuestros de WhatsApp por desvío.

## Qué puedes hacer

1. **Cambia tu código de desbloqueo si alguien lo sabe.** Es la primera defensa, porque el consentimiento no cuenta aunque otra persona conozca el código [6].
2. **Revisa la accesibilidad.** Ajustes › Accesibilidad, y mira si en las apps descargadas hay alguna que no reconoces con el interruptor activado. La ruta puede cambiar según el fabricante [37].
3. **Revisa quién lee tus notificaciones.** Ajustes › Apps › Acceso especial a apps › Acceso a notificaciones. Quitarlo a apps legítimas puede romper cosas como el autorrelleno de códigos SMS [69].
4. **Mira los administradores del dispositivo y la ubicación.** La ruta habitual para los administradores del dispositivo no está verificada en una fuente oficial (ver Matices y límites), y la API exige que el usuario la active [40]. En Ajustes › Seguridad y privacidad › Privacidad › Administrador de permisos › Ubicación, mira qué apps tienen "Permitir siempre" [41]. El Panel de privacidad (Ajustes › Seguridad y privacidad › Panel de privacidad, Android 12 o superior) muestra qué apps accedieron a ubicación, cámara y micrófono [70].
5. **Activa Google Play Protect y no te fíes solo de él.** Play Store › icono de perfil › Play Protect › Ajustes › "Analizar apps con Play Protect". Está activado por defecto, y detectó el 53 % en la prueba [71][36].
6. **En WhatsApp, mira Dispositivos vinculados y activa la verificación en dos pasos.** Es el remedio contra el secuestro por desvío [52][19].
7. **Revisa tus dispositivos de Google y con quién compartes la ubicación.** En tu cuenta de Google, en Google Maps y en Buscar [55][56][51].
8. **En iPhone, mira los perfiles, los dispositivos de la cuenta y la Comprobación de seguridad.** Ajustes › General › VPN y gestión de dispositivos, Ajustes › tu nombre, y Ajustes › Privacidad y seguridad › Comprobación de seguridad [47][48][49].
9. **Si tienes un ordenador, pasa `revisa.py`.** Conecta tu móvil por cable con la depuración USB activada. Solo lee, por adb, y no cambia nada en el móvil. Que no salga nada no garantiza que no haya nada [44].
10. **Reinicia el móvil una vez a la semana.** Lo recomienda CISA, aunque no es una garantía [68].
11. **Si encuentras una app espía, no la borres sin un plan.** Pide ayuda desde un teléfono que esa persona no haya tocado nunca y llama a las líneas de la sección anterior [24][58].

## Fuentes

1. Apple, About Apple threat notifications and protecting against mercenary spyware (13 ago 2026). <https://support.apple.com/en-us/102174>
2. Forbidden Stories, About the Pegasus Project. <https://forbiddenstories.org/about-the-pegasus-project/>
3. Citizen Lab, New Pegasus Spyware Abuses Identified in Mexico (oct 2022). <https://citizenlab.ca/2022/10/new-pegasus-spyware-abuses-identified-in-mexico/>
4. Citizen Lab, CatalanGate (abril de 2022). <https://citizenlab.ca/2022/04/catalangate-extensive-mercenary-spyware-operation-against-catalans-using-pegasus-candiru/>
5. La Moncloa, Rueda de prensa tras el Consejo de Ministros, 10 mayo 2022 (PDF). <https://www.lamoncloa.gob.es/consejodeministros/ruedas/Documents/2022/Consejo%202022.05.10.pdf>
6. Coalition Against Stalkerware, Information for tech companies. <https://stopstalkerware.org/information-for-tech-companies/>
7. Chatterjee et al., The Spyware Used in Intimate Partner Violence, IEEE S&P 2018. <https://www.cs.cornell.edu/~rahul/papers/IPV_Spyware.pdf>
8. Kaspersky Securelist, The State of Stalkerware in 2023. <https://securelist.com/state-of-stalkerware-2023/112135/>
9. Kaspersky, Half of adults have experienced tech-enabled abuse (nota de prensa, 19 may 2026). <https://www.kaspersky.com/about/press-releases/kaspersky-half-of-adults-have-experienced-tech-enabled-abuse-but-most-dont-recognize-it>
10. Kaspersky, Tech-enabled abuse report page. <https://lp.kaspersky.com/global/tech-enabled-abuse-1>
11. 3GPP TS 22.030, cláusula 6.5.2 y Anexo B (vista iTecSpec). <https://itecspec.com/3gpp/22.030/s/annex-b>
12. Orange, Desvía las llamadas que recibes en tu móvil a otro número. <https://ayuda.orange.es/empresas/mi-orange/activar-servicios/777-desvia-las-llamadas-que-recibes-en-tu-movil-a-otro-numero>
13. Maldita.es, No, marcando *#21# en tu móvil no verás si tu teléfono está siendo rastreado, sino el desvío de llamadas (27 jul 2021). <https://maldita.es/malditobulo/20210727/21-telefono-rastreado-llamadas-desviadas/>
14. Dubawa, TRUE, *#62# will show diverted calls on your phone (sep 2022). <https://dubawa.org/true-62-will-show-diverted-calls-on-your-phone/>
15. 3GPP TS 22.030, cláusula 6.7, Presentation of IMEI (vista iTecSpec). <https://itecspec.com/3gpp/22.030/s/6.7>
16. MakeUseOf, Android's hidden Testing menu (fuente secundaria). <https://www.makeuseof.com/android-testing-menu-shortcode-trick/>
17. PolitiFact, Al marcar *#21#, no sabrás si tu teléfono está siendo espiado, solo si tus llamadas son desviadas (18 mar 2024). <https://www.politifact.com/factchecks/2024/mar/18/facebook-posts/al-marcar-21-no-sabras-si-tu-telefono-esta-siendo>
18. Telcel, Llamadas, transferencia de llamadas. <https://www.telcel.com/personas/servicios/llamadas-y-mensajeria/llamadas>
19. BleepingComputer, Hackers steal WhatsApp accounts using call forwarding trick (31 may 2022). <https://www.bleepingcomputer.com/news/security/hackers-steal-whatsapp-accounts-using-call-forwarding-trick/>
20. WhatsApp Help Center, How to recover a compromised account. <https://faq.whatsapp.com/general/account-and-profile/stolen-accounts/?lang=en>
21. Chequeado, Cómo pueden estafarte por WhatsApp y cómo podés evitarlo. <https://chequeado.com/?p=55247>
22. Apple, If your iPhone or iPad gets too hot or too cold. <https://support.apple.com/en-us/118431>
23. Apple, If the battery in your iPhone or iPad drains too quickly. <https://support.apple.com/en-us/120745>
24. Coalition Against Stalkerware, Detection, removal and prevention. <https://stopstalkerware.org/stalkerware-detection-removal-and-prevention/>
25. INCIBE, Qué hacer si sospecho que están monitorizando mi móvil. <https://www.incibe.es/ciudadania/blog/que-hacer-si-sospecho-que-estan-monitorizando-mi-movil>
26. Futura-Sciences, ¿Clics, ecos o zumbidos? Más habituales de lo que piensas (fuente divulgativa). <https://www.futura-sciences.com/es/?p=22655>
27. INCIBE, Nueva campaña de sextorsión, nadie ha instalado un software espía en tu dispositivo. <https://www.incibe.es/ciudadania/avisos/nueva-campana-de-sextorsion-nadie-ha-instalado-un-software-espia-en-tu>
28. Pan et al., Panoptispy, PoPETs 2018. <https://petsymposium.org/popets/2018/popets-2018-0030.pdf>
29. 404 Media, Here's the Pitch Deck for Active Listening Ad Targeting (26 ago 2024). <https://www.404media.co/heres-the-pitch-deck-for-active-listening-ad-targeting/>
30. TechSpot, Marketing firm admits to eavesdropping on conversations via phone microphones (fuente secundaria). <https://www.techspot.com/news/104566-marketing-firm-admits-eavesdropping-conversations-phone-microphones-serve.html>
31. Apple, About the orange and green indicators. <https://support.apple.com/en-us/108331>
32. Apple, Control access to hardware features on iPhone. <https://support.apple.com/guide/iphone/control-access-to-hardware-features-iph168c4bbd5/ios>
33. Android Help, Check if your camera or microphone is on. <https://support.google.com/android/answer/13532937?hl=en>
34. Android Open Source Project, Indicadores de privacidad. <https://source.android.com/docs/core/permissions/privacy-indicators>
35. Jamf Threat Labs, How Predator Spyware Defeats iOS Recording Indicators (19 feb 2026). <https://www.jamf.com/blog/predator-spyware-ios-recording-indicator-bypass-analysis/>
36. AV-Comparatives, Stalkerware Test 2025. <https://av-comparatives.org/tests/stalkerware-test-2025/>
37. Android Developers, Create your own accessibility service. <https://developer.android.com/guide/topics/ui/accessibility/service>
38. Google Play Console Help, AccessibilityService API policy. <https://support.google.com/googleplay/android-developer/answer/10964491>
39. Android Developers, NotificationListenerService. <https://developer.android.com/reference/android/service/notification/NotificationListenerService>
40. Android Developers, Device administration overview. <https://developer.android.com/work/device-admin>
41. Android Help, Change app permissions. <https://support.google.com/android/answer/9431959?hl=en>
42. Google Play Console Help, Monitoring tool declaration. <https://support.google.com/googleplay/android-developer/answer/12955211?hl=en>
43. Android Help, Learn about restricted settings. <https://support.google.com/android/answer/12623953?hl=en>
44. Laboratorio de Trace, herramientas/revisa.py. <https://github.com/TraceRt314/laboratorio-de-trace/blob/main/herramientas/revisa.py>
45. Apple Platform Security, App security overview. <https://support.apple.com/guide/security/app-security-overview-sec35dd877d0/web>
46. Apple, Personal Safety User Guide. <https://support.apple.com/guide/personal-safety/welcome/web>
47. Apple, Review and delete configuration profiles. <https://support.apple.com/guide/personal-safety/review-and-delete-configuration-profiles-ips327569a75/web>
48. Apple, Review devices signed in to your Apple Account. <https://support.apple.com/en-us/102649>
49. Apple, Safety Check for an iPhone with iOS 16 or later. <https://support.apple.com/guide/personal-safety/safety-check-iphone-ios-16-ips2aad835e1/web>
50. Apple, Safety Check FAQ. <https://support.apple.com/guide/personal-safety/safety-check-faq-ips5f85e089f/web>
51. Apple, Find My and location sharing. <https://support.apple.com/en-us/guide/personal-safety/ips05ede4573/web>
52. WhatsApp Help Center, How to unlink a device. <https://faq.whatsapp.com/834124628020911/?locale=en_US&cms_platform=android>
53. WhatsApp Help Center, How to unlink a device (iPhone). <https://faq.whatsapp.com/834124628020911/?locale=en_US&cms_platform=iphone>
54. WhatsApp Help Center, Account security tips. <https://faq.whatsapp.com/1095301557782068/?locale=en_US>
55. Ayuda de Cuenta de Google, Ver los dispositivos con acceso a la cuenta. <https://support.google.com/accounts/answer/3067630?hl=es>
56. Google Maps Help, Share your real-time location with others in Google Maps. <https://support.google.com/maps/answer/15437054?hl=en&co=GENIE.Platform%3DAndroid>
57. Ayuda de Cuenta de Google, Gestionar los ajustes de Compartir ubicación. <https://support.google.com/accounts/answer/9363497?hl=es&co=GENIE.Platform%3DAndroid>
58. Coalition Against Stalkerware, Resources. <https://stopstalkerware.org/resources/>
59. INCIBE, Víctima de violencia de género descubre una app de rastreo instalada en su móvil. <https://www.incibe.es/linea-de-ayuda-en-ciberseguridad/casos-reales/victima-de-violencia-de-genero-descubre-una-app-de-rastreo-instalada-en-su-movil>
60. NCSC, How to recover an infected device. <https://www.ncsc.gov.uk/guidance/hacked-device-action-to-take>
61. Ministerio de Igualdad, Teléfono 016. <https://violenciagenero.igualdad.gob.es/informacionUtil/recursos/telefono016/home.htm>
62. Gobierno de México, Línea de las Mujeres 079 opción 1 (boletín 119/2026, 21 jul 2026). <https://www.gob.mx/mujeres/prensa/si-vives-violencia-de-genero-no-estas-sola-llama-a-la-linea-de-las-mujeres-079-opcion-1-y-recibe-acompanamiento-integral?idiom=es>
63. Argentina.gob.ar, Línea 144. <https://www.argentina.gob.ar/generos/linea-144>
64. Lila.help, directorio internacional de líneas de ayuda. <https://lila.help/>
65. MVT, Mobile Verification Toolkit. <https://github.com/mvt-project/mvt>
66. Echap, stalkerware-indicators. <https://github.com/AssoEchap/stalkerware-indicators>
67. Coalition Against Stalkerware, TinyCheck. <https://stopstalkerware.org/?p=828>
68. CISA, Follow Cybersecurity Best Practices to Protect Yourself from Tracking Technologies and Spyware. <https://www.cisa.gov/resources-tools/training/follow-cybersecurity-best-practices-protect-yourself-tracking-technologies-and-spyware>
69. Google Messages Help, Control message storage & access. <https://support.google.com/messages/answer/10252674?hl=en-419>
70. Android Help, Manage permissions from the privacy dashboard. <https://support.google.com/android/answer/13530434?hl=en>
71. Android Help, Use Google Play Protect. <https://support.google.com/android/answer/2812853?hl=en>
72. INCIBE, Línea de Ayuda en Ciberseguridad 017. <https://www.incibe.es/linea-de-ayuda-en-ciberseguridad>
