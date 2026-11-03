#!/usr/bin/env python3
"""Revisa por adb los sitios donde se esconde una app espía en un Android: accesibilidad, administradores del dispositivo,
acceso a notificaciones, apps sin icono, apps instaladas fuera de la tienda y último uso de micrófono, cámara y ubicación.
Solo lee: no cambia nada en el móvil.

  python3 lab/espia/revisa.py            # con el móvil conectado por USB y la depuración USB activada
"""
import re, subprocess, sys

STORES = {"com.android.vending", "com.google.android.packageinstaller"}  # Play Store; el instalador del sistema es «a mano»
OPS = {"RECORD_AUDIO": "micrófono", "CAMERA": "cámara", "FINE_LOCATION": "ubicación"}


def sh(*cmd):
    return subprocess.run(["adb", "shell", *cmd], capture_output=True, text=True).stdout


def pkgs_of(text):
    return sorted({m.split("/")[0] for m in re.split(r"[:\s]", text) if "/" in m and "." in m.split("/")[0]})


def main():
    if "device" not in subprocess.run(["adb", "get-state"], capture_output=True, text=True).stdout:
        sys.exit("no hay ningún móvil conectado con la depuración USB activada")
    third = {}
    for line in sh("pm", "list", "packages", "-3", "-i").splitlines():
        m = re.match(r"package:(\S+)\s+installer=(\S+)", line)
        if m:
            third[m.group(1)] = m.group(2)
    icons = set(re.findall(r"packageName=(\S+)", sh("cmd", "package", "query-activities", "-a", "android.intent.action.MAIN", "-c", "android.intent.category.LAUNCHER")))
    sections = [
        ("Accesibilidad (puede leer y tocar todo lo que hay en pantalla)", pkgs_of(sh("settings", "get", "secure", "enabled_accessibility_services"))),
        ("Administradores del dispositivo (pueden bloquear o borrar el móvil, y cuesta desinstalarlos)", pkgs_of(" ".join(re.findall(r"admin=ComponentInfo\{([^}]+)\}", sh("dumpsys", "device_policy"))))),
        ("Acceso a notificaciones (lee tus mensajes al llegar)", pkgs_of(sh("settings", "get", "secure", "enabled_notification_listeners"))),
        ("Apps instaladas sin icono en el escritorio", sorted(p for p in third if p not in icons)),
        ("Apps instaladas fuera de la tienda", sorted(p for p, i in third.items() if i not in STORES)),
    ]
    for title, items in sections:
        print(f"\n▸ {title}")
        print("\n".join(f"   {p}{'   ← no viene con el móvil' if p in third else ''}" for p in items) or "   nada")
    hits = {}
    for _, items in sections:
        for p in items:
            if p in third:
                hits[p] = hits.get(p, 0) + 1
    print("\n▸ Último uso de micrófono, cámara y ubicación (apps que no vienen con el móvil)")
    found = False
    for p in sorted(third):
        uses = []
        for op, name in OPS.items():
            m = re.search(r"time=\+?([^;\s]+)\s+ago", sh("cmd", "appops", "get", p, op))
            if m:
                uses.append(f"{name} hace {m.group(1)}")
        if uses:
            found = True
            print(f"   {p}: {', '.join(uses)}")
    if not found:
        print("   nada")
    for p, n in sorted(hits.items(), key=lambda x: -x[1]):
        if n >= 2:
            print(f"\n⚠ {p} aparece en {n} apartados: si no sabes qué es, no la quites aún; lee antes qué hacer (el enlace está en la descripción)")


if __name__ == "__main__":
    main()
