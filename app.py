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

@app.route('/upload', methods=['POST'])
#def upload():
#    imagem = request.files['imagem']
#    if 'imagem' not in request.files:
#        return jsonify({'mensagem': 'Nenhuma imagem foi localizada'}), 400
#
#    if imagem.filename == '':
#        return jsonify({'mensagem': 'Nenhuma imagem selecionada para upload'}), 400
#
#    # Chama a função extrai_recurso
#    features = extrai_recurso(imagem)
#
#    if features is not None:
#        # Chama a função gera_paleta
#        gera_paleta(features)
#
#        # Converte a imagem para base64 para exibi-la na página HTML
#        img_str = img_to_base64(imagem)
#        return jsonify({'mensagem': 'Imagem processada com sucesso'}), 200
#    else:
#        return jsonify({'mensagem': 'Erro ao processar a imagem'}), 400
#
#def extrai_recurso(imagem):
#    image = mpl.imread(imagem)
#    if image is None:
#        print(f"Erro ao carregar a imagem: {imagem}")
#        return None
#    # Transforma a imagem em uma matriz 1D
#    image = image.reshape(-1, 3)
#    return image
#
##def gera_paleta(imagem):
##    modelo =  KMeans(n_clusters=5, init='k-means++', algorithm='elkan', n_init=1, random_state=42)
##    novos_clusters = modelo.fit_predict(imagem)
##    # Exibe a contagem de pixels em cada cluster
##
##    # Visualiza a paleta de cores para a nova imagem
##    new_palette_2 = modelo.cluster_centers_.astype(int)
##    new_palette_hex = ['#%02x%02x%02x' % (r, g, b) for (r, g, b) in new_palette_2]
##
##    plt.imshow([new_palette_2])
##    #plt.axis('off')
##    plt.savefig('static/upload/paleta.png')  # Salva a paleta como uma imagem
##    plt.clf()
#def gera_paleta(imagem):
#    # Redimensiona a imagem para uma lista de pixels
#    imagem_reshaped = imagem.reshape(-1, 3)
#
#    # Cria o modelo KMeans
#    modelo = KMeans(n_clusters=5, init='k-means++', algorithm='elkan', n_init=1, random_state=42)
#    novos_clusters = modelo.fit_predict(imagem_reshaped)
#
#    # Recupera os centros dos clusters
#    new_palette_2 = modelo.cluster_centers_.astype(int)
#
#    # Aplica as cores dos centros dos clusters de volta aos pixels correspondentes
#    imagem_clusterizada = new_palette_2[novos_clusters].reshape(imagem.shape)
#
#    # Salva a imagem original com os clusters aplicados
#    plt.imshow(imagem_clusterizada)
#    plt.axis('off')  # Remove os eixos
#    plt.savefig('static/upload/imagem_clusterizada.png', bbox_inches='tight', pad_inches=0)
#    plt.clf()
#
#    # Visualiza e salva a paleta de cores
#    plt.imshow([new_palette_2])
#    plt.axis('off')  # Remove os eixos
#    plt.savefig('static/upload/paleta.png', bbox_inches='tight', pad_inches=0)
#    plt.clf()
#
#def img_to_base64(imagem):
#    image = mpl.imread(imagem)
#    img_str = BytesIO()
#    plt.imsave(img_str, image)
#    img_str.seek(0)
#    img_base64 = base64.b64encode(img_str.read()).decode('utf-8')
#    return f"data:image/png;base64,{img_base64}"


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

        # Converte a imagem para base64 para exibi-la na página HTML
        #img_str = img_to_base64(imagem_clusterizada_path)
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
    hora = datetime.datetime.now()
    hora = hora.strftime("%d_%m_%Y_%I_%M")
    # Redimensiona a imagem para uma lista de pixels
    imagem_reshaped = imagem_array.reshape(-1,3)

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
    plt.savefig(f'static/upload/imagem_clusterizada_{hora}.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    # Visualiza e salva a paleta de cores
    plt.imshow([new_palette_2])
    plt.axis('off')  # Remove os eixos
    plt.savefig(f'static/upload/paleta_{hora}.png', bbox_inches='tight', pad_inches=0)
    plt.clf()

    #return 'static/upload/paleta.png', 'static/upload/imagem_clusterizada.png'

def img_to_base64(imagem_path):
    with open(imagem_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
if __name__ == '__main__':
    app.run(debug=True)
