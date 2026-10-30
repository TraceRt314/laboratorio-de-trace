# Saben quién eres aunque borres las cookies y uses incógnito

Documentación técnica del episodio 005 de El Laboratorio de Trace: cómo una web reconoce tu navegador sin guardar nada en él, qué miden los estudios y qué navegadores se defienden.

Fuentes consultadas el 29 de octubre de 2026.

## Cómo funciona por dentro

**Qué es.** La huella del navegador es un identificador que un sitio calcula combinando características observables del navegador y del dispositivo, sin guardar nada en él. El Grupo de Privacidad del W3C distingue la huella pasiva (cabeceras e IP) de la activa, en la que el sitio ejecuta código y observa más, como el tamaño de ventana, las fuentes o los sensores. Esa nota admite que eliminarla del todo es "implausible" con medios técnicos generales y que sus recomendaciones son mitigaciones, no soluciones [1]. Un estudio de 2025 la califica de técnica encubierta e involuntaria, fuera de cualquier protocolo estándar y sin consentimiento [2].

**Las señales.**

- *Cabeceras.* User agent, idiomas aceptados y codificaciones. Fueron las primeras que usó Panopticlick [3]. Chrome redujo el detalle del user agent y ofrece el resto bajo petición con Client Hints. En 2025 pedían client hints de alta entropía el 3,3 % de los sitios de escritorio y el 5,1 % de los móviles [10].
- *Pantalla, zona horaria, idioma, plugins y fuentes.* Son los atributos clásicos de AmIUnique, que usó 17 en total [4]. Los plugins casi han desaparecido y con ellos una gran fuente de entropía [4].
- *Canvas.* El sitio dibuja un texto o una escena y lee los píxeles. Las diferencias de GPU, sistema, fuentes y suavizado dan imágenes ligeramente distintas. En el trabajo original de Mowery y Shacham (2012) hubo 116 resultados distintos en 294 experimentos, 5,73 bits de entropía [7].
- *WebGL.* En el mismo trabajo, el test dio 4,30 bits en 300 muestras y 51 grupos [7].
- *Audio.* El sitio genera una señal con un oscilador y la procesa. Las diferencias de hardware y software dan un valor estable por equipo y navegador. Englehardt y Narayanan lo midieron a escala en 2016 [8].
- *Otras.* Núcleos de CPU, memoria, batería, almacenamiento y las extensiones instaladas, comprobando si se puede cargar un recurso interno de cada una [17]. A esto se suma la IP y la subred. Eckersley estimó que no más de 15 o 20 bits identificarían casi siempre un navegador conocidas su IP y su subred [3].

**Por qué sirve un hash.** El sitio concatena los valores, calcula un hash y lo guarda. La próxima vez repite el cálculo y lo busca. Basta con que la combinación sea rara. El hash es frágil, porque si cambia un atributo cambia el resultado, y por eso los vendedores comparan huellas parecidas [6].

**Entropía.** Un bit parte en dos a un conjunto de personas. Con 33 bits independientes, 2^33 son unos 8.590 millones, más que la población mundial. Narayanan usó esa idea con 6.600 millones de personas, una cifra antigua [12]. El W3C usa la misma regla, con algo más de treinta bits [1]. La huella de Panopticlick tenía al menos 18,1 bits (18,8 con Flash o Java) [3]. Los bits solo se suman si las señales son independientes. La AEPD pone el ejemplo de la fecha de nacimiento, 8,5 bits, a la que el signo zodiacal no añade nada [11]. 33 bits es un tope teórico, no una medida.

## El experimento del laboratorio

Una tienda de juguete en local (`lab/huella/`) calcula la huella con el mismo tipo de señales que usan los scripts reales y la envía a un servidor. El servidor reconoce al visitante por cookie y, si no la trae, por huella. Las señales son user agent, pantalla, zona horaria, idioma, núcleos, memoria, renderer de WebGL, 50 fuentes comprobadas por ancho de texto, y un hash del canvas y del audio.

