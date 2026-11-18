
cd ~/proyectos || exit 1

set -e

echo "=== PREPARANDO PERFIL ==="

if [ ! -d "$HOME/proyectos/github-profile/.git" ]; then
    git clone \
    https://github.com/RenanEspinar/RenanEspinar.git \
    "$HOME/proyectos/github-profile"
fi

cd "$HOME/proyectos/github-profile"

if [ -n "$(git status --porcelain)" ]; then
    echo "Hay cambios locales. No se modificara nada."
    exit 1
fi

git pull --ff-only origin main

echo "=== ACTUALIZANDO README ==="

python3 - <<'PY'
from pathlib import Path
import re

p = Path("README.md")
text = p.read_text(encoding="utf-8")

def replace_once(pattern, replacement):
    global text
    text, n = re.subn(
        pattern,
        lambda m: replacement,
        text,
        count=1,
        flags=re.S
    )
    if n != 1:
        raise RuntimeError(
            "No se encontro la seccion: " + pattern[:70]
        )

header = '''<div align="center">

<h1>Renán Andrés Espinar Saavedra</h1>

<p>
<strong>Mechatronics Engineer · Master's Degree in Biomedical Engineering</strong>
<br>
Software Developer · Applied R&D · Biomedical Instrumentation
<br>
La Paz, Bolivia · Remote Engineering
</p>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&amp;size=18&amp;duration=2600&amp;pause=1100&amp;color=3976B9&amp;center=true&amp;vCenter=true&amp;width=760&amp;height=46&amp;lines=Python+%7C+Linux+%7C+Robotics;Android+%7C+IoT+%7C+Embedded+Systems;Biomedical+Instrumentation+%7C+DSP;Research+%7C+Prototyping+%7C+Validation" alt="Engineering specialties" />

<p>
<a href="https://www.linkedin.com/in/renanessaa"><img src="https://img.shields.io/badge/LinkedIn-Profile-24292F?style=flat-square&amp;logo=linkedin&amp;logoColor=white" alt="LinkedIn"/></a>
<a href="https://orcid.org/0009-0007-1918-7177"><img src="https://img.shields.io/badge/ORCID-Research-24292F?style=flat-square&amp;logo=orcid&amp;logoColor=white" alt="ORCID"/></a>
<a href="mailto:renanespinar.19@gmail.com"><img src="https://img.shields.io/badge/Email-Contact-24292F?style=flat-square&amp;logo=gmail&amp;logoColor=white" alt="Email"/></a>
</p>
'''

replace_once(
    r'\A<div align="center">.*?(?=</div>I develop software)',
    header
)

intro = '''</div>

## About

I develop software that interacts with physical systems: Android applications, Linux services, embedded electronics, automation and biomedical prototypes.

My work combines **software engineering, mechatronics, biomedical instrumentation and applied research**.

**Current roles:** Remote software development and R&D at Andes Labs (since 2025); Research Coordinator for Technology and Computer Science at Universidad del Valle (UNIVALLE), Bolivia.

**Academic background:** Mechatronics Engineering degree (UCB) and University Master's Degree in Biomedical Engineering (VIU). Experience in university teaching, experimental engineering and technical research.

## Selected engineering projects'''

replace_once(
    r'</div>I develop software.*?Selected engineering projects',
    intro
)

stethoscope = '''<strong><a href="https://github.com/RenanEspinar/digital-stethoscope-viu-2024">Electronic Stethoscope</a></strong><br>
<sub>VIU Thesis 2022–2023 · ESP32 · Wi-Fi · Python · DSP</sub>

<p>Designed and built an electronic stethoscope prototype for cardiac-sound acquisition, wireless transmission, WAV recording, digital filtering and signal visualization.</p>

<p>The original thesis documents a functional physical prototype and exploratory recordings from five patients reviewed by a medical specialist. The device is a research prototype, not a certified diagnostic instrument.</p>

<a href="https://github.com/RenanEspinar/digital-stethoscope-viu-2024">
<img src="https://raw.githubusercontent.com/RenanEspinar/digital-stethoscope-viu-2024/main/assets/prototype_real_photo.jpg" width="240" alt="Original electronic stethoscope prototype"/>
</a>

<p><sub>Original 2023 prototype. The modular 2026 redesign is a separate research phase.</sub></p>

<a href="https://github.com/RenanEspinar/digital-stethoscope-viu-2024"><img src="https://img.shields.io/badge/Research-Project-64748B?style=flat-square" alt="Research project"/></a>
<a href="https://github.com/RenanEspinar/digital-stethoscope-viu-2024/blob/main/docs/THESIS_2023.md"><img src="https://img.shields.io/badge/VIU-Thesis%20Documentation-64748B?style=flat-square" alt="Thesis documentation"/></a>'''

replace_once(
    r'<strong><a href="https://github.com/RenanEspinar/digital-stethoscope-viu-2024">Digital Stethoscope</a></strong><br>.*?(?=\s*</td>)',
    stethoscope
)

focus = '''</table>

## Engineering focus

| Area | Technologies and experience |
|---|---|
| Software | Python, Java, Flutter, FastAPI, Linux, Git |
| Embedded | ESP32, Arduino, sensors, IoT |
| Infrastructure | Docker, Home Assistant, networking |
| Engineering | Robotics, CAD, 3D printing, PID control |
| Research | Biomedical instrumentation, DSP, experimental validation |

**Research:** Co-author of *MAMBU: A Bolivian Case of Response to Artificial Ventilators Shortage*, IEEE ANDESCON 2022 ([DOI](https://doi.org/10.1109/ANDESCON56260.2022.9989651)).

'''

replace_once(
    r'</table>Repository activity.*?(?=<details>)',
    focus
)

additional = '''<details>
<summary><strong>Additional engineering projects</strong></summary>

- [Bode Diagram Analyzer](https://github.com/RenanEspinar/detector-de-bode) — MATLAB frequency-response visualization.
- [Stability Detector](https://github.com/RenanEspinar/detector-de-estabilidad) — MATLAB stability analysis.
- [Klipper / XYZ Da Vinci Pro](https://github.com/RenanEspinar/Klipper---XYZ-Davinci-Pro-V1.0) — 3D-printer retrofit project.
- [F450 / APM 2.8](https://github.com/RenanEspinar/Parametros-De-Drone-F450-APM2.8-) — flight-controller configuration.

</details>

## GitHub activity'''

replace_once(
    r'<details>\s*<summary><strong>Additional engineering projects</strong></summary>.*?</details>GitHub activity',
    additional
)

text = text.replace("</div><details>", "</div>\n\n<details>")
text = text.replace("</details><sub>", "</details>\n\n<sub>")

if "#cardiac-audio-recordings" in text:
    raise RuntimeError("Enlace antiguo de audio detectado")

p.write_text(text.rstrip() + "\n", encoding="utf-8")
print("README actualizado")
PY

echo "=== VALIDANDO ==="
git diff --check
git diff --stat

echo "=== CONFIGURANDO AUTOR ==="
git config user.name "Renán Andrés Espinar Saavedra"
git config user.email "renanespinar.19@gmail.com"

echo "=== PUBLICANDO ==="
gh auth setup-git
git add README.md
git commit -m "docs: refresh engineering profile and VIU thesis"
git push origin main

echo "=== RESULTADO ==="
git status
git log -1 --oneline

