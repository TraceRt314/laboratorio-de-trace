# El dueño del bar sabe que abriste Tinder

Documentación técnica del episodio 004 de El Laboratorio de Trace: qué ve de ti quien controla una red wifi pública aunque uses HTTPS, y dónde está el riesgo real.

Fuentes consultadas el 28 de octubre de 2026, salvo que se indique otra fecha. Las páginas de ayuda "vivas" (Android, Chrome, AOSP) no tienen fecha de edición y se citan por la fecha de consulta.

## Cómo funciona por dentro

**HTTPS cubre el contenido.** Según el Informe de Transparencia de Google, citado en su entrada de octubre de 2025, la serie de navegaciones por HTTPS en Chrome pasó de entre el 30 y el 45 % en 2015 a entre el 95 y el 99 % hacia 2020 y desde entonces se ha estancado. Por plataforma, contando todas las navegaciones, Linux ronda el 84 % y Windows el 95 %. Limitado a sitios públicos, Linux llega al 97 %, Windows al 98 % y Android y Mac superan el 99 % [1]. La mayor parte del HTTP que queda es a sitios privados (intranets, 192.168.x.x), que solo puede abusar quien esté en tu propia red local, como una red wifi [1]. El Web Almanac 2025 mide otra cosa (portadas) y da 97,5 % en escritorio y 97,3 % en móvil [3]. Las cifras salen del texto del blog [1]. Chrome 154 (22 de septiembre de 2026 según las notas de la versión; el blog de Google lo había anunciado para octubre) activa por defecto un aviso antes de abrir sitios públicos sin HTTPS, que el usuario puede desactivar [1][2].

**Lo que va por fuera.**

- *DNS clásico.* Escucha en el puerto 53, por UDP y TCP [4]. Google lo resume como consultas y respuestas sin cifrar, vulnerables a espionaje y suplantación [5]. Por defecto el móvil usa el servidor DNS que le da la red a la que se conecta, es decir, el del local [6].
- *SNI.* El nombre del servidor viaja en la extensión `server_name` del ClientHello de TLS, sin cifrar, para que el servidor elija el certificado. Cloudflare lo llama "la señal más clara" de con qué servidor habla un cliente [13][14].
- *IP de destino, momento y volumen.* Siguen visibles aunque haya ECH [13]. En sitios que comparten IP no siempre identifica la web, pero sí cuando la web es pequeña y tiene IP propia, que es una inferencia, no una cifra medida.

**DNS cifrado.** DoT es el RFC 7858 (mayo de 2016) y DoH el RFC 8484 (octubre de 2018) [7][11]. Android ofrece DNS privado desde Android 9. En modo automático, los dispositivos mejoran a DoT si el servidor DNS de la red lo admite. Con un nombre de host fijado, Android envía las consultas a ese servidor por canal seguro y, si no puede alcanzarlo, marca la red como sin acceso a internet [6]. La ayuda de Android lista las opciones Desactivado, Automático o nombre de host del proveedor, y aclara que solo protege las consultas de DNS, no otro tipo de tráfico [8]. Chrome usa DNS seguro en modo automático y, si falla, consulta en claro. Con proveedor personalizado, no vuelve al modo sin cifrar [9]. Decide la mejora con una lista de proveedores DoH conocidos. Si el DNS del local no está en la lista, no hay mejora [10]. En iPhone, iOS 14 y posteriores admiten DoT y DoH a nivel de sistema, pero se configuran con una app de red o un perfil de gestión, sin menú propio [12]. Instalar el perfil de un proveedor que tú elegiste es distinto de aceptar el que ofrece un portal.

**ECH.** RFC 9849 (marzo de 2026) es un estándar. Cloudflare lo activó en todas las zonas gratuitas el 29 de septiembre de 2023 y abrió el acceso a los planes de pago por solicitud [16]. Mozilla anunció el 3 de octubre de 2023 que ECH se desplegaba a usuarios de Firefox de todo el mundo [17]. En Android, el soporte de sistema para apps llega con Android 17 (API 37), y solo si la librería de red de la app lo soporta [18]. Solo cifra el nombre si el sitio publica sus claves en DNS y el navegador consulta ese DNS de forma cifrada [13][17].

**Portales cautivos.** Android sondea `connectivitycheck.gstatic.com/generate_204` por HTTP, y por HTTPS `www.google.com/generate_204` [20]. Esas comprobaciones sirven sobre todo para detectar portales cautivos [20][21]. En el laboratorio, sin portal la respuesta fue 204. Apple usa `captive.apple.com` en los puertos 80 y 443 [22]. La sonda es HTTP simple, así que la propia detección es tráfico visible en la red. Los RFC 8908 y 8910 definen una API y el aviso por DHCP o RA del portal [23].