- **Primera visita con Chromium.** Un navegador recién abierto, sin cookies. El servidor lo apuntó como visitante 1.
- **Segunda visita.** Se cierra el navegador y se abre de nuevo sin nada guardado. Esto simula el efecto de una ventana privada, pero no es una ventana de incógnito real de Chrome. El servidor respondió "te reconozco, visitante 1, por tu huella", sin cookie. La huella salió igual.
- **Audio.** La suma de 500 muestras del oscilador dio 172,67 en Chromium y 75,83 en Firefox. El mismo equipo da números distintos.
- **Firefox normal.** Huella distinta y visitante nuevo. El renderer de la tarjeta gráfica salió genérico ("Intel HD Graphics, or similar") y la memoria quedó oculta.
- **Firefox en Estricta.** Se activa solo `privacy.fingerprintingProtection`, que es lo que pone la opción Estricta del menú (aleatorización del canvas y menos información del sistema) [30]. La zona horaria y los núcleos siguen siendo los reales (Europe/Madrid, 8), pero el canvas sale distinto en cada sesión, así que la huella cambia y el servidor lo trató las tres veces como visitante nuevo. Si además se activa `privacy.resistFingerprinting`, Firefox falsea también la zona horaria y los núcleos, pero Mozilla lo describe como un modo no soportado que puede romper webs y no viene en Estricta [30].

Límites. Es un servidor propio, con una sola máquina y unas versiones concretas, y la tienda usa un conjunto de señales elegido por el autor. No demuestra que un sitio real, con su propio script, consiga lo mismo. Muestra el mecanismo.

## Qué dicen los estudios

- **Eckersley (EFF, 2010).** 470.161 navegadores de visitantes voluntarios de Panopticlick, una muestra sesgada hacia gente informada. El 83,6 % tenía una huella única y otro 5,3 % la compartía con una sola persona. Con Flash o Java, el 94,2 % era único. De 8.833 usuarios con cookies que volvieron pasadas 24 horas, el 37,4 % había cambiado de huella. El autor avisa de que la cifra puede estar inflada. Cambiar el user agent no ayudaba ya en 2010 [3].
- **AmIUnique (Laperdrix et al., 2016).** 118.934 huellas con 17 atributos durante un año, un 89,4 % únicas. En escritorio, el 90 %, en móvil, el 81 %. El público estaba sesgado (57 % Windows, 5 % Android) [4].
- **Gómez-Boix et al. (2018).** 2.067.942 huellas de uno de los 15 sitios más visitados de Francia, entre diciembre de 2016 y junio de 2017. Solo el 33,6 % era único (35,7 % en ordenador, 18,5 % en móvil). Las huellas no únicas son frágiles, y más del 85 % de ciertas huellas pasaban a ser únicas al cambiar determinados atributos. Francia, 2016 y 2017, solo usuarios que aceptaron cookies [5].
- **FP-STALKER (Vastel et al., 2018).** 98.598 huellas de 1.905 instancias de navegador durante dos años. Las huellas cambian de horas a días, pero se enlazan. De media se rastreó un navegador 54,48 días y un 26 % más de 100 días. La muestra eran usuarios con una extensión instalada [6].
- **Canvas a escala.** Englehardt y Narayanan (enero de 2016, millón de sitios más populares) lo hallaron en 14.371 sitios (1,6 %), el 98,2 % por terceros [8]. Luo et al. (IMC 2025, rastreo de mayo de 2025) lo hallaron en 2.067 de los 16.276 sitios del top 20.000 que se pudieron rastrear (12,7 %) y en 1.715 de 17.260 de una muestra de la cola (9,9 %) [2]. Los bloqueadores de anuncios apenas lo reducen (~5 %). El 49 % de los sitios del top con canvas (52 % en la cola) usa un script servido como de primera parte. Entre todos los sitios con canvas, el 45 % tiene al menos un dibujo de prueba generado y extraído dos veces, una comprobación con la que se detecta si el navegador añade ruido distinto en cada dibujo. Firefox añade el mismo ruido durante toda la sesión, así que esa comprobación no lo delata [2]. Los autores señalan que el uso asociado a seguridad es minoritario, y que entre el 37 y el 45 % de los dibujos de prueba los genera un script incluido en listas de bloqueo [2]. FP-Inspector da el 10,18 % de las 100.000 webs más populares [9]. Las cifras no son comparables entre sí (distinta muestra y definición). Orden de magnitud, entre el 5 y el 13 %.


