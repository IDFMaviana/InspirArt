from flask import Flask, render_template, request, send_file,session,jsonify
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpl
from PIL import Image
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import base64
from io import BytesIO
import os
import warnings
warnings.filterwarnings("ignore")
import datetime
import shutil


os.environ['LOKY_MAX_CPU_COUNT'] = '4'

app = Flask(__name__)

allowed_ext = set(['png','jpg','jpeg'])
app.secret_key ='chave_secreta'
def tipo_permitido(filename):
    return '.' in filename and filename.rsplit('.',1)[''].lower() in allowed_ext

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/suapaleta')
def suapaleta():
    return render_template('suapaleta.html')

@app.route('/galeria')
def galeria():
    return render_template('galeria.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'imagem' not in request.files:
        return jsonify({'mensagem': 'Nenhuma imagem foi localizada'}), 400

    imagem = request.files['imagem']
    if imagem.filename == '':
        return jsonify({'mensagem': 'Nenhuma imagem selecionada para upload'}), 400

    # Chama a função extrai_recurso
    features = extrai_recurso(imagem)

    if features is not None:
        # Chama a função gera_paleta
        gera_paleta(features)
        return jsonify({'mensagem': 'Imagem processada com sucesso',# 'img_str': img_str
                        }), 200
    else:
        return jsonify({'mensagem': 'Erro ao processar a imagem'}), 400

def extrai_recurso(imagem):
    # Lê a imagem usando PIL
    image = Image.open(imagem.stream)
    # Converte a imagem para o formato RGB se necessário
    if image.mode != 'RGB':
        image = image.convert('RGB')
    # Transforma a imagem em um array NumPy
    image_array = np.array(image)
    return image_array

def gera_paleta(imagem_array):
    # Grava a hora da operação
    hora = datetime.datetime.now()
    hora = hora.strftime("%d_%m_%Y_%I_%M")
    
    # Diretório para salvar os arquivos
    diretorio = "static/upload/"
    
    #Verifica se o diretório existe
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    # Verifica se já existem três pastas criadas
    contador_pastas = len(os.listdir(diretorio))

    
    # Cria uma nova pasta se o número de pastas criadas for menor ou igual a 3
    if contador_pastas <= 3:
        nova_pasta = diretorio + f'pasta_{contador_pastas}'
        os.makedirs(nova_pasta)
    else:
        nova_pasta = diretorio + f'pasta_{contador_pastas - 1}'
    
    # Redimensiona a imagem para uma lista de pixels
    imagem_reshaped = imagem_array.reshape(-1, 3)

    # Cria o modelo KMeans
    modelo = KMeans(n_clusters=8, init='k-means++', algorithm='elkan', n_init=1, random_state=42)
    novos_clusters = modelo.fit_predict(imagem_reshaped)

    # Recupera os centros dos clusters
    new_palette_2 = modelo.cluster_centers_.astype(int)

    # Aplica as cores dos centros dos clusters de volta aos pixels correspondentes
    imagem_clusterizada = new_palette_2[novos_clusters].reshape(imagem_array.shape)

    # Salva a imagem original com os clusters aplicados
    plt.imshow(imagem_clusterizada)
    plt.axis('off')  # Remove os eixos
    plt.savefig(os.path.join(nova_pasta, f'imagem_clusterizada.png'), bbox_inches='tight', pad_inches=0)
    plt.clf()

    # Salva a paleta de cores
    plt.imshow([new_palette_2])
    plt.axis('off')  # Remove os eixos
    plt.savefig(os.path.join(nova_pasta, f'paleta.png'), bbox_inches='tight', pad_inches=0)
    plt.clf()

def img_to_base64(imagem_path):
    with open(imagem_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def limpa_diretorio(diretorio):
    shutil.rmtree(diretorio)
    return 200

#limpa a pasta com as palhetas
@app.route('/exclui_pasta', methods=['POST'])
def exclui_pastas():
    # Diretório
    diretorio = "static/upload"

    # Chama a função para limpar o diretório
    resultado = limpa_diretorio(diretorio)
    return jsonify({'mensagem': 'Pasta limpa com sucesso'}),resultado

if __name__ == '__main__':
    app.run(debug=True)