**MAC aleatoria.** Android genera una dirección aleatoria por red (por SSID) y persiste, de modo que olvidar la red y volver a conectarse da la misma dirección. Va por defecto desde Android 10 [27]. iOS 14 introdujo la dirección wifi privada. Desde iOS 18 hay tres modos, y por defecto es Fija en redes WPA2 o superiores y Rotativa (cada dos semanas) en redes débiles o abiertas. Olvidar la red elimina la dirección privada, salvo que hayan pasado menos de 24 horas [28].

## El experimento del laboratorio

Montado en Docker con scripts de `lab/wifi/`. El "router del bar" es un contenedor con `tshark` escuchando la interfaz `docker0`. Otro contenedor hace de cliente. Todo es tráfico de prueba y las credenciales son inventadas.

- **Qué ve el router.** El cliente visitó por HTTPS tinder.com, bbva.es y doctoralia.es. El router registró, para cada web y con hora, una consulta DNS en claro y después el nombre en el SNI, y ninguna ruta ni contenido.
- **Una web sin candado.** Un inicio de sesión de prueba (usuario y clave inventados) enviado por HTTP. El router registró la petición POST entera con el usuario y la clave en claro.
- **DNS cifrado.** Repetida la prueba con el cliente enviando el DNS por HTTPS (DoH, contra un resolutor público). El router ya no vio las consultas, pero siguió viendo el SNI de cada web.
- **Portal cautivo de juguete.** Sin portal, la comprobación de conectividad de Android recibió `204 No Content`. Con un portal que desvía ese nombre, recibió `302 Found` hacia la página de inicio de sesión del bar.

Límites. El laboratorio simula una red, no una cafetería real, y el DoH se forzó desde el cliente. No se probó el modo automático de DNS privado en un móvil real: que en un local cuyo DNS no admita DoT las consultas salgan en claro es una consecuencia de lo que documenta Android [6], no una captura propia.

## Qué dicen los estudios

- Ali, Osman, Mannan y Youssef (Universidad Concordia, preimpresión de 2019) analizaron 67 portales cautivos de Montreal (cafés, centros comerciales, bancos, aeropuertos, trenes) entre septiembre de 2018 y abril de 2019. Veintisiete (40,3 %) usaban login social o formulario de registro para recoger datos, 19 de forma obligatoria. Cuarenta (59,7 %) creaban cookies de rastreo persistentes de terceros, de hasta 20 años, y 26 (38,8 %) las creaban antes del consentimiento. Siete portales (Via Rail, Fairview Pointe-Claire, Carrefour Laval, Roots, McDonald's, Tim Hortons y Harvey's) tenían una cookie de tercero de network-auth.com válida 20 años. Otros 40 (59,7 %) exponían la MAC a terceros. Cinco filtraban por HTTP nombre, correo, teléfono, dirección o fecha de nacimiento, y dos declaraban enlazar la MAC con datos personales. De 22 portales probados con un Google Pixel 3 (Android 9) y un Nexus 4 (Android 5.1.1), cambiando la MAC a mano, 9 guardaban cookies persistentes en la app de portal y podían seguir al dispositivo pese al cambio de MAC. Un ejemplo es Tim Hortons, con una cookie de 20 años que usa para autenticar el dispositivo [24].
- Ikram et al. (IMC 2016, CSIRO/ICSI) analizaron 283 apps de VPN de Android, de un corpus de más de 1,4 millones de apps de Google Play. Más del 38 % tenía algún positivo de malware en VirusTotal, el 18 % usaba túneles sin cifrar, alrededor del 66 % no encaminaba el DNS por el túnel y alrededor del 84 % no encaminaba IPv6 [29].
- Citizen Lab y la Universidad Estatal de Arizona (informe "Hidden Links", agosto de 2025; reseña de Malwarebytes del 4 de septiembre de 2025) analizaron VPN entre las 100 más descargadas, con más de 700 millones de descargas conjuntas. Encontraron familias de apps con propietarios no declarados, vínculos con China y fallos de seguridad compartidos, como contraseñas incrustadas en el código [32].
- Un barrido independiente del 3 de agosto de 2025 sobre cerca de un millón de dominios populares (lista Tranco; 948.810 resolvieron) encontró 155.450 con ECH, alrededor del 16 % de los que resolvieron, y casi todos tras Cloudflare. Es el blog de un investigador y vale como orden de magnitud [19].

## Matices y límites