## Matices y límites

- **Único no es seguido.** Una huella única en una muestra no demuestra seguimiento. Hace falta que se mantenga y se pueda enlazar [6]. Y la cifra "el 90 % somos únicos" viene de sitios con público sesgado [3][4][5].
- **Las cifras de Fingerprint son de marketing.** Anuncia identificación "que dura meses o años" y que reconoce al mismo usuario en sesiones de incógnito, y promete un "ID permanente" para cada visitante [13]. Son declaraciones de la propia empresa, sin auditoría independiente citada. Su documentación habla de un ejemplo hipotético del 98 % y de identificación probabilística con puntuación de confianza si no hay almacenamiento [14].
- **Google.** En diciembre de 2024 avisó de que desde el 16 de febrero de 2025 dejaría de prohibir el fingerprinting a quienes usan sus productos de publicidad. El ICO (19 de diciembre de 2024) escribió "We think this change is irresponsible" y recordó que Google dijo en 2019 "We think this subverts user choice and is wrong" [15]. Esa frase es del 22 de agosto de 2019, en la entrada "Building a more private web" del blog de Google, donde añade que "los usuarios no pueden borrar su huella" [31]. Es la política de anuncios de Google, no el navegador Chrome.
- **LinkedIn.** BleepingComputer informó el 3 de abril de 2026 de un script que comprueba 6.236 extensiones de Chrome y recoge datos del dispositivo. LinkedIn dice que lo hace para proteger la plataforma, que no infiere información sensible y que las afirmaciones son erróneas. BleepingComputer comprobó que el script revisa 6.236 extensiones, pero no pudo verificar cómo se usan los datos ni si se comparten [17]. La denuncia original viene de la asociación Fairlinked e.V. ("BrowserGate"). El vídeo lo cita como ejemplo de que lo raro destaca, y eso es una extrapolación.
- **Chrome.** Incógnito bloquea cookies de terceros y la ayuda no menciona fingerprinting [26]. Google retiró el 17 de octubre de 2025 varias tecnologías de Privacy Sandbox, incluida IP Protection [16]. Chrome no anuncia una defensa contra la huella equivalente a la de Firefox, Safari o Brave, aunque sí recorta el detalle del user agent. En septiembre de 2026 Chrome tenía el 66 % del uso mundial según StatCounter [32], es decir, dos de cada tres usuarios, no "casi todos".
- **Firefox.** Firefox 145 (noviembre de 2025) añadió una segunda fase de protección, al inicio solo en Navegación privada y en ETP Estricta, y Mozilla dice que reduce casi a la mitad el porcentaje de usuarios vistos como únicos [18]. Firefox 151 (19 de mayo de 2026) lo extiende al modo Estándar, con una reducción media de ~14 % de usuarios identificables de forma única, ~49 % en macOS [19].
- **Safari.** Safari 17 añadió ruido en canvas, WebGL y audio y valores fijos de pantalla en navegación privada [21]. Safari 26 impide a "scripts de fingerprinting conocidos" acceder a ciertas APIs, y que esté activado por defecto lo cita 9to5Mac a partir de Apple [22]. Al depender de una lista, un script a medida puede escaparse. El vídeo agrupa Safari con la uniformidad, y en rigor mezcla ruido y valores fijos.
- **Brave y Tor.** Brave usa "farbling" (valores derivados de una semilla por sesión y sitio) y admite que los ataques de fingerprinting siempre serán posibles [23]. Retiró su modo Estricto en enero de 2024, y su afirmación de ser la protección más fuerte es de la propia empresa [24]. Tor busca la uniformidad, y su diseño (documento de 2019) dice que ha resultado mejor estrategia que aleatorizar [25].
- **Incógnito.** No guarda historial ni cookies, pero los sitios y tu proveedor siguen viendo tu actividad [26]. La AEPD llama "falsa seguridad" a creer que cambia la huella, con un estudio de 2018 y 2019 [11]. En Firefox y Safari la navegación privada recibe más protección que la normal, así que depende del navegador, no solo del modo.
- **Antifraude.** Es un uso real. El estudio IMC identifica servicios de huella que anuncian usos de seguridad, como detectar bots o simplificar la autenticación, y los sitúa como uso minoritario [2]. Fingerprint anuncia casos de fraude de cuentas y pagos [13]. No hay una fuente primaria que confirme qué bancos concretos la usan ni con qué finalidad. La política de cookies de Santander cita el fingerprinting entre las técnicas que regula, sin precisar su finalidad [33]. Las Directrices del CEPD no tratan el fraude, así que si el antifraude queda exento de consentimiento no se desprende de ellas [27].

