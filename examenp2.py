from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Definimos las expresiones regulares para los componentes del CURP real
CURP_REGEX = r'^[A-Z]{4}\d{6}[HM][A-Z]{2}[A-Z]{3}[A-Z0-9]{2}$'

# Función para analizar el CURP
def analizar_curp(curp):
    # Verificar la longitud del CURP
    if len(curp) != 18:
        return None, "La CURP debe tener 18 caracteres."
    
    # Validar formato de CURP
    match = re.match(CURP_REGEX, curp)
    if not match:
        return None, "Formato de CURP inválido."
    
    # Extraemos los componentes de la CURP
    apellido_paterno = curp[0:2]
    apellido_materno = curp[2]
    nombre = curp[3]
    año = curp[4:6]
    mes = curp[6:8]
    dia = curp[8:10]
    sexo = curp[10]
    estado = curp[11:13]
    consonante_paterno = curp[13]
    consonante_materno = curp[14]
    consonante_nombre = curp[15]
    homoclave = curp[16:18]

    # Descripciones de los tokens
    tokens = [
        ("Apellido paterno", apellido_paterno),
        ("Apellido materno", apellido_materno),
        ("Nombre", nombre),
        ("Año de nacimiento", año),
        ("Mes de nacimiento", mes),
        ("Día de nacimiento", dia),
        ("Sexo", sexo),
        ("Estado de nacimiento", estado),
        ("Consonante interna del apellido paterno", consonante_paterno),
        ("Consonante interna del apellido materno", consonante_materno),
        ("Consonante interna del nombre", consonante_nombre),
        ("Homoclave", homoclave)
    ]

    return tokens, "Válida"

@app.route('/')
def index():
    return render_template('vistaexamenp2.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    curp = request.form.get('curp')
    
    if not curp:
        return render_template('vistaexamenp2.html', error="No se proporcionó ningún CURP.")
    
    tokens, valida = analizar_curp(curp)
    
    if valida != "Válida":
        return render_template('vistaexamenp2.html', error=valida, curp=curp, valida="No válida")
    else:
        return render_template('vistaexamenp2.html', tokens=tokens, curp=curp, valida=valida)

if __name__ == '__main__':
    app.run(debug=True)