- **El DNS privado "Automático" no es una garantía.** Android mejora a DoT solo si el servidor DNS de la red lo admite [6]. Si no lo admite, las consultas siguen en claro, y los routers de muchos locales reenvían a los DNS de su operador. Solo un nombre de host fijado evita el modo en claro [6][8].
- **ECH aún no tapa el SNI en la práctica.** Solo una minoría de la web lo publica [19] y exige DNS cifrado [13].
- **El MAC aleatorio ayuda, no hace invisible.** La AEPD recuerda que dentro de una red la MAC se mantiene constante, que el procedimiento de generación no está estandarizado, que se estima que entre el 5 y el 10 % de dispositivos no la usan y que hay técnicas que identifican dispositivos aunque cambien de MAC [25]. En iOS olvidar la red renueva la dirección (salvo que hayan pasado menos de 24 horas) y en Android no, así que "olvida la red para cambiar de identidad" solo vale en iPhone [27][28]. La rotación cada dos semanas en redes abiertas o débiles aplica desde iOS 18 [28].
- **Los estudios son antiguos.** Concordia es de 2019, con una muestra pequeña y preimpresión [24]. Ikram es de 2016 y analiza apps de entonces [29]. Marcan el patrón, no la situación de un local concreto.
- **Una red gemela ve lo mismo que la legítima.** CISA define el ataque (un atacante imita un punto de acceso con señal más potente) y aconseja confirmar el nombre con el establecimiento [26]. Con HTTPS válido, esa red ve dominios, horas y volumen. El peligro está en lo que cedas en un portal falso o instales. Esto último es inferencia, coherente con [1].
- **La guía de la AEPD trata el seguimiento por wifi, no los portales cautivos.** Su guía de mayo de 2024 describe cómo se rastrean móviles por sus tramas wifi (por ejemplo, en un centro comercial) y analiza las bases legales del RGPD. Como el rastreo suele hacerse sin que el móvil se conecte, el consentimiento (art. 6.1.a) resulta en principio difícil de obtener y solo cabe, por ejemplo, si el usuario se conecta voluntariamente y se le informa. El interés legítimo exige garantías (anonimización, datos agregados, opt-out), y los escenarios con repetición de visitas alejan una ponderación favorable [25]. Es normativa sobre rastreo wifi, no sobre portales.
- **Cookies y casillas premarcadas.** El TJUE (asunto C-673/17, Planet49, 1 de octubre de 2019) declaró que una casilla marcada por defecto no es un consentimiento válido para instalar cookies [35].
- **Recomendaciones oficiales.** INCIBE aconseja evitar redes públicas salvo necesidad, priorizar datos móviles, usar VPN y desactivar la conexión automática [30][31]. Sus materiales citados no distinguen entre VPN gratuitas y de pago.
- **Quad9** es operado por la fundación suiza sin ánimo de lucro Quad9 Foundation, con sede en Zúrich [36].

## Qué puedes hacer

1. **Para lo sensible, datos móviles o tu propio punto de acceso.** Sin banca ni compras en red pública salvo necesidad [30].
2. **Desactiva la conexión automática y olvida las redes públicas.** iPhone, Ajustes, Wi-Fi, Editar, botón (i), "Forget This Network" o el interruptor "Auto-Join" (nombres en inglés de la ayuda de Apple) [33]. Android, Ajustes, Redes e Internet, Internet, mantén pulsada la red y elige Olvidar.
3. **En el portal, el mínimo de datos.** Evita el login con cuenta social y no instales perfiles ni certificados [24][26]. En iPhone los perfiles se revisan en Ajustes, General, VPN y gestión de dispositivos [34].
4. **Avisa antes de abrir sitios sin HTTPS.** Chrome 154 lo trae activado [2].
5. **Fija un DNS privado.** Android, Ajustes, Redes e Internet, DNS privado, "Nombre de host del proveedor de DNS privado", con un proveedor que elijas (Google documenta `dns.google` para DoT, y Quad9 `dns.quad9.net`) [5][8][36]. En Chrome, Usar DNS seguro [9]. En iPhone, con una app o perfil de un proveedor tuyo [12].
6. **VPN solo de pago, de un proveedor fiable y auditado.** Comprueba que no se filtra el DNS ni IPv6 fuera del túnel [29][32].
7. **Mantén activa la MAC privada.** Android, ajustes de la red, "Dirección MAC aleatoria" [27]. iPhone, "Dirección wifi privada" [28].
8. **Actualiza el móvil y el navegador.** Chrome 154, ECH en Android 17 y el DNS cifrado mejoran solos algunos puntos [2][18].

## Fuentes