## Marco legal

El artículo 5.3 de la Directiva ePrivacy exige consentimiento para acceder a información almacenada en el equipo, con excepciones. El CEPD recuerda que el fingerprinting entra en su ámbito y que si el sitio envía código que ordena al navegador enviar información, ese acceso entra en el artículo (Directrices 2/2023, versión 2.0, 7 de octubre de 2024) [27]. El artículo admite excepciones, por ejemplo cuando el acceso es estrictamente necesario para un servicio que el usuario ha pedido. La Guía de cookies de la AEPD (mayo de 2024) dice que el artículo 22.2 de la LSSI se aplica también al fingerprinting [28]. Su estudio añade que, si la huella se asocia a una cookie, borrar cookies no es eficaz porque la huella permite restituirla [11].

## Qué puedes hacer

1. **Usa un navegador que combata la huella por defecto.** Firefox 151 o posterior, Safari 26, Brave o Tor si el riesgo es alto [18][19][22][23][25]. Pesa más que cualquier extensión.
2. **Mantenlo actualizado.** Las protecciones llegan por versión (Firefox 145 y 151, Safari 26), y uno desactualizado es otra señal.
3. **Firefox, sube a Estricta.** Ajustes, Privacidad y seguridad, Protección mejorada contra el rastreo, Estricta. Según la documentación de Firefox, Estricta activa la protección contra fingerprinting en navegación normal y privada, y el modo Estándar solo en privada, aunque desde Firefox 151 parte de la protección llega también a Estándar [19][30]. Estricta no falsifica la zona horaria ni los núcleos.
4. **Safari, activa la protección avanzada en toda la navegación.** En Mac, Safari, Ajustes, Avanzadas, protección avanzada contra rastreo y fingerprinting. En iPhone con iOS 26, Ajustes, Apps, Safari, Avanzado, Protección avanzada contra el rastreo y la huella digital, Toda la navegación (según cobertura de prensa [34]).
5. **Brave, deja los Escudos por defecto.** Ya no hay modo Estricto [24].
6. **Perfiles o navegadores separados** para trabajo, compras y redes. No elimina la huella, pero evita que todo se consolide bajo el mismo identificador (recomendación de la AEPD) [11].
7. **No te disfraces.** Cambiar el user agent no ayudó ni en 2010 [3], AmIUnique detecta incoherencias entre el user agent y `navigator.platform` [4], y extensiones raras pueden ser una señal si pocos las usan. Una VPN cambia la IP, no el navegador [11].
8. **Un bloqueador ayuda a medias.** Reduce detecciones (AEPD 2018), pero en 2025 solo ~5 % de los sitios con canvas [2][11].
9. **Mídelo con Cover Your Tracks.** Compara con otros visitantes de esa web, un público sesgado, así que "único allí" no es "único en el mundo" [29][5].

## Fuentes

1. W3C, Mitigating Browser Fingerprinting in Web Specifications (nota del Grupo de Privacidad, 25 sep 2025). https://www.w3.org/TR/fingerprinting-guidance/
2. Luo, Ritter, Savage y Voelker, canvas fingerprinting, IMC 2025. https://cseweb.ucsd.edu/~savage/papers/IMC25Canvas.pdf
3. Eckersley, How Unique Is Your Web Browser?, PETS 2010. https://coveryourtracks.eff.org/static/browser-uniqueness.pdf
4. Laperdrix, Rudametkin y Baudry, Beauty and the Beast, IEEE S&P 2016. https://inria.hal.science/hal-01285470/document
5. Gómez-Boix, Laperdrix y Baudry, Hiding in the Crowd, WWW 2018. https://inria.hal.science/hal-01718234/document
6. Vastel et al., FP-STALKER, IEEE S&P 2018. https://inria.hal.science/hal-01652021/document
7. Mowery y Shacham, Pixel Perfect, 2012. https://hovav.net/ucsd/dist/canvas.pdf
8. Englehardt y Narayanan, Online Tracking, CCS 2016. https://senglehardt.com/papers/ccs16_online_tracking.pdf
9. Iqbal et al., Fingerprinting the Fingerprinters, IEEE S&P 2021. https://arxiv.org/html/2008.04480
10. Web Almanac 2025, Privacidad. https://almanac.httparchive.org/en/2025/privacy
11. AEPD, Estudio sobre fingerprinting o huella digital del dispositivo (2018). https://www.aepd.es/guias/estudio-fingerprinting-huella-digital.pdf
12. Arvind Narayanan, 33 Bits of Entropy. https://33bits.wordpress.com/about/
13. Fingerprint, Identification. https://fingerprint.com/products/identification/
14. Fingerprint Docs, precisión y confianza. https://docs.fingerprint.com/docs/identification-accuracy-and-confidence
15. ICO, respuesta al cambio de política de Google, 19 dic 2024. https://ico.org.uk/about-the-ico/media-centre/news-and-blogs/2024/12/our-response-to-google-s-policy-change-on-fingerprinting
16. Privacy Sandbox, Update on plans, 17 oct 2025. https://privacysandbox.google.com/blog/update-on-plans-for-privacy-sandbox-technologies
17. BleepingComputer, LinkedIn y las extensiones de Chrome, 3 abr 2026. https://www.bleepingcomputer.com/news/security/linkedin-secretely-scans-for-6-000-plus-chrome-extensions-collects-data
18. Mozilla, Firefox expands fingerprint protections, nov 2025. https://blog.mozilla.org/en/firefox/fingerprinting-protections/
19. Firefox 151, notas de la versión, 19 may 2026. https://www.firefox.com/en-US/firefox/151.0/releasenotes/
20. BleepingComputer, Mozilla Firefox gets new anti-fingerprinting defenses, 10 nov 2025 (fuente secundaria). https://www.bleepingcomputer.com/news/security/mozilla-firefox-gets-new-anti-fingerprinting-defenses/
21. WebKit, Private Browsing 2.0. https://webkit.org/blog/15697/private-browsing-2-0/
22. WebKit, Safari 26.0 (https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) y 9to5Mac, 1 sep 2025 (https://9to5mac.com/2025/09/01/security-bite-my-favorite-privacy-features-in-ios-26/)
23. Brave, Fingerprinting Protections. https://github.com/brave/brave-browser/wiki/Fingerprinting-Protections
24. Brave, Sunsetting Strict fingerprinting mode, 18 ene 2024. https://brave.com/privacy-updates/28-sunsetting-strict-fingerprinting-mode/
25. Tor Project, Design and Implementation (edición de 2019). https://2019.www.torproject.org/projects/torbrowser/design/
26. Ayuda de Chrome, Incógnito. https://support.google.com/chrome/answer/95464
27. CEPD, Directrices 2/2023 v2.0, 7 oct 2024. https://www.edpb.europa.eu/system/files/2024-10/edpb_guidelines_202302_technical_scope_art_53_eprivacydirective_v2_en_0.pdf
28. AEPD, Guía sobre el uso de las cookies, mayo de 2024. https://www.aepd.es/guias/guia-cookies.pdf
29. EFF, Cover Your Tracks. https://coveryourtracks.eff.org/
30. Firefox Source Docs, Privacy Capabilities Overview (ETP). https://firefox-source-docs.mozilla.org/toolkit/components/antitracking/anti-tracking/etp-matrix/
31. Google, Building a more private web, 22 ago 2019. https://www.blog.google/products/chrome/building-a-more-private-web/
32. StatCounter, Browser Market Share Worldwide. https://gs.statcounter.com/browser-market-share/monthly/worldwide
33. Banco Santander, Política de cookies. https://www.bancosantander.es/es/politica-de-cookies
34. BGR, iOS 26 Advanced Tracking and Fingerprinting Protection (fuente secundaria). https://www.bgr.com/1962665/ios-26-advanced-tracking-fingerprinting-protections-google/