1. Google, HTTPS by default, 28 oct 2025. <https://blog.google/security/https-by-defau/>
2. Chrome 154, notas de la versión, 22 sep 2026 (el blog [1] lo anunció para octubre). <https://developer.chrome.com/release-notes/154>
3. Web Almanac 2025, Seguridad (HTTP Archive). <https://almanac.httparchive.org/en/2025/security>
4. RFC 1035, nov 1987. <https://www.rfc-editor.org/rfc/rfc1035.txt>
5. Google Public DNS, DNS-over-TLS. <https://developers.google.com/speed/public-dns/docs/dns-over-tls>
6. Android Developers Blog, DNS over TLS en Android P, 13 abr 2018. <https://android-developers.googleblog.com/2018/04/dns-over-tls-support-in-android-p.html>
7. RFC 7858, mayo de 2016. <https://www.rfc-editor.org/rfc/rfc7858.txt>
8. Ayuda de Android, DNS privado. <https://support.google.com/android/answer/9654714>
9. Ayuda de Chrome, DNS seguro. <https://support.google.com/chrome/answer/10468685>
10. Chromium Blog, Secure DNS, 19 may 2020. <https://blog.chromium.org/2020/05/a-safer-and-more-private-browsing-DoH.html>
11. RFC 8484, oct 2018. <https://www.rfc-editor.org/rfc/rfc8484.txt>
12. Apple, WWDC20, Enable encrypted DNS (iOS 14). <https://developer.apple.com/videos/play/wwdc2020/10047>
13. Cloudflare, Good-bye ESNI, hello ECH, 8 dic 2020. <https://blog.cloudflare.com/encrypted-client-hello/>
14. RFC 8446 (TLS 1.3), ago 2018, y RFC 6066, ene 2011. https://www.rfc-editor.org/rfc/rfc8446.txt y <https://www.rfc-editor.org/rfc/rfc6066.txt>
15. RFC 9849, TLS Encrypted Client Hello, mar 2026. <https://www.rfc-editor.org/rfc/rfc9849.txt>
16. Cloudflare, Encrypted Client Hello, the last puzzle piece, 29 sep 2023. <https://blog.cloudflare.com/announcing-encrypted-client-hello/>
17. Mozilla, Encrypted Hello, 3 oct 2023. <https://blog.mozilla.org/en/firefox/encrypted-hello/>
18. Android Developers, Network Security Config (ECH en Android 17). <https://developer.android.com/privacy-and-security/security-config>
19. How often is the DNS HTTPS record used?, 3 ago 2025 (blog independiente). <https://000yesnt.github.io/posts/dns-https-stats>
20. AOSP NetworkStack, config.xml. <https://android.googlesource.com/platform/packages/modules/NetworkStack/+/refs/heads/main/res/values/config.xml>
21. Mullvad, comprobaciones de conectividad en Android, 25 abr 2024. <https://mullvad.net/en/help/configure-connectivity-checks-on-android>
22. Apple, Usar productos Apple en redes empresariales. <https://support.apple.com/en-us/101555>
23. RFC 8908 y RFC 8910, sep 2020. https://www.rfc-editor.org/rfc/rfc8908.txt y <https://www.rfc-editor.org/rfc/rfc8910.txt>
24. Ali, Osman, Mannan y Youssef, On Privacy Risks of Public WiFi Captive Portals, arXiv, 3 jul 2019. <https://arxiv.org/pdf/1907.02142>
25. AEPD, Tecnologías de seguimiento wifi, mayo de 2024. <https://www.aepd.es/guias/orientaciones-wifi-tracking-seguimiento.pdf>
26. CISA, Securing Wireless Networks. <https://www.cisa.gov/news-events/news/securing-wireless-networks>
27. AOSP, aleatorización de MAC wifi. <https://source.android.com/docs/core/connect/wifi-mac-randomization>
28. Apple, Dirección wifi privada, 5 dic 2025. <https://support.apple.com/en-us/102509>
29. Ikram et al., Android VPN Permission-enabled Apps, IMC 2016. <https://research.csiro.au/isp/wp-content/uploads/sites/106/2016/08/paper-1.pdf>
30. INCIBE, tríptico Conexiones seguras. <https://www.incibe.es/sites/default/files/docs/osi_cuadriptico_conexiones-seguras.pdf>
31. INCIBE, Conexiones inalámbricas seguras, 13 may 2024. <https://www.incibe.es/ciudadania/blog/conexiones-inalambricas-seguras-sabes-como-conseguirlo>
32. Malwarebytes, Popular Android VPN apps found to have security flaws and China links, 4 sep 2025 (reseña del informe de Citizen Lab y ASU). <https://www.malwarebytes.com/blog/news/2025/09/popular-android-vpn-apps-found-to-have-security-flaws-and-china-links>
33. Apple, Olvidar una red wifi. <https://support.apple.com/en-mn/102480>
34. Apple, Guía de seguridad personal. <https://support.apple.com/guide/personal-safety/ips327569a75/web>
35. TJUE, comunicado de prensa 125/19 (asunto C-673/17, Planet49), 1 oct 2019. <https://curia.europa.eu/jcms/upload/docs/application/pdf/2019-10/cp190125es.pdf>
36. Quad9, traslado a Suiza (fundación sin ánimo de lucro). <https://quad9.net/news/blog/quad9-public-domain-name-service-moves-to-switzerland-for-maximum-internet-privacy-protection/>
